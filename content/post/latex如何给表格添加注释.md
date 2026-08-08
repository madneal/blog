---
title: "LaTeX 表格脚注：用 threeparttable 给表格加注释"
author: "Neal"
summary: "论文表格需要对单元格加说明时，用 threeparttable + tablenotes 的完整写法、常见错误，以及和 table note 的对比。"
tags: [LaTeX, 论文写作]
categories: [论文写作]
date: "2015-12-10"
lastmod: "2026-08-08"
---


写实验论文时，表格里经常要解释「粗体表示更优」「单位是秒」「某列为 30 次独立运行的均值」。把说明塞进 caption 会又臭又长；直接写在表格外又对不齐。`threeparttable` 就是为这种「表 + 脚注」准备的。

## 最小工作示例

```latex
\usepackage{threeparttable}
\usepackage{booktabs} % 可选，更美观的三线表

\begin{table}[htbp]
  \centering
  \begin{threeparttable}
    \caption{两种算法在测试集上的 IGD 统计（30 次独立运行）}
    \label{tab:igd}
    \begin{tabular}{lcccc}
      \toprule
      Instance & mean & std & best & worst \\
      \midrule
      $F_1$ & $3.90\times10^{-3}$ & $1.39\times10^{-4}$ & $3.70\times10^{-3}$ & $4.20\times10^{-3}$ \\
      $F_2$ & $\mathbf{3.70\times10^{-3}}$\tnote{1} & $9.83\times10^{-5}$ & $3.50\times10^{-3}$ & $3.90\times10^{-3}$ \\
      \bottomrule
    \end{tabular}
    \begin{tablenotes}
      \small
      \item[1] 粗体表示在该实例上更优。
      \item 所有结果在相同随机种子策略下复现。
    \end{tablenotes}
  \end{threeparttable}
\end{table}
```

要点：

1. `table` 负责浮动与 caption  
2. `threeparttable` 把「表体 + 注释」绑成同一宽度逻辑  
3. `\tnote{1}` 在单元格里打标记，`tablenotes` 里用 `\item[1]` 对应  

## 双栏模板用 `table*`

会议模板常是双栏，宽表要用 `table*`：

```latex
\begin{table*}[htbp]
  \begin{threeparttable}
    % ... tabular ...
  \end{threeparttable}
\end{table*}
```

## 常见坑

| 现象 | 原因 | 处理 |
|------|------|------|
| 注释比表格宽出去 | 没用 threeparttable，只是手写段落 | 包进 `threeparttable` |
| `\tnote` 未定义 | 包未导入或写在环境外 | `\usepackage{threeparttable}` |
| 编号与正文引用混乱 | caption 的 label 放错位置 | `\label` 紧跟 `\caption` 后 |
| 与 `beamer` 不兼容折腾 | 幻灯片表格脚注需求不同 | 幻灯片直接写在 frame 底部更简单 |

## 和 `\footnote` 的区别

在 `tabular` 里直接 `\footnote` 往往失效或跑到错误位置。`threeparttable` 的 `\tnote` 是表格语义上的注释，不会和页脚注混用，审稿人读表更自然。

## 排版建议

- 注释用 `\small` 或 `\footnotesize`，避免比正文还抢眼  
- 指标单位、运行次数、硬件环境优先放 caption 第一句，细节放 notes  
- 统计显著性若只对部分格成立，用 `tnote` 逐个标，不要只在 caption 含糊说「部分加粗」  

掌握 `threeparttable` 之后，实验表从「一堆数」变成「可独立阅读的结果单元」，这在 rebuttal 阶段特别省事。
