---
title: "gobuster源码阅读--dir篇"
author: Neal
tags: [web安全, gobuster, 源码阅读]
keywords: [web安全, gobuster, 源码阅读]
categories: [源码阅读]
date: "2022-04-21" 
---

在本系列的第一篇中，主要阅读了 gobuster 入口的这一部分。后续主要是阅读各个模块工作的细节，本文主要讲解 `dir` 模块。`dir` 模块主要是实现目录包括的功能，其主要命令行配置项包括以下内容：

```
Usage:
  gobuster dir [flags]

Flags:
  -f, --add-slash                     Append / to each request
  -c, --cookies string                Cookies to use for the requests
  -e, --expanded                      Expanded mode, print full URLs
  -x, --extensions string             File extension(s) to search for
  -r, --follow-redirect               Follow redirects
  -H, --headers stringArray           Specify HTTP headers, -H 'Header1: val1' -H 'Header2: val2'
  -h, --help                          help for dir
  -l, --include-length                Include the length of the body in the output
  -k, --no-tls-validation             Skip TLS certificate verification
  -n, --no-status                     Don't print status codes
  -P, --password string               Password for Basic Auth
  -p, --proxy string                  Proxy to use for requests [http(s)://host:port]
  -s, --status-codes string           Positive status codes (will be overwritten with status-codes-blacklist if set) (default "200,204,301,302,307,401,403")
  -b, --status-codes-blacklist string Negative status codes (will override status-codes if set)
      --timeout duration              HTTP Timeout (default 10s)
  -u, --url string                    The target URL
  -a, --useragent string              Set the User-Agent string (default "gobuster/3.1.0")
  -U, --username string               Username for Basic Auth
  -d, --discover-backup               Upon finding a file search for backup files
      --wildcard                      Force continued operation when wildcard found

Global Flags:
  -z, --no-progress       Don't display progress
  -o, --output string     Output file to write results to (defaults to stdout)
  -q, --quiet             Don't print the banner and other noise
  -t, --threads int       Number of concurrent threads (default 10)
      --delay duration    Time each thread waits between requests (e.g. 1500ms)
  -v, --verbose           Verbose output (errors)
  -w, --wordlist string   Path to the wordlist
```

`dir` 模块的调用在前文中提到过，也是依据 cobra 的命令行来进行控制，入口函数为 `cmd/dir.go` 中的 `runDir` 函数。

```go
// 全局配置项初始化
globalopts, pluginopts, err := parseDirOptions()
// dir 配置项初始化
plugin, err := gobusterdir.NewGobusterDir(globalopts, pluginopts)
```

`cli.Gobuster` 是整个 CLI 程序的入口，是 gobuster 的核心函数。所有模块的功能都是通过该入口进入，这个函数有三个参数，分别为 `ctx`, `opts` 以及 `plugin`。后面两个分别为全局的配置项以及各个模块所属的配置项内容。

## ErrWildcard

在 `dir` 模块有一个单独的内容想提及一下就是 `ErrWildcard`，这是针对 `wildcard response` 的一种报错。经常会听到泛解析，那么 `wildcard response` 是什么含义呢？

HTTP 的请求状态码都被赋予了特定的含义，比如 200、404、403。但是现在很多公司的业务响应已经不区分状态码了，所有请求的状态码统统都是 200，这一点在国内尤其更为明显，也算得上是中国特色了。对于这种情形，根据状态码去判断请求的响应状态就不可以了，因为已经无法区分了。

这个错误的产生主要是来源于 `func (d *GobusterDir) PreRun` 函数，这也是 gobuster 每个模块通用的函数之一。这个函数主要的逻辑是生成一个随机 uid，然后将这个 uid 拼接到 url 中进行访问，获取返回的状态码。如果 `StatusCodesBlacklistParsed` 中不包含这个状态码或者 `StatusCodesParsed` 中包含这个状态码，则会产生 `ErrWildcard`。这代表着状态码返回可能是异常的，因为按照常理来说，uid 拼接的 url 一定是一个不存在的 url。

```go
guid := uuid.New()
url := fmt.Sprintf("%s%s", d.options.URL, guid)
if d.options.UseSlash {
    url = fmt.Sprintf("%s/", url)
}

wildcardResp, wildcardLength, _, _, err := d.http.Request(ctx, url, libgobuster.RequestOptions{})
if d.options.StatusCodesBlacklistParsed.Length() > 0 {
    if !d.options.StatusCodesBlacklistParsed.Contains(*wildcardResp) {
        return &ErrWildcard{url: url, statusCode: *wildcardResp, length: wildcardLength}
    }
} else if d.options.StatusCodesParsed.Length() > 0 {
    if d.options.StatusCodesParsed.Contains(*wildcardResp) {
        return &ErrWildcard{url: url, statusCode: *wildcardResp, length: wildcardLength}
    }
} else {
    return fmt.Errorf("StatusCodes and StatusCodesBlacklist are both not set which should not happen")
}
```

在本地起一个最简单的 server：

```go
package main                                                                              

import (                                                                                  
    "fmt"                                                                                
    "net/http"                                                                           
)    
     
func HelloHandler(w http.ResponseWriter, r *http.Request) {                              
    w.WriteHeader(200)                                                                   
    fmt.Fprintf(w, "Hello")                                                              
}    
     
func main() {                                                                            
    http.HandleFunc("/", HelloHandler)                                                   
    http.ListenAndServe(":8080", nil)                                                    
}
```

上面的 server 无论请求任何路径，返回的状态响应码都是 200，这种情形下，就会产生 `ErrWildcard`。假如将状态码响应返回始终设置为 404，则不会产生这种错误。这种错误的产生在枚举国内应用的情况是经常发生的。

![image.jpg](https://s2.loli.net/2022/04/22/DN8OojprshBYmUq.jpg)

再次回归到主线分析过程中的 Gobuster 函数。在这个函数中，抛开一些配置项的初始化以及打印的过程，核心内容包括以下内容：

```go
var wg sync.WaitGroup

outputMutex := new(sync.RWMutex)
o := &outputType{
    Mu:              outputMutex,
    MaxCharsWritten: 0,
}

wg.Add(1)
go resultWorker(gobuster, opts.OutputFilename, &wg, o)

wg.Add(1)
go errorWorker(gobuster, &wg, o)

if !opts.Quiet && !opts.NoProgress {
    wg.Add(1)
    go progressWorker(ctxCancel, gobuster, &wg, o)
}
```

以上的几个 goroutine 分别负责不同的任务，并且最终需要确保这些 goroutine 都执行完毕。`resultWorker` 和 `errorWorker` 分别负责结果写入到文件中以及错误的输出，并且通过读写锁来控制输出的写入或者读的场景。

## Label

`Run` 函数中有一个比较少见的语法：

```go
Scan:
	for scanner.Scan() {
		select {
		case <-ctx.Done():
			break Scan
		default:
			word := scanner.Text()
			perms := g.processPatterns(word)
			// add the original word
			wordChan <- word
			// now create perms
			for _, w := range perms {
				select {
				// need to check here too otherwise wordChan will block
				case <-ctx.Done():
					break Scan
				case wordChan <- w:
				}
			}
		}
	}
```

咋一看我没看明白这里的 `Scan` 的含义，因为它没有任何的定义。后来才明白这种语法是 Golang 中的类似于 `C/C++` 中的 `goto` 的语法。这种语法其实在很多语言都不推荐使用，有的语言甚至根本就没有这种语法。不过这种写法在日常的业务场景中不太经常碰到，笔者没有使用过这种写法。不过这里这种写法的原因应该是这里用了 `for` 和 `select`。这个写法的作用主要是用于获取扫描用的字典。

## 核心 worker

```
	var workerGroup sync.WaitGroup
	workerGroup.Add(g.Opts.Threads)
	wordChan := make(chan string, g.Opts.Threads)

	for i := 0; i < g.Opts.Threads; i++ {
		go g.worker(ctx, wordChan, &workerGroup)
	}
```

以上代码是扫描任务执行的核心逻辑，通过 `Threads` 来控制扫描任务的并发数量。通过 `worker` 进入，可以看到的也是依据 `workChan` 来进行扫描任务的爆破。`worker` 中的核心函数为 `g.plugin.Run`，其它的主要也是任务的结束以及一些超时的处理。值得注意的是 gobuster 中各个模块都是通过 `libgobuster/interfaces.go` 中的 `GobusterPlugin` 来实现的。找到对应的实现方法。不过 `Run` 函数的逻辑也变得非常直白了，主要是通过 `urlsToCheck` 来构建需要扫描的 url 链接，比如是否扫描备份文件或者指定后缀路径。最终请求的结果，如果状态码不在 `StatusCodesBlacklistParsed` 中或者状态码在 `StatusCodesParsed` 则认为其为有效结果。

## 总结

至此，dir 模块的主要实现逻辑基本上讲清楚了。gobuster 实现的逻辑还是非常清晰的，因为 Golang 的并发优势，所以其在做这种网络操作上有着天生的优势，并发的写法也会方便很多。