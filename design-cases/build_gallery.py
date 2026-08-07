#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成案例画廊页 cases.html：从 projects.json + 分类规则构建"""
import json, re, html

with open('/Users/xiangzhong/Projects/personal-site/design-cases/projects.json', encoding='utf-8') as fh:
    projects = {p['slide']: p for p in json.load(fh)}

# ---- 标题修正 ----
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

# ---- 分类 ----
CATS = [
    ('规划与城市设计', [1,2,3,4,5,6]),
    ('城市更新与改造', [8,9,10,11,12]),
    ('商业与综合体', [7,13,14,15,16,17,18,19,22,23,26,27,28,29,32,38,44,63,64,65,70,77,78,80,88,96,101]),
    ('产业园区与办公', [31,33,34,35,36,37,39,40,41,42,74,79,91,94,95,98]),
    ('居住建筑', [51,52,53,55,56,57,58,59,60,61,62,66,67,68,69,71,72,73,75,76,81,82,83,84,85,86,87]),
    ('文旅·酒店·公建', [20,45,46,47,48,49,50,92,93,97,102]),
    ('幕墙与专项', [89,90]),
    ('室内设计', [100,103]),
    ('BIM与数字化', [104,105,106,107,108,109,110,111,112]),
]
DIVIDERS = {21, 24, 25, 30, 43, 54, 99}

def meta_line(p):
    """生成卡片信息行"""
    f = p['fields']
    bits = []
    addr = f['项目地址'] or ''
    if addr and '省' not in addr and '市' not in addr and addr != '成都市':
        addr = addr
    if addr: bits.append(addr)
    if f['建筑面积']: bits.append(f['建筑面积'])
    elif f['用地面积']: bits.append('用地' + f['用地面积'])
    elif f['规划面积']: bits.append('规划' + f['规划面积'])
    elif f['设计面积']: bits.append(f['设计面积'])
    if f['设计阶段']: bits.append(f['设计阶段'])
    if f['设计时间']: bits.append(f['设计时间'])
    return ' · '.join(bits)

def card_html(p, has_img):
    n = p['slide']
    title = html.escape(fix_title.get(n, p['title']))
    meta = html.escape(meta_line(p))
    if has_img:
        media = f'<img src="design-cases/slides/S{n:03d}.jpg" alt="{title}" loading="lazy">'
    else:
        media = f'<div class="ph" style="background:linear-gradient(135deg,#1e293b,#0f172a)"><b>{title}</b></div>'
    return (f'<a class="pcard" href="design-cases/slides/S{n:03d}.jpg" target="_blank" '
            f'title="{title}">'
            f'{media}'
            f'<div class="pinfo"><b>{title}</b><span>{meta}</span></div></a>')

sections = []
total = 0
import os
SLIDES_DIR = '/Users/xiangzhong/Projects/personal-site/design-cases/slides'
for cat, slides in CATS:
    items = []
    for s in slides:
        if s not in projects or s in DIVIDERS: continue
        has_img = os.path.exists(os.path.join(SLIDES_DIR, f'S{s:03d}.jpg'))
        items.append(card_html(projects[s], has_img))
    if not items: continue
    total += len(items)
    sections.append(f'<section><h2>{cat}<span class="cnt">{len(items)}</span></h2><div class="grid">' + ''.join(items) + '</div></section>')

page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>建筑设计案例 · 向忠</title>
<meta name="description" content="洲宇设计作品集 — 规划、商业、产业园、居住、文旅、BIM 全类型建筑项目案例。">
<style>
  :root {{
    --bg: #0f172a; --bg2: #1e293b; --fg: #e2e8f0; --muted: #94a3b8;
    --accent: #38bdf8; --card: rgba(30,41,59,.6);
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
    background:var(--bg); color:var(--fg); line-height:1.6;
  }}
  .wrap {{ max-width:1060px; margin:0 auto; padding:2.5rem 1.5rem 4rem; }}
  header {{ text-align:center; padding:1rem 0 2rem; }}
  header h1 {{ font-size:1.6rem; }}
  header .sub {{ color:var(--muted); margin-top:.5rem; font-size:.92rem; }}
  .back {{ display:inline-block; margin-top:1rem; color:var(--accent); text-decoration:none; font-size:.88rem; }}
  .back:hover {{ text-decoration:underline; }}
  section {{ margin-top:2.2rem; }}
  h2 {{
    font-size:1.05rem; color:var(--accent); margin-bottom:.9rem;
    display:flex; align-items:center; gap:.5rem;
  }}
  h2::after {{ content:""; flex:1; height:1px; background:rgba(148,163,184,.25); }}
  .cnt {{ background:rgba(56,189,248,.12); border:1px solid rgba(56,189,248,.3);
         border-radius:999px; padding:.05rem .55rem; font-size:.75rem; color:var(--accent); }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:1rem; }}
  .pcard {{
    background:var(--card); border:1px solid rgba(148,163,184,.15); border-radius:12px;
    overflow:hidden; text-decoration:none; color:var(--fg); display:block;
    transition:transform .15s, border-color .15s;
  }}
  .pcard:hover {{ transform:translateY(-3px); border-color:rgba(56,189,248,.5); }}
  .pcard img, .ph {{ width:100%; aspect-ratio:16/11; object-fit:cover; display:block; background:var(--bg2); }}
  .ph {{ display:flex; align-items:center; justify-content:center; color:var(--accent); }}
  .ph b {{ padding: 1rem; text-align:center; font-weight:600; }}
  .pinfo {{ padding:.7rem .9rem .85rem; }}
  .pinfo b {{ display:block; font-size:.92rem; color:#f1f5f9; margin-bottom:.25rem; }}
  .pinfo span {{ color:var(--muted); font-size:.78rem; line-height:1.5; display:block; }}
  footer {{ text-align:center; color:var(--muted); font-size:.8rem; margin-top:3rem; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>建筑设计案例</h1>
    <p class="sub">洲宇设计 · 精选项目作品集（{total} 个案例 · 点击图片查看大图）</p>
    <a class="back" href="index.html">← 返回主页</a>
  </header>
  {''.join(sections)}
  <footer>© 2026 向忠 · Built with GitHub Pages</footer>
</div>
</body>
</html>'''

with open('/Users/xiangzhong/Projects/personal-site/cases.html', 'w', encoding='utf-8') as fh:
    fh.write(page)
print(f'cases.html 生成完成, 共 {total} 个项目')
