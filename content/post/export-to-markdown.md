---
title: "大佬，您这是在借鉴嘛"
author: Neal
tags: [前端开发, Chrome 插件]
categories: [前端开发]
date: "2024-06-27" 
---

今天闲来没事看到一篇文章，感觉质量挺好的，就想翻译一下。之前写过一个将文档导出成 markdown 的插件，因为这个插件一开始是为了翻译 Medium 文章开发的，但是后来因为 Medium 的 json 接口启用了，所以这个插件后面也不怎么维护了。不搜不知道，一搜吓一跳，居然发现一个和插件差不多的插件，不会吧，这么烂的插件也有人抄？后来仔细看了一看，这个大佬应该是在借鉴我的插件，辛苦地改了几个中文。

![export-markdown1.png](https://s2.loli.net/2024/06/27/UFshrZmgiaCtRPb.png)

两款插件名名字几乎一模一样，只是这个借鉴者加了一个后缀：掘金翻译计划版。不确定和掘金有没有关系，我知道掘金是有一个翻译项目的，以前我也参与过。

## 对比

### 插件介绍

#### 我的插件

![image.png](https://s2.loli.net/2024/06/27/NiF2Wmut8VcIoQL.png)

![image.png](https://s2.loli.net/2024/06/27/YkpfmW3UrxcsGFP.png)

#### 李鬼插件

![image.png](https://s2.loli.net/2024/06/27/zwrQXv1eHiDOmox.png)

![image.png](https://s2.loli.net/2024/06/27/5W9kGABKdOEcxiY.png)

### 代码对比

上面的简洁基本上已经展现了浓重的李鬼味道，本着客观严谨的态度，我还是去看了一下代码。

#### 我的插件

![image.png](https://s2.loli.net/2024/06/27/6DE4ZUfvYnMrkpV.png)

#### 李鬼插件

![image.png](https://s2.loli.net/2024/06/27/Ok9YVIlLcMg3Rty.png)

除了一个 js 文件的引用，几乎可以说是一模一样了。核心的文件是 widget.js 这个文件，这个属于插件自身的 js 文件。

![image.png](https://s2.loli.net/2024/06/27/hoHp1TNFe7kbx8Y.png)

从这代码对比，可以看得出这个借鉴者巨大的工作量。

## 总结

鄙人的这款[插件](https://github.com/madneal/export-to-markdown)是在 GitHub 上开源的，当时也是出于个人需求搞得这么个小玩意，但是没想到居然还有李鬼借鉴，还真是离谱他妈给离谱开门。大家如果有空的话，还是动一下发财的小手点一下 Report，这个[李鬼插件](https://chromewebstore.google.com/detail/olfhadgfelbdikjlnejcfjeockobpijm?hl=zh-CN&utm_source=ext_sidebar)还是下架比较好。我也联系了这个开发同学，希望他能及时下架。




