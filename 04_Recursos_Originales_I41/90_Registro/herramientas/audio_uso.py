#!/usr/bin/env python3
"""Audio de I41: quién usa cada sonido y cuándo suena (solo con evidencia del código/SWF).

Fuentes de evidencia por sonido (linkage):
  - referencias literales "nombre" en los scripts AS2 (archivo:línea + tipo de uso)
  - voces de unidades: jesivie.voiceHit / voiceDie dentro de createNewUnitKrin(...)
  - diálogos de combate: rengi.speeches.push({player, say, voiceOver}) dentro de un combate KBR
  - movimientos: addNewMove(..., "sfx_x") -> nombre del movimiento
  - música: soundPlayArray (rotación) y _music_boss
  - StartSound en líneas de tiempo (sprite/fotograma)
  - flujos de audio en sprites (cinemáticas)
uso: audio_uso.py scripts_dir inventory.json personajes.json flujos.json out_dir
"""
import sys, os, re, json, csv, glob, collections

sdir, inv_p, pers_p, flu_p, out = sys.argv[1:6]
os.makedirs(out, exist_ok=True)
inv = json.load(open(inv_p)); C = inv['characters']
sounds = {n: int(k) for k, c in C.items() if c['tag'] == 'DefineSound' for n in c['exports']}
info = {int(k): c for k, c in C.items() if c['tag'] == 'DefineSound'}
refs = collections.defaultdict(list)
BID0 = 0
SPEECH = {}
for lp in glob.glob(os.path.join(sdir, 'frame_41', '*.as')):
    for line in open(lp, encoding='utf-8', errors='replace'):
        m = re.match(r'^KrinLang\.ENGLISH\.BATTLESPEECH\[(\d+)\] = "(.*)";', line)
        if m: SPEECH[int(m.group(1))] = m.group(2)
files = [p for p in glob.glob(os.path.join(sdir, '**', '*.as'), recursive=True) if '__Packages' not in p]
pat = re.compile(r'"(%s)"' % '|'.join(re.escape(n) for n in sorted(sounds, key=len, reverse=True)))


def kind(line):
    l = line.strip()
    if 'voiceHit' in l: return 'voz_golpe_unidad'
    if 'voiceDie' in l: return 'voz_muerte_unidad'
    if 'voiceOver' in l: return 'voz_dialogo_combate'
    if l.startswith('addNewMove'): return 'sonido_de_movimiento'
    if 'soundPlayArray' in l: return 'lista_musica'
    if 'attachSound' in l: return 'attachSound'
    if 'addSound' in l: return 'addSound'
    if 'soundToMake' in l or 'missToMake' in l: return 'sonido_asignado_en_variable'
    return 'otra_referencia'


# contexto: unidad actual (createNewUnitKrin), combate actual (KBR), movimiento
for p in files:
    rel = os.path.relpath(p, sdir)
    unit = None; battle = None; bid = BID0
    for i, line in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
        mb = re.match(r'^battleCreationID = (\d+);', line)
        if mb: bid = int(mb.group(1))
        if line.strip() == 'createNewBattle();':
            bid += 1; battle = 'KBR%d' % bid
        m = re.match(r'^createNewUnitKrin\("([^"]+)"', line)
        if m: unit = m.group(1)
        m = re.search(r'createNewBattleKrin\(|^rengi = _root\["KBR" \+ ([^\]]+)\]', line)
        for mm in pat.finditer(line):
            n = mm.group(1); k = kind(line)
            r = {"archivo": rel, "linea": i, "uso": k, "texto": line.strip()[:220]}
            if k.startswith('voz_') and k != 'voz_dialogo_combate' and unit:
                r["unidad"] = unit
            if k == 'voz_dialogo_combate':
                pm = re.search(r'player:"([^"]*)"', line); r["personaje"] = pm.group(1) if pm else None
                sm = re.search(r'say:sayBayK\[(\d+)\]', line)
                if sm:
                    r["frase_indice"] = int(sm.group(1)); r["frase_texto"] = SPEECH.get(int(sm.group(1)))
                if battle: r["combate_contexto"] = battle
            if k == 'sonido_de_movimiento':
                mv = re.match(r'\s*addNewMove\("([^"]+)"', line); r["movimiento"] = mv.group(1) if mv else None
            refs[n].append(r)

# StartSound en líneas de tiempo
ss = collections.defaultdict(list)
for k, c in C.items():
    for s in c.get('start_sounds', []) or []:
        ss[s['soundId']].append({"sprite": int(k), "linkage_sprite": c['exports'], "fotograma": s['f']})
for s in inv['root'].get('start_sounds', []):
    ss[s['soundId']].append({"sprite": 0, "linkage_sprite": ["(escenario principal)"], "fotograma": s['f']})

flows = json.load(open(flu_p))
rows = []
for n, sid in sorted(sounds.items(), key=lambda kv: kv[1]):
    c = info[sid]; R = refs.get(n, [])
    usos = collections.Counter(r['uso'] for r in R)
    combates = sorted({r['combate_contexto'] for r in R if r.get('combate_contexto')}, key=lambda x: int(x[3:]))
    quien = sorted({r.get('unidad') or r.get('personaje') or r.get('movimiento') for r in R if (r.get('unidad') or r.get('personaje') or r.get('movimiento'))})
    if n.startswith('_music'):
        cuando = 'musica: ' + ('combate de jefe / progressLevelOn 24,30,36 (addSound Music 2)' if n == '_music_boss' else 'rotacion soundPlayArray (menus con Music 1, combates con Music 2)')
    elif usos.get('voz_golpe_unidad'): cuando = 'al recibir golpe en combate (addSound Effects voiceHit[random(3)])'
    elif usos.get('voz_muerte_unidad'): cuando = 'al morir en combate (addSound Effects voiceDie)'
    elif usos.get('voz_dialogo_combate'): cuando = 'dialogo durante el combate (speeches.voiceOver)'
    elif usos.get('sonido_de_movimiento'): cuando = 'al usar el movimiento (addNewMove, ultimo argumento)'
    elif usos.get('addSound') or usos.get('attachSound'): cuando = 'llamada directa addSound/attachSound (ver referencias)'
    elif ss.get(sid): cuando = 'StartSound en linea de tiempo'
    elif R: cuando = 'referenciado en codigo (ver referencias)'
    else: cuando = 'SIN REFERENCIA ENCONTRADA (posible nombre construido dinamicamente o no usado)'
    rows.append({"characterId": sid, "linkage": n, "formato": c['soundFormat'], "hz": c['soundRate'],
                 "canales": 2 if c['stereo'] else 1, "duracion_s": round(c['sampleCount'] / c['soundRate'], 3),
                 "archivo": '01_Recursos/sonidos/original_mp3/%d_%s.mp3' % (sid, n),
                 "quien": '|'.join(quien)[:400], "cuando": cuando,
                 "usos": '|'.join('%s:%d' % kv for kv in sorted(usos.items())),
                 "combates": '|'.join(combates), "frase": ' / '.join(sorted({r.get('frase_texto') or '' for r in R if r.get('frase_texto')}))[:300], "n_referencias": len(R), "startsound": '|'.join('%d@f%d' % (s['sprite'], s['fotograma']) for s in ss.get(sid, [])),
                 "referencias": R})
# sonidos sin linkage
for sid, c in info.items():
    if not c['exports']:
        rows.append({"characterId": sid, "linkage": "", "formato": c['soundFormat'], "hz": c['soundRate'],
                     "canales": 2 if c['stereo'] else 1, "duracion_s": round(c['sampleCount'] / c['soundRate'], 3),
                     "archivo": '', "quien": "", "combates": "", "frase": "", "cuando": 'StartSound en linea de tiempo' if ss.get(sid) else 'sin linkage ni StartSound',
                     "usos": "", "n_referencias": 0, "startsound": '|'.join('%d@f%d' % (s['sprite'], s['fotograma']) for s in ss.get(sid, [])), "referencias": []})
# flujos de cinemáticas: qué etiqueta del escenario los contiene
root_labels = sorted(inv['root']['labels'], key=lambda l: l['f'])
place = collections.defaultdict(set)
memo = {}


def desc(i):
    if i in memo: return memo[i]
    memo[i] = {i}
    s = {i}
    for k in C.get(str(i), {}).get('children', []): s |= desc(k)
    memo[i] = s; return s


for ev in inv['root']['timeline']:
    if 'ch' in ev:
        lab = None
        for l in root_labels:
            if l['f'] <= ev['f']: lab = l['label']
        for k in desc(ev['ch']): place[k].add(lab)
flow_rows = []
for f in flows:
    flow_rows.append(dict(f, archivo='01_Recursos/sonidos/flujos_en_sprites/' + f['archivo'],
                          etiquetas_escenario=sorted(x for x in place.get(f['spriteId'], []) if x),
                          duracion_s=round(f['bloques'] / 30.0, 2)))
json.dump({"sonidos": rows, "flujos_cinematicas": flow_rows,
           "sistema": {"addSound": "frame_42/DoAction_2.as l.1-90: Effects -> 3 canales my_sound1..3 al 80% de volumen; Music 1/2 -> crossfade entre music1/music2",
                       "lista_musica": "frame_41/DoAction.as l.4522 soundPlayArray (12 entradas, rota)",
                       "musica_jefe": "_music_boss si Krin.bossFight/bossMusic o progressLevelOn 24/30/36"}},
          open(os.path.join(out, 'audio_uso.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(out, 'audio_uso.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=[k for k in rows[0] if k != 'referencias'] + ['primeras_referencias'])
    w.writeheader()
    for r in rows:
        r2 = {k: v for k, v in r.items() if k != 'referencias'}
        r2['primeras_referencias'] = ' ; '.join('%s:%d %s' % (x['archivo'], x['linea'], x['uso']) for x in r['referencias'][:5])
        w.writerow(r2)
cnt = collections.Counter(r['cuando'].split(' (')[0] for r in rows)
print(len(rows), 'sonidos'); [print(' ', v, k) for k, v in cnt.most_common()]
print('flujos', [(f['spriteId'], f['etiquetas_escenario']) for f in flow_rows])
