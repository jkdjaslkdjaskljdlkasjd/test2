#!/usr/bin/env python3
"""Lámina (contact sheet) de PNGs con rótulos.
uso: lamina.py salida.png titulo cols celda "ruta|rótulo" ...
   o: lamina.py salida.png titulo cols celda @lista.txt  (una entrada "ruta|rótulo" por línea)
Fondo a cuadros para ver la transparencia. No altera las imágenes: solo las reduce para encajar.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

out, title, cols, cell = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
items = sys.argv[5:]
if len(items) == 1 and items[0].startswith('@'):
    items = [l.rstrip('\n') for l in open(items[0][1:]) if l.strip()]
entries = [i.split('|', 1) if '|' in i else (i, i.split('/')[-1]) for i in items]
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    tfont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
except Exception:
    font = tfont = ImageFont.load_default()
lab_h = 34
rows = (len(entries) + cols - 1) // cols
W, H = cols * cell, rows * (cell + lab_h) + 36
sheet = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(sheet)
d.text((8, 8), title, fill=(0, 0, 0), font=tfont)


def checker(w, h, s=8):
    im = Image.new('RGB', (w, h), (235, 235, 235))
    dd = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if (x // s + y // s) % 2:
                dd.rectangle([x, y, x + s - 1, y + s - 1], fill=(205, 205, 205))
    return im


for n, (path, label) in enumerate(entries):
    r, c = divmod(n, cols)
    x0, y0 = c * cell, 36 + r * (cell + lab_h)
    bg = checker(cell - 6, cell - 6)
    try:
        im = Image.open(path).convert('RGBA')
        im.thumbnail((cell - 10, cell - 10), Image.LANCZOS)
        bg.paste(im, ((bg.width - im.width) // 2, (bg.height - im.height) // 2), im)
    except Exception as e:
        ImageDraw.Draw(bg).text((4, 4), 'ERROR\n' + str(e)[:60], fill=(200, 0, 0), font=font)
    sheet.paste(bg, (x0 + 3, y0 + 3))
    lines = label.split('\\n')
    for i, ln in enumerate(lines[:2]):
        d.text((x0 + 4, y0 + cell + 1 + i * 15), ln[:int(cell / 7.2)], fill=(0, 0, 0), font=font)
sheet.save(out)
print(out, sheet.size)
