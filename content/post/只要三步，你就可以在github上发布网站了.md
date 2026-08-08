---
title: "三步用 GitHub Pages 发布网站"
author: Neal
summary: "对应 GitHub 推出的简化 Pages 流程：建仓库、提交内容、开启 Pages；补充今天仍适用的注意点与和完整博客的区别。"
tags: [Git, 开发工具, 博客, GitHub Pages]
categories: [开发工具]
date: "2016-12-09"
lastmod: "2026-08-08"
---

## 背景

GitHub 曾发文介绍让文档/站点发布更简单的体验（[Publishing with GitHub Pages, now as easy as 1, 2, 3](https://github.blog/2016-08-22-publishing-with-github-pages-now-as-easy-as-1-2-3/) 一类公告）。核心理念没变：**仓库即站点源，Markdown/HTML 可直接被 Pages 服务**。

## 三步

1. **创建仓库**（用户站 `username.github.io` 或项目站任意名）  
2. **提交内容**（`index.md` / `index.html` 或 docs 目录）  
3. **Settings → Pages** 选择分支与目录，保存  

几分钟后访问：

- 用户站：`https://<user>.github.io`  
- 项目站：`https://<user>.github.io/<repo>/`

## 今天仍建议知道的细节

| 点 | 说明 |
|----|------|
| 构建器 | 可能是 HTML 直出，或 Actions 构建（Hugo/Jekyll 等） |
| 自定义域 | 配 DNS 与 `CNAME` |
| HTTPS | Pages 默认提供 |
| 私有仓 | 视套餐是否支持私有 Pages |
| 与完整博客 | 本站用 Hugo + Actions 发布到 Pages，比「只丢 md」可控得多 |

## 和当年吐槽的关系

国内访问 GitHub 不稳定时，写作体验会差；但 **Pages 作为静态托管** 仍然简单可靠。CSDN 类平台省事，主题与数据所有权则弱一些。

## 小结

「三步上线」适合简历页、项目文档、活动页。内容复杂后上静态生成器（Hugo 等）+ CI，仍然落在 Pages 上，只是构建链更长。
