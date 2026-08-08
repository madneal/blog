---
draft: true
title: "CSS 盒子模型：margin / padding / border 简写"
author: Neal
summary: "系统整理 padding、margin 的 1～4 值简写顺序，以及 border 简写与常见笔误，方便前端排版速查。"
tags: [前端, CSS]
categories: [web前端]
date: "2015-10-24"
lastmod: "2026-08-08"
---

## 为什么用简写

盒子模型里 `margin`、`padding`、`border` 最常调。分开写四行清晰但冗长；简写能减少重复，也是读别人样式时的基本功。

## padding / margin 的四值顺序

**上 → 右 → 下 → 左**（顺时针，从 top 开始）：

```css
/* 等价于四条 longhand */
padding: 0 20px 30px 10px;
/* top right bottom left */

margin: 0 20px 30px 10px;
```

## 更短的形式

| 写法 | 含义 |
|------|------|
| `padding: 20px;` | 四边相同 |
| `padding: 10px 20px;` | 上下 10，左右 20 |
| `padding: 10px 20px 30px;` | 上 10，左右 20，下 30 |
| `padding: 1px 2px 3px 4px;` | 上右下左 |

`margin` 规则相同。注意 **margin 折叠**：相邻垂直 margin 可能合并，与 padding 行为不同。

## border 简写

```css
border-width: 1px;
border-style: solid;
border-color: black;

/* 简写：宽度 样式 颜色（顺序可部分省略，但 style 通常不可少） */
border: 1px solid black;
```

也可分边：

```css
border-top: 2px dashed #333;
```

## 和 box-sizing

```css
box-sizing: border-box; /* 宽高含 padding+border，布局更好控 */
```

现代布局里几乎总是全局设 `border-box`。

## 小结

记住 **顺时针 TRBL** 和 **1/2/3/4 值规则**，再配合 `border` 三联简写，就能覆盖日常盒子间距。旧文里的 `boder` 拼写是笔误，标准属性是 `border`。


## 与布局一起记

- 块级元素默认占满一行宽度，margin 可「顶开」相邻元素  
- 替代方案：`gap`（flex/grid）控制子项间距，有时比父子 padding/margin 更清晰  
- 调试时用浏览器 Computed 面板看最终 margin/padding，避免被简写绕晕  

简写是语法糖，**算盒模型时仍按四边展开理解**。面试若只背 `padding: 1px 2px` 不够，要能口述四边各是多少。
