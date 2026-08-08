---
title: "LaTeX 画一张简单三线表"
author: "Neal"
summary: "从 tabular 基础列格式讲到 booktabs 三线表、caption/label 与跨页长表入口，给出论文里最常用的最小模板。"
tags: [LaTeX, 论文写作]
categories: [论文写作]
date: "2015-09-26"
lastmod: "2026-08-08"
---


LaTeX 表格的基本单元是 `tabular`：先声明每一列怎么对齐，再一行行填单元格。论文里更推荐 **三线表**（`booktabs`），而不是满屏竖线。

## 最小例子

```latex
\begin{table}[htbp]
  \centering
  \caption{算法时间复杂度对比}
  \label{tab:complexity}
  \begin{tabular}{cc}
    \hline
    Algorithm & Time complexity \\
    \hline
    RM-MEDA  & $O(NM)$ \\
    IRM-MEDA & $O(NK)$ \\
    \hline
  \end{tabular}
\end{table}
```

列格式：

- `c` 居中，`l` 左，`r` 右  
- `p{3cm}` 固定宽度并自动换行  
- `|` 画竖线（正式论文常不用）

## 更推荐的三线表

```latex
\usepackage{booktabs}

\begin{table}[htbp]
  \centering
  \caption{算法时间复杂度对比}
  \label{tab:complexity}
  \begin{tabular}{ll}
    \toprule
    Algorithm & Time complexity \\
    \midrule
    RM-MEDA  & $O(NM)$ \\
    IRM-MEDA & $O(NK)$ \\
    \bottomrule
  \end{tabular}
\end{table}
```

`\toprule \midrule \bottomrule` 线宽层次更符合排版规范。

## 合并单元格

```latex
\multicolumn{2}{c}{Overall} \\
```

多行合并用 `multirow` 宏包。

## 浮动体位置

`[htbp]` 是建议位置：here / top / bottom / page。不要迷信 `[h]` 一定「就在这」——LaTeX 会整体优化。大表可用 `table*`（双栏模板）。

## 常见错误

1. `\caption` 放在 `tabular` 外、`table` 内（正确）；放反会报错或编号乱。  
2. `\label` 必须在 `\caption` **之后**。  
3. 单元格里的 `_` 要进数学模式 `$O(N_m)$`。  
4. 超宽表：换 `p{}`、`tabularx` 或缩小 `\small`。  

## 下一步

- 表注：见《threeparttable》一文  
- 超长表：`longtable`  
- 与数据生成：用脚本吐 LaTeX 行，避免手敲实验数字  

## 小结

先掌握 `tabular` + `table` + `caption`，再换成 `booktabs` 三线表，就覆盖了 80% 的论文表格需求。简单，但是要写对浮动与引用。
