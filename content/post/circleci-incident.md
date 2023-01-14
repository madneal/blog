---
title: "CircleCI 20230104 安全事件报告"
author: Neal
tags: [网络安全,安全事件,事件报告]
keywords: [网络安全,安全事件,事件报告,CircleCI]
categories: [网络安全]
date: "2023-01-14" 
---

# CircleCI 20230104 安全事件报告

>原文：[CircleCI incident report for January 4, 2023 security incident(https://circleci.com/blog/jan-4-2023-incident-report/)
>
>译者：[madneal](https://github.com/madneal)
>
>welcome to star my [articles-translator](https://github.com/madneal/articles-translator/), providing you advanced articles translation. Any suggestion, please issue or contact [me](mailto:bing@stu.ecnu.edu.cn)
>
>LICENSE: [MIT](https://opensource.org/licenses/MIT)

[2023 年 1 月 4 日，我们提醒客户](https://circleci.com/blog/january-4-2023-security-alert/) 一起安全事件。 今天，我们想与您分享发生的事情、我们学到的知识以及我们未来不断改善安全态势的计划。

我们要感谢我们的客户对于重置密钥的关注，并对此次事件可能对您的工作造成的任何干扰表示歉意。我们鼓励尚未采取行动的客户采取行动，以防止未经授权访问第三方系统和存储。此外，我们要感谢我们的客户和社区在我们进行彻底调查期间的耐心等待。为了实现负责任的披露，我们已尽最大努力在共享信息的速度与保持调查的完整性之间取得平衡。

**本报告包含:**

* 发生了什么？
* 我们怎么知道这个攻击向量已经关闭并且可以安全构建？
* 与客户的沟通和支持
* 如何判断我是否受影响？
* 可能有助于您的团队进行内部调查的详细信息
* 我们从这次事件中学到了什么以及我们下一步将做什么
* 关于员工责任与系统保障措施的说明
* 安全最佳实践
* 结语

## 发生了什么？

*除非另有说明，否则所有日期和时间均以 UTC 报告。*

2022 年 12 月 29 日，我们的一位客户提醒我们注意可疑的 GitHub OAuth 活动。此通知启动了 CircleCI 的安全团队与 GitHub 的更深入审查。

2022 年 12 月 30 日，我们了解到该客户的 GitHub OAuth 令牌已被未经授权的第三方泄露。尽管该客户能够迅速解决问题，但出于谨慎考虑，我们在 2022 年 12 月 31 日代表客户主动启动了更换所有 GitHub OAuth 令牌的流程。尽管与 GitHub 合作提高 API 速率限制，但轮换过程需要时间 虽然目前尚不清楚其他客户是否受到影响，但我们继续扩大分析范围。

到 2023 年 1 月 4 日，我们的内部调查已经确定了未经授权的第三方入侵的范围和攻击的进入路径。迄今为止，我们了解到未经授权的第三方利用部署到 CircleCI 工程师笔记本电脑上的恶意软件来窃取有效的、支持 2FA 的 SSO session。这台机器于 2022 年 12 月 16 日遭到入侵。我们的防病毒软件未检测到该恶意软件。我们的调查表明，该恶意软件能够执行 session cookie 盗窃，使他们能够在远程位置冒充目标员工，然后升级为对我们生产系统子集的访问。

由于目标员工有权生成生产访问令牌作为员工日常职责的一部分，因此未经授权的第三方能够从数据库和存储的子集访问和泄露数据，包括客户环境变量、令牌和密钥。我们有理由相信，未经授权的第三方在 2022 年 12 月 19 日进行了侦察活动。2022 年 12 月 22 日 发生了泄露事件，这是我们生产系统中最后一次未经授权活动的记录。尽管所有泄露的数据都是静态加密的，但第三方从正在运行的进程中提取了加密密钥，使他们能够访问加密数据。

虽然我们对内部调查的结果充满信心，但我们已聘请第三方网络安全专家协助我们进行调查并验证我们的调查结果。我们迄今为止的发现基于对我们的身份验证、网络和监控工具的分析，以及我们合作伙伴提供的系统日志和日志分析。

针对这一事件，我们采取了以下行动：

* 2023 年 1 月 4 日 16:35 UTC，我们关闭了帐户被盗员工的所有访问权限。
* 2023 年 1 月 4 日 28:30 UTC，我们关闭了几乎所有员工的生产访问权限，限制了极少数群体的访问权限以解决运营问题。在此调查期间，我们从未有任何证据表明任何其他员工或他们的设备的凭证已被泄露，但我们采取此行动是为了限制潜在的攻击面。
* 2023 年 1 月 4 日 22:30 UTC，我们修改了了所有可能暴露的生产主机，以确保安全的生产机器。
* 2023 年 1 月 5 日 03:26 UTC，我们撤销了所有项目 API 令牌。
* 2023 年 1 月 6 日 05:00 UTC，我们撤销了在 2023 年 1 月 5 日 00:00 UTC 之前创建的所有个人 API 令牌。
* 2023 年 1 月 6 日 06:40 UTC，我们开始与 Atlassian 的合作伙伴合作，代表我们的客户轮换所有 Bitbucket token。这项工作于 2023 年 1 月 6 日 10:15 UTC 完成。
* 2023 年 1 月 7 日 07:30 UTC，我们完成了 GitHub OAuth 令牌的修改，该修改是我们于 2022 年 12 月 31 日 04:00 UTC 开始的。
* 2023 年 1 月 7 日 18:30 UTC，我们开始与 AWS 的合作伙伴合作，通知客户可能受影响的 AWS token。据我们了解，这些通知已于 2023 年 1 月 12 日 00:00 UTC 时完成。

在此期间，我们在外部调查人员的支持下继续进行取证调查，在我们的平台上推出额外的安全层，并构建和分发额外的工具（更多详情见下文）以支持我们的客户保护他们的 secrets。

## 我们怎么知道这个攻击向量已经关闭并且可以安全构建？

我们相信客户可以安全地在 CircleCI 上构建。

自从意识到这种攻击以来，我们采取了许多措施，既关闭了攻击向量，又增加了额外的安全层，包括：

* 通过我们的 MDM 和 A/V 解决方案添加了针对此次攻击中使用的恶意软件表现出的特定行为的检测和阻止。
* 由于我们实施了额外的安全措施，因此仅限极少数员工访问生产环境 我们对我们平台的安全性充满信心，并且没有迹象表明任何其他员工的设备遭到入侵。
* 对于保留生产访问权限的员工，我们添加了额外的升级身份验证步骤和控制。 这将帮助我们防止可能的未经授权的生产访问，即使在 2FA 支持的 SSO session 被盗的情况下也是如此。
* 跨多个触发器并通过各种第三方供应商对我们在此场景中确定的特定行为模式实施监控和警报。

我们知道安全工作永远不会结束。除了关闭这个特定的向量，我们还进行了增强和持续的审查，以确保加强对潜在攻击的防御。

## 与客户的沟通和支持

在 2023 年 1 月 4 日 22:30 UTC 完成所有生产主机的轮换后，我们确信我们已经消除了攻击向量和破坏主机的可能性。

2023 年 1 月 5 日 02:30 UTC，我们发送了披露电子邮件，[在我们的博客上发布了安全通知](https://circleci.com/blog/january-4-2023-security-alert/)，通过我们的社交媒体帐户和我们的讨论论坛通知客户，并创建了一篇关于如何执行建议的安全步骤的支持文章。

我们建议所有客户更改他们的 secrets，包括 OAuth 令牌、项目 API 令牌、SSH 密钥等（有关更多详细信息，请参阅博客文章或讨论文章）。

此披露启动了与我们客户的积极和持续的沟通期。我们要感谢我们的客户对这一事件的一致响应，以及帮助我们找到机会为您提供额外的工具。我们接受了这些反馈，并作为回应构建并发布了新工具并修改了我们现有的工具，以通过以下方式为客户加快修复速度：

* [秘密发现脚本](https://github.com/CircleCI-Public/CircleCI-Env-Inspector) 以创建可操作的秘密轮换列表。
* CircleCI API 的两个关键变化：
     * 返回结帐密钥的 SHA-256 签名的新功能，以便更好地匹配 GitHub UI。
     * `updated_at` 字段已添加到 Contexts API 中，以便客户可以验证这些变量是否已成功轮换。
* 免费和付费计划的所有客户都可以访问审计日志，以帮助客户审查 CircleCI 平台活动。

我们感谢客户就我们可以改进沟通的地方提供的所有反馈，包括让事件在我们的渠道中更加明显的机会。

## 我怎么知道我是否受到了影响？

### 我的数据有风险吗？

在此事件中，未经授权的行为者于 2022 年 12 月 22 日窃取了客户信息，其中包括第三方系统的环境变量、密钥和令牌。如果您在此期间将机密信息存储在我们的平台上，请假设它们已被访问并采取建议的缓解措施。我们建议您从 2022 年 12 月 16 日开始调查系统中的可疑活动，并在我们于 2023 年 1 月 4 日披露后完成机密修改之日结束。2023 年 1 月 5 日之后进入系统的任何内容都可以被认为是安全的。

### 是否有未经授权的行为者使用该数据访问我的任何系统？

由于此事件涉及第三方系统的密钥和令牌外泄，我们无法知道您的 secret 是否被用于未经授权访问这些第三方系统。 我们在下面提供了一些详细信息，以帮助客户进行调查。

**在发布时，只有不到 5 位客户通知我们由于此事件而未经授权访问第三方系统。**

## 可能有助于您的团队进行内部调查的详细信息

在第三方取证调查员的帮助下，我们最近确认了可能有助于客户进行审计和调查的更多详细信息。

### 影响日期：

* 我们在 2022 年 12 月 19 日看到未经授权的第三方访问，数据泄露发生在 2022 年 12 月 22 日。
* 我们没有证据表明 2022 年 12 月 19 日之前有影响客户的活动。出于谨慎考虑，我们建议您调查从 2022 年 12 月 16 日事件开始到 1 月之后修改 secret 之间的这段时间系统中存在异常活动。

### 识别为被威胁行为者使用的 IP 地址：

* 178.249.214.10
* 89.36.78.75
* 89.36.78.109
* 89.36.78.135
* 178.249.214.25
* 72.18.132.58
* 188.68.229.52
* 111.90.149.55

### Data centers and VPN providers identified as being used by the threat actor:

### 数据中心和 VPN 提供商被识别为被威胁行为者使用：

* Datacamp Limited
* Globalaxs Quebec Noc
* Handy Networks, LLC
* Mullvad VPN

### Malicious files to search for and remove:

### 搜索和删除的恶意文件：

* /private/tmp/.svx856.log
* /private/tmp/.ptslog
* PTX-Player.dmg (SHA256: 8913e38592228adc067d82f66c150d87004ec946e579d4a00c53b61444ff35bf)
* PTX.app

### 拦截以下域名

* potrax[.]com

### 查看 GitHub 审核日志文件以查找意外命令，例如：

* repo.download_zip

## 我们从这次事件中学到了什么以及我们接下来要做什么

**我们了解到：虽然我们有适当的工具来阻止和检测攻击，但总有机会加强我们的安全态势。**

我们拥有的身份验证、安全和跟踪工具使我们能够全面诊断和修复问题。随着恶意攻击者越来越复杂，我们正在不断改进我们的安全标准并推动最佳实践以保持领先于未来的威胁。我们将越来越积极地使用安全工具。展望未来，为了支持更保守的立场并防止攻击者不当访问我们的系统，我们将优化现有工具的配置以创建额外的防御层。

### 我们的计划：

首先，我们将为所有客户启动定期自动 OAuth 令牌轮换。 我们的计划还包括从 OAuth 到 GitHub 应用程序的转变，使我们能够在令牌中实施更精细的权限。我们还计划完成对我们所有工具配置的全面分析，包括第三方审查。我们将继续采取其他措施，包括扩大告警范围、减少会话信任、添加额外的身份验证因素以及执行更定期的访问轮换。最后，我们将使我们的系统权限更加短暂，严格限制从类似事件中获得的任何令牌的目标值。

### 我们学习到：我们可以让客户更轻松地采用我们最先进的安全功能。

通过 CircleCI 的发展，我们不断引入功能来提高客户构建管道的安全性。虽然客户可以使用高级安全功能，但我们可以做更多工作来提高这些功能的采用率。

### 我们的计划：

客户必须更容易无缝地采用可用的最新和最先进的安全功能，包括 OIDC 和 IP 范围。我们还在探索其他主动步骤，例如，自动令牌过期和未使用 secret 的通知。我们将使我们的客户更简单、更方便地创建和维护高度安全的管道，在智能管理风险的同时实现云的每一个优势。

## 关于员工责任与系统保障措施的说明

我们想说清楚。虽然一名员工的笔记本电脑通过这种复杂的攻击被利用，但安全事件是系统故障。作为一个组织，我们的责任是建立多层防护措施来抵御所有攻击向量。

## 安全最佳实践

鉴于成熟和有动机的攻击者越来越多，我们致力于与我们的客户分享最佳实践，以加强我们对未来不可避免的尝试的集体防御。以下是客户可以用来提高管道安全性的建议：

* 尽可能使用 [OIDC 令牌](https://circleci.com/docs/openid-connect-tokens/) 以避免在 CircleCI 中存储长期存在的凭据。
* 利用 [IP 范围](https://circleci.com/docs/ip-ranges/) 将您系统的入站连接限制为仅已知 IP 地址。
* 使用 [Contexts](https://circleci.com/docs/contexts/) 合并共享机密并将对机密的访问限制为特定项目，然后可以[通过 API 自动轮换](https://circleci.com /docs/contexts/#rotating-environment-variables）。
* 对于特权访问和其他控制，您可以选择使用 [runners](https://circleci.com/docs/runner-overview/#circleci-runner-use-cases)，它允许您将 CircleCI 平台连接到 您自己的计算和环境，包括 IP 限制和 IAM 管理。

## 结语

我们知道没有合适的时间来响应关键系统上的安全事件，我们要衷心感谢所有在事件发生后立即采取行动的客户。正是通过这种集体行动，我们将能够更有力地应对未来的威胁。我们还亲眼目睹了我们客户社区的力量和慷慨，你们中的许多人前往我们的讨论论坛分享知识并互相帮助。感谢您在我们努力解决此事件时的支持和耐心。