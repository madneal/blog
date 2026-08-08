---
draft: true
title: "MATLAB：批量 load 后按文件名重命名变量"
author: "Neal"
summary: "多个 .mat 内变量同名时，用脚本按文件名重命名并写回；对比 eval 与动态字段名，并提醒 eval 的风险。"
tags: [MATLAB, 计算机视觉]
categories: [matlab]
date: "2015-09-08"
lastmod: "2026-08-08"
---


做实验常会存一堆 `gds1.mat` … `gdsN.mat`，但每个文件内部变量都叫 `gds`。一次性 `load` 会互相覆盖，所以需要 **按文件名重命名** 再保存或送进后续分析。

## 典型脚本

```matlab
rootname = 'gds';
ext = '.mat';
n = 10;  % 文件个数

for i = 1:n
    varname = sprintf('%s%d', rootname, i);  % gds1
    filename = [varname, ext];               % gds1.mat
    S = load(filename);                      % 结构体，字段是原变量名
    % 假设文件内变量名为 gds
    data = S.gds;
    out.(varname) = data;                    % 动态字段，避免 eval
    save(filename, '-struct', 'tmp', varname); % 见下一种写回方式
end
```

更直白的写回：

```matlab
for i = 1:n
    varname = sprintf('gds%d', i);
    filename = [varname, '.mat'];
    S = load(filename);
    tmp = struct(varname, S.gds);
    save(filename, '-fromStruct', tmp); % 旧版本可用 save(filename, varname) 配合 assign
end
```

兼容旧习惯的 `eval` 写法（**不推荐，但能看懂旧笔记**）：

```matlab
load(filename);                 % 得到 gds
eval([varname '= gds;']);       % gds1 = gds
save(filename, varname);
clear gds
```

## 为什么优先不用 eval

| 方式 | 优点 | 缺点 |
|------|------|------|
| `eval` | 短 | 难调试、有注入感、静态分析失效 |
| `load` 返回 struct | 清晰 | 稍长 |
| `matfile` 对象 | 大文件友好 | API 需熟悉 |

## 批量进工作区一次分析

```matlab
allData = struct();
for i = 1:n
    fn = sprintf('gds%d.mat', i);
    S = load(fn);
    allData.(sprintf('gds%d', i)) = S.gds;
end
```

后续 `allData.gds3` 即可，不必污染一堆全局变量。

## 小结

批量重命名的本质是：**文件名 → 新变量名 → save**。能用 struct 动态字段就别用 `eval`；旧实验脚本可以继续跑，新脚本请写得可维护一些。


## 完整可运行示例

假设目录下有 `gds1.mat` … `gds5.mat`，内部变量均为 `gds`：

```matlab
n = 5;
for i = 1:n
    oldFile = sprintf('gds%d.mat', i);
    S = load(oldFile);
    newName = sprintf('gds%d', i);
    out = struct(newName, S.gds);
    save(oldFile, '-struct', 'out');
    fprintf('rewrote %s variable as %s\n', oldFile, newName);
end
```

若只想在内存里汇总、不改文件：

```matlab
allData = struct();
for i = 1:n
    S = load(sprintf('gds%d.mat', i));
    allData.(sprintf('gds%d', i)) = S.gds;
end
% 使用 allData.gds3 ...
```

## 何时该换存储格式

实验一多，`.mat` 同名变量会反复折磨人。可考虑：

- 每个文件只存 `data` 字段，文件名编码参数  
- 改用 `table` / CSV / HDF5，参数进元数据  
- 小项目用 `containers.Map` 管理  

批处理重命名是权宜之计；**命名规范** 才是长久方案。
