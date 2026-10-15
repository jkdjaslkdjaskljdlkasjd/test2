#!/usr/bin/env python3
"""Interfaz de I41: botones y textos organizados por pantalla, con estados y comportamiento.

Por botón (DefineButton2): pantallas (etiquetas del escenario principal desde las que es alcanzable),
contenedores (sprite padre y nombre de instancia), estados up/over/down/hit con sus caracteres y archivos,
acciones de botón (on(press)/on(release)...) con resumen de destino (gotoAndPlay/Stop, llamadas a funciones,
variables _root asignadas). Textos (DefineEditText): variable vinculada, texto inicial, pantalla.
uso: interfaz.py inventory.json scripts_dir out_dir
"""
import sys, os, re, json, csv, glob, collections

inv_p, sdir, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
inv = json.load(open(inv_p)); C = inv['characters']
labels = sorted(inv['root']['labels'], key=lambda l: l['f'])


def label_at(f):
    cur = '(antes de etiquetas)'
    for l in labels:
        if l['f'] <= f: cur = l['label']
    return cur


memo = {}


def desc(i):
    if i in memo: return memo[i]
    memo[i] = {i}; s = {i}
    c = C.get(str(i), {})
    for k in c.get('children', []): s |= desc(k)
    memo[i] = s; return s


reach = collections.defaultdict(set)
root_inst = collections.defaultdict(set)
for ev in inv['root']['timeline']:
    if 'ch' in ev:
        lab = label_at(ev['f'])
        for k in desc(ev['ch']): reach[k].add(lab)
    if ev.get('name') and 'ch' in ev:
        root_inst[ev['ch']].add(ev['name'])
# contenedores con nombre de instancia
cont = collections.defaultdict(list)
for k, c in C.items():
    for ev in c.get('timeline', []):
        if 'ch' in ev:
            cont[ev['ch']].append({"padre": int(k), "padre_linkage": c['exports'][:1], "instancia": ev.get('name'), "fotograma": ev['f']})
for ev in inv['root']['timeline']:
    if 'ch' in ev:
        cont[ev['ch']].append({"padre": 0, "padre_linkage": ["(escenario)"], "instancia": ev.get('name'), "fotograma": ev['f'], "etiqueta": label_at(ev['f'])})


def summarize(code):
    s = []
    for m in re.finditer(r'(gotoAndPlay|gotoAndStop|_root\.gotoAndPlay|_root\.gotoAndStop)\(([^)]*)\)', code):
        s.append('%s(%s)' % (m.group(1), m.group(2)))
    for m in re.finditer(r'(_root\.[A-Za-z_][\w\.]*)\s*\(', code):
        s.append('llama ' + m.group(1))
    for m in re.finditer(r'^\s*(_root\.[\w\.\[\]"]+)\s*=', code, re.M):
        s.append('asigna ' + m.group(1))
    for m in re.finditer(r'(getURL|loadMovie|fscommand|addSound)\(([^)]*)\)', code):
        s.append('%s(%s)' % (m.group(1), m.group(2)[:60]))
    out_l = []
    for x in s:
        if x not in out_l: out_l.append(x)
    return out_l[:12]


rows = []
for k, c in sorted(C.items(), key=lambda kv: int(kv[0])):
    if c['tag'] != 'DefineButton2': continue
    bid = int(k)
    states = {'up': [], 'over': [], 'down': [], 'hit': []}
    for r in c.get('records', []):
        for st in states:
            if r.get(st): states[st].append(r['ch'])
    acts = {}
    for p in glob.glob(os.path.join(sdir, 'DefineButton2_%d' % bid, '*.as')) + glob.glob(os.path.join(sdir, 'DefineButton2_%d_*' % bid, '*.as')):
        ev = re.sub(r'^BUTTONCONDACTION ', '', os.path.basename(p)[:-3])
        acts[ev] = open(p, encoding='utf-8', errors='replace').read()
    resumen = sorted({x for a in acts.values() for x in summarize(a)})
    pant = sorted(reach.get(bid, []))
    ct = cont.get(bid, [])
    rows.append({"buttonId": bid, "pantallas": '|'.join(pant) or 'NO ALCANZABLE DESDE EL ESCENARIO (adjuntado por codigo o sin uso)',
                 "instancias": '|'.join(sorted({x['instancia'] for x in ct if x['instancia']})),
                 "contenedores": '|'.join(sorted({'%d%s' % (x['padre'], ('(' + x['padre_linkage'][0] + ')') if x['padre_linkage'] else '') for x in ct}))[:200],
                 "estado_up": '|'.join(map(str, states['up'])), "estado_over": '|'.join(map(str, states['over'])),
                 "estado_down": '|'.join(map(str, states['down'])), "estado_hit": '|'.join(map(str, states['hit'])),
                 "eventos": '|'.join(sorted(acts)), "acciones_resumen": ' ; '.join(resumen)[:400],
                 "archivos_png": '01_Recursos/botones/png_x2/DefineButton2_%d/' % bid,
                 "archivos_svg": '01_Recursos/botones/svg/DefineButton2_%d/' % bid,
                 "codigo": '03_Codigo/scripts_as/scripts/DefineButton2_%d/' % bid if acts else '',
                 "_acciones": acts, "_contenedores": ct})
texts = []
for k, c in sorted(C.items(), key=lambda kv: int(kv[0])):
    if c['tag'] not in ('DefineEditText', 'DefineText'): continue
    ct = cont.get(int(k), [])
    texts.append({"characterId": int(k), "tipo": c['tag'], "variable": c.get('variableName') or '',
                  "texto_inicial": (c.get('initialText') or '')[:160].replace('\n', ' '),
                  "pantallas": '|'.join(sorted(reach.get(int(k), []))),
                  "instancias": '|'.join(sorted({x['instancia'] for x in ct if x['instancia']})),
                  "contenedores": '|'.join(sorted({str(x['padre']) for x in ct}))[:120],
                  "archivo": '01_Recursos/textos/plano/%d.txt' % int(k)})
# índice por pantalla
por_pantalla = collections.defaultdict(lambda: {"botones": [], "textos": []})
for r in rows:
    for p in r['pantallas'].split('|'): por_pantalla[p]['botones'].append(r['buttonId'])
for t in texts:
    for p in (t['pantallas'] or 'NO ALCANZABLE').split('|'): por_pantalla[p]['textos'].append(t['characterId'])
order = {l['label']: l['f'] for l in labels}
json.dump({"botones": rows, "textos": texts,
           "por_pantalla": {k: v for k, v in sorted(por_pantalla.items(), key=lambda kv: order.get(kv[0], 9999))}},
          open(os.path.join(out, 'interfaz.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(out, 'botones.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=[k for k in rows[0] if not k.startswith('_')]); w.writeheader()
    for r in rows: w.writerow({k: v for k, v in r.items() if not k.startswith('_')})
with open(os.path.join(out, 'textos.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(texts[0])); w.writeheader(); [w.writerow(t) for t in texts]
print(len(rows), 'botones;', sum(1 for r in rows if r['pantallas'].startswith('NO')), 'no alcanzables;', len(texts), 'textos')
for p, v in list(json.load(open(os.path.join(out, 'interfaz.json')))['por_pantalla'].items())[:40]:
    print(' ', p, len(v['botones']), 'botones', len(v['textos']), 'textos')
