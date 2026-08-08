---
title: "差分进化（DE）算法原理与 MATLAB 示例"
author: "Neal"
summary: "讲清 DE 的变异、交叉、选择三步，参数 F/CR/N 的含义，并给出可运行的 MATLAB 最小化示例与调参注意点。"
tags: [算法, 机器学习, MATLAB]
categories: [机器学习]
date: "2015-10-26"
lastmod: "2026-08-08"
---


差分进化（Differential Evolution, DE）是一类简单高效的实数编码进化算法，特别适合连续空间的全局优化。它没有遗传算法里复杂的编码解码，核心就是：**用个体之间的差分向量做变异，再交叉、再贪婪选择**。

## 算法在解决什么问题

给定目标函数 \(f(\mathbf{x})\)，在边界框 \(\mathbf{a} \le \mathbf{x} \le \mathbf{b}\) 内找使 \(f\) 最小（或最大）的 \(\mathbf{x}\)。DE 不依赖梯度，因此对不可微、多峰函数更友好，但也不保证全局最优。

## 标准流程（DE/rand/1/bin 思路）

设种群规模 \(N\)，维度 \(D\)，第 \(g\) 代个体 \(\mathbf{x}_{i,g}\)。

1. **初始化**：在边界内均匀随机采样 \(N\) 个个体，计算适应度。  
2. **变异（Mutation）**：对每个目标个体，构造供体向量，经典形式：
   \[
   \mathbf{v}_{i} = \mathbf{x}_{r1} + F \cdot (\mathbf{x}_{r2} - \mathbf{x}_{r3})
   \]
   其中 \(r1,r2,r3\) 互不相同且不等于 \(i\)，\(F\) 为缩放因子（常用 0.5–0.9）。也有 `best` 变种用当前最优代替 \(x_{r1}\)。  
3. **交叉（Crossover）**：以概率 \(CR\) 从 \(\mathbf{v}_i\) 与 \(\mathbf{x}_i\) 组装试验向量 \(\mathbf{u}_i\)，并保证至少一维来自 \(\mathbf{v}_i\)。  
4. **选择（Selection）**：若 \(f(\mathbf{u}_i)\) 优于 \(f(\mathbf{x}_i)\)，则替换。  
5. 重复直到达到迭代上限或收敛阈值。

## 参数直觉

| 参数 | 含义 | 经验 |
|------|------|------|
| \(N\) | 种群大小 | 大致 \(5D\)–\(10D\)，太小易早熟 |
| \(F\) | 差分步长 | 偏大探索强，偏小开发强 |
| \(CR\) | 交叉率 | 高维可略大，问题相关 |
| \(itmax\) | 迭代次数 | 总评价次数约 \(N \times itmax\) |

## MATLAB 示例（六驼峰型函数）

目标（示意）：
\[
f(x_1,x_2)=4x_1^2-2.1x_1^4+x_1^6/3+x_1x_2-4x_2^2+4x_2^4
\]

```matlab
clear; close all; clc

% 目标函数（向量化）
objf = @(x1,x2) 4*x1.^2 - 2.1*x1.^4 + (x1.^6)/3 + x1.*x2 - 4*x2.^2 + 4*x2.^4;

D = 2;
N = 20;          % 种群
itmax = 50;
F = 0.8; CR = 0.5;

% 边界
lo = [-1.9, -1.1];
hi = [ 1.9,  1.1];

% 初始化
x = lo + (hi - lo) .* rand(N, D);
fx = objf(x(:,1), x(:,2));
[fxbest, ib] = min(fx);
xbest = x(ib,:);

for it = 1:itmax
    u = x;
    for i = 1:N
        % 选三个不同下标
        idxs = setdiff(1:N, i);
        r = idxs(randperm(numel(idxs), 3));
        v = x(r(1),:) + F * (x(r(2),:) - x(r(3),:));
        % 边界处理：截断
        v = min(max(v, lo), hi);

        % 二项交叉
        mask = rand(1,D) < CR;
        if ~any(mask), mask(randi(D)) = true; end
        trial = x(i,:);
        trial(mask) = v(mask);

        ft = objf(trial(1), trial(2));
        if ft < fx(i)
            x(i,:) = trial;
            fx(i) = ft;
        end
    end
    [fxbest, ib] = min(fx);
    xbest = x(ib,:);
    fprintf('iter %d best=%.6f at [%.4f, %.4f]\n', it, fxbest, xbest(1), xbest(2));
end
```

旧笔记里的 `inline` + 手写置换矩阵也能跑，但可读性差，且 `é` 这类字符是编码损坏的减号，直接复制会报错。上面版本更适合学习与改写。

## 工程注意点

1. **边界**：变异后可能越界，需截断或反弹。  
2. **约束优化**：有约束时要加罚函数或可行化策略。  
3. **随机种子**：写论文请固定 seed，报告多次独立运行统计。  
4. **不要神化**：多峰极难问题时，要和 PSO、CMA-ES 等对比，而不是只贴一个 DE 曲线。  

## 和安全/工程的关系（为什么还留这篇）

DE 本身不是安全主题，但在 **参数调优、模糊测试调度、超参搜索** 里仍能见到进化策略的影子。把它写清楚，是为了让「算法笔记」变成可运行、可解释的条目，而不是一坨乱码 MATLAB。

## 小结

DE 的骨架只有三步：差分变异 → 交叉 → 贪婪选择。把 \(F/CR/N\) 调顺、边界处理做对，就能在很多连续优化问题上得到有竞争力的结果。示例代码请以本文可运行版本为准，旧文中的 OCR/编码损坏片段请丢弃。
