---
title: "利用tesseract-ocr进行验证码识别"
author: Neal
description: "因为爬虫项目需要模拟登陆，可是有一个网站的登录需要输入验证码。其实这种登录有2种解决方案，一种是利用cookie，一种是识别图片。前者需要人工登录一次，而且有时效限制，故不太现实。后者可以，但是难点是如何识别出验证码。 
这里面就要介绍一个神器了，tesseract-ocr这个项目是一个开源项目，可以用于图像识别。不过这个项目现在托管于google，所以不好下载，你可以搜一下，选择在国内下载。 
一"
tags: [验证码识别]
categories: [计算机视觉]
date: "2016-04-26 13:35:29"
---
因为爬虫项目需要模拟登陆，可是有一个网站的登录需要输入验证码。其实这种登录有2种解决方案，一种是利用cookie，一种是识别图片。前者需要人工登录一次，而且有时效限制，故不太现实。后者可以，但是难点是如何识别出验证码。
这里面就要介绍一个神器了，tesseract-ocr这个项目是一个开源项目，可以用于图像识别。不过这个项目现在托管于google，所以不好下载，你可以搜一下，选择在国内下载。http://download.csdn.net/detail/neal1991/9502931
一开始我觉得我的验证码还挺好识别的，因为都是数字，如下图：
![这里写图片描述](http://img.blog.csdn.net/20160426132742951)
但是我发觉直接来识别还是来识别不了的，最好还是先要对图片进行一些预处理。说到图片的预处理就要说到另外一个软件了，就是imagemagick，这个是一个开源的图片处理项目，你可以去http://www.imagemagick.org/script/binary-releases.php根据你自己的系统进行相应得下载。这个软件还有相应的开发api，你可以自行的根据需要去下载。记住，这个软件安装后，配置环境变量后，需要重新启动的，一开始我还以为是什么问题呢。后来发现重新启动之后，就生效了，可以直接在cmd中使用。在这我就不说什么别的了。
首先是对图片进行预处理：

```
convert 1.jpg -colorspace gray -normalize -threshold 50% 1.tif
```
这里主要是先做一个灰度图转化，然后进行归一化处理，最后设立一个阈值，进行二值化，这样最后的结果还是比较清晰的，如下图：![这里写图片描述](http://img.blog.csdn.net/20160426133416350)
然后再用tesseract进行识别：

```
tesseract 1.tif result
```
是不是很简单？
在github上面写了一个nodejs的程序可以直接执行，不过需要安装nodejs,链接如下：
https://github.com/neal1991/code-recognition
