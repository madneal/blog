---
title: "SFTP 未关闭 Session 导致服务器 sshd 进程残留"
author: Neal
summary: "JSch 使用 ChannelSftp 后只 disconnect channel 不够：必须关闭 Session，否则远端 sshd 会话进程堆积。附正确释放顺序与 finally 模板。"
tags: [后端, Java, 工具, SFTP]
categories: [java开发]
date: "2016-07-28"
lastmod: "2026-08-08"
---

## 现象

项目里用 **JSch** 做 SFTP 上传下载。代码上线后，服务器上多了很多迟迟不退出的进程（与 sshd/会话相关）。业务「看起来能传文件」，但主机连接数与进程表被慢慢打满。

## 错误用法

常见写法：连上 → 传文件 → `sftp.quit()` / `sftp.disconnect()`，以为结束了。

```java
protected boolean connectToServer() {
    try {
        JSch jsch = new JSch();
        Session sshSession = jsch.getSession(userName, hostname, port);
        sshSession.setPassword(password);
        Properties sshConfig = new Properties();
        sshConfig.put("StrictHostKeyChecking", "no"); // 生产请正确校验 host key
        sshSession.setConfig(sshConfig);
        sshSession.setTimeout(TIMEOUT);
        sshSession.connect();
        sftp = (ChannelSftp) sshSession.openChannel("sftp");
        sftp.connect();
        return sftp.isConnected();
    } catch (Exception ex) {
        logger.error("sftp connect failed", ex);
        return false;
    }
}
```

只关 channel：

```java
sftp.quit();
sftp.disconnect();
// Session 仍在！
```

**Channel 关了，Session 还活着**，远端会话与本地资源都可能残留。

## 正确释放顺序

建议：

1. 退出 SFTP 子系统（`exit`/`quit`）  
2. `disconnect` Channel  
3. **`disconnect` Session**  
4. 全部放进 `finally`，避免异常路径泄漏  

```java
Session session = null;
ChannelSftp sftp = null;
try {
    // connect ...
    session = jsch.getSession(userName, hostname, port);
    // ...
    session.connect();
    sftp = (ChannelSftp) session.openChannel("sftp");
    sftp.connect();
    // upload / download ...
} finally {
    if (sftp != null) {
        try { sftp.disconnect(); } catch (Exception ignore) {}
    }
    if (session != null) {
        try { session.disconnect(); } catch (Exception ignore) {}
    }
}
```

关键一行（在仍持有 channel 时也可）：

```java
if (sftp != null && sftp.getSession() != null) {
    sftp.getSession().disconnect();
}
```

## 为何会堆进程

SSH 是会话型协议：每个 Session 对应一组服务端状态。只关 SFTP channel 等于关了一个子系统，**登录会话未结束**，服务端侧仍可能保留进程/连接，直到超时。高频任务下就会「进程越堆越多」。

## 额外建议

| 项 | 建议 |
|----|------|
| 连接复用 | 池化 Session，但必须有空闲回收与强制 disconnect |
| 超时 | `setTimeout` / ServerAlive 避免僵死连接 |
| 安全 | 避免 `StrictHostKeyChecking=no`；用密钥而非硬编码密码 |
| 可观测 | 指标：活跃 session 数、上传失败率 |
| 替代 | 长期可评估 MinIO/对象存储 SDK，减少自运维 SFTP |

## 小结

JSch 资源释放的口诀：**Channel 和 Session 都要断，且放在 finally**。只 `sftp.disconnect()` 等于只关了一半门，sshd 侧的「人」还没走。
