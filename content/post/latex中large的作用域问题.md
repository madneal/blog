---
title: "LaTeX 中 large 命令的作用域：为什么第一种写法会污染后面全文"
author: "Neal"
summary: "对比 large 的三种写法与分组作用域，解释字体切换命令如何收尾，给出论文排版实用建议。"
tags: [LaTeX, 论文写作]
categories: [论文写作]
date: "2017-01-06"
lastmod: "2026-08-08"
---


写毕业论文时，我踩过一次 `\large` 的坑：只想放大三个词，结果后面整段都变大。根因是 **字体大小命令的作用域靠分组（group）**，不是靠「函数参数」那种直觉。

## 三种写法

```latex
I am cool \large{you are right}, yeah, yeah, yeah

I am cool {\large you are right}, yeah, yeah, yeah

I am cool
\begin{large}
you are right
\end{large}, yeah, yeah, yeah
```

期望：只有 `you are right` 变大。

## 结果

1. **错误**：`\large{you are right}`  
   `\large` 是 **声明式** 字体命令，不是 `\textbf` 那种必吃参数的宏。后面的 `{...}` 只是普通分组内容，**不会**自动结束 `\large`。于是 `\large` 一直生效到当前组结束——常常是到环境/文档更大范围，于是后面的 `yeah` 也变大。

2. **正确**：`{\large you are right}`  
   显式分组：进入 `{` 后切换 large，`}` 结束恢复原字体。

3. **正确但啰嗦**：`\begin{large}...\end{large}`  
   环境自带分组，效果对，但为短文本过重。

## 同类命令

`\tiny \scriptsize \footnotesize \small \normalsize \large \Large \LARGE \huge \Huge` 都是声明式，正确局部用法统一为：

```latex
{\Large 标题片段}
```

相对地，`\textbf{...}` `\textit{...}` `\emph{...}` 是带参数的命令，写法不同。

## 实用建议

| 场景 | 建议 |
|------|------|
| 临时放大几词 | `{\large ...}` |
| 标题 | 用 `\section` 等结构命令 |
| 全文默认字号 | 文档类选项 `11pt`/`12pt` |
| 强调 | 优先语义命令 `\emph` |

## 小结

LaTeX 里「看起来像函数」的不一定吃参数。**字体大小靠分组收尾**；记住 `{\large ...}` 就能避免「放大传染病」。旧文截图外链可能失效，但结论不变。
