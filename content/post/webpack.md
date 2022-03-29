---
title: "hey,我能看到你的源码哎"
author: Neal
tags: [web安全, webpack, 信息泄露, chrome插件]
keywords: [web安全, webpack, 信息泄露, chrome插件]
categories: [web安全]
date: "2022-03-07" 
---

最近偶然间有看到某家的一个站点中的网站中的前端代码的“泄露”。此处的泄露为什么打引号，因为一般来说网站的前端代码都是可以通过浏览器即可访问。但是一般生产环境中的 JavsScript 代码都是经过压缩和混淆的，所以可读性大大降低，这也提升了从前端的角度挖取更多信息的门槛。这里的泄露指的是在 Chrome 浏览器的 Sources 面板中可以看到完整的以及原始的前端代码。

![image.png](https://s2.loli.net/2022/03/06/WeHphMDZx1dGc9f.png)

通过这样的源码，可以非常清晰地了解应用的前端业务，包括接口信息，如果前端包含加解密的逻辑的话，这样也非常有利于攻击者进行破解。

目前市面上绝大多数应用都是前后端分离，基本上绝大多数是基于 Vue 或者 React 这样的前端框架。而大多数应用配套的构建工具则是 Webpack。而这种源码的泄露真是因为 sourceMap 而导致的，但是这种配置在前端开发环境中是必不可少的，因为如果缺少了 sourceMap 那么前端开发者就无法进行前端代码的调试，sourceMap 正是帮助开发者进行前端代码的调试。通常通过 `devtool` 的配置即可开启 sourceMap，Webpack 会为相应的 js 文件生成对应的 map 文件，在 js 文件的最后一行会有 sourceMap 的申明，表示 map 文件的地址。

```
module.exports = {
    ...
    devtool: 'source-map',
    ...
}
```

市面上的绝大多数浏览器都是支持 sourceMap 的，Chrome 浏览器默认支持。打开浏览器的开发者工具，在 Sources 面板中的设置可以看到相应的配置项，勾选后即可在面板中看到对应解析的源码。

![image.png](https://s2.loli.net/2022/03/07/arGfHwSqNVi8xFn.png)

![image.png](https://s2.loli.net/2022/03/07/pQ7CqLrlw8MkYXv.png)

不过大家可能有一个疑惑，在 Chrome 的 Network 面板中看不到 map 文件的网络请求。但是如果直接使用抓包工具去抓包的话，是可以看到对应的 map 文件的请求的。通过 `chrome://net-export` 可以捕获请求，通过 `https://netlog-viewer.appspot.com/#events` 即可查看捕获的日志文件，可以看到对应的 map 文件的请求记录。

![image.png](https://s2.loli.net/2022/03/07/mW3RuNJoxUwzfBZ.png)

![source-map.png](https://s2.loli.net/2022/03/06/xqLWS2B9NADG5sX.png)

毫无疑问，sourceMap 如果在生产环境开启的话，必然具有一定的安全风险，因为从很大程度上帮助攻击者了解应用，获取应用的更多信息。那么，我们是不是可以写一个 Chrome 插件来检测这种问题并且来直接进行源码的下载呢。实现这样的插件不是件很困难的，检测 js 文件请求，然后尝试请求对应的 map 文件。有不少开源库能够进行 sourceMap 的解析，Mozilla 的 [source-map](https://github.com/mozilla/source-map) 即是一个能够解析 sourceMap 的 js 库，亦可以通过这个库生成 js 的对应的 sourceMap。

![image.png](https://s2.loli.net/2022/03/07/n1i4asOoWcAUCZ2.png)

```
<script src="https://unpkg.com/source-map@0.7.3/dist/source-map.js"></script>
<script>
    sourceMap.SourceMapConsumer.initialize({
        "lib/mappings.wasm": "https://unpkg.com/source-map@0.7.3/lib/mappings.wasm"
    });
</script>
```

之前其实已经有人写过类似的插件 [SourceDetector](https://github.com/SunHuawei/SourceDetector)。不过这个插件目前缺乏维护，它的插件已经被下线，并且编译过程依赖项比较多并且目前因为部分依赖过于陈旧没有办法完成 build，所以我就想完成一个开箱即用，无须过多依赖的插件。插件的实现过程主要是 `webrequest` API 去监听请求，实现的流程基本是按照上面的流程图实现，然后基于 `jszip` 来进行内容的写入并完成下载。目前源代码已经放在 [Github](https://github.com/madneal/leaked),感兴趣的可以看看。目前因为还没有发布到 chrome 插件模式，可以通过开发者模式加载来使用。
![leaked.gif](https://s2.loli.net/2022/03/07/WflIST1gkPMtaC8.gif)

不过目前插件还是存在比较初级的阶段，UI 方面非常简单粗暴，并且有一些开源库的 sourceMap 没有排除出去，后续的话会持续更新，感兴趣的话持续关注。