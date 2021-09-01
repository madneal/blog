---
title: "富文本场景下的 XSS"
author: Neal
tags: [web 安全, XSS, JS, GO]
categories: [安全]
date: 2021-08-30
---

富文本编辑器是一个常见的业务场景，一般来说，通过富文本编辑器编辑的内容最终也会 html 的形式来进行渲染，比如 VUE，一般就会使用 `v-html` 来承载富文本编辑的内容。因为文本内容需要通过 html 来进行渲染，那么显然普通的编码转义不适合这种场景了，因为这样最终的呈现的效果就不是我们想要的了。针对于这种场景，显然过滤是唯一的解决方案了，不过过滤其实可以在后端和前端都是可以做的，后端做的话，一般是在数据存储在数据库之前。前端做的话，则是在数据最终在页面渲染之前做过滤。

前端的过滤方案，可以尝试使用开源的 `[js-xss](https://github.com/leizongmin/js-xss)`。先介绍一下这个库的使用方法，这个库可以在 nodejs 中使用，同样也可以在浏览中直接引入使用。

```
// nodejs 中使用
var xss = require("xss");
var html = xss('<script>alert("xss");</script>');
console.log(html);
```

```
// 浏览器中使用
<script src="https://rawgit.com/leizongmin/js-xss/master/dist/xss.js"></script>
<script>
  // apply function filterXSS in the same way
  var html = filterXSS('<script>alert("xss");</scr' + "ipt>");
  alert(html);
</script>
```

一般在 vue 的项目中，通过 webpack 也可以直接通过 CommonJS 的方式引入，与 nodejs 的引入方式基本一致。值得注意的一个问题是，默认情况下会去禁用 style 属性，这样会导致富文本的样式展示异常，需要禁用 css 过滤或者使用白名单的方式来进行过滤。

```javascript
const xssFilter = new xss.FilterXSS({
    css: false
});
html = xssFilter.process('<script>alert("xss");</script>');
```

```javascript
const xssFilter = new xss.FilterXSS({
  css: {
    whiteList: {
      position: /^fixed|relative$/,
      top: true,
      left: true,
    },
  },
});
html = xssFilter.process('<script>alert("xss");</script>');
```

其实 js-xss 的原理并不是很复杂，如果去扒一下源码，原理其实主要就是实现标签和属性的白名单过滤，这样的方案简单有效。因为默认配置了大部分标签以及属性的白名单方案，所以一般可以做到开箱即用，当然如果有定制化的需求需要进一步定制化函数。

```javascript
function getDefaultWhiteList() {
  return {
    a: ["target", "href", "title"],
    abbr: ["title"],
    address: [],
    area: ["shape", "coords", "href", "alt"],
    article: [],
    aside: [],
    audio: [
      "autoplay",
      "controls",
      "crossorigin",
      "loop",
      "muted",
      "preload",
      "src",
    ],
    b: [],
    bdi: ["dir"],
    bdo: ["dir"],
    big: [],
    blockquote: ["cite"],
    br: [],
    caption: [],
    center: [],
    cite: [],
    code: [],
    col: ["align", "valign", "span", "width"],
    colgroup: ["align", "valign", "span", "width"],
    dd: [],
    del: ["datetime"],
    details: ["open"],
    div: [],
    dl: [],
    dt: [],
    em: [],
    figcaption: [],
    figure: [],
    font: ["color", "size", "face"],
    footer: [],
    h1: [],
    h2: [],
    h3: [],
    h4: [],
    h5: [],
    h6: [],
    header: [],
    hr: [],
    i: [],
    img: ["src", "alt", "title", "width", "height"],
    ins: ["datetime"],
    li: [],
    mark: [],
    nav: [],
    ol: [],
    p: [],
    pre: [],
    s: [],
    section: [],
    small: [],
    span: [],
    sub: [],
    summary: [],
    sup: [],
    strong: [],
    strike: [],
    table: ["width", "border", "align", "valign"],
    tbody: ["align", "valign"],
    td: ["width", "rowspan", "colspan", "align", "valign"],
    tfoot: ["align", "valign"],
    th: ["width", "rowspan", "colspan", "align", "valign"],
    thead: ["align", "valign"],
    tr: ["rowspan", "align", "valign"],
    tt: [],
    u: [],
    ul: [],
    video: [
      "autoplay",
      "controls",
      "crossorigin",
      "loop",
      "muted",
      "playsinline",
      "poster",
      "preload",
      "src",
      "height",
      "width",
    ],
  };
}
```