#!/usr/bin/env python3
"""Organiza piezas exportadas por JPEXS en carpetas por linkage y escribe pieza.json con el anclaje.

Anclaje (punto de registro del símbolo = origen donde attachMovie lo coloca dentro del hueso):
  en el SVG: (tx, ty) del grupo raíz -> el origen está en (tx, ty) px desde la esquina superior izquierda.
  en el PNG xZ: JPEXS añade un margen; origen_png = ((Wpng - Wsvg*Z)/2 + tx*Z, (Hpng - Hsvg*Z)/2 + ty*Z).
uso: organizar_piezas.py inventory.json export_dir zoom out_dir grupo:LINKAGE[,LINKAGE...] ...
"""
import sys, os, re, json, glob, shutil
from PIL import Image

inv_p, exp, zoom, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
groups = sys.argv[5:]
C = json.load(open(inv_p))['characters']
by = {n: int(k) for k, c in C.items() for n in c['exports']}


def svg_canvas(p):
    t = open(p, encoding='utf-8').read(2000)
    m = re.search(r'height="([\d.]+)px" width="([\d.]+)px"', t)
    m2 = re.search(r'<g transform="matrix\(1\.0, 0\.0, 0\.0, 1\.0, ([-\d.]+), ([-\d.]+)\)"', t)
    return float(m.group(2)), float(m.group(1)), float(m2.group(1)), float(m2.group(2))


def sprite_dir(kind, cid):
    g = glob.glob(os.path.join(exp, kind, 'DefineSprite_%d' % cid)) + glob.glob(os.path.join(exp, kind, 'DefineSprite_%d_*' % cid))
    return g[0] if g else None


def clos(i, acc):
    acc.append(i)
    for k in C[str(i)].get('children', []) + C[str(i)].get('deps', []):
        if k not in acc:
            clos(k, acc)
    return acc


index = []
for g in groups:
    gname, names = g.split(':', 1)
    for lk in names.split(','):
        cid = by[lk]
        d = os.path.join(out, gname, '%s__chid%d' % (lk, cid))
        os.makedirs(os.path.join(d, 'subelementos'), exist_ok=True)
        meta = {"linkage": lk, "characterId": cid, "tipo": C[str(cid)]['tag'], "grupo": gname,
                "fuente": "SONNY2.swf I41 (SHA-256 6b26ee6d...8812)", "archivos": {}, "subelementos": []}
        sv = sprite_dir('sprite_svg', cid)
        sp = sprite_dir('sprite_png', cid)
        if sv:
            shutil.copy(os.path.join(sv, '1.svg'), os.path.join(d, 'pieza.svg'))
            W, H, tx, ty = svg_canvas(os.path.join(sv, '1.svg'))
            meta['archivos']['svg'] = 'pieza.svg'
            meta['svg_lienzo_px'] = [W, H]
            meta['anclaje_svg_px'] = [tx, ty]
        if sp:
            shutil.copy(os.path.join(sp, '1.png'), os.path.join(d, 'pieza_x%d.png' % zoom))
            pw, ph = Image.open(os.path.join(sp, '1.png')).size
            meta['archivos']['png'] = 'pieza_x%d.png' % zoom
            meta['png_tamano'] = [pw, ph]
            meta['png_escala'] = zoom
            if sv:
                meta['anclaje_png_px'] = [round((pw - W * zoom) / 2 + tx * zoom, 3), round((ph - H * zoom) / 2 + ty * zoom, 3)]
        for k in clos(cid, [])[1:]:
            c = C[str(k)]
            e = {"characterId": k, "tipo": c['tag'], "linkage": c['exports'], "archivos": []}
            for src, kind in ((os.path.join(exp, 'shape_svg', '%d.svg' % k), 'svg'),
                              (os.path.join(exp, 'shape_png', '%d.png' % k), 'png')):
                if os.path.exists(src):
                    dst = os.path.join('subelementos', '%s_%d.%s' % (c['tag'], k, kind))
                    shutil.copy(src, os.path.join(d, dst))
                    e['archivos'].append(dst)
            if c['tag'] == 'DefineSprite':
                for kind, ext in (('sprite_svg', 'svg'), ('sprite_png', 'png')):
                    s2 = sprite_dir(kind, k)
                    if s2:
                        dst = os.path.join('subelementos', 'DefineSprite_%d.%s' % (k, ext))
                        shutil.copy(os.path.join(s2, '1.' + ext), os.path.join(d, dst))
                        e['archivos'].append(dst)
            # colocación dentro de la pieza (matriz, filtros) tal como está en el SWF
            e['colocaciones_en_padre'] = [ev for p in [cid] + clos(cid, [])
                                          for ev in C[str(p)].get('timeline', []) if ev.get('ch') == k]
            meta['subelementos'].append(e)
        meta['lista_visualizacion'] = C[str(cid)].get('timeline', [])
        json.dump(meta, open(os.path.join(d, 'pieza.json'), 'w'), indent=1, ensure_ascii=False)
        index.append(meta)
json.dump(index, open(os.path.join(out, 'indice_piezas.json'), 'w'), indent=1, ensure_ascii=False)
print(len(index), 'piezas')
