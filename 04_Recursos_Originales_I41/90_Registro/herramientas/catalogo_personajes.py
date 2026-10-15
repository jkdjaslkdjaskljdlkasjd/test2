#!/usr/bin/env python3
"""Catálogo de personajes (apariencias) + láminas.
uso: catalogo_personajes.py render_dir inventory.json out_personajes out_catalogo out_laminas
"""
import sys, os, json, csv, glob, shutil, re, subprocess
from PIL import Image

render, inv_p, outp, outc, outl = sys.argv[1:6]
C = json.load(open(inv_p))['characters']
os.makedirs(outp, exist_ok=True); os.makedirs(outc, exist_ok=True); os.makedirs(outl, exist_ok=True)
rows, full = [], []
for d in sorted(glob.glob(os.path.join(render, 'AP*'))):
    ap = os.path.basename(d)
    rp = os.path.join(d, 'informe_ensamblaje.json')
    if not os.path.exists(rp):
        rows.append({"apariencia": ap, "estado": "ERROR_CONSTRUCCION"}); continue
    r = json.load(open(rp)); s = r['spec']
    model = C[str(r['model_id_original'])]
    labels = {l['f']: l['label'] for l in model['labels']}
    dst = os.path.join(outp, ap); os.makedirs(dst, exist_ok=True)
    shutil.copy(os.path.join(d, ap + '.swf'), os.path.join(dst, ap + '_reconstruccion.swf'))
    shutil.copy(rp, os.path.join(dst, 'informe_ensamblaje.json'))
    poses = []
    pd = glob.glob(os.path.join(d, 'poses_png_x2', '*'))
    if pd:
        os.makedirs(os.path.join(dst, 'poses_png_x2'), exist_ok=True)
        for p in sorted(glob.glob(os.path.join(pd[0], '*.png')), key=lambda x: int(os.path.basename(x)[:-4])):
            f = int(os.path.basename(p)[:-4])
            name = '%03d_%s.png' % (f, labels.get(f, 'f%d' % f))
            shutil.copy(p, os.path.join(dst, 'poses_png_x2', name))
            poses.append(name)
    sv = glob.glob(os.path.join(d, 'f1_svg', '*', '1.svg'))
    if sv:
        shutil.copy(sv[0], os.path.join(dst, 'f001_stand.svg'))
    missing = sorted({l['attachMovie'] for l in r['attachMovie_log'] if 'attachMovie' in l and not l['existe_en_biblioteca']})
    pieces = sorted({(l['attachMovie'], l['characterId']) for l in r['attachMovie_log'] if l.get('existe_en_biblioteca')})
    fuentes = s.get('fuentes', [])
    tipos = sorted({f['tipo'] for f in fuentes})
    if any(t.startswith('unidad') or t.startswith('miembro') or t == 'forma_estado' for t in tipos):
        evid = 'codigo_original'
    else:
        evid = 'solo_catalogo_mod'
    row = {"apariencia": ap, "nombres": '|'.join(s.get('nombres', [])),
           "fuentes": ' ; '.join('%s:%s%s' % (f['tipo'], f.get('nombre') or f.get('forma'),
                                               (' KNU%d' % f['KNU']) if 'KNU' in f else (' idx%d' % f['indice'] if 'indice' in f else '')) for f in fuentes),
           "evidencia": evid, "model": s['model'], "piel": s['skin'], "pelo": s['hair'], "genero": s['gender'],
           "forma_standard": s.get('standard', 'STANDARD'),
           "equip_0cabeza_1torso_2manos_3piernas_4pies_5arma1_6arma2": '|'.join(map(str, s['equip'])),
           "piezas_adjuntadas": '|'.join('%s(%s)' % p for p in pieces),
           "attachMovie_sin_efecto": '|'.join(missing),
           "notas": ' ; '.join(r.get('notas', [])),
           "estado_render": 'OK' if poses else 'SIN_RENDER',
           "carpeta": os.path.relpath(dst, os.path.dirname(outp))}
    rows.append(row)
    full.append(dict(row, spec=s, poses=poses, attachMovie_log=r['attachMovie_log'], huesos=r['huesos']))
    # lámina de poses del personaje
    if poses:
        ims = []
        for p in poses:
            im = Image.open(os.path.join(dst, 'poses_png_x2', p)).convert('RGBA')
            ims.append((p, im))
        bb = None
        for _, im in ims:
            b = im.getbbox()
            if b:
                bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
        if bb:
            cw, ch = bb[2] - bb[0], bb[3] - bb[1]
            sheet = Image.new('RGBA', (cw * len(ims), ch + 20), (58, 58, 58, 255))
            from PIL import ImageDraw
            dr = ImageDraw.Draw(sheet)
            for i, (p, im) in enumerate(ims):
                sheet.alpha_composite(im.crop(bb), (i * cw, 20))
                dr.text((i * cw + 3, 3), p[:-4], fill=(255, 255, 255))
            sheet.save(os.path.join(dst, 'lamina_poses.png'))
json.dump(full, open(os.path.join(outc, 'catalogo_personajes.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(outc, 'catalogo_personajes.csv'), 'w', newline='', encoding='utf-8') as f:
    keys = list(rows[0].keys()) if rows else []
    w = csv.DictWriter(f, fieldnames=sorted({k for r in rows for k in r}, key=lambda k: keys.index(k) if k in keys else 99))
    w.writeheader(); [w.writerow(r) for r in rows]
# lámina general: fotograma 1 de cada apariencia
items = []
for r in rows:
    p = os.path.join(outp, r['apariencia'], 'poses_png_x2', '001_stand.png')
    if not os.path.exists(p):
        cand = glob.glob(os.path.join(outp, r['apariencia'], 'poses_png_x2', '001_*.png'))
        p = cand[0] if cand else p
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA'); b = im.getbbox()
        if b:
            cp = '/tmp/claude-0/ap_%s.png' % r['apariencia']
            bg = Image.new('RGBA', (b[2] - b[0], b[3] - b[1]), (58, 58, 58, 255)); bg.alpha_composite(im.crop(b)); bg.save(cp)
            items.append('%s|%s\\n%s' % (cp, r['apariencia'][:5] + ' ' + r['nombres'][:22], r['evidencia']))
for k in range(0, len(items), 48):
    part = items[k:k + 48]
    lst = '/tmp/claude-0/lam_%d.txt' % k
    open(lst, 'w').write('\n'.join(part))
    subprocess.run([sys.executable, '-I', os.path.join(os.path.dirname(__file__), 'lamina.py'),
                    os.path.join(outl, 'personajes_fotograma1_%02d.png' % (k // 48 + 1)),
                    'Apariencias de personaje I41 (%d-%d) - reconstruccion segun codigo, render JPEXS' % (k + 1, k + len(part)),
                    '8', '200', '@' + lst], check=True)
print(len(rows), 'apariencias;', sum(1 for r in rows if r.get('estado_render') == 'OK'), 'con render')
