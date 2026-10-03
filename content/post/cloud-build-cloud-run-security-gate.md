---
title: "从自动发布到安全发布：Cloud Build 白盒扫描实践"
author: "Neal"
cover: "https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/optimized/covers/8577d5bbfff35a6c2b07.webp"
date: "2026-10-03T12:00:00+08:00"
summary: "在 Cloud Build 中接入 Go-SAST，以硬编码检测验证源码扫描、失败阻断、镜像发布和 Cloud Run 部署的安全卡点。"
tags: [GCP, Cloud Build, Cloud Run, SAST, DevSecOps]
categories: [安全]
draft: false
---

## 背景

最近在做 GCP 应用发布流程的安全卡点，重点关注通过 Cloud Build 构建应用、打包镜像，再部署到 Cloud Run 的场景。

自动化交付提高了发布效率，但也需要回答一个问题：**如何在部署前检查源码，并阻止存在安全问题的版本继续发布？**

本次使用个人 GitHub 仓库进行演示：

- [mcpgogo](https://github.com/madneal/mcpgogo)：测试应用，用于验证构建、镜像推送和部署流程。
- [go-sast](https://github.com/madneal/go-sast)：白盒扫描工具，本次以硬编码问题检测验证安全卡点。

GitHub 只是演示中的代码来源。企业环境也可以接入内部 GitLab，根据实际部署方式配置仓库连接、构建触发和网络访问。

## 整体架构

白盒扫描放在 Cloud Build 获取源码之后、应用镜像构建之前。扫描通过，流水线继续；发现需要阻断的问题或扫描执行失败，流水线终止。

![Cloud Build 与 Cloud Run 白盒安全卡点架构图](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/optimized/content/5ad21011a96d778dd6dd.webp)

[查看高清架构图](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/optimized/content/5ad21011a96d778dd6dd.webp)

主流程自上而下，失败分支向左退出。各组件的职责如下：

| 组件 | 职责 |
|---|---|
| GitHub / 内部 GitLab | 托管代码，提供构建触发来源 |
| [Cloud Build](https://cloud.google.com/build/docs) | 执行扫描、测试、构建和部署步骤 |
| Go-SAST | 检查源码中的硬编码问题 |
| [Artifact Registry](https://cloud.google.com/artifact-registry/docs) | 存储扫描器镜像和应用镜像 |
| [Cloud Run](https://cloud.google.com/run/docs) | 运行发布的应用容器 |

## 接入白盒扫描

将 Go-SAST 打包为独立容器镜像并推送到 Artifact Registry 后，Cloud Build 可以直接调用它检查本次构建中的源码。

这里需要区分两种镜像：**扫描器镜像用于执行检查，应用镜像用于部署运行。** 架构图省略了扫描器镜像的拉取过程，以突出应用发布主线。

扫描步骤的配置示例如下：

```yaml
steps:
  - id: go-sast
    name: asia-southeast1-docker.pkg.dev/${PROJECT_ID}/security-gate/go-sast:153d312
    args:
      - --path
      - /workspace
      - --fail-on-findings
```

镜像地址需要对应实际存放扫描器的仓库。`${PROJECT_ID}` 引用构建项目，`/workspace` 是扫描目标目录。工具版本应固定，便于追踪检查结果和规则变化；需要更严格的版本约束时，可以使用镜像摘要。

扫描通过后，流水线继续执行格式检查、单元测试、应用构建、镜像构建与推送，最后部署到 Cloud Run。演示中的实现可以查看 [mcpgogo 测试 PR](https://github.com/madneal/mcpgogo/pull/2)。

## 让扫描成为发布条件

增加扫描步骤，并不自动意味着建立了安全卡点。关键是让扫描结果决定后续步骤能否执行。

| 扫描结果 | 流水线行为 |
|---|---|
| 未发现达到阻断标准的问题 | 继续后续步骤 |
| 发现需要阻断的问题 | 返回失败，终止发布 |
| 工具异常或扫描未完成 | 返回失败，终止发布 |

不能忽略扫描错误，也不能让部署步骤通过并行执行绕过检查。随着规则增加，还需要明确问题分级、阻断标准和例外审批机制。

本次以硬编码检测验证链路，只覆盖特定类型的问题。扫描通过表示满足当前规则要求，不代表应用不存在其他漏洞。

## 防止卡点被绕过

正式环境建议将 PR / MR 检查与发布流程分开：代码评审阶段执行扫描，尽早反馈问题；合并到受保护分支后，发布流水线再次检查实际要部署的源码。

还需要落实以下约束：

- **保证版本一致。** 扫描本次提交，从同一份源码构建，并部署本次产出的镜像。演示此前使用 `latest` 标签，正式发布更适合记录并使用镜像摘要。
- **保护构建配置。** 删除扫描步骤、调整阻断规则或忽略失败等变更，应经过审核。
- **限制发布权限。** 控制直接部署 Cloud Run 和修改构建触发器的权限，避免绕过流水线。
- **分离构建与运行身份。** 构建账号按需获得推送和部署权限，应用运行账号仅保留运行所需权限。

Cloud Run 入口认证和应用自身登录属于访问控制，与源码白盒检查解决不同的问题，需要分别设计。

## 接入内部 GitLab

将代码来源换成内部 GitLab 后，扫描、阻断和发布机制保持一致，主要变化在仓库接入层。

首先，需要确保构建环境能够访问代码源；对于私有网络中的 GitLab，需要配套的网络连接。其次，仓库访问凭据应受控管理，并限制授权范围。最后，应区分 MR 检查与发布分支构建，同时保护流水线配置及发布权限。

个人 GitHub 仓库适合验证流程，内部 GitLab 则可以承载企业研发协作。两者都应遵循同一个原则：**在受控的发布链路中检查源码，并用检查结果决定是否允许发布。**

## 实践结果与后续方向

本次已取得扫描、测试、构建和镜像推送的成功记录，完成过 Cloud Run 服务部署，并将部署步骤加入构建配置。最后几次配置精简后的完整执行结果，仍需单独核验。

后续可以扩展静态分析规则，完善问题分级、例外审批和扫描记录追踪。白盒卡点的价值不仅在于发现问题，还在于让需要阻断的问题无法通过正常发布流程进入运行环境。
