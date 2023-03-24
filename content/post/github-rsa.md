---
title: "GitHub 更新了 RSA SSH host key"
author: Neal
tags: [GitHub,cybersecurity,RSA,git]
categories: [security]
date: "2023-03-24" 
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