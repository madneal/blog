#!/usr/bin/env python3
"""Probe and classify image references in Hugo markdown content.

This is the shipped entry point used for inventory and final verification.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
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
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlparse

MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
COVER = re.compile(
    r"""^(?:cover|image|thumbnail|featured_image|featureImage|banner):\s*["']?([^\s"']+)""",
    re.M | re.I,
)
HTML_SRC = re.compile(
    r"""(?:src)=["']([^"']+\.(?:png|jpe?g|gif|webp|svg|ico|bmp))(?:\?[^"']*)?["']""",
    re.I,
)
# bare image-like URLs in markdown (conservative)
BARE_URL = re.compile(
    r"""(?<![\(\["'])(https?://[^\s)\]"'<>]+\.(?:png|jpe?g|gif|webp|svg|ico|bmp)(?:\?[^\s)\]"'<>]*)?)""",
    re.I,
)

SKIP_HOST_PREFIXES = (
    # code/docs examples often not real post images
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
        add("html", "", m.group(1))
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


def probe_http(url: str, timeout: float = 12.0) -> Tuple[str, str, Optional[int]]:
    """Return (status, reason, code). status in ok|inaccessible."""
    ctx = ssl.create_default_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; blog-image-probe/1.0)",
        "Accept": "image/*,*/*;q=0.8",
    }
    # HEAD first, then GET if needed
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                code = getattr(resp, "status", None) or resp.getcode()
                ct = (resp.headers.get("Content-Type") or "").lower()
                if method == "GET":
                    # read small prefix to detect html error pages
                    data = resp.read(64)
                    if data.lstrip()[:15].lower().startswith((b"<!doctype", b"<html", b"{")):
                        if "image" not in ct:
                            return "inaccessible", f"body not image ct={ct}", code
                if 200 <= int(code) < 400:
                    # some CDNs return 200 html for missing
                    if "text/html" in ct and "image" not in ct:
                        return "inaccessible", f"html content-type {ct}", code
                    return "ok", f"{method} {code} {ct}", int(code)
                return "inaccessible", f"{method} {code}", int(code)
        except urllib.error.HTTPError as e:
            # some hosts reject HEAD
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return "inaccessible", f"HTTP {e.code}", e.code
        except Exception as e:
            if method == "HEAD":
                continue
            return "inaccessible", f"{type(e).__name__}: {e}", None
    return "inaccessible", "unreachable", None


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
    payload = {
        "blog_root": str(blog_root),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": summary,
        "inaccessible": [asdict(r) for r in bad],
        "all" if not args.only_inaccessible else "inaccessible_only": (
            [asdict(r) for r in probed] if not args.only_inaccessible else [asdict(r) for r in bad]
        ),
    }
    # simplify keys
    if args.only_inaccessible:
        payload["items"] = [asdict(r) for r in bad]
    else:
        payload["items"] = [asdict(r) for r in probed]

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
