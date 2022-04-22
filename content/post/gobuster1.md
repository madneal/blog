---
title: "gobuster源码阅读--入口篇"
author: Neal
tags: [web安全, gobuster, 源码阅读]
keywords: [web安全, gobuster, 源码阅读]
categories: [源码阅读]
date: "2022-04-21" 
---

[gobuster](https://github.com/OJ/gobuster) 作为一款信息收集工具，深受安全业界的欢迎。希望通过阅读优秀工具的源码，能够了解其工作的具体细节，为自己日后造轮子也做好准备工作。

## 入口

得益于 Golang 的跨平台属性，其编译过程极其简单，编译的结果直接为二进制程序，可以直接使用，这也是越来越多安全工具选择 Golang 的原因之一。对于每一个 Golang 项目，其根目录下都有一个 `main.go` 的文件，gobuster 也不例外。

```go
func main() {
	cmd.Execute()
}
```

这里即是作为程序的入口来展开这次代码之旅。`Execute` 其实主要是接受程序中断的信号做相应的处理操作，里面的主要涉及的知识点为 `context` 以及 `Signal`，前者主要是为了方便程序的取消、退出，后者则是捕获系统中断的信号。`Notify` 函数负责将 signal 一直传送到管道 `c`，这个函数可以一直调用。直到调用 `sinal.Stop` 的时候，`signalChan` 中的 sinal 则会被清空。这一段代码里面的内容主要是 `signal` 这一块的内容，可以参考 Golang 的[官方文档](https://pkg.go.dev/os/signal#Notify)，里面讲的非常的详细。

```go
func Execute() {
	var cancel context.CancelFunc
	mainContext, cancel = context.WithCancel(context.Background())
	defer cancel()

	signalChan := make(chan os.Signal, 1)
	signal.Notify(signalChan, os.Interrupt)
	defer func() {
		signal.Stop(signalChan)
		cancel()
	}()
	go func() {
		select {
		case <-signalChan:
			fmt.Println("\n[!] Keyboard interrupt detected, terminating.")
			cancel()
		case <-mainContext.Done():
		}
	}()

	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
```

## cmd

gobuster 中的 `cmd` 模块主要为其程序的命令行控制，可将其视作为程序的输入。通过命令行传入的各种参数，从而运行相应的命令来执行操作。`cmd` 下的几个文件也分别对应了 gobuster 的几个模块功能，包括以下：

* dir.go
* dns.go
* fuzz.go
* http.go
* s3.go
* vhost.go

`cmd` 模块的功能很大程序上是基于 [cobra](https://github.com/spf13/cobra)。这个库主要是作为 Goland 的 CLI 的交互使用，功能非常强大。社区有很多 CLI 工具都有使用这个库，那么如果以后考虑开发 CLI 工具的话，必然会考虑到这个库。在上述的几个模块中，都具有两个非常类似的函数，分别为 `init` 以及 `parse*Options` 函数，分别进行命令的注册工作以及命令行参数的初始化工作。在 `root.go` 中进行了一些全局配置项的初始化工作。

在命令行参数中，会包含两项内容，一项为 `commad`，另一项则为 `flag`，以下示例为例，`server` 是 `command`，`port` 是 `flag`。

```
hugo server --port=1234
```

关于这些配置项的数据结构分别存放在以下目录中的 `options.go` 中：

* gobusterdir
* gobusterdns
* gobusterfuzz
* gobuster
* libgobuster
* gobusters3
* gobustervhost

`HTTPOptions` 也会作为一些基础配置项集成到其它的配置项中。

```
// gobusterdir/options.go
type OptionsDir struct {
	libgobuster.HTTPOptions
	Extensions                 string
	ExtensionsParsed           libgobuster.StringSet
	StatusCodes                string
	StatusCodesParsed          libgobuster.IntSet
	StatusCodesBlacklist       string
	StatusCodesBlacklistParsed libgobuster.IntSet
	UseSlash                   bool
	HideLength                 bool
	Expanded                   bool
	NoStatus                   bool
	DiscoverBackup             bool
	ExcludeLength              []int
}
```

## 总结

本文是 gobuster 的第一次探索，主要是看了下程序的入口以及一些配置项的初始化工作，后续会阅读每个对应模块的具体实现细节。