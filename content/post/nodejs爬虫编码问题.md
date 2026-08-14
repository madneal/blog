---
title: "Node.js 爬虫中文乱码：GBK/GB2312 正确解码"
author: Neal
summary: "爬取非 UTF-8 站点时中文乱码：用 encoding:null 拿 Buffer，再用 iconv-lite 按实际编码解码；附 charset 探测与常见坑。"
cover: "/img/post-covers/nodejs-crawler-encoding-e4348aa7a6.jpg"
tags: [JavaScript, Node.js, 后端]
categories: [web前端]
date: "2016-04-16"
lastmod: "2026-08-08"
---

## 现象

写 Node 爬虫时，部分站点中文变成「锟斤拷」或乱码。原因通常不是 cheerio 坏了，而是：**页面不是 UTF-8**，却被按 UTF-8 解成了字符串。

国内老站仍常见 **GBK / GB2312**。浏览器能正常显示，是因为 HTTP 头或 `<meta charset>` 声明了编码；你的脚本若默认 UTF-8，就会错。

## 怎么确认编码

1. DevTools → Network → 文档响应头 `Content-Type: text/html; charset=gbk`  
2. 查看源码 `<meta charset="gbk">` / `gb2312`  
3. 仍不确定时，可用 `chardet` 类库做探测（不要 100% 盲信）

## 正确做法：先拿字节，再解码

`request`（或其它 HTTP 库）若自动把 body 转成字符串，会按错误编码损坏数据。应：

1. 禁用自动字符串解码，拿到 **Buffer**  
2. 用 `iconv-lite` 按真实编码 decode  

```javascript
const request = require('request');
const cheerio = require('cheerio');
const iconv = require('iconv-lite');

request(
  {
    url: 'https://example.com/',
    encoding: null, // 关键：body 为 Buffer
  },
  (err, res, body) => {
    if (err) throw err;

    // 按站点实际编码修改
    const html = iconv.decode(body, 'gbk');
    const $ = cheerio.load(html);
    console.log($('head title').text());
  }
);
```

注意旧笔记里的笔误：`encodeing` 应为 `encoding`；`cheerio` 不要写成 `request('cheerio')`。

## 现代写法（axios / fetch）

```javascript
const axios = require('axios');
const iconv = require('iconv-lite');

const res = await axios.get(url, { responseType: 'arraybuffer' });
const html = iconv.decode(Buffer.from(res.data), 'gbk');
```

## 常见坑

| 坑 | 说明 |
|----|------|
| 先 `toString('utf8')` 再转 | 信息已丢，无法救 |
| 编码写死 gbk | 多站点要按响应头切换 |
| 忽略压缩 | 确保先解 gzip 再解码 |
| 合规 | 爬虫需遵守 robots/授权与频率限制 |

## 小结

乱码问题的本质是 **字节序列被用错字符集解释**。爬虫链路固定为：**Buffer → 判定 charset → iconv-lite → 再 parse DOM**。
