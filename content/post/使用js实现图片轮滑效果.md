---
draft: true
title: "原生 JS 实现图片轮播：结构、样式与交互"
author: "Neal"
summary: "用 HTML/CSS/JS 实现带指示点与左右箭头的轮播：绝对定位叠图、自动播放、悬停暂停，以及无障碍与性能注意点。"
tags: [前端, JavaScript, CSS]
categories: [web前端]
date: "2015-10-21"
lastmod: "2026-08-08"
---


电商首页那种「几秒换一张、可点圆点、可点左右箭头」的效果，叫轮播（carousel）。框架很多，但自己用原生 JS 写一遍，能搞清 **显示层、状态、定时器** 三件事。

## HTML 结构

```html
<div id="flash" class="carousel">
  <ul id="pic" class="slides">
    <li class="is-active"><img src="1.jpg" alt="slide 1"></li>
    <li><img src="2.jpg" alt="slide 2"></li>
    <li><img src="3.jpg" alt="slide 3"></li>
  </ul>
  <ol id="num" class="dots"></ol>
  <button type="button" id="left" class="arrow" aria-label="上一张">‹</button>
  <button type="button" id="right" class="arrow" aria-label="下一张">›</button>
</div>
```

要点：图片用有意义的 `alt`；箭头用 `button` 而不是空链接，对键盘与无障碍更友好。

## CSS 关键

```css
.carousel { position: relative; width: 730px; height: 454px; overflow: hidden; }
.slides li { position: absolute; inset: 0; display: none; }
.slides li.is-active { display: block; }
.dots { position: absolute; left: 50%; bottom: 12px; transform: translateX(-50%); z-index: 2; }
.dots li { display: inline-block; width: 10px; height: 10px; margin: 0 4px; border-radius: 50%; background: #666; cursor: pointer; }
.dots li.is-active { background: #f00; }
.arrow { position: absolute; top: 50%; z-index: 2; transform: translateY(-50%); }
#left { left: 8px; } #right { right: 8px; }
```

所有 slide 叠在同一位置，只显示带 `is-active` 的那一张。也可用 `opacity` + `transition` 做淡入淡出。

## JavaScript 逻辑

```javascript
(function () {
  const slides = [...document.querySelectorAll('#pic li')];
  const dotsBox = document.querySelector('#num');
  let index = 0;
  let timer = null;

  // 生成圆点
  slides.forEach((_, i) => {
    const li = document.createElement('li');
    if (i === 0) li.className = 'is-active';
    li.addEventListener('click', () => go(i));
    dotsBox.appendChild(li);
  });
  const dots = [...dotsBox.children];

  function go(i) {
    slides[index].classList.remove('is-active');
    dots[index].classList.remove('is-active');
    index = (i + slides.length) % slides.length;
    slides[index].classList.add('is-active');
    dots[index].classList.add('is-active');
  }

  document.querySelector('#left').onclick = () => go(index - 1);
  document.querySelector('#right').onclick = () => go(index + 1);

  function play() { timer = setInterval(() => go(index + 1), 3000); }
  function stop() { clearInterval(timer); }
  const root = document.querySelector('#flash');
  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', play);
  play();
})();
```

状态只有一个 `index`；所有 UI 都从 `go` 派生，避免左右箭头与圆点各写一套。

## 常见坑

1. **定时器叠加**：每次 `play` 前先 `clearInterval`。  
2. **图片未统一尺寸**：容器会被撑乱，CSS 里固定高宽并 `object-fit: cover`。  
3. **只有 display 切换无过渡**：要动画需 `opacity` 或位移轨道。  
4. **移动端**：需考虑滑动手势；也可用 `scroll-snap` 做更现代方案。  

## 无障碍与性能

- 自动播放应提供暂停（悬停/按钮）  
- 用户 `prefers-reduced-motion` 时可关闭自动播放  
- 非首屏图 `loading="lazy"`，首图优先  

## 小结

轮播 = **绝对定位叠图 + 当前索引 + 定时器**。原生实现几十行就够理解；上线项目可再换 Swiper 等库，但原理相同。旧笔记里的完整 CSS/JS 可按本文结构重写，比复制一长串无注释代码更易维护。
