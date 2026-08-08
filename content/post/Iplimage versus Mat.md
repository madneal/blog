---
title: "OpenCV：IplImage 与 Mat 该用哪个？"
author: "Neal"
summary: "对比 C-API 的 IplImage 与 C++ API 的 Mat：内存管理、生态现状，以及 cvarrToMat 转换与迁移建议。"
tags: [计算机视觉, OpenCV]
categories: [计算机视觉]
date: "2015-04-15"
lastmod: "2026-08-08"
---


学 OpenCV 时总会撞见两套图像结构：老的 **`IplImage`** 和新的 **`cv::Mat`**。2015 年前后教材还在大量用 IplImage；今天结论已经很明确：**新代码用 Mat**。

## 简史

- `IplImage` 来自 Intel Image Processing Library 风格，是 C-API 核心类型。需要 `cvCreateImage` / `cvReleaseImage` 手动管理。  
- `cv::Mat` 是 C++ API 的矩阵/图像类，**引用计数** 自动释放，支持 ROI、类型系统、与现代 STL 风格算法更好集成。

## 对比

| 维度 | IplImage | Mat |
|------|----------|-----|
| 语言风格 | C | C++ |
| 内存 | 手动 | 自动（引用计数） |
| 新功能 | 基本冻结 | 持续更新 |
| 示例代码 | 老书/老博客 | 官方新文档 |
| 安全性 | 易泄漏/悬挂 | 仍可能误用，但轻松很多 |

## 转换

```cpp
IplImage* ipl = ...;
cv::Mat m = cv::cvarrToMat(ipl); // 共享数据，注意生命周期

// 深拷贝：
cv::Mat m2 = cv::cvarrToMat(ipl).clone();
```

反过来（仅维护老接口时）：

```cpp
IplImage ipl = cvIplImage(mat); // 视 OpenCV 版本 API 略有差异
```

注意：共享数据时，**不要先 release 源再用目标**。

## 迁移建议

1. 新项目直接 `Mat` + `VideoCapture` + `imshow`  
2. 维护老项目时，在边界 `cvarrToMat`，内部别继续扩散 IplImage  
3. OpenCvSharp 用户使用与 `Mat` 对应的类型，避免 `IplImage` 封装  

## 小结

「有的方法只有 IplImage 才有」在早期部分成立，现在几乎不成立。把 IplImage 当作历史兼容层即可；**默认 Mat**。
