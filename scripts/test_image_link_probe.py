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


    def test_extensionless_googleusercontent_html(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            content = root / "content"
            content.mkdir()
            md = content / "c.md"
            md.write_text(
                '<p><img src="https://lh3.googleusercontent.com/ABC123xyzNoExt"></p>\n'
                '<img src="https://example.com/script.js">\n'
                "![](https://2.bp.blogspot.com/foo/bar.png)\n",
                encoding="utf-8",
            )
            refs = p.extract_refs(md, root)
            refs_set = {r.ref for r in refs}
            self.assertIn("https://lh3.googleusercontent.com/ABC123xyzNoExt", refs_set)
            self.assertIn("https://2.bp.blogspot.com/foo/bar.png", refs_set)
            # non-image script should not be inventoried as html image
            self.assertNotIn("https://example.com/script.js", refs_set)

    def test_looks_like_image_ref_helper(self):
        self.assertTrue(p._looks_like_image_ref("https://lh3.googleusercontent.com/xyz"))
        self.assertTrue(p._looks_like_image_ref("/img/recovered/a.png"))
        self.assertFalse(p._looks_like_image_ref("https://example.com/app.js"))
        self.assertFalse(p._looks_like_image_ref("javascript:void(0)"))

    def test_looks_like_image_bytes(self):
        self.assertTrue(p.looks_like_image_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 16))
        self.assertTrue(p.looks_like_image_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 16))
        self.assertTrue(p.looks_like_image_bytes(b"GIF89a" + b"\x00" * 16))
        self.assertTrue(p.looks_like_image_bytes(b"RIFF" + b"\x00" * 4 + b"WEBP" + b"\x00" * 8))
        self.assertFalse(p.looks_like_image_bytes(b'<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">'))
        self.assertFalse(p.looks_like_image_bytes(b"<!DOCTYPE html><html>"))
        self.assertFalse(p.looks_like_image_bytes(b'{"error":true}'))
        self.assertTrue(p.looks_like_image_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'))

    def test_local_rejects_non_image_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            static = root / "static" / "img"
            static.mkdir(parents=True)
            (static / "feed.png").write_text(
                '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"></feed>',
                encoding="utf-8",
            )
            content = root / "content"
            content.mkdir()
            md = content / "d.md"
            md.write_text("![](/img/feed.png)\n", encoding="utf-8")
            refs = p.extract_refs(md, root)
            probed = [p.probe_ref(r, root) for r in refs]
            self.assertEqual(probed[0].status, "inaccessible")
            self.assertIn("not image", probed[0].reason)


if __name__ == "__main__":
    unittest.main()
