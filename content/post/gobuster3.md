---
title: "gobuster源码阅读--终篇"
author: Neal
tags: [web安全, gobuster, 源码阅读]
keywords: [web安全, gobuster, 源码阅读]
categories: [源码阅读]
date: "2022-04-22" 
---

在搞完 gobuster 系列源码阅读的[第一篇]以及[dir篇]之后，对于 gobuster 的实现思路已经比较熟悉。本文就对剩下的模块进行一个讲解，由于一些公共模块在前面的两篇文章中已经提过，所以本文主要专注于每个模块所独有的部分。

在前面的文章中提到过，gobuster 中的各个模块中的核心功能都是基于 `libgobuster/interfaces.go` 中接口的实现。而 `PreRun` 以及 `Run` 函数则是每个模块实现的核心所在，所以关注其它模块这两个函数的实现的即可。

## dns

对于 `dns` 模块中的 `PreRun`，其内部也有一个 `ErrWildcard` 的实现。其实现过程也有一点类似于 `dir` 模块。通过将 `uid` 和 `domain` 进行拼接，理论上这个域名应该不存在，会报一个 `no such host` 的报错。如果不存在这个报错，则表明对于任意域名都会解析成同一个 IP。如果没有报错，则表明这里可能存在 `ErrWildcard`。

```go
wildcardIps, err := d.dnsLookup(ctx, fmt.Sprintf("%s.%s", guid, d.options.Domain))
if err == nil {
    d.isWildcard = true
    d.wildcardIps.AddRange(wildcardIps)
    if !d.options.WildcardForced {
        return &ErrWildcard{wildcardIps: d.wildcardIps}
    }
}
```

在通过 `PreRun` 函数之后，即是 `Run` 函数的实现，这个函数的实现基本上逻辑非常简单，就是解析出域名对应的 IP 即可。

## s3

s3 模块主要用于亚马逊云存储桶的包括，里面的实现逻辑比较简单，主要是基于 `https://%s.s3.amazonaws.com/?max-keys=%d` url 的请求访问结果。可以在 github 上随便找一个公开的链接访问看看。

![image.png](https://s2.loli.net/2022/04/22/3hgmbpGaYCiZ6E4.png)

如果是一个实际存在的 bucket，则会返回 xml 内容。否则的话，状态响应码则为 400 或者 404。另外在 s3 模块中 `Run` 函数的实现还会对获取的 xml 内容进行解析。

## vhost 

vhost 模块的 `PreRun` 函数亦是做了一些检查工作，不过里面做一项比较特别的工作。在该函数中分别会正常请求一次，再请求一次 uid 和 domain 拼接起来的 Host 的响应体，分别为 `normalBody` 以及 `abnormalBody`。

```go
// request default vhost for normalBody
_, _, _, body, err := v.http.Request(ctx, v.options.URL, libgobuster.RequestOptions{ReturnBody: true})
v.normalBody = body

// request non existent vhost for abnormalBody
subdomain := fmt.Sprintf( "%s.%s", uuid.New(), v.domain)
_, _, _, body, err = v.http.Request(ctx, v.options.URL, libgobuster.RequestOptions{Host: subdomain, ReturnBody: true})
v.abnormalBody = body
```

在 `Run` 函数的处理逻辑中，通过将响应体的内容和 `normalBody` 与 `abnormalBody` 进行对比，如果都不一样的话，则为有效 Host。

## fuzz

fuzz 模块基本上与 dir 模块的内容接近，只不过它是通过 fuzz 的形式来进行枚举，通过替换 url 中的执行词来进行 fuzz 操作。

除了以上的模块，其它的主要是一些辅助的公共函数，比如数据结构的处理以及发送请求的方法。

## 总结

至此，gobuster 的源码基本阅读完了。gobuster 的源码相对来说比较简短精悍，没有晦涩难懂的语法，非常适合源码的阅读。同时，其在并发请求上的处理也非常有借鉴意义，非常适合作为造轮子的参考工具。