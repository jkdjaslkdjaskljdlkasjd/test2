#!/usr/bin/env python3
"""Compone fotogramas con PIL usando SOLO PNG de piezas + anclaje_png + matrices de la línea de tiempo.
uso: png_compose_check.py inventory.json informe.json export_dir(sprite_png,sprite_svg) jpexs_png_dir jpexs_svg_f1 zoom frames out_dir"""
import sys, os, re, json, glob
sys.path.insert(0, os.path.dirname(__file__))
import anim
from PIL import Image, ImageChops
inv_p, rep_p, exp, jpng, jsvg, zoom, fr, out = sys.argv[1:9]
Z = float(zoom); os.makedirs(out, exist_ok=True)
C = json.load(open(inv_p))['characters']; rep = json.load(open(rep_p))
model = C[str(rep['model_id_original'])]; st = anim.frame_states(model['timeline'], model['frames'])
bone = {d: v['contenido'] for v in rep['huesos'].values() for d in v['profundidades_en_model']}
def canvas(p):
    t = open(p).read(2000)
    m = re.search(r'height="([\d.]+)px" width="([\d.]+)px"', t); m2 = re.search(r'matrix\(1\.0, 0\.0, 0\.0, 1\.0, ([-\d.]+), ([-\d.]+)\)', t)
    return float(m.group(2)), float(m.group(1)), float(m2.group(1)), float(m2.group(2))
def part(cid):
    d = (glob.glob(f'{exp}/sprite_png/DefineSprite_{cid}') + glob.glob(f'{exp}/sprite_png/DefineSprite_{cid}_*'))[0]
    s = (glob.glob(f'{exp}/sprite_svg/DefineSprite_{cid}') + glob.glob(f'{exp}/sprite_svg/DefineSprite_{cid}_*'))[0]
    im = Image.open(d + '/1.png').convert('RGBA'); W, H, tx, ty = canvas(s + '/1.svg')
    return im, ((im.width - W * Z) / 2 + tx * Z, (im.height - H * Z) / 2 + ty * Z)
W, H, OX, OY = canvas(jsvg)
a, b = map(int, fr.split('-')); res = []
for f in range(a, b + 1):
    A = Image.open(f'{jpng}/{f}.png').convert('RGBA'); padx, pady = (A.width - W * Z) / 2, (A.height - H * Z) / 2
    canvas_im = Image.new('RGBA', A.size, (0, 0, 0, 0))
    for d in sorted(st[f - 1]):
        o = st[f - 1][d]; m = o['matrix']
        items = [it['characterId'] for it in sorted(bone[d], key=lambda x: x['profundidad_timeline'])] if d in bone else [o['ch']]
        for cid in items:
            im, (ax, ay) = part(cid)
            # canvas = Z*(Mlin*((u-anc)/Z) + t/20 + O) + pad  => canvas = Mlin*(u-anc) + Z*(t/20+O) + pad
            ex = Z * (m[4] / 20 + OX) + padx; ey = Z * (m[5] / 20 + OY) + pady
            # inversa de x' = a*u + c*v + ex' ...
            aa, bb, cc, dd = m[0], m[1], m[2], m[3]; det = aa * dd - bb * cc
            ia, ib, ic, id_ = dd / det, -bb / det, -cc / det, aa / det
            # u-anc = inv*(x'-e)
            coeffs = (ia, ic, -(ia * ex + ic * ey) + ax, ib, id_, -(ib * ex + id_ * ey) + ay)
            layer = im.transform(A.size, Image.AFFINE, coeffs, resample=Image.BICUBIC)
            if o.get('cx'):
                rm, gm, bm_, am, ra, ga, ba, aa2 = o['cx']
                r, g, bch, al = layer.split()
                layer = Image.merge('RGBA', [r.point(lambda v: max(0, min(255, v * rm / 256 + ra))), g.point(lambda v: max(0, min(255, v * gm / 256 + ga))),
                                             bch.point(lambda v: max(0, min(255, v * bm_ / 256 + ba))), al.point(lambda v: max(0, min(255, v * am / 256 + aa2)))])
            canvas_im.alpha_composite(layer)
    canvas_im.save(f'{out}/png_compuesto_{f:03d}.png')
    aA = A.getchannel('A').point(lambda v: 255 if v > 127 else 0); aB = canvas_im.getchannel('A').point(lambda v: 255 if v > 127 else 0)
    ni = sum(1 for v in ImageChops.multiply(aA, aB).get_flattened_data() if v); nu = sum(1 for v in ImageChops.lighter(aA, aB).get_flattened_data() if v)
    res.append({'frame': f, 'iou_alpha': round(ni / nu, 4)})
json.dump(res, open(f'{out}/comparacion_png.json', 'w'), indent=1)
print('IoU min', min(r['iou_alpha'] for r in res), 'media', round(sum(r['iou_alpha'] for r in res) / len(res), 4))
