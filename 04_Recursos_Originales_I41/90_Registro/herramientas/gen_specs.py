#!/usr/bin/env python3
"""Genera una spec de ensamblaje por APARIENCIA única a partir de personajes.json.
Cada apariencia lista todas las fuentes (unidad KNU, miembro de equipo, forma, catálogo del mod) que la usan.
uso: gen_specs.py personajes.json out_dir
"""
import sys, json, os, re

P = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
looks = {}


def norm(v):
    return 0 if v in (0, None, "0") else v


def add(spec, fuente):
    key = json.dumps([spec['model'], spec['skin'], spec['hair'], spec['gender'], [norm(x) for x in spec['equip']],
                      spec.get('standard', 'STANDARD'), spec.get('weapon1', ''), spec.get('weapon2', '')])
    if key not in looks:
        looks[key] = dict(spec, fuentes=[])
    looks[key]['fuentes'].append(fuente)


for u in P['unidades_KNU']:
    m = u['model']
    if not isinstance(m, list):
        continue
    add({"model": m[0], "skin": m[1], "hair": m[2], "gender": m[3], "equip": u['equip_efectivo']},
        {"tipo": "unidad_KNU", "KNU": u['KNU'], "nombre": u['nombre'], "linea": u['linea'],
         "model_por_defecto": u.get('model_por_defecto', False)})
for p in P['miembros_equipo']:
    m = p['model']
    add({"model": m[0], "skin": m[1], "hair": m[2], "gender": m[3], "equip": [0] * 7},
        {"tipo": "miembro_equipo_sin_objetos", "indice": p['indice'], "nombre": p['nombre']})
    if any(x not in (0, None) for x in p['equip_inicial']):
        add({"model": m[0], "skin": m[1], "hair": m[2], "gender": m[3], "equip": p['equip_inicial']},
            {"tipo": "miembro_equipo_equipo_inicial", "indice": p['indice'], "nombre": p['nombre']})
for f in P['formas_estado']:
    if f['forma'] == 'STANDARD':
        continue
    add({"model": f['model'], "skin": f['skin'], "hair": f['hair'], "gender": f['gender'], "equip": [0] * 7,
         "standard": f['standard'], "weapon1": f['weapon1'], "weapon2": f['weapon2']},
        {"tipo": "forma_estado", "forma": f['forma'], "linea": f['linea'], "condicion": f['condicion_cercana']})
for n in P['catalogo_mod']:
    m = n['model']
    if not isinstance(m, list) or any(isinstance(x, dict) for x in m) or any(isinstance(x, dict) for x in n['equip']):
        continue
    add({"model": m[0], "skin": m[1], "hair": m[2], "gender": m[3], "equip": n['equip']},
        {"tipo": "catalogo_mod", "indice": n['indice'], "nombre": n['nombre'], "linea": n['linea']})

index = []
for i, (k, s) in enumerate(sorted(looks.items(), key=lambda kv: kv[1]['fuentes'][0].get('nombre', kv[1]['fuentes'][0].get('forma', '')))):
    first = s['fuentes'][0]
    nm = first.get('nombre') or first.get('forma')
    slug = re.sub(r'[^A-Za-z0-9]+', '_', nm).strip('_')
    s['name'] = 'AP%03d_%s' % (i + 1, slug)
    s['nombres'] = sorted({f.get('nombre') or f.get('forma') for f in s['fuentes']})
    json.dump(s, open(os.path.join(out, s['name'] + '.json'), 'w'), indent=1, ensure_ascii=False)
    index.append({"apariencia": s['name'], "nombres": s['nombres'], "fuentes": s['fuentes'],
                  "model": s['model'], "skin": s['skin'], "hair": s['hair'], "gender": s['gender'],
                  "equip": s['equip'], "standard": s.get('standard', 'STANDARD')})
json.dump(index, open(os.path.join(out, '_indice_apariencias.json'), 'w'), indent=1, ensure_ascii=False)
print(len(index), 'apariencias unicas')
