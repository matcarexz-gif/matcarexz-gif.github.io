#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把生成的 101 张轮播注入 index.html + 更新 JS 懒加载"""
import re

base = '/Users/xiangzhong/Projects/personal-site'
with open(base + '/index.html', encoding='utf-8') as fh:
    idx = fh.read()
with open(base + '/design-cases/carousel_slides.html', encoding='utf-8') as fh:
    slides_html = fh.read().strip()

# 1) 替换 <div class="slides">...</div> 整块
pattern = re.compile(r'<div class="slides">.*?</div>\s*(?=<button class="nav prev")', re.S)
idx2, n = pattern.subn(lambda m: '<div class="slides">\n' + slides_html + '\n</div>\n', idx)
print('slides 块替换次数:', n)

# 2) JS: go() 里懒加载当前+下一张
old_js = """  function go(n) {
    idx = (n + slides.length) % slides.length;
    for (var i = 0; i < slides.length; i++) slides[i].classList.toggle('active', i === idx);
    for (var j = 0; j < dots.length; j++) dots[j].classList.toggle('active', j === idx);
  }"""
new_js = """  function loadImg(slide) {
    var img = slide.querySelector('img');
    var src = slide.getAttribute('data-src');
    if (!img.getAttribute('src') && src) img.setAttribute('src', src);
  }
  function go(n) {
    idx = (n + slides.length) % slides.length;
    for (var i = 0; i < slides.length; i++) slides[i].classList.toggle('active', i === idx);
    for (var j = 0; j < dots.length; j++) dots[j].classList.toggle('active', j === idx);
    loadImg(slides[idx]);
    loadImg(slides[(idx + 1) % slides.length]);
  }"""
if old_js in idx2:
    idx2 = idx2.replace(old_js, new_js)
    print('JS 懒加载已注入')
else:
    print('⚠️ 未找到 JS 锚点')

# 3) 初始预加载前两张
old_init = "  restart();\n})();"
new_init = "  loadImg(slides[0]); loadImg(slides[1]);\n  restart();\n})();"
if old_init in idx2:
    idx2 = idx2.replace(old_init, new_init)
    print('JS 初始预加载已注入')
else:
    print('⚠️ 未找到 init 锚点')

with open(base + '/index.html', 'w', encoding='utf-8') as fh:
    fh.write(idx2)
print('index.html 已写入, 大小:', len(idx2))
