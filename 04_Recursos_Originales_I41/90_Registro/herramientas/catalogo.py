#!/usr/bin/env python3
"""Catálogo de recursos de I41 -> CSV + JSON.

Por cada CharacterID: tipo de etiqueta, nombres exportados (linkage), límites, fotogramas, etiquetas,
padres/hijos/dependencias, etiquetas del escenario principal desde las que es alcanzable,
clasificación (con la regla que la justifica), uso por apariencias de personaje (según los informes
de ensamblaje generados a partir del código) y todos los archivos exportados que le corresponden.

Clasificación: solo por evidencia (nombre exportado o relación demostrable). Si no hay evidencia:
"sin_clasificar".
uso: catalogo.py inventory.json raiz_entrega render_dir out_dir
"""
import sys, os, re, json, csv, glob, collections

inv_p, root, render_dir, out = sys.argv[1:5]
inv = json.load(open(inv_p))
C = inv['characters']
os.makedirs(out, exist_ok=True)

# ---------- archivos por id ----------
files = collections.defaultdict(list)
pat_id = [
    (r'^01_Recursos/formas/[^/]+/(\d+)\.(svg|png)$', None),
    (r'^01_Recursos/morphs/[^/]+/(\d+)\.(?:start\.|end\.)?(svg|png)$', None),
    (r'^01_Recursos/imagenes/[^/]+/(\d+)\.\w+$', None),
    (r'^01_Recursos/sonidos/[^/]+/(\d+)_.*$', None),
    (r'^01_Recursos/sonidos/flujos_en_sprites/(\d+)_stream.*$', 'flujo_audio_del_sprite'),
    (r'^01_Recursos/fuentes/(\d+)_.*$', None),
    (r'^01_Recursos/textos/[^/]+/(\d+)\.txt$', None),
    (r'^01_Recursos/botones/[^/]+/DefineButton2?_(\d+)(?:_[^/]*)?/.*$', None),
    (r'^01_Recursos/sprites/[^/]+/DefineSprite_(\d+)(?:_[^/]*)?/.*$', None),
    (r'^02_Datos/animaciones_json/sprite_(\d+)(?:_.*)?\.json$', None),
    (r'^03_Codigo/[^/]+/scripts/DefineSprite_(\d+)(?:_[^/]*)?/.*$', None),
    (r'^03_Codigo/[^/]+/scripts/DefineButton2_(\d+)(?:_[^/]*)?/.*$', None),
]
cpat = [(re.compile(p), n) for p, n in pat_id]
for dp, dn, fn in os.walk(root):
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), root)
        for rx, note in cpat:
            m = rx.match(rel)
            if m:
                files[int(m.group(1))].append(rel)
                break


def summarize_files(lst):
    """Agrupa: muchos fotogramas de un sprite -> carpeta + recuento."""
    groups = collections.defaultdict(list)
    for r in lst:
        d = os.path.dirname(r)
        groups[d].append(os.path.basename(r))
    out_l = []
    for d, fs in sorted(groups.items()):
        if len(fs) > 4:
            out_l.append('%s/ (%d archivos)' % (d, len(fs)))
        else:
            out_l += ['%s/%s' % (d, f) for f in sorted(fs)]
    return out_l


# ---------- alcance desde el escenario principal ----------
root_tl = inv['root']
labels = sorted(root_tl['labels'], key=lambda l: l['f'])


def label_at(f):
    cur = None
    for l in labels:
        if l['f'] <= f:
            cur = l['label']
    return cur or '(antes de la 1a etiqueta)'


reach = collections.defaultdict(set)
memo = {}


def desc(i):
    if i in memo:
        return memo[i]
    memo[i] = set()
    s = {i}
    c = C.get(str(i), {})
    for k in c.get('children', []) + c.get('deps', []):
        s |= desc(k)
    memo[i] = s
    return s


for ev in root_tl['timeline']:
    if 'ch' in ev:
        lab = label_at(ev['f'])
        for k in desc(ev['ch']):
            reach[k].add(lab)

# ---------- uso por apariencias ----------
used_by = collections.defaultdict(set)
ap_names = {}
for rp in glob.glob(os.path.join(render_dir, 'AP*', 'informe_ensamblaje.json')):
    r = json.load(open(rp))
    ap = r['spec']['name']
    ap_names[ap] = r['spec'].get('nombres', [])
    for l in r['attachMovie_log']:
        if l.get('existe_en_biblioteca') and l.get('characterId'):
            for k in desc(l['characterId']):
                used_by[k].add(ap)
    used_by[r['model_id_original']].add(ap)

# ---------- clasificación ----------
SLOTS = {'HEAD', 'CHEST', 'ARM', 'HAND', 'LEG2', 'FOOT', 'SHOULDER'}
bone_ph = set()
for k, c in C.items():
    for n in c['exports']:
        if re.match(r'^MODEL\d+$', n):
            for ev in c['timeline']:
                if 'ch' in ev and ev.get('name'):
                    sub = C[str(ev['ch'])]
                    if sub['tag'] == 'DefineSprite' and any(e.get('clipActions') for e in sub['timeline']):
                        bone_ph.add(ev['ch'])


def classify(c):
    for n in c['exports']:
        m = re.match(r'^([MF])_S([A-Z0-9]+?)_(.+)$', n)
        if m and m.group(2) in SLOTS | {'WEAPON', 'SHOULDER'}:
            return 'personaje.pieza_piel', 'linkage %s: genero %s, ranura %s, piel %s (attachMovie G_S<RANURA>_<piel>)' % (n, m.group(1), m.group(2), m.group(3))
        m = re.match(r'^([MF])_([A-Z0-9]+?)_(.+)$', n)
        if m and m.group(2) in SLOTS:
            return 'personaje.pieza_equipo', 'linkage %s: genero %s, ranura %s, set %s (attachMovie G_<RANURA>_<set>)' % (n, m.group(1), m.group(2), m.group(3))
        if m and m.group(2) == 'WEAPON':
            return 'personaje.pieza_arma', 'linkage %s (attachMovie M_WEAPON_<looks>)' % n
        if n.startswith('HAIR_'):
            return 'personaje.pelo', 'linkage %s (attachMovie HAIR_<pelo>)' % n
        if re.match(r'^MODEL\d+$', n):
            return 'personaje.esqueleto_modelo', 'linkage %s (attachMovie(model[0]) en __nzRawDress)' % n
        if n.startswith('BOOM_'):
            return 'efecto.impacto', 'linkage %s (boomType en addNewMove)' % n
        if n.upper().startswith('KRIN.'):
            return 'efecto.proyectil', 'linkage %s (projectileModel)' % n
        if c['tag'] == 'DefineSound':
            if re.match(r'^(hit|dead)_', n):
                return 'sonido.voz_combate', 'linkage %s (voiceHit/voiceDie)' % n
            if re.match(r'^v\d*_', n):
                return 'sonido.voz_dialogo', 'linkage %s (voiceOver de speeches)' % n
            if n.startswith('sfx_') or n.startswith('Click'):
                return 'sonido.efecto', 'linkage %s' % n
            return 'sonido.otro', 'linkage %s' % n
    if c['id'] in bone_ph:
        return 'personaje.hueso_marcador', 'instancia-hueso de un MODEL con marcador que hace unloadMovie(this)'
    if c['tag'] == 'DefineSound':
        return 'sonido.sin_nombre', 'DefineSound sin linkage'
    if c['tag'].startswith('DefineFont'):
        return 'fuente', c['tag']
    if c['tag'] in ('DefineEditText', 'DefineText'):
        return 'interfaz.texto', c['tag']
    if c['tag'] == 'DefineButton2':
        return 'interfaz.boton', c['tag']
    return 'sin_clasificar', ''


rows = []
for k in sorted(C, key=int):
    c = C[k]
    cat, why = classify(c)
    parents = c.get('parents', [])
    # herencia de categoría: subelemento de una pieza de personaje
    if cat == 'sin_clasificar':
        anc = [p for p in parents if p and classify(C[str(p)])[0].startswith('personaje.pieza') or (p and classify(C[str(p)])[0] == 'personaje.pelo')]
        if anc:
            cat, why = 'personaje.subelemento_de_pieza', 'usado dentro de ' + ', '.join('%d %s' % (p, C[str(p)]['exports']) for p in anc[:4])
        elif any(p and C[str(p)]['id'] in bone_ph for p in parents):
            cat, why = 'personaje.marcador_NINJA_descartado', 'contenido de hueso-marcador; el juego lo descarga (unloadMovie) y no se ve'
    b = c.get('bounds')
    rows.append({
        "characterId": int(k), "tipo": c['tag'], "linkage": '|'.join(c['exports']),
        "categoria": cat, "evidencia_categoria": why,
        "ancho_px": round((b[2] - b[0]) / 20, 2) if b else '', "alto_px": round((b[3] - b[1]) / 20, 2) if b else '',
        "fotogramas": c.get('frames', ''), "etiquetas": '|'.join('%d:%s' % (l['f'], l['label']) for l in c.get('labels', [])),
        "hijos": '|'.join(map(str, c.get('children', []))), "dependencias": '|'.join(map(str, c.get('deps', []))),
        "padres": '|'.join(map(str, parents)),
        "etiquetas_escenario_alcanzable": '|'.join(sorted(reach.get(int(k), []))),
        "usado_por_apariencias": '|'.join(sorted(used_by.get(int(k), []))),
        "personajes_con_evidencia": '|'.join(sorted({n for ap in used_by.get(int(k), []) for n in ap_names.get(ap, [])})) or ('DESCONOCIDO' if cat.startswith('personaje.') else ''),
        "sonido": ('%s %dHz %s %d muestras' % (c['soundFormat'], c['soundRate'], 'estereo' if c['stereo'] else 'mono', c['sampleCount'])) if c['tag'] == 'DefineSound' else '',
        "texto_variable": c.get('variableName') or '', "texto_inicial": (c.get('initialText') or '')[:200],
        "fuente": ('%s (%d glifos)' % (c.get('fontName'), c.get('numGlyphs', 0))) if c['tag'].startswith('DefineFont') else '',
        "initaction": bool(c.get('has_initaction')),
        "orden_en_swf": c['tag_index'],
        "archivos": summarize_files(files.get(int(k), [])),
    })

json.dump({"fuente": "SONNY2.swf I41 sha256 6b26ee6d5b1005a15824d10864941cee452072ef1942880aeb65fa6917738812",
           "total": len(rows), "recursos": rows}, open(os.path.join(out, 'catalogo_recursos.json'), 'w'),
          ensure_ascii=False, indent=0)
with open(os.path.join(out, 'catalogo_recursos.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        r2 = dict(r)
        r2['archivos'] = ' ; '.join(r['archivos'])
        w.writerow(r2)
cnt = collections.Counter(r['categoria'] for r in rows)
print(len(rows), dict(cnt))
print('sin archivos:', collections.Counter(r['tipo'] for r in rows if not r['archivos']))
