# AdSense remediation status

Date: 2026-08-08

## Current state

| Metric | Result |
|--------|--------|
| Public posts | **199** |
| Draft posts | **4** |
| Public posts with prose < 800 | **61** |
| Public posts with prose < 300 | **0** |
| About / Privacy trust pages | Yes |
| Menu + footer links | Yes |
| Root page layout warning | Fixed (`layouts/_default/single.html`) |
| Fragile external post images (csdn/ax1x/…) | Removed or replaced with notes |
| languageCode | `zh-cn` |
| Legacy UA Analytics | Cleared (set empty; ready for GA4) |

## Content actions

- Expanded high-value security/engineering posts
- `draft: true` remains only on four clearly obsolete or low-value pages; the
  previously broad draft batch was rolled back so substantive technical notes
  remain publicly accessible.
- Recovered body images are stored in `madneal/blog-image` and referenced by
  CDN URLs; binary copies are intentionally not kept in this repository.
- Translator practice notes on public translations

## Re-review advice

1. Review whether the 61 shorter public posts should be expanded or grouped
2. Merge & deploy this branch
3. Wait for Google recrawl (Search Console)
4. Then request AdSense review
5. Optional later: GA4 ID and further archive of non-core long posts
