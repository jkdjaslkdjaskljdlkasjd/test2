#!/usr/bin/env python3
"""Exporta la animación de uno o varios sprites a JSON legible para reconstrucción (p. ej. Godot).

Por sprite:
  id, linkage (nombres exportados), frames, fps, etiquetas,
  acciones_por_fotograma (rutas a los .as exportados por JPEXS si existen),
  sonidos_por_fotograma (StartSound),
  eventos (crudos, tal como están en el SWF),
  fotogramas[f] = lista ordenada por profundidad de
     {depth, instancia, characterId, linkage, tipo, matriz{a,b,c,d,tx_px,ty_px}, color[rm..aa]|null,
      ratio, clipDepth, filtros, blend, colocado_en}
Unidades: tx/ty en píxeles SWF (twips/20). a,b,c,d como en Flash: x'=a*x+c*y+tx ; y'=b*x+d*y+ty.

uso: export_timeline.py inventory.json scripts_dir out_dir ID [ID...] | all_sprites
"""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(__file__))
import anim

inv_p, scripts_dir, out_dir = sys.argv[1:4]
ids = sys.argv[4:]
inv = json.load(open(inv_p))
C = inv['characters']
os.makedirs(out_dir, exist_ok=True)
if ids == ['all_sprites']:
    ids = [k for k, c in C.items() if c['tag'] == 'DefineSprite']
FPS = 30.0


def script_paths(sid):
    c = C[str(sid)]
    d = glob.glob(os.path.join(scripts_dir, 'DefineSprite_%s' % sid)) + \
        glob.glob(os.path.join(scripts_dir, 'DefineSprite_%s_*' % sid))
    res = {}
    for dd in d:
        for p in glob.glob(os.path.join(dd, 'frame_*', '*.as')):
            f = int(os.path.basename(os.path.dirname(p)).split('_')[1])
            res.setdefault(f, []).append(os.path.relpath(p, scripts_dir))
    return {str(k): sorted(v) for k, v in sorted(res.items())}


def mtx(m):
    return {"a": m[0], "b": m[1], "c": m[2], "d": m[3], "tx_px": m[4] / 20.0, "ty_px": m[5] / 20.0}


summary = []
for sid in ids:
    c = C[str(sid)]
    if c['tag'] != 'DefineSprite':
        continue
    st = anim.frame_states(c['timeline'], c['frames'])
    frames = []
    for i, s in enumerate(st):
        lst = []
        for d in sorted(s):
            o = s[d]
            ch = o.get('ch')
            cc = C.get(str(ch), {})
            lst.append({"depth": d, "instancia": o.get('name'), "characterId": ch,
                        "linkage": cc.get('exports', []), "tipo": cc.get('tag'),
                        "matriz": mtx(o['matrix']), "color": o.get('cx'), "ratio": o.get('ratio'),
                        "clipDepth": o.get('clipDepth'), "filtros": o.get('filters'), "blend": o.get('blend'),
                        "clipActions": o.get('clipActions', False), "colocado_en": o.get('placed_f')})
        frames.append({"f": i + 1, "objetos": lst})
    data = {"id": int(sid), "linkage": c['exports'], "frames": c['frames'], "fps": FPS,
            "etiquetas": c.get('labels', []), "acciones_por_fotograma": script_paths(sid),
            "sonidos_por_fotograma": c.get('start_sounds', []), "eventos_crudos": c['timeline'],
            "fotogramas": frames}
    name = 'sprite_%s%s.json' % (sid, ('_' + c['exports'][0]) if c['exports'] else '')
    json.dump(data, open(os.path.join(out_dir, name), 'w'), ensure_ascii=False, separators=(',', ':'))
    summary.append(name)
print(len(summary), 'animaciones exportadas')
