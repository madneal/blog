---
title: "通过 Cookie Tossing 劫持 OAUTH 流程"
author: Neal
tags: [安全]
keywords: [API,web 安全]
categories: [安全]
date: "2025-02-06" 
---

> 原文：[Hijacking OAUTH flows via Cookie Tossing](https://snyk.io/articles/hijacking-oauth-flows-via-cookie-tossing/)
>
> 译者：[madneal](https://github.com/madneal)
>
> welcome to star my [articles-translator](https://github.com/madneal/articles-translator/), providing you advanced articles translation. Any suggestion, please issue or contact [me](mailto:bing.ecnu@gmail.com)
>
> LICENSE: [MIT](https://opensource.org/licenses/MIT)

我们最近在瑞士苏黎世的Area41会议上展示了我们的 GitHub Action 研究。在会议的第一天，[Thomas Houhou](https://www.thomashouhou.com/about-me) 进行了一个有趣的演讲，介绍了如何[利用 Cookie Tossing 攻击](https://www.youtube.com/watch?v=xLPYWim60jA)来增强 Self-XSS 问题的影响，使其变得值得报告。这次演讲非常精彩，展示了一些新颖的 Cookie Tossing 在劫持多步骤流程中的应用。作为一种技术，Cookie Tossing 常常被忽视或不为人知，关于这一主题的发表内容也很少。

我们希望扩展目前有限的研究，看看 Cookie Tossing 攻击还可能导致哪些额外的影响。我们发现，Cookie Tossing 可以用来劫持 OAUTH 流程，并导致身份提供者（IdP）的账户接管。

## 什么是 Cookie Tossing?

Cookie Tossing 是一种技术允许一个子域名（例如 securitylabs.snyk.io）在其父域名（例如 snyk.io）上设置 cookie。在我们查看一些问题场景之前，先来了解一下 HTTP cookie 是什么。

## 什么是 HTTP cookies？

根据 RFC 6265 的定义，Cookie 是服务器与用户的网页浏览器之间交换的一小段数据。这些 Cookie 对于网络应用至关重要，因为它们能够存储有限的数据并帮助维护状态信息，从而解决 HTTP 协议固有的无状态特性。通过 Cookie，用户会话可以持续，偏好设置可以被保存，并且可以提供个性化的体验。

Cookie 具有各种属性和标志定义它们的行为和范围。以下是关于 Cookie 关键属性和标志的简要介绍：

| Attributes   | Attributes   | Attributes | Attributes | Attributes | Flags    | Flags     |  
|-------------|-------------|------------|------------|------------|----------|-----------|  
| Expires     | Max-Age     | Domain     | Path       | SameSite   | Secure   | HttpOnly  |

## 属性

1. **Expires**:

* 设置 cookie 的过期日期和时间。
* 示例：`Expires=Wed, 21 Oct 2024 07:28:00 GMT`

2. **Max-Age**:

* 定义 cookie 的生命周期（以秒为单位）。
* 示例：`Max-Age=3600`(1 小时)

3. **Domain**:

* 指定 cookie 有效的域名，允许子域名访问。
* 示例：`Domain=.snyk.io`

4. **Path**:

* 将cookie限制在域内的特定路径。
* 示例：`Path=/account`

5. **SameSite**:

* 控制跨站请求中的cookie发送，以防止 CSRF 攻击。
* 值： `Strict`, `Lax`, `None`
* 示例：`SameSite=Lax`

## 标志

1. **Secure**:

* 确保 cookie 仅通过 HTTPS 发送。
* 示例：`Secure`

2. **HttpOnly**:

* 防止通过 JavaScript 访问cookie，增强安全性。
* 示例：`HttpOnly`

这些属性和标志定义了 cookie 的生命周期、范围和安全性，从而实现有效和安全的用户会话管理。

## 设置 cookie

Cookies 可以通过 HTTP 响应中的 `Set-Cookie` 头部或使用 JavaScript Cookie API 设置。以下是这两种方法的基本示例：

## 使用 `Set-Cookie` 头设置 cookies

HTTP 响应可以包含 Set-Cookie 头部来设置一个 cookie：

```
HTTP/1.1 200 OK
Set-Cookie: userId=patch01; Expires=Wed, 21 Oct 2024 07:28:00 GMT; Domain=.snyk.io; Path=/;  Secure; HttpOnly; SameSite=Lax
```

## 使用 JavaScript 设置 Cookie

使用 JavaScript Cookie API，可以这样设置 cookie：

```
document.cookie = "userId=patch01; expires=Wed, 21 Oct 2024 07:28:00 GMT; path=/; domain=.snyk.io; secure; samesite=lax";
```

在浏览器中，Cookies 以包含键、值和属性的元组形式存储。当浏览器将 Cookie 发送回服务器时，仅包含键和值，而不包括属性。此外，浏览器对每个域名的 Cookie 数量有最大限制。

## Cookie 域

Cookie 的 Domain 属性指定了哪些域可以访问该 Cookie。默认情况下，Cookie 仅对设置它的域可用。然而，你可以使用 Domain 属性来扩展 Cookie 的可访问性。例如，如果一个 Cookie 是由 `blog.snyk.io` 设置的，并且具有 `Domain=.snyk.io` 属性，它将对 `snyk.io` 的所有子域可用，例如 `app.snyk.io` 和 `snyk.io` 本身。相反，虽然父域（snyk.io）可以使用 `Domain=.snyk.io` 设置一个 Cookie，使其可被所有子域访问，但它不能明确为特定子域（如 `blog.snyk.io`）设置 Cookie。这种方法在多子域应用程序中提供了更大的灵活性，同时保持对哪些域可以共享 Cookie 数据的控制。

## Cookie 路径和顺序

Cookie 的 Path 属性指定了 Cookie 适用的 URL 子集。默认情况下，Cookie 可用于创建它的请求 URL 的路径及其子目录。例如，使用 `Path=/account` 设置的 Cookie 将可用于 /account 及其任何子目录，例如 /account/settings。Cookie 还根据其 Path 属性进行排序；具有更具体路径（例如 /account/settings）的 Cookie 会在具有较少具体路径（例如 /account）的 Cookie 之前发送。这种顺序确保在多个 Cookie 匹配请求 URL 时，最具体的 Cookie 被优先考虑。 

## 利用 Cookie Tossing 攻击

域名和路径属性的特性可以被利用来执行 Cookie Tossing 攻击。当攻击者通过 XSS 漏洞或设计（例如为客户创建子域名的服务）控制了一个子域名时，他们可以在父域名上设置 cookies。这乍一看似乎并不危险，但可以通过在受害者的浏览器上为特定端点设置攻击者的会话 cookie 来加以利用。

例如，攻击者可以设置一个 `Domain=.snyk.io` 和 `Path=/api/payment` 的 cookie。当受害者使用该应用程序时，一切看起来都是正常的，他们登录了自己的正确账户。然而，当他们访问处理敏感数据的某些 API 端点时，例如添加支付卡，应用程序却使用了攻击者的 cookie。这导致受害者的支付方式被添加到攻击者的账户中，而不是他们自己的账户。

利用这种情况并不太简单，因为利用 anti-CSRF 令牌的应用程序可能会带来重大挑战。在这种情况下，请求中包含的是受害者的 CSRF 令牌，而不是攻击者的，这导致合法请求未能通过 anti-CSRF 检查而被丢弃。尽管存在这一障碍，许多应用程序仍然容易受到这些类型的攻击。这是因为许多基于 JSON 的 API 端点并未实施 anti-CSRF 机制，而是依赖同源策略（SOP）来防止带有 `application/json` 内容类型的跨源请求，除非通过适当的跨源资源共享（CORS）头部允许。然而，仅依靠 CORS 预检来防止 CSRF 攻击可能会导致 CSRF 令牌被视为不必要，这可能使端点暴露于跨子域攻击。此外，使用自定义头部或授权头部来管理会话状态的应用程序不易受到 cookie tossing 攻击，因为浏览器不会像自动提交 cookies 那样自动提交这些头部。

还值得一提的是，由于在 SameSite cookie 的上下文中对站点的定义放宽，SameSite cookie 属性在这里并不提供任何保护。由于 cookie tossing 攻击需要从子域发起，这已经满足了 SameSite 的要求，即使设置为 `lax` 或 `strict`。

## 重新审视 GitPod

[GitPod](https://www.gitpod.io/) 是一个流行的云开发环境（CDE），允许客户在几秒钟内部署完整的开发环境。我们之前在对 [WebSockets](https://snyk.io/blog/gitpod-remote-code-execution-vulnerability-websockets/) 的研究中已经关注过 GitPod，并且从中了解到 GitPod 在 `gitpod.io` 域名的子域上托管其环境，并且可以在该子域上执行 JavaScript。基于这一知识，我们决定探索 Cookie Tossing 攻击可能带来的影响，使用一个真实应用作为测试平台，以展示其合法影响。

由于 GitPod 需要访问用户的源代码库，以便工程师能够使用其产品进行代码检出和提交，我们的一个想法是检查 GitPod 到 GitHub 或 BitBucket 等提供者的 OAUTH 流程是如何处理的，以及它们是否可能受到此攻击的影响。在配置新的 Git 服务商时，我们监控了该流程，观察到一个典型的 OAUTH 流程，并决定尝试将攻击者的会话 cookie 投放到与 OAUTH 过程相关的 API 端点上。

为了测试这一场景，我们创建了一些 JavaScript，并将其托管在我们的 CDE 实例 `redacted.ws–eu114.gitpod.io` 上，以便将 `_gitpod_io_jwt2_` cookie 的值设置为我们攻击者的会话 cookie 值，路径设置为以下内容：

* /api/authorize
* /auth/bitbucket/callback

我们在这篇文章中不会详细讨论如何利用我们的 GitPod 工作区托管任意 JavaScript，因为我们已经在[这里](https://snyk.io/blog/gitpod-remote-code-execution-vulnerability-websockets/)进行了说明，但一旦我们的 JavaScript 负载设置完成，我们可以将工作区的 URL 发送给受害者，当他们访问该 URL 时，将会设置我们上面所述的 Cookies。

受害者不会看到任何异常，当他们返回使用 GitPod 时，他们的会话看起来完全正常。然而，如果受害者决定将他们的账户连接到 Git 服务商，GitPod 将从攻击者账户开始 OAUTH 流程，当提供者将客户端重定向回 GitPod 并带上 OAUTH 代码时，将会把受害者的 Git 账户与我们的攻击者 GitPod 账户连接起来。

这使我们能够从受害者用户有权限访问的任何代码库创建 GitPod 工作区，包括能够推送新的提交和修改受害者代码库中的源代码。

下面的时序图可以用来可视化上述针对 GitPod 的 Cookie 投掷攻击的完整流程。

![](https://res.cloudinary.com/snyk/image/upload/f_auto,w_2560,q_auto/v1732628085/Screenshot_2024-11-26_at_8.34.18_AM.png)

此问题于2024年6月26日报告给GitPod，并于2024年7月1日通过利用 __Host-（原作者误将 __Host- 前缀写作 `__Host__` ） cookie前缀迅速修复 [在此PR中](https://github.com/gitpod-io/gitpod/pull/19973)。该漏洞被标记为CVE-2024-21583。

## __Host- cookie 前缀

幸运的是，解决 Cookie Tossing 问题有一个简单的方案。可以使用 `__Host-` cookie 前缀来限制 cookie 仅发送到设置该 cookie 的 host。此外，带有 `__Host-` 前缀的 cookie 不能修改 `domain` 或 `path` 属性，这防止了恶意子域能够在父域上设置 cookie 或针对特定路径。

最后的思考

Cookie Tossing 是一种独特且常被忽视的漏洞，影响那些没有明确使用 `__Host-` cookie 前缀的应用程序。我们已经展示了这种弱点如何被利用，以迫使敏感请求在攻击者的会话上下文中执行，从而可能暴露敏感数据。在复杂的工作流程中，例如利用 OAuth 协议的工作流程，这可能无意中授予攻击者对第三方服务资源的访问权限。我们之前的研究表明，使用 `__Host-` 前缀的情况很少，这使得许多组织，特别是那些在子域上托管应用程序的组织，处于脆弱状态。每当状态改变请求满足本文所述的条件时，它们可能会受到劫持的威胁。