#!/usr/bin/env python3
"""伪纪实图文连载叠字模板：字幕 + 相机日期水印 + 恐怖预警卡。
用法：改 DATA 区 → python3 overlay_doc_subtitles.py
输入图放 ./pages/（01.png, 02.png, …），输出到 ./out/。
type=warning 的页不生图，直接画警示卡。
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
IN_DIR = 'pages'
OUT_DIR = 'out'
W, H = 1440, 2560  # seedream 9:16 原尺寸

# ---- 每页数据：text=字幕（自动折两行），date=相机水印日期，type 可选 'warning' ----
DATA = [
    {"file": "01.png", "text": "我今年20岁，高中毕业后就没再上学。", "date": "2016.09.20"},
    {"file": "02.png", "text": "那天家里来了一个奇怪的外国人。", "date": "2016.09.20"},
    {"file": None, "type": "warning", "text": "恐怖预警\n前方高能 请谨慎观看"},
]

def font(sz):
    return ImageFont.truetype(FONT, sz, index=2)  # index=2 = 简体SC

def draw_outlined_text(d, xy, text, fnt, fill=(255,255,255), stroke=6, anchor='mm'):
    x, y = xy
    d.text((x, y), text, font=fnt, fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=(0,0,0))

def wrap_two_lines(text, fnt, max_w, d):
    """在标点处折成两行（尽量均衡）。"""
    if d.textlength(text, font=fnt) <= max_w:
        return [text]
    seps = '，。！？；、… '
    best = None
    for i, ch in enumerate(text):
        if ch in seps and 0 < i < len(text)-1:
            a, b = text[:i+1], text[i+1:]
            diff = abs(d.textlength(a, font=fnt) - d.textlength(b, font=fnt))
            if best is None or diff < best[0]:
                best = (diff, a, b)
    if best:
        return [best[1], best[2]]
    # 无标点硬切
    mid = len(text)//2
    return [text[:mid], text[mid:]]

def overlay_subtitle(img, text, date=None):
    d = ImageDraw.Draw(img)
    fnt = font(64)
    max_w = W - 160
    lines = wrap_two_lines(text, fnt, max_w, d)
    if len(lines) == 1:
        ys = [H - 260]
    else:
        ys = [H - 360, H - 260]
    for line, y in zip(lines, ys):
        draw_outlined_text(d, (W//2, y), line, fnt, stroke=7)
    if date:
        df = font(38)
        # 相机时间戳风格：右下角橙红字
        d.text((W-60, H-120), date, font=df, fill=(255,120,40,255),
               anchor='rm', stroke_width=1, stroke_fill=(40,10,0))
    return img

def make_warning_card(text, out_path):
    img = Image.new('RGB', (W, H), (5,5,5))
    d = ImageDraw.Draw(img)
    # 警戒条纹（顶部和底部）
    stripe_h = 90
    for y0 in (140, H-230):
        x = -200
        while x < W+200:
            d.polygon([(x, y0), (x+90, y0), (x+90+stripe_h, y0+stripe_h), (x+stripe_h, y0+stripe_h)],
                      fill=(200,30,20))
            x += 180
    # 红色三角感叹号
    cx, cy, r = W//2, H//2 - 260, 230
    d.polygon([(cx, cy-r), (cx-r, cy+r//1.15+120), (cx+r, cy+r//1.15+120)], fill=(210,30,25))
    tf = font(200)
    d.text((cx, cy+70), "!", font=tf, fill=(255,255,255), anchor='mm')
    # 文案
    lines = text.split('\n')
    f1 = font(110); f2 = font(64)
    draw_outlined_text(d, (W//2, H//2+260), lines[0], f1, fill=(230,40,30), stroke=4)
    if len(lines) > 1:
        draw_outlined_text(d, (W//2, H//2+400), lines[1], f2, fill=(220,220,220), stroke=3)
    img.save(out_path, quality=95)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    n_out = 0
    for i, item in enumerate(DATA, 1):
        out_path = os.path.join(OUT_DIR, f'{i:02d}.jpg')
        if item.get('type') == 'warning':
            make_warning_card(item['text'], out_path)
            print('warning card ->', out_path); n_out += 1; continue
        src = os.path.join(IN_DIR, item['file'])
        img = Image.open(src).convert('RGB')
        if img.size != (W, H):
            img = img.resize((W, H), Image.LANCZOS)
        img = overlay_subtitle(img, item['text'], item.get('date'))
        img.save(out_path, quality=92)
        print('subtitle ->', out_path); n_out += 1
    print(f'done: {n_out} pages -> {OUT_DIR}/')

if __name__ == '__main__':
    main()
