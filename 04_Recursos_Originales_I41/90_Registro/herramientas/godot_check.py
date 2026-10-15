#!/usr/bin/env python3
"""Recompone con semántica Godot (Node2D.transform * Sprite2D(scale=1/Z, offset=-anclaje)) el primer
fotograma de cada animación de datos_animacion.json y lo compara con el render JPEXS del personaje.
uso: godot_check.py escena_dir jpexs_poses_dir jpexs_svg_f1 zoom_jpexs out_dir"""
import sys, os, re, json, glob
from PIL import Image, ImageChops
d_, poses, svg1, zj, out = sys.argv[1:6]
ZJ = float(zj); os.makedirs(out, exist_ok=True)
D = json.load(open(os.path.join(d_, 'datos_animacion.json'))); ZT = D['zoom_texturas']
t = open(svg1).read(2000)
H, W = map(float, re.search(r'height="([\d.]+)px" width="([\d.]+)px"', t).groups())
OX, OY = map(float, re.search(r'matrix\(1\.0, 0\.0, 0\.0, 1\.0, ([-\d.]+), ([-\d.]+)\)', t).groups())
res = []
for an in D['animaciones']:
    f = an['fotogramas_swf'][0]
    A = Image.open(os.path.join(poses, '%d.png' % f)).convert('RGBA')
    padx, pady = (A.width - W * ZJ) / 2, (A.height - H * ZJ) / 2
    can = Image.new('RGBA', A.size, (0, 0, 0, 0))
    for nd, tr in zip(D['nodos'], an['tracks']):
        if not tr['visible'][0]: continue
        a, b, c, dd, ox, oy = tr['transform'][0]
        for sp in sorted(nd['sprites'], key=lambda s: s['z_attach']):
            im = Image.open(os.path.join(d_, 'texturas', sp['textura'])).convert('RGBA')
            ax, ay = sp['anclaje_png']
            # punto en lienzo = ZJ*(M_lin*((u-anc)/ZT) + o + O) + pad
            k = ZJ / ZT
            A2, B2, C2, D2 = a * k, b * k, c * k, dd * k
            ex = ZJ * (ox + OX) + padx; ey = ZJ * (oy + OY) + pady
            det = A2 * D2 - B2 * C2
            ia, ib, ic, idd = D2 / det, -B2 / det, -C2 / det, A2 / det
            coeffs = (ia, ic, -(ia * ex + ic * ey) + ax, ib, idd, -(ib * ex + idd * ey) + ay)
            can.alpha_composite(im.transform(A.size, Image.AFFINE, coeffs, resample=Image.BICUBIC))
    can.save(os.path.join(out, 'godot_%03d_%s.png' % (f, an['nombre'])))
    aA = A.getchannel('A').point(lambda v: 255 if v > 127 else 0); aB = can.getchannel('A').point(lambda v: 255 if v > 127 else 0)
    ni = sum(1 for v in ImageChops.multiply(aA, aB).get_flattened_data() if v); nu = sum(1 for v in ImageChops.lighter(aA, aB).get_flattened_data() if v)
    res.append({"animacion": an['nombre'], "fotograma": f, "iou_alfa": round(ni / nu, 4) if nu else None})
json.dump(res, open(os.path.join(out, 'comparacion_godot_vs_jpexs.json'), 'w'), indent=1)
for r in res: print(r)
