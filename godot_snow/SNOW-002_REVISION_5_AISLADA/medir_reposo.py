#!/usr/bin/env python3
"""Mide en coordenadas del SLOT (unidades SWF; origen = origen del slot player<n>) la caja real del
personaje vestido en reposo ('stand', todos sus fotogramas) y su punto de apoyo.

Regla del juego (evidencia): BATTLESCREEN["player"+id].attachMovie(model,"inner",0) -> el MODEL queda en el
origen del slot con matriz identidad (MODEL5: _xscale/_yscale *0.8 y _y += 10, frame_217/DoAction.as l.19-24).
La caja F1 de la revisión 4 es el MODEL1 crudo 'inner2' del marcador 2503 en (-9,-4), que se autodescarga.

Mide con el rig (misma semántica que la escena Godot) a escala alta y umbral de alfa 128:
  - caja del cuerpo sin sombra (min/max sobre todos los fotogramas de stand y por fotograma)
  - apoyo: y más baja del cuerpo (pies) y centro x de los pies en esa franja
  - sombra: centro y tamaño de 'shadower'
uso: medir_reposo.py out.json escena_dir:etiqueta:modelo ...
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from rig import Rig
import numpy as np

out = sys.argv[1]
S = 8.0
OX, OY = 800, 900
res = {}
for arg in sys.argv[2:]:
    d, label, model = arg.split(':')
    R = Rig(d)
    st = R.anims['stand']
    fx = (0.8, 0.8, 0.0, 10.0) if model == 'MODEL5' else (1.0, 1.0, 0.0, 0.0)
    per = []
    for i in range(st['n']):
        p, m = R.pose('stand', i)
        # transform del contenedor 'inner' (solo MODEL5 lo cambia)
        for k in p:
            a, b, c, dd, x, y = p[k]
            p[k] = [a * fx[0], b * fx[1], c * fx[0], dd * fx[1], x * fx[0] + fx[2], y * fx[1] + fx[3]]
        body = R.render(p, m, size=(1600, 1400), origin=(OX, OY), scale=S, skip=('shadower',))
        A = np.array(body.getchannel('A')) > 127
        ys, xs = np.nonzero(A)
        if not len(ys):
            continue
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        band = A[max(y1 - 2 * int(S), 0):y1 + 1]          # 2 u SWF por encima del punto más bajo
        fxs = np.nonzero(band.any(axis=0))[0]
        sh = None
        if 'shadower' in p:
            only = R.render({'shadower': p['shadower']}, None, size=(1600, 1400), origin=(OX, OY), scale=S)
            sa = np.array(only.getchannel('A')) > 40
            sy, sx = np.nonzero(sa)
            if len(sy):
                sh = [round((sx.min() - OX) / S, 2), round((sy.min() - OY) / S, 2), round((sx.max() - OX) / S, 2), round((sy.max() - OY) / S, 2)]
        per.append({"f": i + 1, "xMin": round((x0 - OX) / S, 2), "xMax": round((x1 - OX) / S, 2),
                    "yMin": round((y0 - OY) / S, 2), "yMax_pies": round((y1 - OY) / S, 2),
                    "pies_x": [round((fxs.min() - OX) / S, 2), round((fxs.max() - OX) / S, 2)], "sombra": sh})
    ag = {"xMin": min(q['xMin'] for q in per), "xMax": max(q['xMax'] for q in per),
          "yMin": min(q['yMin'] for q in per), "yMax_pies": max(q['yMax_pies'] for q in per)}
    ag['w'] = round(ag['xMax'] - ag['xMin'], 2); ag['h'] = round(ag['yMax_pies'] - ag['yMin'], 2)
    f1 = per[0]
    res[label] = {"escena": d, "model": model, "contenedor_inner": {"escala": fx[0], "dy": fx[3]},
                  "reposo_f1": f1, "stand_todos": ag,
                  "apoyo_f1": {"y": f1['yMax_pies'], "x_centro_pies": round(sum(f1['pies_x']) / 2, 2)},
                  "variacion_pies_y_en_stand": [min(q['yMax_pies'] for q in per), max(q['yMax_pies'] for q in per)],
                  "fotogramas": per}
    print(label, model, 'F1 caja', (f1['xMin'], f1['yMin'], f1['xMax'], f1['yMax_pies']), 'apoyo y', f1['yMax_pies'],
          'pies x', f1['pies_x'], 'sombra', f1['sombra'], '| stand min/max pies', res[label]['variacion_pies_y_en_stand'])
json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)
