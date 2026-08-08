#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 projects.json 生成主页全量案例轮播 HTML（懒加载 data-src）"""
import json, os, re, html

BASE = '/Users/xiangzhong/Projects/personal-site'
with open(os.path.join(BASE, 'design-cases/projects.json'), encoding='utf-8') as fh:
    projects = {p['slide']: p for p in json.load(fh)}

fix_title = {
    4: '成都香城五矿·未来公园城', 5: '圆中聚华·眉山彭山项目', 6: '兴锦城投·城市更新项目',
    14: '大商汇·昆明超高层综合体', 17: 'OPPO中心', 19: '奥园·成都天府五街办公',
    69: '新希望·长粼府', 73: '万华·麓湖生态城·玥港', 100: 'OMG办公室（上海）',
    104: '鼎骏置业·住宅项目（BIM）', 105: '云南环球世纪·昆明滇池项目（BIM）',
    106: '武汉龙嘉·商业办公项目（BIM）', 107: '南京名华·综合体项目（BIM）',
    108: '西安传化盛世·项目（BIM）', 109: '广和置业·眉山旅游地产（BIM）',
    110: '万华·高端住宅（BIM）', 111: '蔚蓝卡地亚·五星级酒店（BIM咨询）',
    112: '城投置地·商业酒店（幕墙BIM）',
}
CATS = [
    ('规划与城市设计', [1,2,3,4,5]),
    ('城市更新与改造', [6,8,9,10,11,12]),
    ('商业与综合体', [7,13,14,15,16,17,18,19,22,23,26,27,28,29,32,38,44,64,65,70,77,78,80,88,101]),
    ('产业园区与办公', [31,33,34,35,36,37,39,40,41,42,74,79]),
    ('居住建筑', [51,52,53,55,56,57,58,59,60,61,63,66,67,68,69,71,72,73,75,76,81,82,83,84,85,86,87]),
    ('文旅·酒店·公建', [20,45,46,47,48,49,50]),
    ('景观设计', [97,98]),
    ('幕墙设计', [89,90,91,92,93,94,95,96]),
    ('室内设计', [100,102,103]),
    ('BIM与数字化', [104,105,106,107,108,109,110,111,112]),
]
DIVIDERS = {21, 24, 25, 30, 43, 54, 99}
EXCLUDE = {101, 62, 94, 95}

def year_of(p):
    t = p['fields'].get('设计时间', '')
    m = re.search(r'(19|20)\d{2}', t)
    return int(m.group(0)) if m else 9999

SLIDES_DIR = os.path.join(BASE, 'design-cases/slides')
seen, items = set(), []
for cat, slides in CATS:
    for s in slides:
        if s not in projects or s in DIVIDERS or s in EXCLUDE or s in seen:
            continue
        if not os.path.exists(os.path.join(SLIDES_DIR, f'S{s:03d}.jpg')):
            continue
        seen.add(s)
        title = html.escape(fix_title.get(s, projects[s]['title']))
        items.append((year_of(projects[s]), s, title))
items.sort(key=lambda t: (t[0], t[1]))

lines = []
for i, (_, s, title) in enumerate(items):
    cls = 'slide active' if i == 0 else 'slide'
    lines.append(
        f'<a class="{cls}" href="design-cases/slides/S{s:03d}.jpg" target="_blank" '
        f'data-src="design-cases/slides/S{s:03d}.jpg" data-cap="{title}">'
        f'<img alt="{title}"><div class="cap">{title}</div></a>'
    )

out = '\n'.join(lines)
with open(os.path.join(BASE, 'design-cases/carousel_slides.html'), 'w', encoding='utf-8') as fh:
    fh.write(out)
print(f'生成 {len(items)} 张轮播图 -> design-cases/carousel_slides.html')
