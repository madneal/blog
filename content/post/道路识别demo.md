---
title: "简易车道线检测 Demo：OpenCvSharp 与 C++ OpenCV"
author: "Neal"
summary: "回顾早期车道线检测流水线：降采样、ROI、灰度、高斯、Canny、概率霍夫，并说明角度过滤与工程局限。"
tags: [计算机视觉, OpenCV, C#]
categories: [计算机视觉]
date: "2015-04-15"
lastmod: "2026-08-08"
---


很早以前做道路/车道线相关练习时，先找到一个 **OpenCvSharp** 示例，再改成 C++ OpenCV。流水线经典而粗糙，但足够建立直觉。本文保留思路，并写明局限——它不是生产级自动驾驶感知。

## 经典流水线

```text
读帧 → 缩小/模糊 → 取下半幅 ROI → 灰度
    → Gaussian → Canny → HoughLinesP → 按角度过滤 → 画线
```

| 步骤 | 作用 |
|------|------|
| ROI 裁剪 | 天空无车道，减计算、减误检 |
| Canny | 提边缘 |
| 概率霍夫 | 把边缘点聚成线段 |
| 角度过滤 | 去掉近似水平的噪线（引擎盖、阴影） |

## C++ 伪代码结构

```cpp
while (capture.read(frame)) {
    Mat roi = frame(Rect(0, frame.rows/2, frame.cols, frame.rows/2));
    Mat gray, edges;
    cvtColor(roi, gray, COLOR_BGR2GRAY);
    GaussianBlur(gray, gray, Size(5,5), 0);
    Canny(gray, edges, 50, 200);
    vector<Vec4i> lines;
    HoughLinesP(edges, lines, 1, CV_PI/180, 50, 50, 100);
    for (auto l : lines) {
        double angle = atan2(l[3]-l[1], l[2]-l[0]) * 180 / CV_PI;
        if (fabs(angle) <= 10) continue; // 过滤近水平
        line(roi, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,0,255), 2);
    }
    imshow("lane", frame);
    if (waitKey(30) == 27) break;
}
```

OpenCvSharp 版本 API 不同（`IplImage`/`CvCapture` 偏老），逻辑一致。新代码请优先 `Mat`。

## 参数怎么调

- **Canny 高低阈值**：比值常 1:2 或 1:3；过低噪点爆炸  
- **Hough 阈值与最小线长**：城市车道可加长 `minLineLength`  
- **角度**：水平过滤 10° 只是经验值，弯道/坡道要自适应  

## 明显局限

1. 强依赖边缘，雨夜、强光、磨损标线会挂  
2. 无左右车道建模，只是「画很多红线」  
3. 无时间序列跟踪，帧间抖动大  
4. 老 API（`IplImage`）与现代 OpenCV4 不兼容  

进阶应看：透视变换鸟瞰、滑动窗口拟合、U-Net 分割、或现成开源车道方案。

## 小结

这个 demo 的价值是 **跑通视觉流水线**，不是上街。若你仍在用 OpenCvSharp，建议迁移到 OpenCvSharp4 + `Mat`，并固定输入视频做回归，避免「调参玄学」。
