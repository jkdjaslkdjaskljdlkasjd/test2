#!/usr/bin/env python3
"""Comprobación independiente del ensamblaje.

Compone cada fotograma de un MODEL vestido usando SOLO:
  - el estado de la línea de tiempo extraído (anim.frame_states sobre inventory.json),
  - el informe de ensamblaje (qué pieza va en qué hueso y a qué profundidad),
  - el SVG de cada pieza exportado por JPEXS desde I41 (fotograma 1),
lo rasteriza con Chromium (Skia) y lo compara con el PNG que JPEXS (Java2D) genera del SWF reconstruido.
Si coinciden, los datos exportados (matrices, orden de profundidad, anclajes) bastan para rehacer
el personaje fuera de Flash.

uso: compose_check.py inventory.json informe.json part_svg_dir jpexs_png_dir jpexs_svg_frame1 frames zoom out_dir
"""
import sys, os, re, json, glob, math
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
import anim
from PIL import Image, ImageChops

inv_p, rep_p, svgdir, jpng, jsvg1, frames_s, zoom_s, outdir = sys.argv[1:9]
zoom = float(zoom_s)
HAIRLINE = os.environ.get('HAIRLINE_PX', '1')
a, b = frames_s.split('-')
frames = list(range(int(a), int(b) + 1))
os.makedirs(outdir, exist_ok=True)
C = json.load(open(inv_p))['characters']
rep = json.load(open(rep_p))
model = C[str(rep['model_id_original'])]
states = anim.frame_states(model['timeline'], model['frames'])
bone_by_depth = {}
for inst, v in rep['huesos'].items():
    for d in v['profundidades_en_model']:
        bone_by_depth[d] = v['contenido']
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
ET.register_namespace('ffdec', 'https://www.free-decompiler.com/flash')
NS = '{http://www.w3.org/2000/svg}'


def find_svg(cid):
    c = glob.glob(os.path.join(svgdir, 'DefineSprite_%d/1.svg' % cid)) + \
        glob.glob(os.path.join(svgdir, 'DefineSprite_%d_*/1.svg' % cid)) + \
        glob.glob(os.path.join(svgdir, '%d.svg' % cid))
    return c[0] if c else None


cache = {}
counter = [0]


def part_markup(cid):
    """Devuelve (defs, cuerpo) del SVG de JPEXS con ids prefijados y sin la traslación de lienzo."""
    if cid in cache:
        return cache[cid]
    p = find_svg(cid)
    if not p:
        cache[cid] = None
        return None
    txt = open(p, encoding='utf-8').read()
    counter[0] += 1
    pre = 'p%d_' % counter[0]
    txt = re.sub(r'id="([^"]+)"', lambda m: 'id="%s%s"' % (pre, m.group(1)), txt)
    txt = re.sub(r'url\(#([^)]+)\)', lambda m: 'url(#%s%s)' % (pre, m.group(1)), txt)
    txt = re.sub(r'href="#([^"]+)"', lambda m: 'href="#%s%s"' % (pre, m.group(1)), txt)
    # Trazos finos (ancho original < 1 px): Flash los dibuja como línea de 1 px de pantalla.
    txt = re.sub(r'(<path[^>]*ffdec:has-small-stroke="true"[^>]*?) stroke-width="[^"]*"',
                 lambda m: m.group(1) + ' vector-effect="non-scaling-stroke" stroke-width="%s"' % HAIRLINE, txt)
    root = ET.fromstring(txt.encode('utf-8'))
    defs, body = [], []
    for ch in root:
        if ch.tag == NS + 'defs':
            defs.append(''.join(ET.tostring(x, encoding='unicode') for x in ch))
        elif ch.tag == NS + 'g' and ch.get('transform', '').startswith('matrix(1.0, 0.0, 0.0, 1.0,'):
            body.append(''.join(ET.tostring(x, encoding='unicode') for x in ch))
        else:
            body.append(ET.tostring(ch, encoding='unicode'))
    cache[cid] = (''.join(defs), ''.join(body))
    return cache[cid]


def mstr(m):
    return 'matrix(%r,%r,%r,%r,%r,%r)' % (m[0], m[1], m[2], m[3], m[4] / 20.0, m[5] / 20.0)


def cx_filter(cx, fid):
    rm, gm, bm, am, ra, ga, ba, aa = cx
    vals = [rm / 256, 0, 0, 0, ra / 255, 0, gm / 256, 0, 0, ga / 255, 0, 0, bm / 256, 0, ba / 255,
            0, 0, 0, am / 256, aa / 255]
    return '<filter id="%s" color-interpolation-filters="sRGB" x="-50%%" y="-50%%" width="200%%" height="200%%">' \
           '<feColorMatrix type="matrix" values="%s"/></filter>' % (fid, ' '.join('%.6f' % v for v in vals))


# lienzo de JPEXS para este sprite (traslación del grupo raíz del SVG del fotograma 1)
t = open(jsvg1, encoding='utf-8').read()
m = re.search(r'<svg[^>]*height="([\d.]+)px" width="([\d.]+)px"', t)
H, W = float(m.group(1)), float(m.group(2))
m = re.search(r'<g transform="matrix\(1\.0, 0\.0, 0\.0, 1\.0, ([-\d.]+), ([-\d.]+)\)"', t)
OX, OY = float(m.group(1)), float(m.group(2))

from playwright.sync_api import sync_playwright
results = []
missing = set()
with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={'width': int(math.ceil(W * zoom)) + 400, 'height': int(math.ceil(H * zoom)) + 400})
    for f in frames:
        st = states[f - 1]
        defs, body = [], []
        for d in sorted(st):
            o = st[d]
            if o.get('clipDepth'):
                body.append('<!-- mascara depth %d no aplicada -->' % d)
                missing.add('clipDepth')
                continue
            inner = []
            if d in bone_by_depth:
                for item in sorted(bone_by_depth[d], key=lambda x: x['profundidad_timeline']):
                    pm = part_markup(item['characterId'])
                    if pm is None:
                        missing.add(item['characterId'])
                        continue
                    defs.append(pm[0])
                    inner.append('<g>%s</g>' % pm[1])
            else:
                pm = part_markup(o['ch'])
                if pm is None:
                    missing.add(o['ch'])
                    continue
                defs.append(pm[0])
                inner.append(pm[1])
            attr = ''
            if o.get('cx'):
                fid = 'cx_%d_%d' % (f, d)
                defs.append(cx_filter(o['cx'], fid))
                attr = ' filter="url(#%s)"' % fid
            body.append('<g transform="%s"%s>%s</g>' % (mstr(o['matrix']), attr, ''.join(inner)))
        jp = glob.glob(os.path.join(jpng, '%d.png' % f))[0]
        AW, AH = Image.open(jp).size
        padx, pady = (AW - W * zoom) / 2.0, (AH - H * zoom) / 2.0   # margen que JPEXS añade al PNG
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
               'width="%d" height="%d"><defs>%s</defs><g transform="translate(%f,%f) scale(%f) translate(%f,%f)">%s</g></svg>'
               % (AW, AH, ''.join(defs), padx, pady, zoom, OX, OY, ''.join(body)))
        sp = os.path.join(outdir, 'compuesto_%03d.svg' % f)
        open(sp, 'w', encoding='utf-8').write(svg)
        pg.set_content('<html><body style="margin:0;background:transparent">%s</body></html>' % svg)
        el = pg.query_selector('svg')
        pp = os.path.join(outdir, 'compuesto_%03d.png' % f)
        el.screenshot(path=pp, omit_background=True)
        # comparación con JPEXS
        jp = glob.glob(os.path.join(jpng, '%d.png' % f))[0]
        A = Image.open(jp).convert('RGBA')
        B = Image.open(pp).convert('RGBA')
        if B.size != A.size:
            B2 = Image.new('RGBA', A.size)
            B2.paste(B, (0, 0))
            B = B2
        aA = A.getchannel('A').point(lambda v: 255 if v > 127 else 0)
        aB = B.getchannel('A').point(lambda v: 255 if v > 127 else 0)
        inter = ImageChops.multiply(aA, aB)
        union = ImageChops.lighter(aA, aB)
        ni = sum(1 for v in inter.get_flattened_data() if v)
        nu = sum(1 for v in union.get_flattened_data() if v)
        # diferencia de color en píxeles opacos en ambos
        dA = A.convert('RGB')
        dB = B.convert('RGB')
        diff = ImageChops.difference(dA, dB)
        tot = cnt = big = 0
        for (r, g, bb), mm in zip(diff.get_flattened_data(), inter.get_flattened_data()):
            if mm:
                v = max(r, g, bb)
                tot += v
                cnt += 1
                big += v > 40
        res = {"frame": f, "iou_alpha": round(ni / nu, 4) if nu else None,
               "dif_media_color_0_255": round(tot / cnt, 2) if cnt else None,
               "pct_pix_dif_mayor_40": round(100 * big / cnt, 2) if cnt else None,
               "bbox_jpexs": A.getbbox(), "bbox_compuesto": B.getbbox()}
        results.append(res)
        # imagen de diferencias
        vis = Image.new('RGB', A.size, (255, 255, 255))
        vis.paste((255, 0, 0), mask=ImageChops.subtract(aA, aB))
        vis.paste((0, 0, 255), mask=ImageChops.subtract(aB, aA))
        vis.save(os.path.join(outdir, 'dif_alpha_%03d.png' % f))
    br.close()
json.dump({"frames": results, "faltantes": sorted(map(str, missing)), "lienzo_px": [W, H, OX, OY],
           "zoom": zoom}, open(os.path.join(outdir, 'comparacion.json'), 'w'), indent=1)
ious = [r['iou_alpha'] for r in results if r['iou_alpha'] is not None]
print('frames', len(results), 'IoU min %.4f media %.4f' % (min(ious), sum(ious) / len(ious)),
      'dif color media max', max(r['dif_media_color_0_255'] for r in results), 'faltantes', missing)
