---
title: "用 Burp MCP 把代理能力接进 Claude CLI"
author: "Neal"
summary: "在 Burp Suite 安装 MCP Server 扩展，配置 Claude CLI 的 SSE 连接，打通 Proxy/Repeater/Scanner 等工具调用，并整理常见报错。"
tags: [安全, Burp, AI, 工具]
categories: [安全]
date: "2026-01-01"
lastmod: "2026-08-08"
---


把 Burp 的流量与工具暴露给 AI 助手，可以显著加快「解释请求、改包、对照扫描结果」这类重复劳动。PortSwigger 生态里的 **MCP Server** 扩展，让 Claude CLI（或其它支持 MCP 的客户端）通过 SSE 调用 Burp 能力。

> 仅在 **授权测试环境** 使用。AI 自动发请求同样可能造成破坏，生产与未授权目标不要接。

## 前置条件

- Burp Suite（Community / Pro 均可，功能集以你的许可为准）  
- 已安装 [Claude CLI](https://docs.anthropic.com/en/docs/claude-code) 或兼容 MCP 的客户端  
- 本机 Java 运行时（通常随 Burp 提供）  
- 浏览器或系统代理已指向 Burp（默认 `127.0.0.1:8080`）

## 步骤 1：安装 MCP Server 扩展

1. 打开 Burp Suite  
2. **Extensions → BApp Store**  
3. 搜索 **MCP Server** 并 Install  
4. 在 **Extensions → Installed** 确认已加载  

扩展默认会在本机拉起 SSE 服务，常见地址：

```text
http://127.0.0.1:9876/
```

注意路径是 **根路径 `/`**，不是想当然的 `/sse`。

## 步骤 2：配置 Claude CLI

在项目根目录创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "burp-mcp": {
      "type": "sse",
      "url": "http://127.0.0.1:9876/"
    }
  }
}
```

若客户端支持全局 MCP 配置，也可以写到用户级配置；原则是 **URL 与 Burp 监听一致**。

## 步骤 3：连接与自检

1. 先开 Burp，再开 Claude CLI  
2. 在 CLI 中执行 `/mcp` 或重启会话  
3. 看到成功连接后，可让助手列出可用 tools  

建议自检：

- 浏览目标站，确认 Proxy History 有流量  
- 让助手读取最近一条 HTTP history  
- 再尝试创建 Repeater tab（只读环境可先不做修改类操作）

## 能力概览（以扩展实际暴露为准）

| 类别 | 可做的事 |
|------|----------|
| Proxy | 读 HTTP/WebSocket 历史 |
| Scanner | 读扫描问题（Pro 更完整） |
| Repeater | 创建/管理 tab |
| Intruder | 送入 Intruder |
| Collaborator | 生成载荷、查交互 |
| 直接请求 | 发 HTTP/1、HTTP/2 |
| 编解码 | Base64、URL 等 |
| 配置 | 读写部分 project/user 选项 |

具体 tool 名称与数量随扩展版本变化，以连接后的清单为准。

## 推荐工作流

1. **人工保证范围**：scope、靶场、流量来源先圈死  
2. **AI 做解释与草稿**：解释参数、猜数据流、起草 PoC  
3. **人工点发送**：高风险 Intruder / 批量请求不要全自动  
4. **结果回写笔记**：把结论贴回 writeup，而不是只留在聊天窗口  

和「纯聊天生成 payload」相比，接上 Burp 的好处是：**上下文来自真实抓包**，幻觉会少很多。

## 故障排除

| 问题 | 处理 |
|------|------|
| `HTTP 404 .../sse` | URL 改为 `http://127.0.0.1:9876/`（根路径） |
| `-32000` / 连接失败 | 确认 Burp 已开、扩展已加载、端口未被占用 |
| 历史为空 | 浏览器是否走 Burp 代理；证书是否信任 |
| 超时 | 本机防火墙/安全软件拦截回环端口 |
| CLI 连上但无 tool | 重启双方；检查 MCP 配置是否被项目覆盖 |

## 安全建议

- MCP 监听绑定在 `127.0.0.1`，**不要**改成 `0.0.0.0` 暴露到局域网  
- 与 AI 云端通信时，注意请求里是否含 token、Cookie；可先脱敏  
- 公司环境需确认：把流量摘要发到外部模型是否合规  

## 小结

Burp MCP 的价值不是「让 AI 替你黑进去」，而是把 **代理里的真实上下文** 接到助手上，缩短从抓包到理解的时间。装好扩展、SSE 指对根路径、先开 Burp 再连 CLI，这三步做对，基本就能用起来；其余是权限、范围与合规问题。
