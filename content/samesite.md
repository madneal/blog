---
title: "SameSite 的七八事：Chrome 默认 Lax 之后，SSO iframe 为什么挂了"
author: "Neal"
summary: "从内网 SSO 在 iframe 中的 cookie 跨站问题出发，讲清 SameSite=Lax/Strict/None 的语义、Chrome 默认变化、以及安全与兼容的配置组合。"
cover: "/img/post-covers/samesite-6b626a3e0a.jpg"
tags: [安全, Web安全, Cookie, 前端]
categories: [安全]
date: "2021-02-17"
lastmod: "2026-08-08"
---


## 起源

写这篇文章的缘由是内网的一个真实需求。公司有一套 **SSO**，部分业务系统用 **iframe** 嵌登录态或统一认证页。Chrome 80 之后，对未声明 `SameSite` 的 Cookie 逐步按 **`Lax`** 默认处理，于是「以前好好的 iframe 登录」开始出现：父页面在 A 域，iframe 在 B 域，B 域会话 Cookie 带不过去，表现为反复跳登录、鉴权失败。

这不是业务代码突然写错了，而是 **浏览器把跨站 Cookie 的默认策略收紧了**。

## SameSite 到底限制什么

`SameSite` 是 Cookie 属性，用来约束 **跨站请求是否携带该 Cookie**。它直接关系 CSRF 防护，也影响嵌入式登录、支付、第三方组件。

| 值 | 大致行为 | 典型用途 |
|----|----------|----------|
| `Strict` | 几乎只有同站导航才带 Cookie | 高敏感会话 |
| `Lax` | 同站全带；跨站仅部分顶层导航 GET 带 | 默认折中 |
| `None` | 跨站也带，**必须同时 `Secure`** | iframe / 跨站 API 会话 |

「同站 / 跨站」按 **可注册域 + scheme** 等现代定义判断（`foo.example.com` 与 `bar.example.com` 通常算同站；`example.com` 与 `other.com` 算跨站）。内网若用不同父域或 IP + 域名混用，也容易被判跨站。

## 为什么 iframe SSO 中招

父页面：`https://app.corp.local`  
iframe：`https://sso.corp.local`（若被判跨站）或完整第三方 IdP。

iframe 内的请求属于 **跨站上下文** 时：

- Cookie 若为默认 `Lax`，在 iframe 的子请求里 **可能被扣下**  
- 登录成功后的会话无法建立或无法回传  
- 表现就是「嵌套登录死循环」

旧世界开发者依赖的是「不写 SameSite = 浏览器比较松」。新世界默认变严，历史系统集中爆雷。

## 正确的配置组合

### 1. 必须跨站携带的会话 Cookie

```http
Set-Cookie: session=...; SameSite=None; Secure; HttpOnly; Path=/
```

注意：

- `None` 没有 `Secure` 会被现代浏览器拒绝  
- 站点必须 HTTPS  
- 能 `HttpOnly` 就 `HttpOnly`，降低 XSS 偷会话风险  

### 2. 仅用于顶层跳转的 SSO

若登录始终是 **顶层 302 跳到 IdP 再跳回**，很多场景 `Lax` 已够用，不必一律 `None`。

### 3. 能不 iframe 就不 iframe

长期看，**顶层重定向 + 明确回调** 比嵌 iframe 更少踩 Cookie 策略。iframe SSO 既要过 SameSite，还要过 `X-Frame-Options` / CSP `frame-ancestors`。

## 和 CSRF 的关系

`SameSite` 是浏览器层对「跨站带 Cookie」的刹车，能挡掉大量经典 CSRF，但：

- 不能替代 CSRF Token（尤其同站子域互不信任时）  
- 对 `SameSite=None` 的接口，更要做好 CSRF / Origin 校验  
- XSS 面前 Cookie 策略帮不上太多忙  

## 排查清单

1. DevTools → Application → Cookies，看 `SameSite` / `Secure` 实际值  
2. Network 里跨站请求是否 **灰色未发送 Cookie**  
3. 是否混用 HTTP/HTTPS 导致 `Secure` Cookie 不生效  
4. 是否被 `Partitioned` / 第三方 Cookie 进一步限制（浏览器仍在演进）  
5. 服务端框架默认 Cookie 策略是否已改为 `Lax`  

## 代码侧（示意）

```python
# Django 示例概念
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
```

```java
// Servlet 概念
cookie.setSecure(true);
cookie.setHttpOnly(true);
// cookie.setAttribute("SameSite", "None"); // 视容器 API 而定
```

## 小结

- Chrome 把默认 `SameSite` 收到 `Lax`，是安全默认值的胜利，也是 iframe SSO 的噩梦。  
- 真要跨站嵌会话：`SameSite=None; Secure`，并补 CSRF 与框架安全头。  
- 能改成顶层跳转就改；少依赖第三方 Cookie。  
- 内网系统一样要测 Chromium 内核浏览器，不能只测旧 IE 心态。

SameSite 的「七八事」其实就一件事：**Cookie 不再默认替你在跨站场景默默打工**。安全工程要做的，是显式声明意图，而不是怀念默认宽松的年代。
