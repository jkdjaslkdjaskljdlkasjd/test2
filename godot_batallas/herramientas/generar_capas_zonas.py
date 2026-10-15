#!/usr/bin/env python3
"""Generaliza generar_capas_godot.py (SNOW-001) a los 10 fondos de combate activos, usando las funciones
SIN CAMBIOS de i40/fuente/capas.py (borde, alfa, fundido, relleno_cielo, BORDES, ACTIVOS).

  <ZONA>_sky.png    = imagen completa (como SNOW-001), o con relleno_cielo si la regla es 'poligono' con
                      relleno (JAIL), igual que el build original de I37
  <ZONA>_ground.png = imagen con alfa del borde (RGBA recto, no premultiplicado: igual que SNOW-001)
uso: generar_capas_zonas.py capas.py dir_fondos_hd out_dir
"""
import sys, os, json, importlib.util
import numpy as np
from PIL import Image

capas_p, src, out = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('original_capas', capas_p)
capas = importlib.util.module_from_spec(spec); spec.loader.exec_module(capas)
FILES = {'SEA': 'SEA_Z0.png', 'JAIL': 'JAIL_Z1.png', 'CHURCH': 'CHURCH_Z2_1.png', 'SNOW': 'SNOW_Z2_2.png',
         'TRAIN': 'TRAIN_Z3.png', 'TUNNEL': 'TUNNEL_Z4.png', 'STREETS': 'STREETS_Z5_1.png',
         'STREETS3': 'STREETS3_Z5_2.png', 'STREETS2': 'STREETS2_Z5_3.png', 'ROME': 'ROME_Z6.png'}
os.makedirs(out, exist_ok=True)
res = {}
for z in capas.ACTIVOS:
    im = Image.open(os.path.join(src, FILES[z])).convert('RGB')
    if im.size != (2560, 1440):
        raise ValueError('%s no es 2560x1440' % z)
    sp = capas.BORDES[z]
    b = capas.borde(im, sp)
    a = capas.alfa(b, f=capas.fundido(sp))
    relleno = sp[0] == 'poligono' and len(sp) > 4 and sp[4]
    sky = capas.relleno_cielo(im, b) if relleno else im
    sky.save(os.path.join(out, '%s_sky.png' % z))
    g = im.copy(); g.putalpha(Image.fromarray(a)); g.save(os.path.join(out, '%s_ground.png' % z))
    res[z] = {"fuente": FILES[z], "regla": [x if not isinstance(x, list) else 'poligono(%d puntos)' % len(x) for x in sp],
              "borde_y_min": round(float(b.min()), 2), "borde_y_max": round(float(b.max()), 2),
              "cielo_con_relleno": bool(relleno), "alfa_min": int(a.min()), "alfa_max": int(a.max())}
    print(z, res[z])
json.dump({"mapa_hd_del_mod": {"JAIL|JAIL": "JAIL", "SNOW|SNOW": "SNOW", "CHURCH|CHURCH": "CHURCH", "CHURCH2|CHURCH": "CHURCH",
                               "CHURCH|ROME": "ROME", "STREETS|STREETS": "STREETS", "STREETS|TUNNEL": "STREETS",
                               "STREETS2|STREETS": "STREETS2", "STREETS3|STREETS3": "STREETS3", "TRAIN|TRAIN": "TRAIN",
                               "TUNNEL|TUNNEL": "TUNNEL", "WHITE NOVEMBER|SEA": "SEA"},
           "fuente_mapa": "frame_42/DoAction_2.as l.39048-39059 (_root.__hdBattleMap[ZoneBG|SkyBG])",
           "zonas": res, "SUBIR": capas.SUBIR, "FUNDIDO": capas.FUNDIDO}, open(os.path.join(out, 'capas_zonas.json'), 'w'), indent=1, ensure_ascii=False)
