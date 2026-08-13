#!/usr/bin/env python3
"""Unit tests for image_link_probe extraction and local path resolution."""
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import image_link_probe as p


class TestExtract(unittest.TestCase):
    def test_extract_md_cover_html(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            content = root / "content"
            content.mkdir()
            md = content / "a.md"
            md.write_text(
                "---\ncover: \"/img/post-covers/x.jpg\"\n---\n\n"
                "![alt](https://example.com/a.png)\n"
                '<img src="/img/recovered/y.png">\n',
                encoding="utf-8",
            )
            refs = p.extract_refs(md, root)
            kinds = {r.kind for r in refs}
            self.assertIn("md", kinds)
            self.assertIn("cover", kinds)
            self.assertIn("html", kinds)
            refs_by = {r.ref: r for r in refs}
            self.assertIn("https://example.com/a.png", refs_by)
            self.assertIn("/img/post-covers/x.jpg", refs_by)

    def test_local_ok_and_miss(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            static = root / "static" / "img"
            static.mkdir(parents=True)
            (static / "ok.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 20)
            content = root / "content"
            content.mkdir()
            md = content / "b.md"
            md.write_text("![](/img/ok.png)\n![](/img/missing.png)\n", encoding="utf-8")
            refs = p.extract_refs(md, root)
            probed = [p.probe_ref(r, root) for r in refs]
            st = {r.ref: r.status for r in probed}
            self.assertEqual(st["/img/ok.png"], "ok")
            self.assertEqual(st["/img/missing.png"], "inaccessible")


if __name__ == "__main__":
    unittest.main()
