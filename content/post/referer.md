---
title: "JavaScript能否修改Referer请求头"
author: Neal
summary: "本文围绕《JavaScript能否修改Referer请求头》梳理安全、Web安全和JavaScript相关的背景、方法和实践细节，可作为排查与学习记录。"
cover: "/img/post-covers/referer-6807e52ec2.jpg"
tags: [安全, Web安全, JavaScript]
categories: [安全]
date: 2021-03-09
lastmod: "2026-08-08"
---

正如题目，本文的也很直白，主要就是围绕这个问题展开。JavaScript 能否修改 Referer 请求头？现在 JavaScript 的能力越来越强大，JavaScript 似乎无所不能，修改一个小小的 Referer 请求头似乎看来不在话下（本文讨论的 JavaScript 仅限于在浏览器中执行，不包括 Nodejs）。

其实不然，在 web 浏览器中，绝大多数浏览器都禁止了 JavaScript 直接去操作 Referfer 请求头，当然这一方面也是出于安全方面的考虑。当然除了 Referer 请求头之外，还有其它请求头也被禁止通过 JavaScript 操作。

Referer 请求头属于 Forbidden header，这种请求头无法通过程序来修改，浏览器客户端一般会禁止这种行为。以 `Proxy-` 和 `Sec-` 开头的请求头都属于 Fobidden header name，还包括以下这些请求头：

```
Accept-Charset
Accept-Encoding
Access-Control-Request-Headers
Access-Control-Request-Method
Connection
Content-Length
Cookie
Cookie2
Date
DNT
Expect
Feature-Policy
Host
Keep-Alive
Origin
Proxy-
Sec-
Referer
TE
Trailer
Transfer-Encoding
Upgrade
Via
```

可以通过一段简单的 demo 来进行验证。可以通过 Chrome 的开发者工具来进行验证，创建一个 xhr 请求，并且尝试来设置请求头。

![image.png](https://i.loli.net/2021/03/09/mwgJZQ2MPtlT14o.png)

可以看出，如果设置 `content-type`，浏览器没有阻止，但是如果设置 `Referer` 的话，浏览器则不允许，提示 `Refused to set unsafe header "Referer"`。

得益于这一特性，其实 Referer 请求头也被用于作为 CSRF 防护的补充手段之一，如果用户是通过恶意网站来访问应用的，可以通过 Referer 请求头来进行验证。但是，因为一些浏览器兼容性的特性以及可以通过某些手段可以强制不带 Referer 请求头，所以这个方法只能作为一个补充方法来进行验证。

## Reference
* https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_header_name


## 为什么浏览器要锁 Referer

`Referer` 参与 CSRF 防护、统计分析、防盗链。若页面脚本可任意改写，攻击者就能伪造来源，绕过「只接受本站 Referer」的弱校验，或污染日志。因此规范把一批请求头列为 **禁止被 JS 篡改**（forbidden request headers），包括 `Cookie`、`Host`、`Referer` 等。

## 开发者能做什么

| 需求 | 做法 |
|------|------|
| 控制发送策略 | `Referrer-Policy` 响应头 |
| 少泄露路径 | `strict-origin-when-cross-origin` 等 |
| 服务端校验 | 勿把 Referer 当唯一 CSRF 防线，应用 Token + SameSite |
| 测试伪造 | 用 Burp 改请求，而不是幻想页面 JS 改 Referer |

## 与安全测试

测试防盗链或 CSRF 时，在代理里改 Referer 是合法手法；前端 XSS 无法直接「设一个完美 Referer」来冒充站内跳转。若业务只靠 Referer 做鉴权，本身就是设计缺陷。

## 小结

浏览器里的 JS **不能**可靠修改 `Referer`。这是平台安全边界，不是 bug。业务安全应建立在 Cookie 策略、CSRF Token 与服务端鉴权上，而不是信任来源头。


## 相关头字段

除 `Referer` 外，`Origin`、`Sec-Fetch-*` 等也为浏览器控制。服务端做 CSRF 判断时可组合这些信号，但仍不能替代 CSRF Token。了解「谁能改什么头」是 Web 安全基本功。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
