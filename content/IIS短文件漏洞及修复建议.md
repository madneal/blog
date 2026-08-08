---
title: "IIS短文件漏洞及修复建议"
author: Neal
summary: "本文围绕《IIS短文件漏洞及修复建议》展开，重点梳理什么是 IIS 短文件漏洞和漏洞修复等内容，提炼背景、思路与实践注意点。"
tags: [安全, Web安全, 漏洞分析]
categories: [安全]
date: "2019-01-14"
lastmod: "2026-08-08"
---

最近公司有几个系统有发现 IIS 短文件名的漏洞，这个漏洞也是比较久的漏洞了，网上也是有不少的修复方案。但是有的修复方案还是没有彻底修复。以下也是自己做一个全面的总结以及彻底以及完美的修复方案。

## 什么是 IIS 短文件漏洞

为了兼容 16 位的 MS-DOS 程序，Windows 为文件名较长的文件（文件夹）生成了对应的 windows 8.3 短文件名。在 Windows 下，对应的短文件名可以使用 `dir /x` 命令来查看。如下图，`.gitconfig` 对应的短文件名就是 `GITCON~1`.



> **（原外链配图已失效移除，请以正文说明为准）**



基于此特性，并结合 IIS 对于请求路径中包含通配符不同的响应的特性，IIS 对于存在的短文件名的响应码为 404，对不存在的短文件名的响应码是 400.根据这个特点，可以暴力破解出 IIS 中存在的短文件名。关于短文件漏洞， Soroush Dalili 在 2012 年就有[论文](https://soroush.secproject.com/downloadable/microsoft_iis_tilde_character_vulnerability_feature.pdf)是关于这方面的研究。里面详细阐述了 IIS 短文件名的漏洞利用原理。


## 漏洞修复

关于该漏洞的修复，一般的修复就是停止创建短文件名，可以通过修改注册表来实现：


但是在修复的过程中会遇到一个问题，通过修改注册表，我们可以以后不再创建短文件名。但是之前已经存在的短文件名还是存在漏洞的。一般的修复建议是要删除部署文件，然后重新部署。但是有时候，我们无法直接删除文件或者不希望删除文件


## Reference

http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/37473/cn_zh/1510647047395/short%20name.png

https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/ff621566(v=ws.11)

https://support.microsoft.com/en-us/help/121007/how-to-disable-8-3-file-name-creation-on-ntfs-partitions

https://www.tecklyfe.com/windows-server-tip-disable-8-3-naming-strip-existing-short-names/


https://serverfault.com/questions/670658/fixing-the-iis-tilde-vulnerability


## 修复要点（务实）

1. 确认问题：用短文件名探测工具在 **授权范围** 内验证 404/400 差异。  
2. 注册表/组策略关闭 8.3 名生成（需评估遗留应用兼容性）。  
3. IIS 配置与补丁按微软与安全厂商通告落地。  
4. 仅关「模糊错误页」往往不够，要组合文件系统策略。  
5. 修复后回归：旧探测路径应不再可区分。

## 业务影响

短文件名泄露可帮助攻击者猜 `.aspx`、备份、`web.config` 等敏感路径，从而加速后续利用。它常被当成「信息泄露」低估，在渗透链路里却很值钱。

## 小结

老洞也能打穿新资产。修复要 **验证—加固—再验证**，并记录兼容性例外，而不是只丢一条「已加固」工单。


## 验证命令思路

在授权环境中对比短名猜测与真实资源响应差异；修复后相同探测应收敛为一致的拒绝或 404。将验证截图与变更单号归档，方便审计复查。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
