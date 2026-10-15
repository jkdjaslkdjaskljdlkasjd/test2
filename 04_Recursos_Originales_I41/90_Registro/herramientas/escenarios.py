#!/usr/bin/env python3
"""Escenarios de I41: capas, posiciones, profundidad y movimiento.

1. pantallas_escenario: para cada etiqueta del escenario principal, lista de capas (profundidad,
   instancia, CharacterID, tipo, linkage, matriz en px, color, filtros, si es añadido HD del mod).
2. fondos_combate: sprites cielo (instancia sin nombre, prof. 73, gotoAndStop(Krin.SkyBG)) y suelo
   (BATTLESCREEN, prof. 89, gotoAndStop(Krin.ZoneBG)); por cada etiqueta: rango de fotogramas
   (animación propia), capas del primer fotograma y, si hay más fotogramas, qué capas se mueven.
3. combates: KBR<n> -> ZoneBG, SkyBG, players, música de jefe (según código).
4. movimiento: referencias de código de cámara/zoom/temblor (GridZoomer, GridShaker, BATTLEBLUR).
uso: escenarios.py inventory.json scripts_dir out_dir
"""
import sys, os, re, json, csv, glob, collections
sys.path.insert(0, os.path.dirname(__file__))
import anim

inv_p, sdir, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
inv = json.load(open(inv_p)); C = inv['characters']
MOD_MIN_ID = 4317  # probable: ids por encima de los 4.316 simbolos del SWF base de PASO1 (heuristica, ver LEEME)


def layer(dp, o):
    ch = o.get('ch'); c = C.get(str(ch), {})
    m = o['matrix']
    nm = o.get('name') or ''
    return {"profundidad": dp, "instancia": nm, "characterId": ch, "tipo": c.get('tag'), "linkage": c.get('exports', [])[:2],
            "x_px": round(m[4] / 20, 2), "y_px": round(m[5] / 20, 2), "a": m[0], "b": m[1], "c": m[2], "d": m[3],
            "color": o.get('cx'), "filtros": [f.get('type') if isinstance(f, dict) else f for f in (o.get('filters') or [])],
            "mascara_hasta": o.get('clipDepth'), "tiene_codigo": o.get('clipActions', False),
            "origen": 'MOD_HD' if (nm.startswith('__hd') or (ch or 0) >= MOD_MIN_ID) else 'original',
            "fotogramas_propios": c.get('frames')}


root = inv['root']
rst = anim.frame_states(root['timeline'], 449)
pantallas = {}
for l in sorted(root['labels'], key=lambda x: x['f']):
    s = rst[l['f'] - 1]
    pantallas[l['label']] = {"fotograma": l['f'], "capas": [layer(dp, o) for dp, o in sorted(s.items())]}


def label_ranges(c):
    ls = sorted(c['labels'], key=lambda x: x['f'])
    out_l = []
    for i, l in enumerate(ls):
        end = (ls[i + 1]['f'] - 1) if i + 1 < len(ls) else c['frames']
        out_l.append((l['label'], l['f'], end))
    return out_l


fondos = {}
for role, sid in (("cielo_SkyBG", 3328), ("suelo_ZoneBG_BATTLESCREEN", 3343)):
    c = C[str(sid)]
    st = anim.frame_states(c['timeline'], c['frames'])
    acts = {}
    for p in glob.glob(os.path.join(sdir, 'DefineSprite_%d*' % sid, 'frame_*', '*.as')):
        f = int(re.search(r'frame_(\d+)', p).group(1)); acts[f] = open(p, encoding='utf-8', errors='replace').read().strip()[:200]
    labs = {}
    for name, a, b in label_ranges(c):
        first = st[a - 1]
        moving = set()
        for f in range(a, b):
            for dp, o in st[f].items():
                if dp not in first or o['matrix'] != first[dp]['matrix'] or o.get('cx') != first[dp].get('cx') or o.get('ch') != first[dp].get('ch'):
                    moving.add(dp)
        labs[name] = {"fotogramas": [a, b], "anima_dentro_del_rango": bool(moving),
                      "capas_que_cambian": sorted(moving),
                      "acciones_en_rango": {f: t for f, t in acts.items() if a <= f <= b},
                      "capas": [layer(dp, o) for dp, o in sorted(first.items())],
                      "render_png": "09_Escenarios/render_fondos/%d_%s_f%d.png" % (sid, name.replace(' ', '_'), a)}
    fondos[role] = {"spriteId": sid, "colocacion_en_combate": [x for x in pantallas['KRINBATTLESCENE']['capas'] if x['characterId'] == sid],
                    "seleccion": "onClipEvent(load){ gotoAndStop(_root.Krin.%s) } (frame_217)" % ('SkyBG' if sid == 3328 else 'ZoneBG'),
                    "etiquetas": labs}

# combates
combates = []
src = os.path.join(sdir, 'frame_42', 'DoAction_2.as')
bid = 0; cur = None
for i, line in enumerate(open(src, encoding='utf-8', errors='replace'), 1):
    m = re.match(r'^battleCreationID = (\d+);', line)
    if m: bid = int(m.group(1))
    if line.strip() == 'createNewBattle();':
        bid += 1; cur = {"combate": "KBR%d" % bid, "linea": i}; combates.append(cur)
    m = re.match(r'^rengi\.(ZoneBG|SkyBG|players|bossFight|bossMusic) = (.*);', line)
    if m and cur: cur[m.group(1)] = m.group(2).strip('"')
# movimiento / cámara
mov = {}
for key in ('GridZoomer', 'GridShaker', 'BATTLEBLUR', 'KrinZoom', 'KrinShake', '__hdBattle'):
    refs = []
    for p in glob.glob(os.path.join(sdir, '**', '*.as'), recursive=True):
        if '__Packages' in p: continue
        for i, line in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
            if key in line:
                refs.append('%s:%d  %s' % (os.path.relpath(p, sdir), i, line.strip()[:140]))
    mov[key] = refs[:40]
json.dump({"pantallas_escenario": pantallas, "fondos_combate": fondos, "combates": combates, "movimiento_codigo": mov,
           "nota": "Coordenadas en px del escenario (800x575). origen=MOD_HD marca capas añadidas por el mod (__hd*), no originales."},
          open(os.path.join(out, 'escenarios.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(out, 'combates.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['combate', 'ZoneBG', 'SkyBG', 'players', 'bossFight', 'bossMusic', 'linea']); w.writeheader()
    for cb in combates: w.writerow({k: cb.get(k, '') for k in w.fieldnames})
with open(os.path.join(out, 'capas_pantallas.csv'), 'w', newline='', encoding='utf-8') as fh:
    keys = ['pantalla', 'fotograma'] + list(layer(1, {"ch": 1, "matrix": [1, 0, 0, 1, 0, 0]}).keys())
    w = csv.DictWriter(fh, fieldnames=keys); w.writeheader()
    for pn, pv in pantallas.items():
        for ly in pv['capas']: w.writerow(dict(ly, pantalla=pn, fotograma=pv['fotograma']))
print('pantallas', len(pantallas), 'combates', len(combates), 'fondos', {k: list(v['etiquetas']) for k, v in fondos.items()})
print({k: (v['anima_dentro_del_rango'], v['fotogramas']) for k, v in fondos['suelo_ZoneBG_BATTLESCREEN']['etiquetas'].items()})
print({k: len(v) for k, v in mov.items()})
