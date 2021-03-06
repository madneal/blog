---
title: "Latex--入门系列二"
author: Neal
description: "Latex 专业的参考tex对于论文写作或者其他的一些需要拍版的写作来说，还是非常有意义的。我在网上看到这个对于Latex的入门介绍还是比较全面的，Arbitrary reference .所以将会翻译出来，供初学者学习 
基本的使用TeX会产生什么最基本的来说，你会生成一个.tex文件，即你的文档，即youfile.tex。运行latex you file.tex可以让TeX工作并且生成your"
tags: [latex]
keywords: [latex]
categories: [论文写作]
date: "2016-12-06 20:24:10"
---
Latex 专业的参考

tex对于论文写作或者其他的一些需要拍版的写作来说，还是非常有意义的。我在网上看到这个对于Latex的入门介绍还是比较全面的，[Arbitrary reference ](http://latex.knobs-dials.com).所以将会翻译出来，供初学者学习
基本的使用


## 基本的使用

###  TeX会产生什么

最基本的来说，你会生成一个.tex文件，即你的文档，即`youfile.tex`。

运行`latex you file.tex`可以让TeX工作并且生成`your file.dvi`，这是当下的输出。dvi是一个独立的排版语言。

因为dvi不能够存储图像， 所以它经常被用来作为媒介步骤来产生文档。

dvi也可以被转化成pdf文件，所以pdf文件经常是可以立即生成的，不要dvi文件作为媒介可以直接调用`pdflatex yourfile.tex`。

### 输出文件:

LaTeX运行一次会产生很多文件，其中很多文件产生的原因是因为LaTeX是单流的;很多文件指示文档编译的信息文件，它们也能用于下次运行，当你编译文档的时候你还可以引用它们。比如，图的引用，章节的引用，以及其他文献的引用。鉴于此，它产生的数据是有特定用途的。(`.aux`文件是引用的，`toc`是给章头用的等等)，这些数据下次运行还可以继续使用。

注意这可能是你经常需要运行LaTeX两次来确保引用正常工作从而来更新它们。在一些特别变态的情况下，你甚至要运行更多次。你可以忽略掉这些额外的文件，你可以在生成文档后删除这些文件。

如果你用的是unix的系统，我建议你可以看看[rubber](http://www.pps.jussieu.fr/~beffara/soft/rubber/)。它的目的是为了在必要的时候重新编译文档。它不是特别简单的，但是能给你带来很多便利。

一个`.log`文件也会产生，它是tex文件编译产生的一些相关信息。

注意一点，一旦这个文件生成了，你无需担心保存除了原始数据(.text, .bib)其它的任何数据。log,aux, toc文件可能在运行之后看起来比较混乱，你也可以删掉它们。

### 其他可能输出的格式

除了在unix系统用于xdvi以及打印，dvi格式并不是很有用。上文曾经提到过，通过`dvips`软件可以将dvi文件转化为PostScript。你甚至可以先转成PS,然后再转成pdf文件，或者直接转成pdf文件。但是这些间接的步骤可能只是引发新的问题，在pdf方面经常不会怎么使用。更重要的是，这还会存在一个[字体渲染的问题](http://www.utdallas.edu/~cantrell/online/tex-pdf.html)。对于pdf，我建议你使用`pdflatex`或者类似的工具从而避免字体的一系列问题。你必须将所有的`.ps/.eps`文件转化为pdf，但这不是很困难的事。你可以在图片章节找到更多的细节。