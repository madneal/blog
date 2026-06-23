---
title: "SameSite 的七八事"
author: Neal
summary: "本文围绕《SameSite 的七八事》展开，重点梳理起源等内容，提炼背景、思路与实践注意点。"
cover: "/img/post-covers/samesite-6b626a3e0a.jpg"
tags: [安全, Web安全, 漏洞分析, 前端]
categories: [安全]
date: "2021-02-17"
---

## 起源

本篇文章是讨论关于 SameSite 这一属性的相关内容。这次讨论的缘由是内网的一个需求。内网有一个 SSO 应用，但是在 Chrome 80 版本之后，将会强制实行 SameSite 的属性。即 SameSite 的属性默认为 Lax。而这一变化则会影响到这一应用，因为这个 SSO 使用了 iframe，所以会涉及到 cookie 的跨域。
