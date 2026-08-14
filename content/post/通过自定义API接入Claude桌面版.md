---
title: "改三个 JSON，让 Claude 桌面版用上你自己的 API"
author: Neal
summary: "Claude Desktop 默认只能官方账号登录。本文基于 cc-switch 源码分析与实操，讲解如何利用官方内置的 3p 企业网关模式，通过三个 JSON 配置文件让桌面版接入任意 Anthropic 兼容 API，并复用 Claude Code CLI 的现有配置。"
cover: "/img/post-covers/claude-3p-gateway-v2-20260801.jpg"
tags: [AI, 工具]
keywords: [Claude, Claude Desktop, Claude Code, cc-switch, API, 网关, Anthropic]
categories: [开发工具]
date: "2026-08-01"
---

> 无需破解、不改 App 本体：利用 Claude Desktop 官方内置的企业「推理网关」模式，
> 把请求指向你自己的 Anthropic 兼容 API 端点。本文源自对开源工具
> [cc-switch](https://github.com/farion1231/cc-switch) 的源码分析与一次完整实操。

## 背景

Claude Desktop（桌面版 Claude App）默认只能通过 Anthropic 官方账号登录使用。但很多
场景下我们手里有的是 API：公司内部的 LLM 网关、第三方中转服务、或官方 API key。
Claude Code（CLI）早就支持通过 `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` 环境
变量接入任意兼容端点，而桌面 App 表面上没有提供这个入口。

开源工具 cc-switch 在 v3.x 里实现了「Claude 桌面版切换供应商」，读它的源码
（`src-tauri/src/claude_desktop_config.rs`）可以发现：**Claude Desktop 其实内置了
一个面向企业的「第三方部署模式」（`deploymentMode: "3p"`）和推理网关（inference
gateway）配置通道**。所谓"通过 API 接入"，就是把 App 切到这个模式，再把你的 API
地址和 key 伪装成一个网关 profile 写进配置文件。全程只改用户目录下的 JSON 配置，
不碰 App 本体，随时可逆。

## 原理：三个配置文件

以 macOS 为例（Windows 对应 `%LOCALAPPDATA%` 下的同名目录），涉及两个数据目录：

- `~/Library/Application Support/Claude/` —— 官方模式（1p）的数据目录
- `~/Library/Application Support/Claude-3p/` —— 第三方模式（3p）的独立数据目录

需要写入三类文件：

### 1. 部署模式开关

两个目录下的 `claude_desktop_config.json` 都写入：

```json
{ "deploymentMode": "3p" }
```

App 启动时读到 `"3p"` 就会跳过官方账号推理通道，转而加载网关 profile；改回
`"1p"` 即恢复官方登录。

### 2. 网关 profile

`Claude-3p/configLibrary/<PROFILE_ID>.json`（cc-switch 使用固定 ID
`00000000-0000-4000-8000-000000157210`）：

```json
{
  "inferenceProvider": "gateway",
  "inferenceGatewayBaseUrl": "https://your-gateway.example.com/v1",
  "inferenceGatewayApiKey": "sk-xxx",
  "inferenceGatewayAuthScheme": "bearer",
  "disableDeploymentModeChooser": true,
  "coworkEgressAllowedHosts": ["*"],
  "inferenceModels": [
    "claude-sonnet-5",
    { "name": "claude-opus-5", "labelOverride": "我的 Opus" },
    { "name": "claude-sonnet-5", "supports1m": true }
  ]
}
```

这就是核心：App 会按 Anthropic Messages API 格式向 `inferenceGatewayBaseUrl`
发请求，用 Bearer token 认证。`inferenceModels` 可选，不写则用 App 默认模型列表；
条目可以是字符串，也可以是带 `labelOverride`（UI 显示名）和 `supports1m`
（1M 上下文标记）的对象。

### 3. profile 注册表

`Claude-3p/configLibrary/_meta.json`，告诉 App 当前激活哪个 profile：

```json
{
  "appliedId": "00000000-0000-4000-8000-000000157210",
  "entries": [{ "id": "00000000-0000-4000-8000-000000157210", "name": "claude3p" }]
}
```

恢复官方模式时的逆操作：`deploymentMode` 改回 `"1p"`、删除 profile 文件、从
`_meta.json` 移除条目并清掉 `appliedId`，另外清理 3p 配置里 `enterpriseConfig`
下的网关字段。

## 实操中踩到的两个坑

### 坑一：baseUrl 必须是 https

第一次我们直接复用了 CLI 里的内网 `http://` 网关地址，App 启动后弹出报错：

```
Invalid custom3p managed config: baseUrl: must use https (or http on loopback)
failingField: baseUrl
```

**Claude Desktop 对网关地址有强制校验：必须 `https://`，`http://` 仅允许
loopback（`127.0.0.1` / `localhost`）。** 解法有两个：

1. 网关本身支持 https 就直接换协议（用 `curl` 试一下，返回 401 说明 TLS 正常、
   只是没带认证，可以用）；
2. 网关只有 http 的话，在本地起一个 loopback 转发代理，profile 里填
   `http://127.0.0.1:<port>`——cc-switch 的「代理模式」就是这么做的。

### 坑二：模型 ID 必须是 Claude 命名

`inferenceModels` 里的模型 ID 会被 App 内置的校验器检查，必须形如：

```
claude-sonnet-*   claude-opus-*   claude-haiku-*   claude-fable-*
```

（也接受 `anthropic/claude-` 前缀。）**只要有一个不合法（比如 `gpt-4o`），
整组模型都会被拒收**（fail-all）。所以第三方非 Claude 命名的模型不能直连，需要
中间代理把合法的 Claude 模型名映射到真实模型——这也是 cc-switch 代理模式的另一个
存在理由。

## 复用 Claude Code CLI 的配置

如果你已经在用 Claude Code CLI 接第三方 API，那么 `~/.claude/settings.json` 的
`env` 块里已经有全部所需信息，直接搬过来即可：

| CLI 配置（settings.json → env） | 桌面版 profile 字段 |
|---|---|
| `ANTHROPIC_BASE_URL` | `inferenceGatewayBaseUrl`（注意 https 限制） |
| `ANTHROPIC_AUTH_TOKEN` | `inferenceGatewayApiKey`（bearer） |
| `ANTHROPIC_DEFAULT_OPUS/SONNET/HAIKU_MODEL` | `inferenceModels` 列表 |

cc-switch 的直连模式读取的正是这几个字段、原样写入 profile——所以 CLI 能用的
Anthropic 兼容端点，桌面版一定能用（https 前提下）。

## 一个最小实现

我们照 cc-switch 的逻辑写了一个约 300 行的单文件 Python 脚本
（`claude3p.py`），提供三个命令：

```bash
# 复用 CLI 配置一键切换（也可 --base-url/--api-key 手动指定）
./claude3p.py apply --from-cli

# 查看当前模式 / 网关地址 / 模型列表
./claude3p.py status

# 恢复官方账号登录
./claude3p.py restore
```

除了写配置本身，有几个工程细节值得照搬 cc-switch：

- **原子写入**：先写临时文件再 `rename`，避免写一半留下损坏的 JSON；
- **快照回滚**：修改前对四个目标文件做内存快照，中途任何一步失败自动恢复原状；
- **自动备份**：每次操作前把现有文件备份到带时间戳的目录，手工可救；
- **前置校验**：写入前就拦截非 https 地址和非 Claude 命名的模型 ID，
  好过让 App 启动后弹错。

## 限制与注意事项

- 端点必须兼容 **Anthropic Messages API**（App 会请求 `<baseUrl>/v1/messages`）；
  OpenAI 格式端点需要代理做格式转换。
- 3p 模式使用独立的 `Claude-3p` 数据目录，**会话历史与官方账号互不相通**，
  restore 后官方历史原样回来。
- 每次改动后需要**完全退出**（Cmd+Q）并重启 Claude Desktop 才生效。
- 这是官方为企业网关准备的通道，未来 App 版本的校验规则可能变化
  （例如模型角色白名单就随版本更新过）。

## 参考

- [cc-switch 仓库](https://github.com/farion1231/cc-switch)
- [claude_desktop_config.rs 源码](https://github.com/farion1231/cc-switch/blob/main/src-tauri/src/claude_desktop_config.rs)
