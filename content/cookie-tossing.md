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

We recently presented our GitHub Action Research at the Area41 conference in Zurich, Switzerland, where on the first day Thomas Houhou gave an interesting presentation on using Cookie Tossing attacks to increase the impact of Self-XSS issues into something worthy of being reported. This talk was great and showcased some novel uses of how Cookie Tossing can be used to hijack multi-step flows. Cookie Tossing, as a technique, is often overlooked or simply not well-known, and there is little published content on the topic.

We wanted to expand on the limited research currently available and see what additional implications Cookie Tossing attacks can lead to. We’ve found that Cookie Tossing can be used to hijack OAUTH flows and lead to Account Takeovers at the Identity Provider (IdP). 

我们最近在瑞士苏黎世的Area41会议上展示了我们的 GitHub Action 研究。在会议的第一天，[Thomas Houhou](https://www.thomashouhou.com/about-me) 进行了一个有趣的演讲，介绍了如何[利用 Cookie Tossing 攻击](https://www.youtube.com/watch?v=xLPYWim60jA)来增强 Self-XSS 问题的影响，使其变得值得报告。这次演讲非常精彩，展示了一些新颖的 Cookie Tossing 在劫持多步骤流程中的应用。作为一种技术，Cookie Tossing 常常被忽视或不为人知，关于这一主题的发表内容也很少。

我们希望扩展目前有限的研究，看看 Cookie Tossing 攻击还可能导致哪些额外的影响。我们发现，Cookie Tossing 可以用来劫持 OAUTH 流程，并导致身份提供者（IdP）的账户接管。

## What is Cookie Tossing?
## 什么是 Cookie Tossing?

Cookie Tossing is a technique that allows one subdomain (e.g. securitylabs.snyk.io) to set cookies on its parent domain (e.g. snyk.io). Before we look at some problematic scenarios let's first look at what HTTP cookies are.

Cookie Tossing 是一种技术允许一个子域名（例如 securitylabs.snyk.io）在其父域名（例如 snyk.io）上设置 cookie。在我们查看一些问题场景之前，先来了解一下 HTTP cookie 是什么。

## What are HTTP cookies?
## 什么是 HTTP cookies？

A cookie, defined in RFC 6265, is a small piece of data exchanged between a server and a user's web browser. These cookies are essential for web applications as they enable the storage of limited data and help maintain state information, addressing the inherently stateless nature of the HTTP protocol. Through cookies, user sessions can persist, preferences can be saved, and personalized experiences can be delivered.

Cookies come with various attributes and flags that define their behavior and scope. Here’s a primer on the key cookie attributes and flags:

根据 RFC 6265 的定义，Cookie 是服务器与用户的网页浏览器之间交换的一小段数据。这些 Cookie 对于网络应用至关重要，因为它们能够存储有限的数据并帮助维护状态信息，从而解决 HTTP 协议固有的无状态特性。通过 Cookie，用户会话可以持续，偏好设置可以被保存，并且可以提供个性化的体验。

Cookie 具有各种属性和标志，这些属性和标志定义了它们的行为和范围。以下是关于关键 Cookie 属性和标志的简要介绍：

| Attributes   | Attributes   | Attributes | Attributes | Attributes | Flags    | Flags     |  
|-------------|-------------|------------|------------|------------|----------|-----------|  
| Expires     | Max-Age     | Domain     | Path       | SameSite   | Secure   | HttpOnly  |

## Attributes
## 属性

1. **Expires**:

Sets the expiration date and time of the cookie.

Example: `Expires=Wed, 21 Oct 2024 07:28:00 GMT`

* 设置 cookie 的过期日期和时间。
* 例子：`Expires=Wed, 21 Oct 2024 07:28:00 GMT`

2. **Max-Age**:

Defines the cookie's lifetime in seconds.

Example: `Max-Age=3600`(1 hour)

* 定义 cookie 的生命周期（以秒为单位）。
* 例子：`Max-Age=3600`(1 小时)

3. **Domain**:

Specifies the domain the cookie is valid for, allowing subdomains to access it.

Example: `Domain=.snyk.io`

* 指定 cookie 有效的域名，允许子域名访问。
* 例子：`Domain=.snyk.io`

4. **Path**:

Limits the cookie to a specific path within the domain.

Example: `Path=/account`

* 将cookie限制在域内的特定路径。
* 例子：`Path=/account`

5. **SameSite**:

Controls cookie sending with cross-site requests for CSRF protection.
* 控制跨站请求中的cookie发送，以防止 CSRF 攻击。

* 值： `Strict`, `Lax`, `None`
* 例子：`SameSite=Lax`

Example: `SameSite=Lax`

## Flags
## 标志

1. **Secure**:

* Ensures the cookie is sent over HTTPS only.

* Example: `Secure`

* 确保 cookie 仅通过 HTTPS 发送。

* 示例：`Secure`

2. **HttpOnly**:

* Prevents cookie access via JavaScript, enhancing security.

* Example: `HttpOnly`

* 防止通过 JavaScript 访问cookie，增强安全性。

* 示例：`HttpOnly`

These attributes and flags define the lifespan, scope, and security of cookies, enabling effective and secure user session management.

这些属性和标志定义了 cookie 的生命周期、范围和安全性，从而实现有效和安全的用户会话管理。

## Setting cookies

## 设置 cookie

Cookies can be set either by the `Set-Cookie` header in an HTTP response or by using the JavaScript Cookie API. Here's a basic example of both methods:

Cookies 可以通过 HTTP 响应中的 `Set-Cookie` 头部或使用 JavaScript Cookie API 设置。以下是这两种方法的基本示例：

## Setting cookies with `Set-Cookie` header
## 使用 `Set-Cookie` 头设置 cookies

An HTTP response can include the Set-Cookie header to set a cookie: 

HTTP 响应可以包含 Set-Cookie 头部来设置一个 cookie：

```
HTTP/1.1 200 OK
Set-Cookie: userId=patch01; Expires=Wed, 21 Oct 2024 07:28:00 GMT; Domain=.snyk.io; Path=/;  Secure; HttpOnly; SameSite=Lax
```

## Setting cookies with JavaScript
## 使用 JavaScript 设置 Cookie

Using the JavaScript Cookie API, cookies can be set like this:

使用 JavaScript Cookie API，可以这样设置 cookie：

```
document.cookie = "userId=patch01; expires=Wed, 21 Oct 2024 07:28:00 GMT; path=/; domain=.snyk.io; secure; samesite=lax";
```

In the browser, cookies are stored as tuples consisting of the key, value, and attributes. When the browser sends a cookie back to the server, it only includes the key and value, not the attributes. Additionally, browsers have a maximum limit on the number of cookies per domain.

在浏览器中，Cookies 以包含键、值和属性的元组形式存储。当浏览器将 Cookie 发送回服务器时，仅包含键和值，而不包括属性。此外，浏览器对每个域名的 Cookie 数量有最大限制。

## Cookie domains

The Domain attribute of a cookie specifies which domains can access the cookie. By default, a cookie is only accessible to the domain that set it. However, you can use the Domain attribute to extend a cookie's accessibility. For instance, if a cookie is set by `blog.snyk.io` with the `Domain=.snyk.io` attribute, it will be accessible to all subdomains of `snyk.io`, such as `app.snyk.io` and `snyk.io` itself. Conversely, while the parent domain (snyk.io) can set a cookie to be accessible by all its subdomains using `Domain=.snyk.io`, it cannot explicitly set a cookie for a specific subdomain like `blog.snyk.io`. This approach allows for enhanced flexibility in multi-subdomain applications while maintaining control over which domains can share cookie data.

## Cookie paths and ordering

The Path attribute of a cookie specifies the subset of URLs to which the cookie applies. By default, the cookie is available to the path of the request URL that created it and its subdirectories. For instance, a cookie set with `Path=/account` will be accessible to /account and any subdirectories, such as /account/settings. Cookies are also ordered based on their Path attribute; cookies with more specific paths (e.g., /account/settings) are sent before cookies with less specific paths (e.g., /account). This order ensures that the most specific cookie is prioritized when multiple cookies match the request URL.

## Cookie 域

Cookie 的 Domain 属性指定了哪些域可以访问该 Cookie。默认情况下，Cookie 仅对设置它的域可用。然而，你可以使用 Domain 属性来扩展 Cookie 的可访问性。例如，如果一个 Cookie 是由 `blog.snyk.io` 设置的，并且具有 `Domain=.snyk.io` 属性，它将对 `snyk.io` 的所有子域可用，例如 `app.snyk.io` 和 `snyk.io` 本身。相反，虽然父域（snyk.io）可以使用 `Domain=.snyk.io` 设置一个 Cookie，使其可被所有子域访问，但它不能明确为特定子域（如 `blog.snyk.io`）设置 Cookie。这种方法在多子域应用程序中提供了更大的灵活性，同时保持对哪些域可以共享 Cookie 数据的控制。

## Cookie 路径和顺序

Cookie 的 Path 属性指定了 Cookie 适用的 URL 子集。默认情况下，Cookie 可用于创建它的请求 URL 的路径及其子目录。例如，使用 `Path=/account` 设置的 Cookie 将可用于 /account 及其任何子目录，例如 /account/settings。Cookie 还根据其 Path 属性进行排序；具有更具体路径（例如 /account/settings）的 Cookie 会在具有较少具体路径（例如 /account）的 Cookie 之前发送。这种顺序确保在多个 Cookie 匹配请求 URL 时，最具体的 Cookie 被优先考虑。

## Exploiting Cookie Tossing

The behavior of both the Domain and Path attributes can be leveraged to perform a Cookie Tossing attack. When an attacker gains control over a subdomain through an XSS vulnerability or by design (such as a service that creates subdomains for customers), they can set cookies on the parent domain. This might not seem dangerous at first, but it can be exploited by setting the attacker's session cookie on the victim's browser for specific endpoints.

For example, the attacker can set a cookie with `Domain=.snyk.io` and `Path=/api/payment`. As the victim uses the application, everything appears normal, and they are logged into their correct account. However, when they access certain API endpoints that handle sensitive data, such as adding a payment card, the application uses the attacker's cookie instead. This results in the victim's payment method being added to the attacker's account rather than their own.

Exploiting this scenario is not always straightforward, as applications leveraging anti-CSRF tokens can present a significant challenge. In such cases, the request includes the CSRF token from the victim rather than the attacker, causing the legitimate request to fail the anti-CSRF check and be discarded. Despite this hurdle, many applications are still vulnerable to these types of attacks. This is because many JSON-based API endpoints do not implement anti-CSRF mechanisms, relying instead on the Same Origin Policy (SOP) to prevent Cross-Origin requests with a Content-Type of `application/json` unless allowed through appropriate Cross-Origin-Resource-Sharing (CORS) headers. However, relying solely on CORS preflights to prevent CSRF attacks can mean that CSRF tokens are deemed unnecessary, which can leave endpoints exposed to cross-subdomain attacks. Additionally, applications that use custom headers or the Authorization header for managing session state are not susceptible to cookie tossing attacks, as the browser does not automatically submit these headers in the way it automatically submits cookies.

It is also worth mentioning that the SameSite cookie attribute does not provide any protection here due to the relaxed definition of a site within the context of SameSite cookies. Due to cookie tossing attacks needing to be launched from a subdomain, this will already satisfy the SameSite requirement even when set to `lax` or `strict`.

## 利用 Cookie Tossing 攻击

域名和路径属性的行为可以被利用来执行 Cookie Tossing 攻击。当攻击者通过 XSS 漏洞或设计（例如为客户创建子域名的服务）控制了一个子域名时，他们可以在父域名上设置 cookies。这乍一看似乎并不危险，但可以通过在受害者的浏览器上为特定端点设置攻击者的会话 cookie 来加以利用。

例如，攻击者可以设置一个 `Domain=.snyk.io` 和 `Path=/api/payment` 的 cookie。当受害者使用该应用程序时，一切看起来都是正常的，他们登录了自己的正确账户。然而，当他们访问处理敏感数据的某些 API 端点时，例如添加支付卡，应用程序却使用了攻击者的 cookie。这导致受害者的支付方式被添加到攻击者的账户中，而不是他们自己的账户。

利用这种情况并不总是简单，因为利用反 CSRF 令牌的应用程序可能会带来重大挑战。在这种情况下，请求中包含的是受害者的 CSRF 令牌，而不是攻击者的，这导致合法请求未能通过反 CSRF 检查而被丢弃。尽管存在这一障碍，许多应用程序仍然容易受到这些类型的攻击。这是因为许多基于 JSON 的 API 端点并未实施反 CSRF 机制，而是依赖同源策略（SOP）来防止带有 `application/json` 内容类型的跨源请求，除非通过适当的跨源资源共享（CORS）头部允许。然而，仅依靠 CORS 预检来防止 CSRF 攻击可能会导致 CSRF 令牌被视为不必要，这可能使端点暴露于跨子域攻击。此外，使用自定义头部或授权头部来管理会话状态的应用程序不易受到 cookie tossing 攻击，因为浏览器不会像自动提交 cookies 那样自动提交这些头部。

还值得一提的是，由于在 SameSite cookie 的上下文中对站点的定义放宽，SameSite cookie 属性在这里并不提供任何保护。由于 cookie tossing 攻击需要从子域发起，这已经满足了 SameSite 的要求，即使设置为 `lax` 或 `strict`。

## Revisiting GitPod

[GitPod](https://www.gitpod.io/) is a popular Cloud Development Environment (CDE) that allows its customers to deploy complete development environments within seconds. We have previously looked at GitPod during our [research on WebSockets](https://snyk.io/blog/gitpod-remote-code-execution-vulnerability-websockets/) and from this we already knew GitPod hosts its environments on a subdomain of the `gitpod.io`domain and it was possible to execute JavaScript on this subdomain. With this knowledge, we decided to explore what implications the Cookie Tossing attack might have using a real application as our test bed to show a legitimate impact.

With GitPod needing access to its user’s source code repositories to allow engineers to checkout and commit code using their product, one idea was to check how the OAUTH flow from GitPod to providers such as GitHub or BitBucket is handled and if they might be susceptible to this attack. After monitoring the flow when configuring a new Git provider we observed a typical OAUTH flow and decided to try tossing our attacker’s session cookies onto the API endpoints relevant for the OAUTH process. 

To test this scenario, we created some JavaScript that we hosted on our CDE instance at `redacted.ws–eu114.gitpod.io` to toss the` _gitpod_io_jwt2_` cookie to contain the value of our attacker's session cookie value, with the path being set to the following:

* /api/authorize

* /auth/bitbucket/callback

We won’t go into the details on how we were able to host arbitrary JavaScript using our GitPod workspace in this post as we have already covered it [here](https://snyk.io/blog/gitpod-remote-code-execution-vulnerability-websockets/), but once our JavaScript payload is set, we can send a victim the URL to our workspace which when accessed, will set our Cookies as described above. 

The victim will not see anything out of the ordinary, and when they go back to using GitPod their session will appear completely normal. However, if the victim decides to connect their account to a Git provider, GitPod will start the OAUTH flow from the attacker account and when the provider redirects the client back to GitPod with the OAUTH code, it will connect the victim's Git account with our attackers GitPod account.

This allowed us to create Gitpod workspaces from any repositories to which the victim user has access, including being able to push new commits and modify source-code within the victim's repositories.

The sequence diagram below can be used to visualize the complete flow for the above Cookie Tossing attack against GitPod.

![](https://res.cloudinary.com/snyk/image/upload/f_auto,w_2560,q_auto/v1732628085/Screenshot_2024-11-26_at_8.34.18_AM.png)

This issue was reported to GitPod on June 26th 2024 which was promptly fixed on July 1st 2024 [in this PR](https://github.com/gitpod-io/gitpod/pull/19973) by leveraging the __Host- cookie prefix. The vulnerability was issued as CVE-2024-21583.

## __Host- cookie prefix

Fortunately, there exists a simple solution for addressing Cookie Tossing issues. The `__Host-` cookie prefix can be used to restrict cookies from being sent to any host other than the one that set the cookie. Additionally, the cookies with the `__Host-` prefix cannot modify the `domain` or `path` attributes, which prevents a malicious subdomain from being able to set cookies on the parent domain or target a specific path.

 Final thoughts

Cookie Tossing is a unique and often overlooked vulnerability that affects applications not explicitly using the `__Host-` cookie prefix. We have demonstrated how this weakness can be exploited to force sensitive requests to execute under an attacker’s session context, potentially exposing sensitive data. In complex workflows, such as those leveraging the OAuth protocol, this can inadvertently grant an attacker access to resources on third-party services. Our previous research indicates that the use of the `__Host-` prefix is rare, leaving many organizations—particularly those hosting applications on subdomains—vulnerable. Whenever state-changing requests meet the conditions described in this post, they can be susceptible to hijacking.