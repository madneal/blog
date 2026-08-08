---
title: "安全与开发常用在线工具清单（持续整理）"
author: "Neal"
summary: "把原先只有链接的工具表，整理成按场景分类、带用途说明的清单：安全分析、前端调试、写作效率与学术排版。"
tags: [工具, 安全, 开发, 效率]
categories: [工具]
date: "2018-01-01"
lastmod: "2026-08-08"
---


以前这页只是一串超链接，对自己「收藏」有用，对读者几乎没有信息增量。这次按 **使用场景** 重新整理，并补上「什么时候用、注意什么」。链接会失效，以各站点当前页面为准；涉及上传样本的在线工具，**不要提交真实客户数据或未授权资产**。

## 安全分析

| 工具 | 用途 | 备注 |
|------|------|------|
| [CyberChef 类在线编解码](https://emn178.github.io/online-tools/index.html) | Base64、Hash、编码转换 | 敏感数据优先本地工具 |
| [jwt.io](https://jwt.io) | 查看 JWT 结构 | 勿粘贴生产环境未脱敏 token |
| [cmd5](https://www.cmd5.com/) | 哈希查询 | 弱哈希撞库结果不可盲信 |
| [rot13.com](https://rot13.com/) | 经典替换密码 | CTF 入门用 |
| [beautifier.io](https://beautifier.io/) | JS 美化 | 逆向混淆脚本时好用 |
| [HashKiller](https://hashkiller.co.uk/) | 哈希相关 | 注意合规 |
| [app.any.run](https://app.any.run/) | 在线沙箱动态分析 | 上传即可能被分享，慎用 |
| [pcapfix 相关资源](https://f00l.de/hacking/pcapfix.php) | pcap 修复思路参考 | 生产流量包注意隐私 |
| [CTF 在线工具集合](http://ctf.ssleye.com/) | 编码/隐写等 | 仅用于授权训练 |

**自用原则：** 能本地做的编解码，尽量本地（CyberChef 桌面版、Python、Burp）。在线工具方便，但等于把样本交给第三方。

## 前端与页面调试

| 工具 | 用途 |
|------|------|
| [CodePen](https://codepen.io/) | 快速验证 HTML/CSS/JS 片段 |
| [Plunker](https://plnkr.co/) | 多文件前端原型 |
| [RealFaviconGenerator](https://realfavicongenerator.net) | 生成多平台 favicon |
| [Iconfont](https://www.iconfont.cn) | 图标资源 |

做安全研究时，CodePen 也适合复现 **纯前端** 的 DOM 行为（注意不要把 exploit 指向真实站点）。

## 开发与语言

| 工具 | 用途 |
|------|------|
| [Go Playground](https://play.golang.org/) | 分享最小可复现 Go 代码 |
| [regexr](https://regexr.com/) | 正则可视化调试 |
| [devhints](https://devhints.io) | 各类 cheatsheet |
| [DownGit](https://minhaskamal.github.io/DownGit/#/home) | 下载 GitHub 子目录 |
| [programiz](https://www.programiz.com) | 语法速查/练习 |

## 写作、作图与图床

| 工具 | 用途 | 注意 |
|------|------|------|
| [draw.io](https://www.draw.io) | 架构图/流程图 | 可导出 SVG |
| [ProcessOn](https://www.processon.com/) | 在线协作图 | 账号与隐私 |
| [asciiflow](http://asciiflow.com/) | ASCII 示意图 | 适合放进代码评审 |
| [squoosh.app](https://squoosh.app/) | 图片压缩 | 发博文前强烈推荐 |
| [sm.ms](https://sm.ms/) / [postimages](https://postimages.org/) | 图床 | **外链图床会挂**，重要图请放站内 `static/` |
| [百度脑图](https://naotu.baidu.com/) | 思维导图 | — |
| Markdown 转公众号类工具 | 排版迁移 | 注意样式污染 |

博客长期维护的经验：**图床是单点故障**。能进仓库的示意图尽量进仓库。

## 学术 / LaTeX

| 工具 | 用途 |
|------|------|
| [Codecogs LaTeX](http://latex.codecogs.com/) | 公式渲染 |
| [Overleaf Gallery](https://www.overleaf.com/gallery) | 模板参考 |
| [LaTeX 符号表](http://mohu.org/info/symbols/symbols.htm) | 符号速查 |
| [CORE 会议等级](http://portal.core.edu.au/conf-ranks) | 会议参考（仅供参考） |

## 效率杂项

| 工具 | 用途 |
|------|------|
| [smallpdf](https://smallpdf.com/) | PDF 处理 | 敏感文件勿上传 |
| [remove.bg](https://www.remove.bg/) | 抠图 |
| [cvmkr](https://cvmkr.com) | 简历模板类 | 隐私谨慎 |

## 我怎么维护这份清单

1. **按任务找工具**，而不是按名字收藏。  
2. 每加一个链接，写半句「解决什么问题」。  
3. 连续打不开或需强登录墙的，直接删。  
4. 安全类工具优先替换为可自托管/本地方案。

如果你有更好用的替代（尤其是可离线的），欢迎邮件告诉我，我会合并进这页。


## 使用约定

- 每月抽查失效链接并删除  
- 新增工具必须写「解决什么问题」一句  
- 安全类优先可离线替代  
- 不在清单里堆账号墙或恶意软件站  

本页是活文档，欢迎通过邮件提交替换项。把工具当手段，目标仍是把问题解决干净。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
