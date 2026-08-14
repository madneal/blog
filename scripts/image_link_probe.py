#!/usr/bin/env python3
"""Probe and classify image references in Hugo markdown content.

This is the shipped entry point used for inventory and final verification.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse

MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
COVER = re.compile(
    r"""^(?:cover|image|thumbnail|featured_image|featureImage|banner):\s*["']?([^\s"']+)""",
    re.M | re.I,
)
HTML_SRC = re.compile(
    r"""(?:src)=["']([^"']+)["']""",
    re.I,
)
# Hosts that serve images without a file extension in the URL path
EXTENSIONLESS_IMAGE_HOSTS = (
    "googleusercontent.com",
    "ggpht.com",
    "blogspot.com",
    "blogger.com",
    "twimg.com",
    "fbcdn.net",
    "cdninstagram.com",
)
# bare image-like URLs in markdown (conservative)
BARE_URL = re.compile(
    r"""(?<![\(\["'])(https?://[^\s)\]"'<>]+\.(?:png|jpe?g|gif|webp|svg|ico|bmp)(?:\?[^\s)\]"'<>]*)?)""",
    re.I,
)

@dataclass
class ImageRef:
    article: str
    kind: str  # md|cover|html|bare
    alt: str
    ref: str
    status: str = "unknown"  # ok|inaccessible|skip
    reason: str = ""
    http_code: Optional[int] = None



def _looks_like_image_ref(ref: str) -> bool:
    """True if ref is a plausible image URL/path for inventory purposes."""
    if not ref or ref.startswith("#") or ref.startswith("data:") or ref.startswith("javascript:"):
        return False
    r = ref.split("?")[0].split("#")[0]
    low = r.lower()
    if any(low.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".bmp")):
        return True
    # local paths under /img/ or images/
    if low.startswith("/img/") or low.startswith("img/") or "/images/" in low or low.startswith("/images/"):
        return True
    if low.startswith("http://") or low.startswith("https://"):
        try:
            host = urlparse(ref).netloc.lower()
        except ValueError:
            return False
        if any(h in host for h in EXTENSIONLESS_IMAGE_HOSTS):
            return True
        # common image CDN path segments without extension
        if any(seg in low for seg in ("/image", "/images/", "/img/", "/photo", "/media/", "/cms/images/")):
            return True
    return False


def extract_refs(path: Path, blog_root: Path) -> List[ImageRef]:
    rel = path.relative_to(blog_root).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    out: List[ImageRef] = []
    seen = set()

    def add(kind: str, alt: str, raw: str):
        ref = raw.strip().split()[0].strip("\"'")
        if not ref or ref.startswith("#") or ref.startswith("data:"):
            return
        key = (kind, ref)
        if key in seen:
            return
        # skip pure javascript/css false positives
        if ref.startswith("javascript:"):
            return
        seen.add(key)
        out.append(ImageRef(article=rel, kind=kind, alt=alt or "", ref=ref))

    for m in MD_IMG.finditer(text):
        add("md", m.group(1), m.group(2))
    for m in COVER.finditer(text):
        add("cover", "cover", m.group(1))
    for m in HTML_SRC.finditer(text):
        src = m.group(1).strip()
        if _looks_like_image_ref(src):
            add("html", "", src)
    # bare urls only if not already captured
    for m in BARE_URL.finditer(text):
        add("bare", "", m.group(1))
    return out


def local_path_for(ref: str, blog_root: Path) -> Optional[Path]:
    if ref.startswith("http://") or ref.startswith("https://"):
        return None
    r = ref.split("?")[0]
    if r.startswith("/"):
        # Hugo static
        return blog_root / "static" / r.lstrip("/")
    # relative to content rarely used
    return blog_root / "static" / r


def looks_like_image_bytes(data: bytes) -> bool:
    """True if leading bytes match a common raster/vector image signature."""
    if not data or len(data) < 3:
        return False
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if data[:3] == b"\xff\xd8\xff":
        return True
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return True
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return True
    if data[:2] in (b"BM", b"II", b"MM"):  # BMP / TIFF
        return True
    # SVG (text)
    head = data.lstrip()[:256].lower()
    if head.startswith(b"<?xml") and b"<svg" in head:
        return True
    if head.startswith(b"<svg"):
        return True
    # ICO
    if len(data) >= 4 and data[:4] == b"\x00\x00\x01\x00":
        return True
    return False


def _body_not_image_reason(data: bytes, ct: str) -> Optional[str]:
    """Return failure reason if body is not an image payload."""
    stripped = data.lstrip()
    low = stripped[:64].lower()
    if low.startswith((b"<!doctype", b"<html", b"{", b"<?xml")):
        # allow SVG xml only
        if not (b"<svg" in stripped[:512].lower()):
            return f"body not image ct={ct}"
    if not looks_like_image_bytes(data):
        return f"body not image magic ct={ct}"
    return None


def probe_http(url: str, timeout: float = 12.0) -> Tuple[str, str, Optional[int]]:
    """Return (status, reason, code). status in ok|inaccessible.

    Always verifies GET body magic bytes so extension-mismatched CDN blobs
    (e.g. Atom XML saved as .png) are not reported as ok.
    """
    ctx = ssl.create_default_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; blog-image-probe/1.0)",
        "Accept": "image/*,*/*;q=0.8",
    }
    try:
        req = urllib.request.Request(url, method="GET", headers=headers)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            ct = (resp.headers.get("Content-Type") or "").lower()
            data = resp.read(512)
            if not (200 <= int(code) < 400):
                return "inaccessible", f"GET {code}", int(code)
            if "text/html" in ct and "image" not in ct:
                return "inaccessible", f"html content-type {ct}", int(code)
            bad = _body_not_image_reason(data, ct)
            if bad:
                return "inaccessible", bad, int(code)
            return "ok", f"GET {code} {ct}", int(code)
    except urllib.error.HTTPError as e:
        return "inaccessible", f"HTTP {e.code}", e.code
    except Exception as e:
        return "inaccessible", f"{type(e).__name__}: {e}", None


def probe_ref(ref: ImageRef, blog_root: Path) -> ImageRef:
    r = ref.ref
    if r.startswith("http://") or r.startswith("https://"):
        # skip non-image example URLs that are clearly not images
        try:
            host = urlparse(r).netloc.lower()
        except ValueError:
            ref.status = "inaccessible"
            ref.reason = "invalid url"
            return ref
        # localhost examples
        if host in ("localhost", "127.0.0.1") or host.startswith("localhost:"):
            ref.status = "skip"
            ref.reason = "localhost example"
            return ref
        st, reason, code = probe_http(r)
        ref.status = st
        ref.reason = reason
        ref.http_code = code
        return ref

    # local path
    p = local_path_for(r, blog_root)
    if p is None:
        ref.status = "inaccessible"
        ref.reason = "unresolved path"
        return ref
    if p.exists() and p.is_file() and p.stat().st_size > 0:
        head = p.read_bytes()[:512]
        if not looks_like_image_bytes(head):
            ref.status = "inaccessible"
            ref.reason = f"local not image {p.relative_to(blog_root)}"
            return ref
        ref.status = "ok"
        ref.reason = f"local {p.relative_to(blog_root)}"
        return ref
    ref.status = "inaccessible"
    ref.reason = f"missing local {p}"
    return ref


def scan_content(blog_root: Path) -> List[ImageRef]:
    content = blog_root / "content"
    refs: List[ImageRef] = []
    for md in sorted(content.rglob("*.md")):
        refs.extend(extract_refs(md, blog_root))
    return refs


def probe_all(refs: List[ImageRef], blog_root: Path, workers: int = 16) -> List[ImageRef]:
    # local first (fast), then http concurrent
    local, remote = [], []
    for r in refs:
        if r.ref.startswith("http://") or r.ref.startswith("https://"):
            remote.append(r)
        else:
            local.append(r)
    out = [probe_ref(r, blog_root) for r in local]

    def work(r: ImageRef) -> ImageRef:
        return probe_ref(r, blog_root)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(work, r) for r in remote]
        for f in concurrent.futures.as_completed(futs):
            out.append(f.result())
    return out


def summarize(refs: List[ImageRef]) -> dict:
    by_status = Counter(r.status for r in refs)
    bad = [r for r in refs if r.status == "inaccessible"]
    by_article = defaultdict(list)
    by_host = Counter()
    for r in bad:
        by_article[r.article].append(r)
        if r.ref.startswith("http"):
            try:
                by_host[urlparse(r.ref).netloc.lower()] += 1
            except ValueError:
                by_host["(invalid)"] += 1
        else:
            by_host["(local)"] += 1
    return {
        "total_refs": len(refs),
        "by_status": dict(by_status),
        "inaccessible_count": len(bad),
        "articles_with_issues": len(by_article),
        "by_host": dict(by_host.most_common()),
        "by_article_counts": {k: len(v) for k, v in sorted(by_article.items(), key=lambda x: -len(x[1]))},
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--blog-root", type=Path, default=Path.cwd())
    ap.add_argument("--out-json", type=Path, required=True)
    ap.add_argument("--out-md", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--only-inaccessible", action="store_true")
    args = ap.parse_args(argv)

    blog_root = args.blog_root.resolve()
    refs = scan_content(blog_root)
    probed = probe_all(refs, blog_root, workers=args.workers)
    summary = summarize(probed)
    bad = [r for r in probed if r.status == "inaccessible"]
    items = [asdict(r) for r in (bad if args.only_inaccessible else probed)]
    payload = {
        "blog_root": str(blog_root),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": summary,
        "inaccessible": [asdict(r) for r in bad],
        "items": items,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# Image inventory",
        f"",
        f"- blog_root: `{blog_root}`",
        f"- total_refs: **{summary['total_refs']}**",
        f"- inaccessible: **{summary['inaccessible_count']}**",
        f"- by_status: `{summary['by_status']}`",
        f"",
        f"## By host (inaccessible)",
        f"",
    ]
    for h, c in summary["by_host"].items():
        lines.append(f"- {c}: `{h}`")
    lines += ["", "## By article", ""]
    for art, c in summary["by_article_counts"].items():
        lines.append(f"- {c}: `{art}`")
    lines += ["", "## Inaccessible items", ""]
    for r in bad:
        lines.append(f"- `{r.article}` [{r.kind}] `{r.ref}` — {r.reason}")
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
