# Image recovery report

Date: 2026-08-08

## Final status

The image-recovery pass is complete: there are no remaining
`配图未能自动恢复` placeholders in `content/post/`.

- Previous audit baseline: 39 placeholders remained.
- This pass: 39 new image files uploaded to `madneal/blog-image`.
- One existing CSDN image was reused instead of duplicated.
- The quiz-bank article also received its second threshold image, which was
  present in the Tencent Cloud copy but absent from the local Markdown.
- AdSense audit artifacts were not included.

All article references now use the local image host format:

`https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/<file>`

## Sources used in the final pass

- Tencent Cloud Developer articles for the browser-proxy, Stantinko,
  passive-scanner, and quiz-bank posts.
- CSDN migrated images for the Burp debugging screenshots.
- Securelist for the Chrome CVE-2019-13720 article.
- Sekurak's same-author mirror for the AMP4Email screenshots.
- Juejin, Anquanke, and FreeBuf mirrors for the MyBatis, redirect, and Zeek
  articles.
- The imgchr record for the PWK/OSCP pricing image; the original Ax1x host is
  unavailable, so it was fetched through a public image proxy.
- The current blog QR asset for the old Evolutionary Computing footer QR
  image.

## Verification checklist

- `rg '配图未能自动恢复' content/post/` returns no matches.
- Every newly added file is a valid raster image, not an HTML error page.
- CDN URLs are checked for HTTP 200 responses.
- Hugo production build succeeds.
- Only blog content, the recovery report, and the image-repository mapping are
  staged; unrelated local cover files remain untracked.
