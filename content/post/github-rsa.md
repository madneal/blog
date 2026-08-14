---
title: "GitHub 更新了 RSA SSH host key"
author: Neal
summary: "本文围绕《GitHub 更新了 RSA SSH host key》梳理security、安全、Git和开源相关的背景、方法和实践细节，可作为排查与学习记录。"
cover: "/img/post-covers/github-rsa-144c1dec63.jpg"
tags: [安全, Git, 开源]
categories: [security]
date: "2023-03-24"
lastmod: "2026-08-08"
---

今天在 push 自己 GitHub 仓库代码的时候遇到了报错，后来发现是 GitHub 已经将 RSA SSH host key 进行了更新。依据[官方博客](https://github.blog/2023-03-23-we-updated-our-rsa-ssh-host-key/)，GitHub 于 3月24日 05:00 UTC 时间 由于安全原因将 RSA SSH host key 进行了更新。主要是为了避免 GitHub 用户的 git 操作被任何不法分子监听。这个变更仅影响基于 RSA 的 SSH 协议使用 GitHub 进行 git 操作的用户。变更也只影响 RSA 算法，不影响 ECDSA 或者 Ed25519 用户。

GitHub 这周发现了他们的 RSA SSH 密钥在公共仓库中暴露。根据他们的调查结果，这个问题暂不涉及 GitHub 任何系统或者用户信息被窃取。依据他们的解释是保险起见进行 host key 的更新。


报错信息可能如下：

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
SHA256:uNiVztksCsDhcc0u9e8BujQXVUpKZIDTMczCvj3tD2s.
Please contact your system administrator.
Add correct host key in ~/.ssh/known_hosts to get rid of this message.
Host key for github.com has changed and you have requested strict checking.
Host key verification failed.
```

可以通过下述命令移除老的 key，也可以在 `~/.ssh/known_hosts` 文件里面手动删除去更新。

```
ssh-keygen -R github.com
```

你也可在 `~/.ssh/known_hosts` 文件中手动添加新的 RSA SSH 公钥。

```
github.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk=
```

或者通过命令进行自动更新。

```
ssh-keygen -R github.com
$ curl -L https://api.github.com/meta | jq -r '.ssh_keys | .[]' | sed -e 's/^/github.com /' >> ~/.ssh/known_hosts
```

Github Action 用户如果使用带有 `ssh-key` 选项的 `actions/checkout` 用户也可能会看到工作流的失败日志。目前 GitHub 已经对对应的 `actions/checkout` 进行了更新。

## Reference

* https://github.blog/2023-03-23-we-updated-our-rsa-ssh-host-key/


## 操作清单（更新后）

1. 阅读 [GitHub 官方说明](https://github.blog/2023-03-23-we-updated-our-rsa-ssh-host-key/)，确认指纹。  
2. 从 `~/.ssh/known_hosts` 删除旧 `github.com` 条目（`ssh-keygen -R github.com`）。  
3. 重新连接一次：`ssh -T git@github.com`，核对新 RSA 指纹后接受。  
4. 企业代理/跳板机上的 `known_hosts` 也要同步更新，否则 CI 仍会失败。  
5. 若使用 `ssh.github.com` 或自定义 Host 别名，对应条目一并处理。

## 安全含义

Host key 相当于「你连上的是不是真的 GitHub」。泄露或替换 host key 可导致中间人截获 Git 凭据与代码。GitHub 主动轮换是正确响应；用户侧最重要的是 **不要盲目点 yes**，而要对照官方公布的指纹。

## 与密钥类型

此次是 **服务器 host key** 变更，不是你本机 `id_rsa` 用户密钥。用户仍可继续用 Ed25519/ECDSA/RSA 用户密钥；推荐新环境优先 `ed25519`。

## 小结

看到 `REMOTE HOST IDENTIFICATION HAS CHANGED` 先停手，查官方指纹，清理 known_hosts，再恢复 push/pull。把该检查写进团队 onboarding，可减少集体踩坑。


## CI/CD 特别注意

GitHub Actions、Jenkins、GitLab Runner 镜像里的 `known_hosts` 可能被烤进基础镜像。轮换 host key 后，要重建镜像或在 pipeline 里显式更新指纹，否则只有本地能推、流水线全红。

建议在 Ansible/镜像构建脚本中集中管理 Git 托管商 host key，并做版本注释，避免各处手工 `ssh-keygen -R`。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
