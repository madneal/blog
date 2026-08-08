# AdSense Content Audit (madneal.com)

> 生成目的：修复 AdSense **Low value content**。
> 指标 `units` = 去掉代码块/图片后的 **汉字数 + 英文词数**（比 `wc -w` 更适合中文站）。

## 总览

- 文章总数: **203**
- 平均 units: **1178**
- 中位 units: **850**
- 译文标记（含「原文/译者」等）: **34**

### 长度分布

| Units | Count |
|------:|------:|
| <120 | 17 |
| 120-299 | 25 |
| 300-599 | 33 |
| 600-899 | 31 |
| 900-1499 | 46 |
| 1500+ | 51 |

### 建议动作统计

| Action | Count | 含义 |
|--------|------:|------|
| `delete` | **26** | 下线 / `draft: true` / 删除公开索引 |
| `merge` | **3** | 并入系列长文后下线原页 |
| `expand` | **46** | 保留主题，扩写到 800–1200+ units |
| `keep_or_archive` | **21** | 长度尚可但偏题，可保留或归档 |
| `keep_polish` | **28** | 基本可留，补结构/示例/内链 |
| `keep_attr` | **30** | 长译文：保留出处并加原创补充 |
| `keep` | **49** | 主线优质长文，优先保留 |

### 建议目标（复审前）

1. 公开索引中 **`<300 units` 接近 0**
2. 公开文章以 **安全 / 开发** 为主
3. 优先处理 delete(26) + merge(3+0)，立刻提高站内密度
4. 再扩写 expand(46) 中与主线相关的篇目
5. 信任页：About / Privacy（**已完成**：`content/about.md`、`content/privacy.md`，菜单与页脚已接入）

## A. 优先下线（delete）

- `content/post/如何将网络流转化为内存流 C#.md` — **如何将网络流转化为内存流 C#** — 0 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/mihoyo.md` — **米哈游内推** — 12 units — 极薄正文（或图多文少），建议下线/draft
- `content/CVE-2023-32991.md` — **2019 年针对 API 安全的 4 点建议** — 20 units — 极薄正文（或图多文少），建议下线/draft
- `content/checklist.md` — **学术篇** — 23 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/latex如何给表格添加注释.md` — **latex如何给表格添加注释** — 23 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/datagridview里面的checkbox全选和取消全选.md` — **datagridview里面的checkbox全选和取消全选** — 32 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/differential evolution代码实例（DE算法）.md` — **differential evolution代码实例（DE算法）** — 42 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/latex算法步骤如何去掉序号.md` — **latex算法步骤如何去掉序号** — 62 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/数据结构线性表相关操作.md` — **数据结构线性表相关操作** — 63 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/柯西分布.md` — **柯西分布** — 63 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/如何查找django安装路径.md` — **如何查找django安装路径** — 70 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/使用js实现图片轮滑效果.md` — **使用js实现图片轮滑效果** — 82 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/http响应代码解释.md` — **http响应代码解释** — 84 units — 极薄正文（或图多文少），建议下线/draft
- `content/samesite.md` — **SameSite 的七八事** — 104 units — 极薄正文（或图多文少），建议下线/draft
- `content/burp-mcp.md` — **burp-mcp** — 105 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/winform中进行post上传文件.md` — **winform中进行post上传文件** — 110 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/如何用latex画一个简单的表格.md` — **如何用latex画一个简单的表格** — 113 units — 极薄正文（或图多文少），建议下线/draft
- `content/post/歌德巴赫猜想.md` — **歌德巴赫猜想** — 121 units — 短且非主赛道，建议下线
- `content/post/matlab批量修改变量的名称.md` — **matlab批量修改变量的名称** — 131 units — 短且非主赛道，建议下线
- `content/post/每日一练--直接插入排序.md` — **每日一练--直接插入排序** — 137 units — 短且非主赛道，建议下线
- `content/post/常用颜色的RGB分布.md` — **常用颜色的RGB分布** — 155 units — 短且非主赛道，建议下线
- `content/post/道路识别demo.md` — **道路识别demo** — 177 units — 短且非主赛道，建议下线
- `content/post/latex中large的作用域问题.md` — **latex中large的作用域问题** — 231 units — 短且非主赛道，建议下线
- `content/post/一个简单的输入输出算法题.md` — **一个简单的输入输出算法题** — 251 units — 短且非主赛道，建议下线
- `content/post/Iplimage versus Mat.md` — **Iplimage versus Mat** — 267 units — 短且非主赛道，建议下线
- `content/post/剑指offer学习读书笔记--二维数组中的查找.md` — **剑指offer学习读书笔记--二维数组中的查找** — 298 units — 短且非主赛道，建议下线

## B. 合并（merge / merge_or_expand）

- `content/post/the sum of two fixed value.md` — **the sum of two fixed value** — 350 units — 中薄笔记，并入系列后下线单页
- `content/post/回调函数.md` — **回调函数** — 447 units — 中薄笔记，并入系列后下线单页
- `content/post/PCA算法和实例.md` — **PCA算法和实例** — 558 units — 中薄笔记，并入系列后下线单页

## C. 扩写（expand）

- `content/post/sftp没有关闭session导致服务器sshd进程未关闭.md` — **sftp没有关闭session导致服务器sshd进程未关闭** — 121 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/css盒子模型设置的缩略形式.md` — **css盒子模型设置的缩略形式** — 138 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/github命令大全.md` — **github命令大全** — 154 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/nodejs爬虫编码问题.md` — **nodejs爬虫编码问题** — 177 units — 短文但主题相关，扩写到 800+ 有效字
- `content/Logshsh技巧之处理不同的output.md` — **Logstash技巧之处理不同的output** — 187 units — 短文但主题相关，扩写到 800+ 有效字
- `content/lucene中query的实现.md` — **lucene 中 query 的实现** — 190 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/在pythonanywhere部署你的第一个应用.md` — **在pythonanywhere部署你的第一个应用** — 201 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/installsheild2011打包程序internal build error 6213.md` — **installsheild2011打包程序internal build error 6213** — 210 units — 短文但主题相关，扩写到 800+ 有效字
- `content/服务端请求伪造（SSRF）.md` — **服务端请求伪造（SSRF）攻击** — 222 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/判断数组中元素多个属性是否重复.md` — **判断数组中元素多个属性是否重复** — 224 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/combox系列问题集.md` — **combox系列问题集** — 227 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/css样式表的引入方式.md` — **css样式表的引入方式** — 232 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/只要三步，你就可以在github上发布网站了.md` — **只要三步，你就可以在github上发布网站了** — 241 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/WWDC2015.md` — **WWDC2015** — 244 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/sqlite操作.md` — **sqlite操作** — 249 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/剑指offer学习--实现单例模式.md` — **剑指offer学习--实现单例模式** — 261 units — 短文但主题相关，扩写到 800+ 有效字
- `content/post/初识NuGet.md` — **初识NuGet** — 301 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/goland.md` — **goland-2022.01版本最新实用功能** — 308 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/markdown语法规则.md` — **markdown语法规则** — 316 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/github-rsa.md` — **GitHub 更新了 RSA SSH host key** — 318 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/前端面试基础题目.md` — **前端面试基础题目** — 319 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/实现combobox模糊查询的时候报错 InvalidArgument=“0”的值对于“index”无效.md` — **实现combobox模糊查询的时候报错 InvalidArgument=“0”的值对于“index”无效** — 322 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/Django学习——开发你的第一个Django应用2.md` — **Django学习——开发你的第一个Django应用2** — 356 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/opencv视频流的读取和处理.md` — **opencv视频流的读取和处理** — 363 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/check-cve.md` — **cve check** — 374 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/bashed-hack-the-box.md` — **Bashed -- hack the box** — 378 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/indexDB的概念.md` — **indexDB的概念** — 397 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/一个神奇却很简单的css特效.md` — **一个神奇却很简单的css特效** — 397 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/Cronos-hack the box.md` — **Cronos -- hack the box** — 398 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/利用python生成可视化报告.md` — **利用 python 生成可视化报告** — 401 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/javascript中无法将string转化为json对象.md` — **javascript中无法将string转化为json对象** — 402 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/如何实现一个完美的页码跳转.md` — **如何做一个完美的页码跳转** — 419 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/将Medium中的博客导出成markdown.md` — **将Medium中的博客导出成markdown** — 429 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/referer.md` — **JavaScript能否修改Referer请求头** — 431 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/Ext.js性能优化漫谈.md` — **Ext.js性能优化漫谈** — 434 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/moongoose对象无法新增删除属性.md` — **moongoose对象无法新增删除属性** — 434 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/后渗透的文件传输.md` — **后渗透的文件传输** — 443 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/export-to-markdown.md` — **大佬，您这是在借鉴嘛** — 463 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/道路模型--linear-parabolic model.md` — **道路模型--linear-parabolic model** — 478 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/剑指offer--字符串.md` — **剑指offer--字符串** — 480 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/全栈开发教学学习系列1——前言.md` — **全栈开发教学学习系列1——前言** — 488 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/IIS短文件漏洞及修复建议.md` — **IIS短文件漏洞及修复建议** — 495 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/利用tesseract-ocr进行验证码识别.md` — **利用tesseract-ocr进行验证码识别** — 495 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/CVE-2025-55188.md` — **CVE-2025-55188：7-Zip 任意文件写入漏洞** — 523 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/黑产代码解密--利用canvas加载代码.md` — **黑产代码解密--利用canvas加载代码** — 539 units — 中薄，补步骤/踩坑/结论到 800–1200+
- `content/post/ROT13加密和解密.md` — **ROT13加密和解密** — 545 units — 中薄，补步骤/踩坑/结论到 800–1200+

## D. 润色保留（keep_polish / keep_attr）

- `content/post/cpe.md` — **CPE 获取指南** — 602 units — 接近可用：加目录结构、示例与内链
- `content/post/Nibbles-hack-the-box.md` — **Nibbles - Hack the box** — 615 units — 接近可用：加目录结构、示例与内链
- `content/post/Kibana任意代码执行漏洞.md` — **Kibana 任意代码执行漏洞** — 621 units — 接近可用：加目录结构、示例与内链
- `content/post/第一个chrome extension.md` — **第一个chrome extension** — 621 units — 接近可用：加目录结构、示例与内链
- `content/post/微软Visual Studio Code基本特征.md` — **微软Visual Studio Code基本特征** — 649 units — 接近可用：加目录结构、示例与内链
- `content/laoniao.md` — **疯狂的键盘：老鸟成长史** — 655 units — 接近可用：加目录结构、示例与内链
- `content/post/从后台看python--为什么说python是慢的.md` — **从后台看python--为什么说python是慢的** — 660 units — 接近可用：加目录结构、示例与内链
- `content/post/gobuster1.md` — **gobuster源码阅读--入口篇** — 670 units — 接近可用：加目录结构、示例与内链
- `content/post/js的事件流理解.md` — **js的事件流理解** — 675 units — 接近可用：加目录结构、示例与内链
- `content/全栈工程师的成长.md` — **全栈工程师的成长** — 711 units — 接近可用：加目录结构、示例与内链
- `content/post/javascript的继承模式.md` — **javascript的继承模式** — 730 units — 接近可用：加目录结构、示例与内链
- `content/post/基于ELK进行邮箱访问日志的分析.md` — **基于ELK进行邮箱访问日志的分析** — 730 units — 接近可用：加目录结构、示例与内链
- `content/post/Help-hack the box.md` — **Help -- hack the box** — 735 units — 接近可用：加目录结构、示例与内链
- `content/post/Holiday-hack the box.md` — **Holiday -- hack the box** — 738 units — 接近可用：加目录结构、示例与内链
- `content/post/模拟.net post请求属性.md` — **模拟.net post请求属性** — 747 units — 接近可用：加目录结构、示例与内链
- `content/post/如何写一个burp插件.md` — **如何写一个 burp 插件** — 750 units — 接近可用：加目录结构、示例与内链
- `content/post/gobuster3.md` — **gobuster源码阅读--终篇** — 753 units — 接近可用：加目录结构、示例与内链
- `content/post/drive.md` — **Google Drive 的信息检索** — 769 units — 接近可用：加目录结构、示例与内链
- `content/post/stored-xss.md` — **富文本场景下的 XSS** — 770 units — 接近可用：加目录结构、示例与内链
- `content/post/go-vuln-management.md` — **Go 的漏洞管理** — 800 units — 接近可用：加目录结构、示例与内链
- `content/post/偶遇的XSS漏洞.md` — **偶遇 XSS 漏洞** — 813 units — 接近可用：加目录结构、示例与内链
- `content/post/gproxy.md` — **真香系列之 Golang 升级** — 817 units — 接近可用：加目录结构、示例与内链
- `content/post/从一到面试题谈谈setTimeout和setInterval.md` — **从一道面试题谈谈 setTimeout 和 setInterval** — 849 units — 接近可用：加目录结构、示例与内链
- `content/post/service worker之cache实践--sw-precache.md` — **service worker之cache实践--sw-precache** — 850 units — 接近可用：加目录结构、示例与内链
- `content/post/寻找你的第一个漏洞.md` — **寻找你的第一个漏洞** — 850 units — 接近可用：加目录结构、示例与内链
- `content/post/Mongoose中document和object的区别.md` — **Mongoose中document和object的区别** — 871 units — 接近可用：加目录结构、示例与内链
- `content/post/haystack.md` — **Haystack - hack the box** — 896 units — 接近可用：加目录结构、示例与内链
- `content/post/让你的SQL盲注快起来.md` — **让你的SQL盲注快起来** — 897 units — 接近可用：加目录结构、示例与内链
- `content/post/github-bug-bounty.md` — **为什么 2022 年是漏洞赏金奖破纪录的一年** — 930 units — 长译文：保留+出处+补原创点评
- `content/post/火眼.md` — **火眼红队工具遭窃** — 956 units — 长译文：保留+出处+补原创点评
- `content/post/隐写术-深入研究PDF混淆漏洞.md` — **隐写术-深入研究 PDF 混淆漏洞** — 987 units — 长译文：保留+出处+补原创点评
- `content/post/Bootstrap真的总是好的吗.md` — **Bootstrap真的总是好的吗** — 1073 units — 长译文：保留+出处+补原创点评
- `content/post/通过利用immutability的能力编写更安全和更整洁的代码.md` — **通过利用immutability的能力编写更安全和更整洁的代码** — 1075 units — 长译文：保留+出处+补原创点评
- `content/post/你可能不知道谷歌浏览器开发工具的其他用处.md` — **你可能不知道谷歌浏览器开发工具的其他用处** — 1097 units — 长译文：保留+出处+补原创点评
- `content/post/2019年针对API安全的4点建议.md` — **2019 年针对 API 安全的 4 点建议** — 1266 units — 长译文：保留+出处+补原创点评
- `content/post/消灭star大作战-Front-end-tutorial.md` — **消灭 star 大作战--Front-end-tutorial** — 1368 units — 长译文：保留+出处+补原创点评
- `content/post/什么是服务端伪造（SSRF）.md` — **什么是服务端伪造（SSRF）** — 1442 units — 长译文：保留+出处+补原创点评
- `content/post/JavaScript是如何工作的：引擎，运行时间以及调用栈的概述.md` — **JavaScript是如何工作的：引擎，运行时间以及调用栈的概述** — 1611 units — 长译文：保留+出处+补原创点评
- `content/post/聊聊答题应用题库的建立.md` — **聊聊答题应用题库的建立** — 1630 units — 长译文：保留+出处+补原创点评
- `content/post/service worker介绍.md` — **service worker介绍** — 1991 units — 长译文：保留+出处+补原创点评
- `content/post/Chrome最新在野零日漏洞.md` — **Chrome 最新零日漏洞** — 1992 units — 长译文：保留+出处+补原创点评
- `content/post/基于Vue JS, Webpack 以及Material Design的渐进式web应用 [Part 1].md` — **基于Vue JS, Webpack 以及Material Design的渐进式web应用 [Part 1]** — 2055 units — 长译文：保留+出处+补原创点评
- `content/post/XSS.md` — **GMail XSS 漏洞分析** — 2148 units — 长译文：保留+出处+补原创点评
- `content/post/ms-codeql.md` — **微软开源对于 Solorigate 活动捕获的开源 CodeQL 查询** — 2150 units — 长译文：保留+出处+补原创点评
- `content/post/javascript中的对象字面量为啥这么酷.md` — **javascript中的对象字面量为啥这么酷** — 2201 units — 长译文：保留+出处+补原创点评
- `content/post/burp-ai.md` — **不到一分钟拿到可用 PoC：Julen Garrido Estévez 测试 Burp AI** — 2234 units — 长译文：保留+出处+补原创点评
- `content/post/sast.md` — **SAST 测试中要测量的三个参数** — 2443 units — 长译文：保留+出处+补原创点评
- `content/post/出去就餐并且理解Express.js的基本知识.md` — **出去就餐并且理解Express.js的基本知识** — 2524 units — 长译文：保留+出处+补原创点评
- `content/post/git-undo.md` — **如何使用 Git 撤消（几乎）任何操作** — 2546 units — 长译文：保留+出处+补原创点评
- `content/post/cookie-tossing.md` — **通过 Cookie Tossing 劫持 OAUTH 流程** — 2563 units — 长译文：保留+出处+补原创点评
- `content/post/Pornhub Web 开发者访谈.md` — **Pornhub Web 开发者访谈** — 2668 units — 长译文：保留+出处+补原创点评
- `content/post/nodejs回调大坑.md` — **nodejs回调大坑** — 2988 units — 长译文：保留+出处+补原创点评
- `content/post/OSWE.md` — **一键 Shell，我的 OSWE 之旅** — 3683 units — 长译文：保留+出处+补原创点评
- `content/post/circleci-incident.md` — **CircleCI 20230104 安全事件报告** — 3699 units — 长译文：保留+出处+补原创点评
- `content/post/nilayay.md` — **NilAway：实用的 Go Nil Panic 检测方式** — 3952 units — 长译文：保留+出处+补原创点评
- `content/post/Twitter Lite以及大规模的高性能React渐进式网络应用.md` — **Twitter Lite以及大规模的高性能React渐进式网络应用** — 4240 units — 长译文：保留+出处+补原创点评
- `content/post/Elasticsearch团队开发章程.md` — **Elasticsearch 团队开发章程** — 5903 units — 长译文：保留+出处+补原创点评
- `content/post/programer.md` — **菜鸟程序员成长史 --记 Github 1000+ contributions** — 6918 units — 长译文：保留+出处+补原创点评

## E. 优质保留（keep）

- `content/post/hr.md` — **关于招人的那点小事** — 912 units
- `content/post/gorm.md` — **AI 审代码，靠谱吗？** — 915 units
- `content/post/第一个progressive web application，发车！.md` — **第一个progressive web application，发车！** — 931 units
- `content/post/全栈开发系列学习2——django项目搭建.md` — **全栈开发系列学习2——django项目搭建** — 952 units
- `content/post/Django学习——开发你的第一个Django应用1.md` — **Django学习——开发你的第一个Django应用1** — 966 units
- `content/post/webpack.md` — **hey,我能看到你的源码哎** — 979 units
- `content/post/matlab调试技巧.md` — **matlab调试技巧** — 1013 units
- `content/post/wmic使用中的一些问题.md` — **Wmic 使用中的一些问题** — 1020 units
- `content/post/常用的正则表达式.md` — **常用的正则表达式** — 1040 units
- `content/post/前端面试题——系列一.md` — **前端面试题——系列一** — 1046 units
- `content/架构整洁之道读后感.md` — **架构整洁之道读后感** — 1077 units
- `content/post/gobuster2.md` — **gobuster源码阅读--dir篇** — 1120 units
- `content/post/studio-display.md` — **iMac+Studio Display，双 5k 屏体验** — 1126 units
- `content/post/谈谈CS英文论文写作.md` — **谈谈CS英文论文写作** — 1153 units
- `content/post/通过自定义API接入Claude桌面版.md` — **改三个 JSON，让 Claude 桌面版用上你自己的 API** — 1164 units
- `content/post/xiaomi.md` — **Home Assistant 小米门铃视频本地存储** — 1233 units
- `content/post/关于计算机视觉研究.md` — **关于计算机视觉研究** — 1239 units
- `content/post/redirect.md` — **白名单，被谁饶过了？** — 1252 units
- `content/post/POI读取文件的最佳实践.md` — **POI读取文件的最佳实践** — 1254 units
- `content/post/gshark.md` — **多平台的敏感信息检测工具-GShark** — 1270 units
- `content/post/百度前端实习生面试（连跪之旅）.md` — **百度前端实习生面试（连跪之旅）** — 1275 units
- `content/post/Qradar-SIME查询利器.md` — **Qradar SIEM--查询利器 AQL** — 1365 units
- `content/post/通过七牛云建立私有图床.md` — **通过七牛云建立私有图床** — 1442 units
- `content/post/Bastion.md` — **Bastion -- Hack the box** — 1460 units
- `content/post/web狗之writeup--phone.md` — **web 狗之writeup--phone** — 1484 units
- `content/post/持续发布Chrome插件.md` — **持续发布 Chrome 插件** — 1498 units
- `content/post/go-report.md` — **基于golang实现报告生成技术方案** — 1506 units
- `content/post/PWK以及OSCP最常见的问题.md` — **PWK 以及 OSCP 最常见的问题** — 1511 units
- `content/post/全栈工程师的百宝箱.md` — **1024献礼，全栈工程师进击** — 1641 units
- `content/post/cissp-domain1.md` — **文武双全，看我如何过CISSP** — 1761 units
- `content/chatgpt-ato.md` — **ChatGPT账户接管 - 通配符网页缓存欺骗** — 1801 units
- `content/post/shopee.md` — **Shopee 靠谱内推** — 1925 units
- `content/post/OPENCV.md` — **OPENCV** — 2098 units
- `content/post/键盘.md` — **键盘简史** — 2113 units
- `content/post/toolchain.md` — **Go 版本不一致？别慌，这是特性！** — 2136 units
- `content/post/被动扫描器之Chrome插件.md` — **被动扫描器之插件篇** — 2182 units
- `content/post/什么是DDOS.md` — **什么是DDOS** — 2246 units
- `content/post/流量分析的瑞士军刀--zeek.md` — **网络安全分析的瑞士军刀--zeek** — 2274 units
- `content/post/pwa, 上海地铁线路图全新重构.md` — **pwa, 上海地铁线路图全新重构** — 2296 units
- `content/post/GShark-监测你的Github敏感信息泄露.md` — **GShark-监测你的 Github 敏感信息泄露** — 2306 units
- `content/post/反射性XSS知解123.md` — **XSS 漏洞知解 123** — 2330 units
- `content/post/博客文章阶段性总结.md` — **博客考古：从漏洞、工具到生活折腾** — 2528 units
- `content/post/goland-plugin.md` — **第一款Goland的SCA插件开发之旅** — 2563 units
- `content/post/Mybaits和SQL注入的恩恩怨怨.md` — **MyBatis 和 SQL 注入的恩恩怨怨** — 2611 units
- `content/post/理解OutOfMemory异常.md` — **理解 OutOfMemoryError 异常** — 3240 units
- `content/post/跨站请求伪造（CSRF)攻击.md` — **跨站请求伪造（CSRF）攻击** — 3271 units
- `content/post/sop.md` — **安全运营平台从0到1** — 3481 units
- `content/post/botnet.md` — **僵尸网络 Stantinko 犯罪活动新增加密货币挖矿** — 3582 units
- `content/post/使用浏览器作为代理从公网攻击内网.md` — **使用浏览器作为代理从公网攻击内网** — 11099 units

## F. 非主线可归档（keep_or_archive）

- `content/post/剑指offer学习--初级c++面试题.md` — **剑指offer学习--初级c++面试题** — 681 units — 长度尚可，非主线可归档
- `content/post/道路识别.md` — **道路识别** — 733 units — 长度尚可，非主线可归档
- `content/post/Latex--入门系列二.md` — **Latex--入门系列二** — 761 units — 长度尚可，非主线可归档
- `content/post/mac-mini.md` — **mac mini，真香？** — 1121 units — 长文但偏其他主题
- `content/post/Latex--入门系列一.md` — **Latex--入门系列一** — 1145 units — 长文但偏其他主题
- `content/post/独立成分分析（Independent Component Analysis）.md` — **独立成分分析（Independent Component Analysis）** — 1154 units — 长文但偏其他主题
- `content/post/highway.md` — **电车的高速之行** — 1244 units — 长文但偏其他主题
- `content/post/au9999_gold_trend_article.md` — **从1243元跌回935元：近一年黄金到底变弱了吗？** — 1330 units — 长文但偏其他主题
- `content/post/imac.md` — **imac 2020，真香？** — 1344 units — 长文但偏其他主题
- `content/post/CHEVP算法（CannyHough Estimation of Vanishing Points).md` — **CHEVP算法（CannyHough Estimation of Vanishing Points)** — 1364 units — 长文但偏其他主题
- `content/post/Latex--入门系列三.md` — **Latex--入门系列三** — 1384 units — 长文但偏其他主题
- `content/post/xiaopeng.md` — **技术宅的第一辆车--小鹏P7** — 1401 units — 长文但偏其他主题
- `content/post/奇异值分解基础(SVD).md` — **奇异值分解基础(SVD)** — 1459 units — 长文但偏其他主题
- `content/post/骑行.md` — **菜腿的骑行通勤** — 1474 units — 长文但偏其他主题
- `content/post/颈椎.md` — **颈椎康复指南--桌面篇** — 1520 units — 长文但偏其他主题
- `content/post/shanghai.md` — **停车被蹭的那些小事** — 1790 units — 长文但偏其他主题
- `content/post/xp.md` — **提车二月记--小鹏P7** — 1951 units — 长文但偏其他主题
- `content/post/xp-problem.md` — **小鹏 P7 之殤** — 2100 units — 长文但偏其他主题
- `content/post/行车记录仪.md` — **行车记录仪对比 - 盯盯拍mini5 vs 海康威视C8** — 2217 units — 长文但偏其他主题
- `content/post/演化计算会议.md` — **演化计算会议** — 2631 units — 长文但偏其他主题
- `content/post/计算机视觉领域的一些牛人博客，超有实力的研究机构等的网站链接.md` — **计算机视觉领域的一些牛人博客，超有实力的研究机构等的网站链接** — 4776 units — 长文但偏其他主题

## 完整表（按动作 + 长度）

| Units | Action | Date | Title | Path | Reason |
|------:|--------|------|-------|------|--------|
| 0 | `delete` | 2015-04-28 | 如何将网络流转化为内存流 C# | `content/post/如何将网络流转化为内存流 C#.md` | 极薄正文（或图多文少），建议下线/draft |
| 12 | `delete` | 2021-08-07 | 米哈游内推 | `content/post/mihoyo.md` | 极薄正文（或图多文少），建议下线/draft |
| 20 | `delete` | 2019-02-02 | 2019 年针对 API 安全的 4 点建议 | `content/CVE-2023-32991.md` | 极薄正文（或图多文少），建议下线/draft |
| 23 | `delete` |  | 学术篇 | `content/checklist.md` | 极薄正文（或图多文少），建议下线/draft |
| 23 | `delete` | 2015-12-10 | latex如何给表格添加注释 | `content/post/latex如何给表格添加注释.md` | 极薄正文（或图多文少），建议下线/draft |
| 32 | `delete` | 2015-04-22 | datagridview里面的checkbox全选和取消全选 | `content/post/datagridview里面的checkbox全选和取消全选.md` | 极薄正文（或图多文少），建议下线/draft |
| 42 | `delete` | 2015-10-26 | differential evolution代码实例（DE算法） | `content/post/differential evolution代码实例（DE算法）.md` | 极薄正文（或图多文少），建议下线/draft |
| 62 | `delete` | 2015-11-06 | latex算法步骤如何去掉序号 | `content/post/latex算法步骤如何去掉序号.md` | 极薄正文（或图多文少），建议下线/draft |
| 63 | `delete` | 2015-12-28 | 数据结构线性表相关操作 | `content/post/数据结构线性表相关操作.md` | 极薄正文（或图多文少），建议下线/draft |
| 63 | `delete` | 2015-10-12 | 柯西分布 | `content/post/柯西分布.md` | 极薄正文（或图多文少），建议下线/draft |
| 70 | `delete` | 2015-10-10 | 如何查找django安装路径 | `content/post/如何查找django安装路径.md` | 极薄正文（或图多文少），建议下线/draft |
| 82 | `delete` | 2015-10-21 | 使用js实现图片轮滑效果 | `content/post/使用js实现图片轮滑效果.md` | 极薄正文（或图多文少），建议下线/draft |
| 84 | `delete` | 2015-10-10 | http响应代码解释 | `content/post/http响应代码解释.md` | 极薄正文（或图多文少），建议下线/draft |
| 104 | `delete` | 2021-02-17 | SameSite 的七八事 | `content/samesite.md` | 极薄正文（或图多文少），建议下线/draft |
| 105 | `delete` |  | burp-mcp | `content/burp-mcp.md` | 极薄正文（或图多文少），建议下线/draft |
| 110 | `delete` | 2015-04-17 | winform中进行post上传文件 | `content/post/winform中进行post上传文件.md` | 极薄正文（或图多文少），建议下线/draft |
| 113 | `delete` | 2015-09-26 | 如何用latex画一个简单的表格 | `content/post/如何用latex画一个简单的表格.md` | 极薄正文（或图多文少），建议下线/draft |
| 121 | `delete` | 2015-04-11 | 歌德巴赫猜想 | `content/post/歌德巴赫猜想.md` | 短且非主赛道，建议下线 |
| 131 | `delete` | 2015-09-08 | matlab批量修改变量的名称 | `content/post/matlab批量修改变量的名称.md` | 短且非主赛道，建议下线 |
| 137 | `delete` | 2015-10-28 | 每日一练--直接插入排序 | `content/post/每日一练--直接插入排序.md` | 短且非主赛道，建议下线 |
| 155 | `delete` | 2015-05-10 | 常用颜色的RGB分布 | `content/post/常用颜色的RGB分布.md` | 短且非主赛道，建议下线 |
| 177 | `delete` | 2015-04-15 | 道路识别demo | `content/post/道路识别demo.md` | 短且非主赛道，建议下线 |
| 231 | `delete` | 2017-01-06 | latex中large的作用域问题 | `content/post/latex中large的作用域问题.md` | 短且非主赛道，建议下线 |
| 251 | `delete` | 2015-04-11 | 一个简单的输入输出算法题 | `content/post/一个简单的输入输出算法题.md` | 短且非主赛道，建议下线 |
| 267 | `delete` | 2015-04-15 | Iplimage versus Mat | `content/post/Iplimage versus Mat.md` | 短且非主赛道，建议下线 |
| 298 | `delete` | 2015-11-14 | 剑指offer学习读书笔记--二维数组中的查找 | `content/post/剑指offer学习读书笔记--二维数组中的查找.md` | 短且非主赛道，建议下线 |
| 350 | `merge` | 2016-10-26 | the sum of two fixed value | `content/post/the sum of two fixed value.md` | 中薄笔记，并入系列后下线单页 |
| 447 | `merge` | 2015-04-12 | 回调函数 | `content/post/回调函数.md` | 中薄笔记，并入系列后下线单页 |
| 558 | `merge` | 2015-06-20 | PCA算法和实例 | `content/post/PCA算法和实例.md` | 中薄笔记，并入系列后下线单页 |
| 121 | `expand` | 2016-07-28 | sftp没有关闭session导致服务器sshd进程未关闭 | `content/post/sftp没有关闭session导致服务器sshd进程未关闭.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 138 | `expand` | 2015-10-24 | css盒子模型设置的缩略形式 | `content/post/css盒子模型设置的缩略形式.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 154 | `expand` | 2015-10-25 | github命令大全 | `content/post/github命令大全.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 177 | `expand` | 2016-04-16 | nodejs爬虫编码问题 | `content/post/nodejs爬虫编码问题.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 187 | `expand` | 2020-05-18 | Logstash技巧之处理不同的output | `content/Logshsh技巧之处理不同的output.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 190 | `expand` | 2018-10-09 | lucene 中 query 的实现 | `content/lucene中query的实现.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 201 | `expand` | 2015-10-21 | 在pythonanywhere部署你的第一个应用 | `content/post/在pythonanywhere部署你的第一个应用.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 210 | `expand` | 2015-12-20 | installsheild2011打包程序internal build error 6213 | `content/post/installsheild2011打包程序internal build error 6213.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 222 | `expand` | 2019-02-22 | 服务端请求伪造（SSRF）攻击 | `content/服务端请求伪造（SSRF）.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 224 | `expand` | 2016-07-01 | 判断数组中元素多个属性是否重复 | `content/post/判断数组中元素多个属性是否重复.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 227 | `expand` | 2015-04-14 | combox系列问题集 | `content/post/combox系列问题集.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 232 | `expand` | 2015-10-06 | css样式表的引入方式 | `content/post/css样式表的引入方式.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 241 | `expand` | 2016-12-09 | 只要三步，你就可以在github上发布网站了 | `content/post/只要三步，你就可以在github上发布网站了.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 244 | `expand` | 2015-06-09 | WWDC2015 | `content/post/WWDC2015.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 249 | `expand` | 2015-04-15 | sqlite操作 | `content/post/sqlite操作.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 261 | `expand` | 2015-11-13 | 剑指offer学习--实现单例模式 | `content/post/剑指offer学习--实现单例模式.md` | 短文但主题相关，扩写到 800+ 有效字 |
| 301 | `expand` | 2015-04-12 | 初识NuGet | `content/post/初识NuGet.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 308 | `expand` | 2022-05-01 | goland-2022.01版本最新实用功能 | `content/post/goland.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 316 | `expand` | 2015-10-06 | markdown语法规则 | `content/post/markdown语法规则.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 318 | `expand` | 2023-03-24 | GitHub 更新了 RSA SSH host key | `content/post/github-rsa.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 319 | `expand` | 2015-10-30 | 前端面试基础题目 | `content/post/前端面试基础题目.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 322 | `expand` | 2015-05-02 | 实现combobox模糊查询的时候报错 InvalidArgument=“0”的值对于“index”无效 | `content/post/实现combobox模糊查询的时候报错 InvalidArgument=“0”的值对于“index”无效.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 356 | `expand` | 2015-10-11 | Django学习——开发你的第一个Django应用2 | `content/post/Django学习——开发你的第一个Django应用2.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 363 | `expand` | 2015-04-12 | opencv视频流的读取和处理 | `content/post/opencv视频流的读取和处理.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 374 | `expand` | 2019-07-04 | cve check | `content/post/check-cve.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 378 | `expand` | 2019-04-04 | Bashed -- hack the box | `content/post/bashed-hack-the-box.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 397 | `expand` | 2015-10-07 | indexDB的概念 | `content/post/indexDB的概念.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 397 | `expand` | 2015-10-07 | 一个神奇却很简单的css特效 | `content/post/一个神奇却很简单的css特效.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 398 | `expand` | 2019-03-15 | Cronos -- hack the box | `content/post/Cronos-hack the box.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 401 | `expand` | 2018-08-16 | 利用 python 生成可视化报告 | `content/post/利用python生成可视化报告.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 402 | `expand` | 2016-07-01 | javascript中无法将string转化为json对象 | `content/post/javascript中无法将string转化为json对象.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 419 | `expand` | 2018-03-28 | 如何做一个完美的页码跳转 | `content/post/如何实现一个完美的页码跳转.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 429 | `expand` | 2017-09-23 | 将Medium中的博客导出成markdown | `content/post/将Medium中的博客导出成markdown.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 431 | `expand` | 2021-03-09 | JavaScript能否修改Referer请求头 | `content/post/referer.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 434 | `expand` | 2017-02-22 | Ext.js性能优化漫谈 | `content/post/Ext.js性能优化漫谈.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 434 | `expand` | 2016-06-30 | moongoose对象无法新增删除属性 | `content/post/moongoose对象无法新增删除属性.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 443 | `expand` | 2019-05-16 | 后渗透的文件传输 | `content/post/后渗透的文件传输.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 463 | `expand` | 2024-06-27 | 大佬，您这是在借鉴嘛 | `content/post/export-to-markdown.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 478 | `expand` | 2015-05-18 | 道路模型--linear-parabolic model | `content/post/道路模型--linear-parabolic model.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 480 | `expand` | 2015-11-14 | 剑指offer--字符串 | `content/post/剑指offer--字符串.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 488 | `expand` | 2015-10-07 | 全栈开发教学学习系列1——前言 | `content/post/全栈开发教学学习系列1——前言.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 495 | `expand` | 2019-01-14 | IIS短文件漏洞及修复建议 | `content/IIS短文件漏洞及修复建议.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 495 | `expand` | 2016-04-26 | 利用tesseract-ocr进行验证码识别 | `content/post/利用tesseract-ocr进行验证码识别.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 523 | `expand` | 2025-08-11 | CVE-2025-55188：7-Zip 任意文件写入漏洞 | `content/post/CVE-2025-55188.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 539 | `expand` | 2018-08-12 | 黑产代码解密--利用canvas加载代码 | `content/post/黑产代码解密--利用canvas加载代码.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 545 | `expand` | 2015-04-11 | ROT13加密和解密 | `content/post/ROT13加密和解密.md` | 中薄，补步骤/踩坑/结论到 800–1200+ |
| 681 | `keep_or_archive` | 2015-10-21 | 剑指offer学习--初级c++面试题 | `content/post/剑指offer学习--初级c++面试题.md` | 长度尚可，非主线可归档 |
| 733 | `keep_or_archive` | 2015-04-11 | 道路识别 | `content/post/道路识别.md` | 长度尚可，非主线可归档 |
| 761 | `keep_or_archive` | 2016-12-06 | Latex--入门系列二 | `content/post/Latex--入门系列二.md` | 长度尚可，非主线可归档 |
| 1121 | `keep_or_archive` | 2025-02-24 | mac mini，真香？ | `content/post/mac-mini.md` | 长文但偏其他主题 |
| 1145 | `keep_or_archive` | 2016-12-03 | Latex--入门系列一 | `content/post/Latex--入门系列一.md` | 长文但偏其他主题 |
| 1154 | `keep_or_archive` | 2015-04-19 | 独立成分分析（Independent Component Analysis） | `content/post/独立成分分析（Independent Component Analysis）.md` | 长文但偏其他主题 |
| 1244 | `keep_or_archive` | 2021-09-06 | 电车的高速之行 | `content/post/highway.md` | 长文但偏其他主题 |
| 1330 | `keep_or_archive` | 2026-06-20 | 从1243元跌回935元：近一年黄金到底变弱了吗？ | `content/post/au9999_gold_trend_article.md` | 长文但偏其他主题 |
| 1344 | `keep_or_archive` | 2020-09-19 | imac 2020，真香？ | `content/post/imac.md` | 长文但偏其他主题 |
| 1364 | `keep_or_archive` | 2015-04-18 | CHEVP算法（CannyHough Estimation of Vanishing Points) | `content/post/CHEVP算法（CannyHough Estimation of Vanishing Points).md` | 长文但偏其他主题 |
| 1384 | `keep_or_archive` | 2016-12-12 | Latex--入门系列三 | `content/post/Latex--入门系列三.md` | 长文但偏其他主题 |
| 1401 | `keep_or_archive` | 2021-05-01 | 技术宅的第一辆车--小鹏P7 | `content/post/xiaopeng.md` | 长文但偏其他主题 |
| 1459 | `keep_or_archive` | 2015-06-27 | 奇异值分解基础(SVD) | `content/post/奇异值分解基础(SVD).md` | 长文但偏其他主题 |
| 1474 | `keep_or_archive` | 2023-08-12 | 菜腿的骑行通勤 | `content/post/骑行.md` | 长文但偏其他主题 |
| 1520 | `keep_or_archive` | 2020-11-15 | 颈椎康复指南--桌面篇 | `content/post/颈椎.md` | 长文但偏其他主题 |
| 1790 | `keep_or_archive` | 2022-07-20 | 停车被蹭的那些小事 | `content/post/shanghai.md` | 长文但偏其他主题 |
| 1951 | `keep_or_archive` | 2021-06-25 | 提车二月记--小鹏P7 | `content/post/xp.md` | 长文但偏其他主题 |
| 2100 | `keep_or_archive` | 2022-09-25 | 小鹏 P7 之殤 | `content/post/xp-problem.md` | 长文但偏其他主题 |
| 2217 | `keep_or_archive` | 2023-02-12 | 行车记录仪对比 - 盯盯拍mini5 vs 海康威视C8 | `content/post/行车记录仪.md` | 长文但偏其他主题 |
| 2631 | `keep_or_archive` | 2016-01-08 | 演化计算会议 | `content/post/演化计算会议.md` | 长文但偏其他主题 |
| 4776 | `keep_or_archive` | 2015-04-11 | 计算机视觉领域的一些牛人博客，超有实力的研究机构等的网站链接 | `content/post/计算机视觉领域的一些牛人博客，超有实力的研究机构等的网站链接.md` | 长文但偏其他主题 |
| 602 | `keep_polish` | 2022-12-02 | CPE 获取指南 | `content/post/cpe.md` | 接近可用：加目录结构、示例与内链 |
| 615 | `keep_polish` | 2019-03-17 | Nibbles - Hack the box | `content/post/Nibbles-hack-the-box.md` | 接近可用：加目录结构、示例与内链 |
| 621 | `keep_polish` | 2019-10-17 | Kibana 任意代码执行漏洞 | `content/post/Kibana任意代码执行漏洞.md` | 接近可用：加目录结构、示例与内链 |
| 621 | `keep_polish` | 2017-03-04 | 第一个chrome extension | `content/post/第一个chrome extension.md` | 接近可用：加目录结构、示例与内链 |
| 649 | `keep_polish` | 2015-05-02 | 微软Visual Studio Code基本特征 | `content/post/微软Visual Studio Code基本特征.md` | 接近可用：加目录结构、示例与内链 |
| 655 | `keep_polish` | 2024-03-29 | 疯狂的键盘：老鸟成长史 | `content/laoniao.md` | 接近可用：加目录结构、示例与内链 |
| 660 | `keep_polish` | 2015-12-08 | 从后台看python--为什么说python是慢的 | `content/post/从后台看python--为什么说python是慢的.md` | 接近可用：加目录结构、示例与内链 |
| 670 | `keep_polish` | 2022-04-21 | gobuster源码阅读--入口篇 | `content/post/gobuster1.md` | 接近可用：加目录结构、示例与内链 |
| 675 | `keep_polish` | 2016-03-05 | js的事件流理解 | `content/post/js的事件流理解.md` | 接近可用：加目录结构、示例与内链 |
| 711 | `keep_polish` | 2020-08-16 | 全栈工程师的成长 | `content/全栈工程师的成长.md` | 接近可用：加目录结构、示例与内链 |
| 730 | `keep_polish` | 2015-10-24 | javascript的继承模式 | `content/post/javascript的继承模式.md` | 接近可用：加目录结构、示例与内链 |
| 730 | `keep_polish` | 2017-11-16 | 基于ELK进行邮箱访问日志的分析 | `content/post/基于ELK进行邮箱访问日志的分析.md` | 接近可用：加目录结构、示例与内链 |
| 735 | `keep_polish` | 2019-04-22 | Help -- hack the box | `content/post/Help-hack the box.md` | 接近可用：加目录结构、示例与内链 |
| 738 | `keep_polish` | 2019-05-20 | Holiday -- hack the box | `content/post/Holiday-hack the box.md` | 接近可用：加目录结构、示例与内链 |
| 747 | `keep_polish` | 2016-04-25 | 模拟.net post请求属性 | `content/post/模拟.net post请求属性.md` | 接近可用：加目录结构、示例与内链 |
| 750 | `keep_polish` | 2019-08-31 | 如何写一个 burp 插件 | `content/post/如何写一个burp插件.md` | 接近可用：加目录结构、示例与内链 |
| 753 | `keep_polish` | 2022-04-22 | gobuster源码阅读--终篇 | `content/post/gobuster3.md` | 接近可用：加目录结构、示例与内链 |
| 769 | `keep_polish` | 2023-08-28 | Google Drive 的信息检索 | `content/post/drive.md` | 接近可用：加目录结构、示例与内链 |
| 770 | `keep_polish` | 2021-08-30 | 富文本场景下的 XSS | `content/post/stored-xss.md` | 接近可用：加目录结构、示例与内链 |
| 800 | `keep_polish` | 2022-09-07 | Go 的漏洞管理 | `content/post/go-vuln-management.md` | 接近可用：加目录结构、示例与内链 |
| 813 | `keep_polish` | 2019-08-22 | 偶遇 XSS 漏洞 | `content/post/偶遇的XSS漏洞.md` | 接近可用：加目录结构、示例与内链 |
| 817 | `keep_polish` | 2019-09-23 | 真香系列之 Golang 升级 | `content/post/gproxy.md` | 接近可用：加目录结构、示例与内链 |
| 849 | `keep_polish` | 2018-04-21 | 从一道面试题谈谈 setTimeout 和 setInterval | `content/post/从一到面试题谈谈setTimeout和setInterval.md` | 接近可用：加目录结构、示例与内链 |
| 850 | `keep_polish` | 2017-04-22 | service worker之cache实践--sw-precache | `content/post/service worker之cache实践--sw-precache.md` | 接近可用：加目录结构、示例与内链 |
| 850 | `keep_polish` | 2020-08-26 | 寻找你的第一个漏洞 | `content/post/寻找你的第一个漏洞.md` | 接近可用：加目录结构、示例与内链 |
| 871 | `keep_polish` | 2017-09-17 | Mongoose中document和object的区别 | `content/post/Mongoose中document和object的区别.md` | 接近可用：加目录结构、示例与内链 |
| 896 | `keep_polish` | 2019-11-30 | Haystack - hack the box | `content/post/haystack.md` | 接近可用：加目录结构、示例与内链 |
| 897 | `keep_polish` | 2020-03-30 | 让你的SQL盲注快起来 | `content/post/让你的SQL盲注快起来.md` | 接近可用：加目录结构、示例与内链 |
| 930 | `keep_attr` | 2023-01-16 | 为什么 2022 年是漏洞赏金奖破纪录的一年 | `content/post/github-bug-bounty.md` | 长译文：保留+出处+补原创点评 |
| 956 | `keep_attr` | 2020-12-10 | 火眼红队工具遭窃 | `content/post/火眼.md` | 长译文：保留+出处+补原创点评 |
| 987 | `keep_attr` | 2019-01-28 | 隐写术-深入研究 PDF 混淆漏洞 | `content/post/隐写术-深入研究PDF混淆漏洞.md` | 长译文：保留+出处+补原创点评 |
| 1073 | `keep_attr` | 2016-08-15 | Bootstrap真的总是好的吗 | `content/post/Bootstrap真的总是好的吗.md` | 长译文：保留+出处+补原创点评 |
| 1075 | `keep_attr` | 2017-05-21 | 通过利用immutability的能力编写更安全和更整洁的代码 | `content/post/通过利用immutability的能力编写更安全和更整洁的代码.md` | 长译文：保留+出处+补原创点评 |
| 1097 | `keep_attr` | 2016-10-03 | 你可能不知道谷歌浏览器开发工具的其他用处 | `content/post/你可能不知道谷歌浏览器开发工具的其他用处.md` | 长译文：保留+出处+补原创点评 |
| 1266 | `keep_attr` | 2019-02-02 | 2019 年针对 API 安全的 4 点建议 | `content/post/2019年针对API安全的4点建议.md` | 长译文：保留+出处+补原创点评 |
| 1368 | `keep_attr` | 2018-04-07 | 消灭 star 大作战--Front-end-tutorial | `content/post/消灭star大作战-Front-end-tutorial.md` | 长译文：保留+出处+补原创点评 |
| 1442 | `keep_attr` | 2017-08-06 | 什么是服务端伪造（SSRF） | `content/post/什么是服务端伪造（SSRF）.md` | 长译文：保留+出处+补原创点评 |
| 1611 | `keep_attr` | 2017-09-13 | JavaScript是如何工作的：引擎，运行时间以及调用栈的概述 | `content/post/JavaScript是如何工作的：引擎，运行时间以及调用栈的概述.md` | 长译文：保留+出处+补原创点评 |
| 1630 | `keep_attr` | 2018-02-23 | 聊聊答题应用题库的建立 | `content/post/聊聊答题应用题库的建立.md` | 长译文：保留+出处+补原创点评 |
| 1991 | `keep_attr` | 2017-05-02 | service worker介绍 | `content/post/service worker介绍.md` | 长译文：保留+出处+补原创点评 |
| 1992 | `keep_attr` | 2019-11-10 | Chrome 最新零日漏洞 | `content/post/Chrome最新在野零日漏洞.md` | 长译文：保留+出处+补原创点评 |
| 2055 | `keep_attr` | 2017-05-11 | 基于Vue JS, Webpack 以及Material Design的渐进式web应用 [Part 1] | `content/post/基于Vue JS, Webpack 以及Material Design的渐进式web应用 [Part 1].md` | 长译文：保留+出处+补原创点评 |
| 2148 | `keep_attr` | 2019-11-24 | GMail XSS 漏洞分析 | `content/post/XSS.md` | 长译文：保留+出处+补原创点评 |
| 2150 | `keep_attr` | 2021-03-07 | 微软开源对于 Solorigate 活动捕获的开源 CodeQL 查询 | `content/post/ms-codeql.md` | 长译文：保留+出处+补原创点评 |
| 2201 | `keep_attr` | 2016-07-26 | javascript中的对象字面量为啥这么酷 | `content/post/javascript中的对象字面量为啥这么酷.md` | 长译文：保留+出处+补原创点评 |
| 2234 | `keep_attr` | 2026-01-17 | 不到一分钟拿到可用 PoC：Julen Garrido Estévez 测试 Burp AI | `content/post/burp-ai.md` | 长译文：保留+出处+补原创点评 |
| 2443 | `keep_attr` | 2022-03-28 | SAST 测试中要测量的三个参数 | `content/post/sast.md` | 长译文：保留+出处+补原创点评 |
| 2524 | `keep_attr` | 2017-11-12 | 出去就餐并且理解Express.js的基本知识 | `content/post/出去就餐并且理解Express.js的基本知识.md` | 长译文：保留+出处+补原创点评 |
| 2546 | `keep_attr` | 2023-11-12 | 如何使用 Git 撤消（几乎）任何操作 | `content/post/git-undo.md` | 长译文：保留+出处+补原创点评 |
| 2563 | `keep_attr` | 2025-02-06 | 通过 Cookie Tossing 劫持 OAUTH 流程 | `content/post/cookie-tossing.md` | 长译文：保留+出处+补原创点评 |
| 2668 | `keep_attr` | 2019-10-13 | Pornhub Web 开发者访谈 | `content/post/Pornhub Web 开发者访谈.md` | 长译文：保留+出处+补原创点评 |
| 2988 | `keep_attr` | 2016-04-27 | nodejs回调大坑 | `content/post/nodejs回调大坑.md` | 长译文：保留+出处+补原创点评 |
| 3683 | `keep_attr` | 2020-09-06 | 一键 Shell，我的 OSWE 之旅 | `content/post/OSWE.md` | 长译文：保留+出处+补原创点评 |
| 3699 | `keep_attr` | 2023-01-14 | CircleCI 20230104 安全事件报告 | `content/post/circleci-incident.md` | 长译文：保留+出处+补原创点评 |
| 3952 | `keep_attr` | 2024-11-30 | NilAway：实用的 Go Nil Panic 检测方式 | `content/post/nilayay.md` | 长译文：保留+出处+补原创点评 |
| 4240 | `keep_attr` | 2017-04-16 | Twitter Lite以及大规模的高性能React渐进式网络应用 | `content/post/Twitter Lite以及大规模的高性能React渐进式网络应用.md` | 长译文：保留+出处+补原创点评 |
| 5903 | `keep_attr` | 2018-06-16 | Elasticsearch 团队开发章程 | `content/post/Elasticsearch团队开发章程.md` | 长译文：保留+出处+补原创点评 |
| 6918 | `keep_attr` | 2017-05-19 | 菜鸟程序员成长史 --记 Github 1000+ contributions | `content/post/programer.md` | 长译文：保留+出处+补原创点评 |
| 912 | `keep` | 2022-09-17 | 关于招人的那点小事 | `content/post/hr.md` | 主线长文，优先保留 |
| 915 | `keep` | 2025-08-22 | AI 审代码，靠谱吗？ | `content/post/gorm.md` | 主线长文，优先保留 |
| 931 | `keep` | 2017-03-19 | 第一个progressive web application，发车！ | `content/post/第一个progressive web application，发车！.md` | 主线长文，优先保留 |
| 952 | `keep` | 2015-10-10 | 全栈开发系列学习2——django项目搭建 | `content/post/全栈开发系列学习2——django项目搭建.md` | 主线长文，优先保留 |
| 966 | `keep` | 2015-10-10 | Django学习——开发你的第一个Django应用1 | `content/post/Django学习——开发你的第一个Django应用1.md` | 主线长文，优先保留 |
| 979 | `keep` | 2022-03-07 | hey,我能看到你的源码哎 | `content/post/webpack.md` | 主线长文，优先保留 |
| 1013 | `keep` | 2015-10-13 | matlab调试技巧 | `content/post/matlab调试技巧.md` | 主线长文，优先保留 |
| 1020 | `keep` | 2018-06-21 | Wmic 使用中的一些问题 | `content/post/wmic使用中的一些问题.md` | 主线长文，优先保留 |
| 1040 | `keep` | 2015-12-15 | 常用的正则表达式 | `content/post/常用的正则表达式.md` | 主线长文，优先保留 |
| 1046 | `keep` | 2016-03-01 | 前端面试题——系列一 | `content/post/前端面试题——系列一.md` | 主线长文，优先保留 |
| 1077 | `keep` | 2018-11-16 | 架构整洁之道读后感 | `content/架构整洁之道读后感.md` | 主线长文，优先保留 |
| 1120 | `keep` | 2022-04-21 | gobuster源码阅读--dir篇 | `content/post/gobuster2.md` | 主线长文，优先保留 |
| 1126 | `keep` | 2022-08-12 | iMac+Studio Display，双 5k 屏体验 | `content/post/studio-display.md` | 主线长文，优先保留 |
| 1153 | `keep` | 2015-11-27 | 谈谈CS英文论文写作 | `content/post/谈谈CS英文论文写作.md` | 主线长文，优先保留 |
| 1164 | `keep` | 2026-08-01 | 改三个 JSON，让 Claude 桌面版用上你自己的 API | `content/post/通过自定义API接入Claude桌面版.md` | 主线长文，优先保留 |
| 1233 | `keep` | 2024-06-29 | Home Assistant 小米门铃视频本地存储 | `content/post/xiaomi.md` | 主线长文，优先保留 |
| 1239 | `keep` | 2015-04-11 | 关于计算机视觉研究 | `content/post/关于计算机视觉研究.md` | 主线长文，优先保留 |
| 1252 | `keep` | 2021-01-03 | 白名单，被谁饶过了？ | `content/post/redirect.md` | 主线长文，优先保留 |
| 1254 | `keep` | 2017-11-26 | POI读取文件的最佳实践 | `content/post/POI读取文件的最佳实践.md` | 主线长文，优先保留 |
| 1270 | `keep` | 2021-04-17 | 多平台的敏感信息检测工具-GShark | `content/post/gshark.md` | 主线长文，优先保留 |
| 1275 | `keep` | 2016-03-04 | 百度前端实习生面试（连跪之旅） | `content/post/百度前端实习生面试（连跪之旅）.md` | 主线长文，优先保留 |
| 1365 | `keep` | 2018-10-26 | Qradar SIEM--查询利器 AQL | `content/post/Qradar-SIME查询利器.md` | 主线长文，优先保留 |
| 1442 | `keep` | 2018-02-25 | 通过七牛云建立私有图床 | `content/post/通过七牛云建立私有图床.md` | 主线长文，优先保留 |
| 1460 | `keep` | 2019-09-22 | Bastion -- Hack the box | `content/post/Bastion.md` | 主线长文，优先保留 |
| 1484 | `keep` | 2018-08-23 | web 狗之writeup--phone | `content/post/web狗之writeup--phone.md` | 主线长文，优先保留 |
| 1498 | `keep` | 2019-05-27 | 持续发布 Chrome 插件 | `content/post/持续发布Chrome插件.md` | 主线长文，优先保留 |
| 1506 | `keep` | 2022-02-23 | 基于golang实现报告生成技术方案 | `content/post/go-report.md` | 主线长文，优先保留 |
| 1511 | `keep` | 2020-02-20 | PWK 以及 OSCP 最常见的问题 | `content/post/PWK以及OSCP最常见的问题.md` | 主线长文，优先保留 |
| 1641 | `keep` | 2019-10-20 | 1024献礼，全栈工程师进击 | `content/post/全栈工程师的百宝箱.md` | 主线长文，优先保留 |
| 1761 | `keep` | 2022-01-28 | 文武双全，看我如何过CISSP | `content/post/cissp-domain1.md` | 主线长文，优先保留 |
| 1801 | `keep` | 2025-02-10 | ChatGPT账户接管 - 通配符网页缓存欺骗 | `content/chatgpt-ato.md` | 主线长文，优先保留 |
| 1925 | `keep` | 2022-08-07 | Shopee 靠谱内推 | `content/post/shopee.md` | 主线长文，优先保留 |
| 2098 | `keep` | 2015-04-11 | OPENCV | `content/post/OPENCV.md` | 主线长文，优先保留 |
| 2113 | `keep` | 2020-11-07 | 键盘简史 | `content/post/键盘.md` | 主线长文，优先保留 |
| 2136 | `keep` | 2025-08-30 | Go 版本不一致？别慌，这是特性！ | `content/post/toolchain.md` | 主线长文，优先保留 |
| 2182 | `keep` | 2019-09-28 | 被动扫描器之插件篇 | `content/post/被动扫描器之Chrome插件.md` | 主线长文，优先保留 |
| 2246 | `keep` | 2019-01-04 | 什么是DDOS | `content/post/什么是DDOS.md` | 主线长文，优先保留 |
| 2274 | `keep` | 2020-04-18 | 网络安全分析的瑞士军刀--zeek | `content/post/流量分析的瑞士军刀--zeek.md` | 主线长文，优先保留 |
| 2296 | `keep` | 2018-03-21 | pwa, 上海地铁线路图全新重构 | `content/post/pwa, 上海地铁线路图全新重构.md` | 主线长文，优先保留 |
| 2306 | `keep` | 2018-10-31 | GShark-监测你的 Github 敏感信息泄露 | `content/post/GShark-监测你的Github敏感信息泄露.md` | 主线长文，优先保留 |
| 2330 | `keep` | 2020-03-04 | XSS 漏洞知解 123 | `content/post/反射性XSS知解123.md` | 主线长文，优先保留 |
| 2528 | `keep` | 2026-06-19 | 博客考古：从漏洞、工具到生活折腾 | `content/post/博客文章阶段性总结.md` | 主线长文，优先保留 |
| 2563 | `keep` | 2022-05-03 | 第一款Goland的SCA插件开发之旅 | `content/post/goland-plugin.md` | 主线长文，优先保留 |
| 2611 | `keep` | 2019-10-30 | MyBatis 和 SQL 注入的恩恩怨怨 | `content/post/Mybaits和SQL注入的恩恩怨怨.md` | 主线长文，优先保留 |
| 3240 | `keep` | 2018-05-26 | 理解 OutOfMemoryError 异常 | `content/post/理解OutOfMemory异常.md` | 主线长文，优先保留 |
| 3271 | `keep` | 2019-02-21 | 跨站请求伪造（CSRF）攻击 | `content/post/跨站请求伪造（CSRF)攻击.md` | 主线长文，优先保留 |
| 3481 | `keep` | 2022-01-21 | 安全运营平台从0到1 | `content/post/sop.md` | 主线长文，优先保留 |
| 3582 | `keep` | 2019-11-29 | 僵尸网络 Stantinko 犯罪活动新增加密货币挖矿 | `content/post/botnet.md` | 主线长文，优先保留 |
| 11099 | `keep` | 2019-04-15 | 使用浏览器作为代理从公网攻击内网 | `content/post/使用浏览器作为代理从公网攻击内网.md` | 主线长文，优先保留 |

## 数据文件

- 机器可读：`adsense-content-audit.csv`
- 本说明：`ADSENSE-AUDIT.md`

## 本轮交付物

- `ADSENSE-AUDIT.md` — 人工可读审计报告
- `adsense-content-audit.csv` — 机器可读全量表
- `content/about.md` — About 页
- `content/privacy.md` — Privacy Policy（含 Analytics / AdSense / Disqus / Cookie）
- `config.toml` — 主导航增加 About / Privacy
- `layouts/partials/footer.html` — 页脚增加 About / Privacy 链接
