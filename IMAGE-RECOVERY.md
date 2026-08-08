# Image recovery report

Date: 2026-08-08

## Sources used

1. **CSDN image CDN rewrite**: `http://img.blog.csdn.net/{id}` → `https://img-blog.csdn.net/{id}` (same author blog history)
2. **Internet Archive Wayback CDX** for `s1/s2/s3/z3.ax1x.com` snapshots
3. Local copy under `static/img/recovered/` (content-addressed by URL hash)

## Results

| Metric | Count |
|--------|------:|
| Fragile image URLs inventoried | 285 |
| Successfully recovered to local | **131** |
| Not found in public archives | **154** |
| Recovery rate | **45%** |

### By host (recovered)

- CSDN: most historical `img.blog.csdn.net` IDs restored via new host
- ax1x: partial via Wayback Machine (many never crawled)

### Unrecovered

Unrecovered images keep a note with the **original URL** so they can be fixed later if a mirror appears.

Count: 154

## Next manual options

- Upload private backups if you have them
- Check local browser cache / phone gallery for screenshots of HTB writeups
- Re-run Wayback later (rate limits blocked bulk queries)
- Search old CSDN article pages for newer `img-blog.csdnimg.cn` hashes (content may have been re-uploaded)


## Unrecovered URL list

- `https://s1.ax1x.com/2018/02/17/9tMvlT.jpg`
- `https://s1.ax1x.com/2018/10/26/i612ng.png`
- `https://s1.ax1x.com/2019/11/19/MRVc2F.png`
- `https://s1.ax1x.com/2020/04/19/Ju4MX8.png`
- `https://s1.ax1x.com/2020/04/19/Ju4ZtA.png`
- `https://s1.ax1x.com/2020/04/19/Ju4efI.png`
- `https://s1.ax1x.com/2020/04/19/Ju4k0e.png`
- `https://s1.ax1x.com/2020/04/19/JuhOw4.png`
- `https://s1.ax1x.com/2020/04/19/JuhTS0.png`
- `https://s1.ax1x.com/2020/04/25/JsZ5tI.png`
- `https://s1.ax1x.com/2020/04/27/JhNRET.png`
- `https://s1.ax1x.com/2020/09/29/0ZJNKU.png`
- `https://s1.ax1x.com/2020/10/17/0qX6G6.jpg`
- `https://s1.ax1x.com/2020/10/17/0qX7JP.png`
- `https://s1.ax1x.com/2020/11/06/BhW6sK.png`
- `https://s1.ax1x.com/2020/11/06/Bhf1Te.png`
- `https://s1.ax1x.com/2020/11/06/BhfU6P.png`
- `https://s1.ax1x.com/2020/11/07/B4Fvb6.png`
- `https://s1.ax1x.com/2020/11/07/B4kCPe.png`
- `https://s2.ax1x.com/2019/03/15/AE31XQ.png`
- `https://s2.ax1x.com/2019/03/15/AE3l6g.png`
- `https://s2.ax1x.com/2019/03/15/AE3mkt.png`
- `https://s2.ax1x.com/2019/03/15/AE3ntP.png`
- `https://s2.ax1x.com/2019/03/15/AE3uff.png`
- `https://s2.ax1x.com/2019/03/15/AEmLVK.png`
- `https://s2.ax1x.com/2019/04/04/Ag4cn0.png`
- `https://s2.ax1x.com/2019/04/04/AgICRJ.png`
- `https://s2.ax1x.com/2019/04/04/AgIks1.png`
- `https://s2.ax1x.com/2019/04/04/AgfJCd.png`
- `https://s2.ax1x.com/2019/04/04/AgfTPJ.png`
- `https://s2.ax1x.com/2019/04/04/AghBsx.png`
- `https://s2.ax1x.com/2019/04/04/AghFMt.png`
- `https://s2.ax1x.com/2019/04/04/AghhQI.png`
- `https://s2.ax1x.com/2019/04/04/AghxO0.png`
- `https://s2.ax1x.com/2019/04/08/A4W87q.png`
- `https://s2.ax1x.com/2019/04/08/A4WL8S.png`
- `https://s2.ax1x.com/2019/04/08/A4WxDs.png`
- `https://s2.ax1x.com/2019/04/08/A4f3xe.png`
- `https://s2.ax1x.com/2019/04/08/A4fl8O.png`
- `https://s2.ax1x.com/2019/04/08/A4hg6e.png`
- `https://s2.ax1x.com/2019/04/21/EFhSUS.png`
- `https://s2.ax1x.com/2019/04/21/EFhf2j.png`
- `https://s2.ax1x.com/2019/04/21/EFhlvR.png`
- `https://s2.ax1x.com/2019/04/21/EFrlwj.png`
- `https://s2.ax1x.com/2019/05/12/E4k8CF.png`
- `https://s2.ax1x.com/2019/05/12/E4kygH.png`
- `https://s2.ax1x.com/2019/05/13/E40VT1.png`
- `https://s2.ax1x.com/2019/05/13/E40w6g.png`
- `https://s2.ax1x.com/2019/05/13/E42O3R.png`
- `https://s2.ax1x.com/2019/05/13/E42wct.png`
- `https://s2.ax1x.com/2019/05/13/E42xu6.png`
- `https://s2.ax1x.com/2019/05/13/E4chPs.png`
- `https://s2.ax1x.com/2019/05/13/E4dx2D.png`
- `https://s2.ax1x.com/2019/05/13/E4g4Te.png`
- `https://s2.ax1x.com/2019/05/13/E4syKU.png`
- `https://s2.ax1x.com/2019/05/13/E4yEin.png`
- `https://s2.ax1x.com/2019/05/13/E4yzk9.png`
- `https://s2.ax1x.com/2019/05/19/Ej464e.png`
- `https://s2.ax1x.com/2019/05/19/Ej4Lgs.png`
- `https://s2.ax1x.com/2019/05/19/Ej4acR.png`
- `https://s2.ax1x.com/2019/05/19/Ej4oE8.png`
- `https://s2.ax1x.com/2019/05/19/Ej5nUO.png`
- `https://s2.ax1x.com/2019/05/19/EjY0mV.png`
- `https://s2.ax1x.com/2019/05/19/Ejdcss.md.png`
- `https://s2.ax1x.com/2019/05/19/EjjOxK.png`
- `https://s2.ax1x.com/2019/05/19/Ejv2od.png`
- `https://s2.ax1x.com/2019/05/20/Ev7Txg.png`
- `https://s2.ax1x.com/2019/05/20/Evb1cF.png`
- `https://s2.ax1x.com/2019/05/20/EvbGnJ.png`
- `https://s2.ax1x.com/2019/05/20/EvqfaR.png`
- `https://s2.ax1x.com/2019/06/02/VG6DzV.png`
- `https://s2.ax1x.com/2019/06/02/VGW99s.png`
- `https://s2.ax1x.com/2019/06/02/VGWwvt.png`
- `https://s2.ax1x.com/2019/06/07/V09fTs.png`
- `https://s2.ax1x.com/2019/06/07/VwG5on.png`
- `https://s2.ax1x.com/2019/06/07/VwG7WV.png`
- `https://s2.ax1x.com/2019/06/07/VwGYRK.png`
- `https://s2.ax1x.com/2019/06/07/VwGjeJ.png`
- `https://s2.ax1x.com/2019/06/07/VwJ4XD.png`
- `https://s2.ax1x.com/2019/06/07/VwJjc8.png`
- `https://s2.ax1x.com/2019/06/07/Vwt6Rx.png`
- `https://s2.ax1x.com/2019/07/04/ZUIwgH.png`
- `https://s2.ax1x.com/2019/08/03/eDD780.png`
- `https://s2.ax1x.com/2019/08/03/eDrFKO.png`
- `https://s2.ax1x.com/2019/08/03/erZrTA.png`
- `https://s2.ax1x.com/2019/08/03/erlWZT.png`
- `https://s2.ax1x.com/2019/08/04/eyPIxg.png`
- `https://s2.ax1x.com/2019/08/04/eykUVs.png`
- `https://s2.ax1x.com/2019/08/31/mxiIde.png`
- `https://s2.ax1x.com/2019/09/23/uiofjs.th.png`
- `https://s2.ax1x.com/2019/10/18/Kernqe.png`
- `https://s2.ax1x.com/2019/10/21/K1g2se.png`
- `https://s2.ax1x.com/2019/10/21/K1yur9.png`
- `https://s2.ax1x.com/2019/10/22/KG1gjf.png`
- `https://s2.ax1x.com/2019/10/22/KG8uo4.png`
- `https://s2.ax1x.com/2019/10/22/KG9eQx.png`
- `https://s2.ax1x.com/2019/10/22/KGAamq.png`
- `https://s2.ax1x.com/2019/10/22/KGE4rn.png`
- `https://s2.ax1x.com/2019/10/22/KGkTLq.png`
- `https://s2.ax1x.com/2019/10/23/KtG1Jg.png`
- `https://s2.ax1x.com/2019/10/23/Kta5ff.th.png`
- `https://s2.ax1x.com/2019/10/23/KtdwuQ.png`
- `https://s2.ax1x.com/2019/10/23/KtuIAJ.png`
- `https://s2.ax1x.com/2019/11/01/KHvCy6.png`
- `https://s2.ax1x.com/2019/11/02/KL1Qk8.png`
- `https://s2.ax1x.com/2019/11/02/KLM0te.png`
- `https://s2.ax1x.com/2019/11/02/KLM4hQ.png`
- `https://s2.ax1x.com/2019/11/02/KLML7T.png`
- `https://s2.ax1x.com/2019/11/02/KLMgnP.png`
- `https://s2.ax1x.com/2019/11/02/KLMqBV.png`
- `https://s2.ax1x.com/2019/11/02/KLMwkD.png`
- `https://s2.ax1x.com/2019/11/02/KLQPnx.png`
- `https://s2.ax1x.com/2019/11/02/KLQe9H.png`
- `https://s2.ax1x.com/2019/11/02/Kq7dgK.png`
- `https://s2.ax1x.com/2019/11/02/KqIDBj.png`
- `https://s2.ax1x.com/2019/11/02/KqtZxe.png`
- `https://s2.ax1x.com/2019/11/06/Mi0arD.png`
- `https://s2.ax1x.com/2019/11/07/MATiAH.png`
- `https://s2.ax1x.com/2019/11/07/MAhOQU.png`
- `https://s2.ax1x.com/2019/11/07/MAqcJH.gif`
- `https://s2.ax1x.com/2019/11/07/MAxeiT.gif`
- `https://s2.ax1x.com/2019/11/07/MAz09U.gif`
- `https://s2.ax1x.com/2019/11/18/McKGoq.png`
- `https://s2.ax1x.com/2019/11/18/Mceabq.png`
- `https://s2.ax1x.com/2019/11/18/McmnWF.png`
- `https://s2.ax1x.com/2019/11/18/McuZ2F.png`
- `https://s2.ax1x.com/2019/11/19/Mc53RA.png`
- `https://s2.ax1x.com/2019/11/19/Mc5DRs.png`
- `https://s2.ax1x.com/2019/11/19/Mc5WoF.png`
- `https://s2.ax1x.com/2019/11/26/QS2kVI.png`
- `https://s2.ax1x.com/2020/02/19/3ExZJH.png`
- `https://s2.ax1x.com/2020/02/19/3Exlef.png`
- `https://s2.ax1x.com/2020/02/20/3eN9wd.png`
- `https://s2.ax1x.com/2020/02/25/3tuMAU.gif`
- `https://s2.ax1x.com/2020/02/27/3ax38K.png`
- `https://s2.ax1x.com/2020/02/27/3axGvD.png`
- `https://s2.ax1x.com/2020/03/01/3cJFkq.png`
- `https://s2.ax1x.com/2020/03/01/3ctH0J.png`
- `https://s3.ax1x.com/2020/11/14/DPUrVJ.jpg`
- `https://s3.ax1x.com/2020/11/14/DPe1Y9.jpg`
- `https://s3.ax1x.com/2021/01/12/sY0h9I.png`
- `https://s3.ax1x.com/2021/01/12/sYBB5j.png`
- `https://s3.ax1x.com/2021/01/15/s0bnpD.png`
- `https://user-gold-cdn.xitu.io/2018/2/10/1617eae1206b47b4?w=401&h=713&f=png&s=256870`
- `https://user-gold-cdn.xitu.io/2018/2/10/1617eae1b59c001c?w=258&h=258&f=jpeg&s=27683`
- `https://user-gold-cdn.xitu.io/2018/2/10/1617eae1b80a48f3?w=655&h=554&f=png&s=53327`
- `https://user-gold-cdn.xitu.io/2018/2/10/1617eae1bc0f0f75?w=651&h=623&f=png&s=64677`
- `https://user-gold-cdn.xitu.io/2018/2/10/1617eae1c9c6d842?w=680&h=555&f=png&s=165381`
- `https://z3.ax1x.com/2021/04/17/c4Lyh6.png`
- `https://z3.ax1x.com/2021/06/25/R3mRb9.png`
- `https://z3.ax1x.com/2021/06/25/R3ms3T.png`
- `https://z3.ax1x.com/2021/06/25/R3n2z8.png`
- `https://z3.ax1x.com/2021/06/25/R3uewd.png`
- `https://z3.ax1x.com/2021/09/06/h5ZTud.png`


## blog-image CDN 上传与替换（本轮）

- 进程：卡住的 Wayback 恢复任务已结束/清理
- 图床仓库：`madneal/blog-image`（`images/recovered/`）
- 已 `git push` 更新 `MIGRATION-MAP.tsv`（131 条成功映射）
- CDN 格式：`https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/<hash>.ext`
- 博客正文：所有已恢复图的 `/img/recovered/...` 与原始失效外链 **已全部替换为 CDN**
  - 替换次数：140
  - 唯一 CDN 图：120
  - 正文中不再残留可用的 ax1x / `img.blog.csdn.net` 外链（失败项仅在「未能恢复」备注里保留原 URL）
- 未能恢复：124 处备注 + 原地址，见下方列表

验证：GitHub raw 抽样 `200` 且为合法 PNG 魔数。

