#!/usr/bin/env python3
"""Catálogo de apariencias de personajes extraído del código AS2 de I41 (solo lo que el código define).

Fuentes:
  1. Unidades KNU<n> = createNewUnitKrin(nombre,...) + jesivie.model/equipment/skinSetter/voiceHit/voiceDie
     -> apariencia efectiva como en l.2081-2105: equip[0..4]=skinSetter si !=0; resto KRINITEM[equipment].looks
  2. Miembros del equipo Krin.NameSets[i] con SkinSet/HairSet/GSet/equipArray<i> (estado inicial de partida)
  3. Formas de estado: dressChar("FORMA", p_id, standard, model, skin, gender, hair, weapon1, weapon2)
     (rama no STANDARD: cada hueso recibe G_<RANURA>_<standard>)
  4. Catálogo del mod __nzCatalog[n] = {name, model, equip}
uso: personajes.py DoAction_2.as items.json salida.json
"""
import re, sys, json

src, items_p, out = sys.argv[1:4]
L = open(src, encoding='utf-8', errors='replace').read().split('\n')
ITEMS = json.load(open(items_p))


def lit(s):
    """Literal AS2 simple -> python. Resuelve _root["KRINITEM" + n].looks con la tabla de objetos."""
    s = s.strip().rstrip(';')
    s2 = re.sub(r'_root\["KRINITEM"\s*\+\s*(\d+)\]\.looks',
                lambda m: json.dumps({"__item__": int(m.group(1))}), s)
    try:
        v = json.loads(s2)
    except Exception:
        return {"__expr__": s}
    return v


def resolve_items(arr):
    out, prov = [], []
    for x in arr:
        if isinstance(x, dict) and '__item__' in x:
            it = ITEMS.get(str(x['__item__']))
            out.append(it['looks'] if it else None)
            prov.append({"KRINITEM": x['__item__'], "nombre": it['nombre_interno'] if it else None,
                         "looks": it['looks'] if it else None})
        else:
            out.append(x)
            prov.append(None)
    return out, prov


units = []
count = None
cur = None
for i, line in enumerate(L, 1):
    m = re.match(r'^createUnitKrinCount = (\d+);', line)
    if m:
        count = int(m.group(1))
        continue
    m = re.match(r'^createNewUnitKrin\((.*)\);', line)
    if m and count is not None:
        count += 1
        args = [a.strip() for a in m.group(1).split(',')]
        cur = {"fuente": "unidad_KNU", "KNU": count, "nombre": args[0].strip('"'), "args": args, "linea": i,
               "model": ["MODEL1", "ONE", "ONE", "M"], "equipment": [0] * 7, "skinSetter": 0,
               "model_por_defecto": True}
        units.append(cur)
        continue
    m = re.match(r'^jesivie\.(model|equipment|skinSetter|voiceHit|voiceDie|movesA|movesD|movesABS) = (.*);$', line)
    if m and cur is not None:
        cur[m.group(1)] = lit(m.group(2))
        cur.setdefault('lineas', {})[m.group(1)] = i
        if m.group(1) == 'model':
            cur['model_por_defecto'] = False

for u in units:
    eq = [0] * 7
    prov = [None] * 7
    start = 0
    if u['skinSetter'] != 0:
        for t in range(5):
            eq[t] = u['skinSetter']
            prov[t] = {"skinSetter": u['skinSetter']}
        start = 5
    for t in range(start, 7):
        n = u['equipment'][t] if isinstance(u['equipment'], list) and t < len(u['equipment']) else 0
        if n != 0:
            it = ITEMS.get(str(n))
            eq[t] = it['looks'] if it else None
            prov[t] = {"KRINITEM": n, "nombre": it['nombre_interno'] if it else None}
    u['equip_efectivo'] = eq
    u['equip_procedencia'] = prov

# Miembros del equipo (estado inicial)
krin = {}
for i, line in enumerate(L, 1):
    for key in ('NameSets', 'SkinSet', 'HairSet', 'GSet', 'ClassStats'):
        m = re.match(r'^Krin\.%s\[(\d)\] = (.*);$' % key, line)
        if m:
            krin.setdefault(int(m.group(1)), {})[key] = (lit(m.group(2)), i)
    m = re.match(r'^Krin\.equipArray(\d) = (\[.*\]);$', line)
    if m:
        krin.setdefault(int(m.group(1)), {})['equipArray'] = (lit(m.group(2)), i)
    m = re.match(r'^Krin\.(skinArray|hairArray|gArray) = (\[.*\]);$', line)
    if m:
        krin.setdefault('arrays', {})[m.group(1)] = (lit(m.group(2)), i)
arr = krin.pop('arrays')
party = []
for idx in sorted(k for k in krin if isinstance(k, int)):
    d = krin[idx]
    if 'NameSets' not in d or d['NameSets'][0] == 0:
        continue
    sk = d.get('SkinSet', (0, None))[0]
    hr = d.get('HairSet', (0, None))[0]
    g = d.get('GSet', (0, None))[0]
    gender = arr['gArray'][0][g]
    ea = d.get('equipArray', ([0] * 7, None))[0]
    eq, prov = [], []
    for n in ea:
        if n:
            it = ITEMS.get(str(n))
            eq.append(it['looks'] if it else None)
            prov.append({"KRINITEM": n, "nombre": it['nombre_interno'] if it else None})
        else:
            eq.append(0)
            prov.append(None)
    party.append({"fuente": "miembro_equipo", "indice": idx, "nombre": d['NameSets'][0],
                  "model": ["MODEL4" if gender == "F" else "MODEL1", arr['skinArray'][0][sk], arr['hairArray'][0][hr], gender],
                  "ClassStats": d.get('ClassStats', (None,))[0],
                  "equip_inicial": eq, "equip_procedencia": prov,
                  "lineas": {k: v[1] for k, v in d.items()},
                  "nota": "SkinSet/HairSet/GSet por defecto 0 si no se asignan (bucle de inicializacion)."})

# Formas de estado (dressChar no STANDARD)
forms = []
for i, line in enumerate(L, 1):
    m = re.search(r'dressChar\("([^"]+)",p_id,"([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)"\)', line)
    if m:
        ctx = ''
        for j in range(i - 1, max(0, i - 6), -1):
            if 'if' in L[j - 1] or 'case' in L[j - 1]:
                ctx = L[j - 1].strip()
                break
        forms.append({"fuente": "forma_estado_dressChar", "forma": m.group(1), "standard": m.group(2),
                      "model": m.group(3), "skin": m.group(4), "gender": m.group(5), "hair": m.group(6),
                      "weapon1": m.group(7), "weapon2": m.group(8), "linea": i, "condicion_cercana": ctx})

# Catálogo del mod
nz = []
for i, line in enumerate(L, 1):
    m = re.match(r'^\s*_root\.__nzCatalog\[(\d+)\] = \{name:"([^"]*)",model:(\[[^\]]*\]),equip:(\[.*\])\};', line)
    if m:
        model = lit(m.group(3))
        eq, prov = resolve_items(lit(m.group(4)))
        nz.append({"fuente": "catalogo_mod___nzCatalog", "indice": int(m.group(1)), "nombre": m.group(2),
                   "model": model, "equip": eq, "equip_procedencia": prov, "linea": i})

json.dump({"unidades_KNU": units, "miembros_equipo": party, "formas_estado": forms, "catalogo_mod": nz,
           "arrays_apariencia": {k: v[0] for k, v in arr.items()}}, open(out, 'w'), indent=1, ensure_ascii=False)
print('unidades', len(units), 'equipo', len(party), 'formas', len(forms), 'mod', len(nz))
