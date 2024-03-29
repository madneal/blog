---
title: "基于golang实现报告生成技术方案"
author: Neal
tags: [golang, 数据可视化, word, go-echarts]
keywords: [golang, 数据可视化, word, go-echarts]
categories: [开发]
date: "2022-02-23" 
---

最近在做一个基于历史数据生成报告的需求，在做这个需求的时候遇到过一些小坑，所以想在这篇文章分享一下踩坑经验。

最初的需求是基于历史数据来生成一个 word 报告，这种需求其实在大多数应用中也算比较常见的需求。但是由于我们使用的语言是 golang，而 golang 关于 word 方面的轮子是少之又少，只有一个国外的商业产品以及极少的特别不成熟的库，比如做一些简单的文字替换的，这些都比较难以满足需求现状。也不可能为了这么个需求就造一个 word 方面的轮子，况且还不一定造的出来。这种方案实现，如果是使用 java 或者 python 会轻松很多，的确 golang 在某些方面的轮子还是存在缺失。后来想到的方案是，先渲染 html 模板，然后再把 html 转成 pdf。渲染 html 不然，基于 template，理论上可以实现任意文本格式文件的填充，但是转 pdf 又又涉及另外一个轮子，也是一番调研，有一些，但是不太多，看起来也不是特别好用。同时，这个方案也不是很优雅。就在一筹莫展之际时，我想到我们内部其实非常热衷于通过自研的 wiki 平台来分享报告，大家分享的时候也经常通过这个平台来直接链接。（其实中间也看了腾讯文档的开放平台，但是这个开放平台根本就不成熟，都没有开放写入的能力，只开放了创建文档的 API，不能写入，那能有啥用呢。）后来找对应平台的开发聊过，幸好他们提供写入的 API，这样实现报告的方案就实现了。平台支持 markdown 的语法，只需要通过 markdown 的语法来渲染好模板，然后写入就可以了。随便提一句，任何不支持 markdown 语法的编辑器都是极其不友好的，所以非常难理解当初 freebuf 改造 markdown 编辑器居然花了一两年的时间，不知道是如何做到的。其实，我自己都为这个方案拍案叫绝，不过这好像也是唯一能实现的技术方案，但在我看来，也是最优雅的实现方式。

这个需求另外一个小坑就是图标的实现。wiki 平台自身没有提供基于数据实现图表的功能，所欲图表的需求是需要我们自己来实现的。这种最能想到的方式就是基于数据生成图表的图片，然后插入到 markdown 中。在调研图表的方案中，是有看到一个 [go-chart](https://github.com/wcharczuk/go-chart) 的方案。但是这个库看起来可定制型不是很高。echarts 是前端领域大名鼎鼎的数据可视化方案，可以说的上是百度做的开源精品，现在已经属于 apace 基金维护的开源产品。[go-echarts](https://github.com/go-echarts/go-echarts) 是一个基于 echarts 的 golang，其本质应该还是通过 echarts 来渲染前端。所以在使用这个库的时候有一个问题，它不会直接生成图片，而是通过 html 来进行渲染的。那么在嵌入图表的时候就不能使用图片，但是正因为之前使用的方案是 markdown，且一般来说大多数 markdown 是兼容 html 的，所以只要将 html 通过 iframe 的形式嵌入，那么这个问题也就迎刃而解了。

```
<iframe  src="%s"  frameborder=0 width="1000" height="600"></iframe>
```

同时得益于 echarts 的灵活，这个方案也可以实现高度定制化的可视化方案。不过这个库并没有丰富的文档，大多数的使用教程都是通过 [examples](https://github.com/go-echarts/examples) 里面的代码样例来进行说明，这个仓库里面有很多图表的各种形式展现的代码样例。不过在图表的时候也遇到一些问题。比如 x 坐标轴的 label 文字过宽，导致容器容纳有问题，这个一般的做法都是将 label 进行旋转，这在 echarts 里面也是比较常见的做法，在 go-echarts 里面有一定的配置语法。

```
bar.SetGlobalOptions(
    charts.WithXAxisOpts(opts.XAxis{
        AxisLabel: &opts.AxisLabel{Show: true, Rotate: 45},
    }),
)
```

不过后面还是发现了问题，就是 x 坐标轴的 label 好像总是缺失了几个，后来把 `opts.AxisLabel` 中的属性全部试了一遍，后来发现是 `ShowMaxLabel` 和 `ShowMinLabel` 这两个配置项默认是 false，这样导致第一个和最后一个 label 没有进行展示，其实这一块的逻辑是不太合理的。

```
bar.SetGlobalOptions(
    charts.WithXAxisOpts(opts.XAxis{
        AxisLabel: &opts.AxisLabel{Show: true, Rotate: 45, ShowMaxLabel: true, ShowMinLabel: true},
    }),
)
```

最后一个坑也就是数据的汇总了，其实也算不上是坑了，只不过是需要弄一弄 sql 语句。挑一个最常见的需求来说，比如需要汇总近一年内每个月的高中低危漏洞数量的变化。如果想到的最粗暴的实现就是计算每个月的开始时间和结束时间，然后通过12条语句来统计每个月的数据汇总。毫无疑问这种方案就不优雅，也耗费更多的资源。其实通过获取数据的月份做 group by，这样一条语句就可以实现了，由于近一年可能会涉及到往年的数据，所以把年份也加进去 `group by`。同时为了数据能够按照月份进行排序，还是将月份转化为时间来进行排序，如果仅仅通过字符串排序还是有问题。

```
select count(1) as c, str_to_date(concat(year(created_at),'-',month(created_at), '-','1'), '%Y-%m-%d') as month from vuln_table group by month order by month desc
```

不过上述方案还是存在一个问题，就是部门月份没有数据，这样导致数据缺失。后来想到的方案，就是先获取时间，然后将月份进行比对，对于缺失的月份进行补零处理。

以上，就是这次需求遇到的实现问题以及想到的解决方案了。