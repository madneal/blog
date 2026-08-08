---
draft: true
title: "LaTeX 算法环境：去掉 algorithmic 自动行号"
author: "Neal"
summary: "当步骤里已经写了 Step 1/2/3 时，如何去掉 algorithmic 自动编号，并对比 algorithm2e / algpseudocode 的常见写法。"
tags: [LaTeX, 算法, 论文写作]
categories: [论文写作]
date: "2015-11-06"
lastmod: "2026-08-08"
---


论文里贴伪代码时，`algorithm` + `algorithmic` 很常见。默认会在每一行前面自动加 `1: 2: 3:`。若你已经在文本里写了 `Step 1. ...`，就会出现 **双重编号**，既难看也浪费栏宽。

## 目标效果

只要：

```text
Step 1. ...
Step 2. ...
```

不要：

```text
1: Step 1. ...
2: Step 2. ...
```

## 做法：用 `algorithmic` 且不启用行号包变体

```latex
\usepackage{algorithm}
\usepackage{algorithmic} % 注意：不是 algorithmicx 的那套命令混用

\begin{algorithm}[htb]
\caption{SDE 主流程}
\label{alg:sde}
\begin{algorithmic}  % 某些版本可用 \begin{algorithmic}[0] 关闭编号
\STATE Step 1. 计算当前种群协方差矩阵 $C$，并做特征分解 $C=EDE^{T}$。
\STATE Step 2. 将种群投影到特征坐标：$P=X_{G}E$。
\STATE Step 3. 在特征坐标中做差分变异，得到 $P'$。
\STATE Step 4. 变换回原坐标：$X_{G+1}=P'E^{T}$。
\end{algorithmic}
\end{algorithm}
```

说明：

- 经典 `algorithms` 束中的 `algorithmic`，**不显式给行号参数** 时通常就不带 `1: 2:`。  
- 若你用的是 `algpseudocode`（`algorithmicx`），默认 `\begin{algorithmic}[1]` 会编号；改成：

```latex
\begin{algorithmic}[0]
\State Step 1. ...
\end{algorithmic}
```

`[0]` 表示不显示行号。

## 两套宏包不要混

| 体系 | 常见命令 | 行号 |
|------|----------|------|
| `algorithmic` | `\STATE \IF \FOR` | 老风格 |
| `algpseudocode` | `\State \If \For` | `\begin{algorithmic}[1]` |
| `algorithm2e` | `\If{...}\tcp{...}` | 自带另一套选项 |

混用会导致「Undefined control sequence」。选一套用到底。

## 需要引用某一步怎么办

若关掉自动编号又想引用，可以：

- 在 Step 文本里写死编号，正文写「见算法 1 的 Step 3」  
- 或使用 `algorithmicx` 的线标签功能（需要编号时再打开）  

## 排版建议

1. 长公式不要硬塞进 `\STATE` 一行，可 `\STATE` + `equation` 环境。  
2. `\caption` 写「做什么」，细节放步骤。  
3. 双栏模板注意算法浮动体用 `[t]`/`[htbp]`，避免漂到附录。  

## 小结

双重编号 = 自动行号 + 手写 Step 冲突。要么去掉自动行号（`[0]` 或换不编号的 `algorithmic`），要么删掉手写 Step 改用纯行号。论文里我更偏好 **手写 Step + 无自动行号**，审稿人按步骤讨论更自然。
