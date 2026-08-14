---
title: "CSS 样式表引入：link 与 @import 的区别"
author: Neal
summary: "对比 HTML link 与 CSS @import：加载时机、可控性、性能建议，以及何时用哪一种。"
cover: "/img/post-covers/css-import-ways-55e4b07683.jpg"
tags: [前端, CSS]
categories: [web前端]
date: "2015-10-06"
lastmod: "2026-08-08"
---

## 两种写法

```html
<link rel="stylesheet" href="/styles/main.css">
```

```css
@import url("/styles/main.css");
/* 或 */
@import "main.css";
```

视觉上都能挂上样式，但 **机制不同**。

## 关键差异

| 维度 | `<link>` | `@import` |
|------|----------|-----------|
| 出现位置 | HTML | CSS 文件内（须在其它规则前） |
| 并行下载 | 多个 link 可并行 | 常等父 CSS 下载完再拉，易串行 |
| JS 控制 | 可动态增删 link、切主题 | 不方便 |
| 旧 IE 行为 | 相对清晰 | 历史上更多坑 |
| 媒体查询 | `media` 属性自然 | 也支持，但性能仍可能差 |

这也是工程里 **更推荐 link** 的原因：弹性大、性能路径更可控。

## 性能建议

1. 关键路径 CSS 用 `<link rel="stylesheet">` 放在 `<head>`。  
2. 避免在关键 CSS 里层层 `@import`。  
3. 可用 HTTP/2 + 合并/拆分策略，但不要靠 @import 组织巨型依赖树。  
4. 现代打包（webpack/vite）会处理依赖，源码里少手写 @import 远程 CSS。

## 动态换肤示例（link 优势）

```javascript
function setTheme(href) {
  let el = document.getElementById('theme');
  if (!el) {
    el = document.createElement('link');
    el.id = 'theme';
    el.rel = 'stylesheet';
    document.head.appendChild(el);
  }
  el.href = href;
}
```

## 小结

效果都是「应用样式」，**交付方式不同**。默认用 `link`；`@import` 留给 CSS 内少量模块化或遗留代码，并清楚它的加载成本。


## 和工程化的关系

在组件化项目中，样式常通过构建工具 `import './x.css'` 进入打包图，浏览器最终仍多是 `<link>` 或注入 style。源码里的 `@import` 与运行时 `@import` 不是同一回事。

写静态页或邮件模板时，优先 link；只有拆分第三方 CSS 片段且能接受串行代价时，才考虑 `@import`。
