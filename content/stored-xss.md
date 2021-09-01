---
title: "富文本场景下的 XSS"
author: Neal
tags: [web 安全, XSS, JS, GO]
categories: [安全]
date: 2021-08-30
---

富文本编辑器是一个常见的业务场景，一般来说，通过富文本编辑器编辑的内容最终也会 html 的形式来进行渲染，比如 VUE，一般就会使用