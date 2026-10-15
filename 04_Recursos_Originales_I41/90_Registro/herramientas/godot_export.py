#!/usr/bin/env python3
"""Convierte un personaje reconstruido (MODEL + piezas) a una escena Godot 4 (.tscn) con AnimationPlayer.

- Un Node2D por instancia del MODEL (huesos head, chest, arm1... y la sombra), en el orden de profundidad SWF.
- Dentro de cada hueso, un Sprite2D por pieza adjuntada (piel -1, equipo 0, pelo 2) con su textura PNG xZ,
  centered=false, offset=-anclaje_png y scale=1/Z (así 1 unidad Godot = 1 px SWF).
- Una animación por etiqueta del MODEL: pista 'transform' (Transform2D exacto de la matriz SWF, sin
  descomponer) con interpolación NEAREST a 30 fps, pista 'visible' si el hueso no está en algún fotograma,
  y pista 'modulate' si hay transformación de color (solo multiplicadores; los términos aditivos se
  anotan en el JSON).
- Bucle según el código del MODEL: si el último fotograma de la etiqueta hace gotoAndStop(<misma etiqueta>)
  la animación es LOOP; si salta a otra, se anota en metadata 'siguiente'.
uso: godot_export.py inventory.json informe.json tex_png_dir tex_svg_dir zoom scripts_dir out_dir nombre
"""
import sys, os, re, json, glob, shutil
sys.path.insert(0, os.path.dirname(__file__))
import anim
from PIL import Image

inv_p, rep_p, tpng, tsvg, zoom, sdir, out, nombre = sys.argv[1:9]
Z = float(zoom)
C = json.load(open(inv_p))['characters']
rep = json.load(open(rep_p))
mid = rep['model_id_original']
M = C[str(mid)]
st = anim.frame_states(M['timeline'], M['frames'])
SHARED = os.environ.get('TEX_SHARED')          # carpeta de texturas comun (opcional)
RES_TEX = os.environ.get('RES_TEX')            # ruta res:// de esa carpeta
TEXDIR = SHARED or os.path.join(out, 'texturas')
os.makedirs(TEXDIR, exist_ok=True)
os.makedirs(out, exist_ok=True)


def find(d, cid):
    if not d: return None
    g = glob.glob(os.path.join(d, 'DefineSprite_%d' % cid)) + glob.glob(os.path.join(d, 'DefineSprite_%d_*' % cid))
    return g[0] if g else None


def canvas(svgtext):
    H, W = map(float, re.search(r'height="([\d.]+)px" width="([\d.]+)px"', svgtext).groups())
    tx, ty = map(float, re.search(r'matrix\(1\.0, 0\.0, 0\.0, 1\.0, ([-\d.]+), ([-\d.]+)\)', svgtext).groups())
    return W, H, tx, ty


def anchor(cid):
    """PNG estático (sprite de 1 fotograma o forma) a zoom Z."""
    p = find(tpng, cid); s = find(tsvg, cid)
    if p and s:
        png, svg = os.path.join(p, '1.png'), os.path.join(s, '1.svg')
    else:
        png = os.path.join(os.environ.get('SHAPES_PNG', ''), '%d.png' % cid); svg = os.path.join(os.environ.get('SHAPES_SVG', ''), '%d.svg' % cid)
    im = Image.open(png)
    W, H, tx, ty = canvas(open(svg).read(2000))
    return png, ((im.width - W * Z) / 2 + tx * Z, (im.height - H * Z) / 2 + ty * Z), im.size


ZM = float(os.environ.get('ZM', '4'))


def anchor_multi(cid):
    """Sprite con animación propia: todos sus fotogramas PNG (mismo lienzo) a zoom ZM."""
    p = find(os.environ.get('MULTI_PNG'), cid); s = find(os.environ.get('MULTI_SVG'), cid)
    n = C[str(cid)]['frames']
    files = [os.path.join(p, '%d.png' % k) for k in range(1, n + 1)]
    im = Image.open(files[0])
    W, H, tx, ty = canvas(open(os.path.join(s, '1.svg')).read(2000))
    return files, ((im.width - W * ZM) / 2 + tx * ZM, (im.height - H * ZM) / 2 + ty * ZM)


# instancias del MODEL: profundidad -> nombre / carácter
inst = {}
for ev in M['timeline']:
    if ev.get('name') and 'ch' in ev:
        inst[ev['depth']] = (ev['name'], ev['ch'])
bones = {}
for b, v in rep['huesos'].items():
    for d in v['profundidades_en_model']:
        bones[d] = (b, v['contenido'])
# todas las demás profundidades del MODEL (sombra, capas sin nombre, efectos)
chars_at = {}
names_at = {}
for ev in M['timeline']:
    if 'ch' in ev and ev['depth'] not in bones:
        chars_at.setdefault(ev['depth'], [])
        if ev['ch'] not in chars_at[ev['depth']]: chars_at[ev['depth']].append(ev['ch'])
        if ev.get('name'): names_at[ev['depth']] = ev['name']
used_depths = sorted(set(bones) | set(chars_at))
tex = {}
frames_res = {}
ext_id = 0


def texture(cid, link):
    global ext_id
    if cid in tex: return tex[cid]
    p, anc, size = anchor(cid)
    fn = '%s_%d_x%d.png' % (link or 'chid', cid, int(Z))
    if not os.path.exists(os.path.join(TEXDIR, fn)):
        shutil.copy(p, os.path.join(TEXDIR, fn))
    ext_id += 1
    tex[cid] = {"id": "%d_tex" % ext_id, "file": fn, "anclaje_png": anc, "size": size}
    return tex[cid]


def anim_frames(cid, link):
    global ext_id
    if cid in frames_res: return frames_res[cid]
    files, anc = anchor_multi(cid)
    lst = []
    for k, f in enumerate(files, 1):
        fn = '%s_%d_f%03d_x%d.png' % (link or 'chid', cid, k, int(ZM))
        if not os.path.exists(os.path.join(TEXDIR, fn)):
            shutil.copy(f, os.path.join(TEXDIR, fn))
        ext_id += 1
        lst.append({"id": "%d_tex" % ext_id, "file": fn})
    frames_res[cid] = {"frames": lst, "anclaje_png": anc, "sf_id": "SpriteFrames_%d" % cid}
    return frames_res[cid]


nodes = []  # (nombre, depth, [hijos])
for d in used_depths:
    if d in bones:
        name, cont = bones[d]
        sprites = []
        for it in sorted(cont, key=lambda x: x['profundidad_timeline']):
            t = texture(it['characterId'], it['linkage'])
            sprites.append({"nombre": '%s_%s' % (it['nombre'], it['linkage']), "tex": t, "z": it['profundidad_as2'], "cid": it['characterId'], "tipo": "static", "solo_si_cid": False})
        nodes.append((name, d, sprites))
    else:
        name = names_at.get(d, 'capa_%d' % d)
        kids = []
        for cid in chars_at[d]:
            c = C[str(cid)]
            link = '_'.join(c['exports']) or ('%s_%d' % (c['tag'].replace('Define', ''), cid))
            if c['tag'] == 'DefineSprite' and c['frames'] > 1:
                kids.append({"nombre": 'anim_%d' % cid, "anim": anim_frames(cid, link), "z": 0, "cid": cid, "tipo": "anim", "n": c['frames'], "solo_si_cid": True})
            else:
                kids.append({"nombre": 'grafico_%d' % cid, "tex": texture(cid, link), "z": 0, "cid": cid, "tipo": "static", "solo_si_cid": len(chars_at[d]) > 1})
        nodes.append((name, d, kids))

# animaciones por etiqueta
labels = sorted(M['labels'], key=lambda l: l['f'])
acts = {}
for p in glob.glob(os.path.join(sdir, 'DefineSprite_%d*' % mid, 'frame_*', '*.as')):
    acts[int(re.search(r'frame_(\d+)', p).group(1))] = open(p, encoding='utf-8', errors='replace').read()
anims = []
for i, l in enumerate(labels):
    a = l['f']; nxtf = [x['f'] for x in labels if x['f'] > a]
    b = (min(nxtf) - 1) if nxtf else M['frames']
    last = acts.get(b, '')
    loop = bool(re.search(r'gotoAndStop\("%s"\)' % re.escape(l['label']), last))
    nxt = re.search(r'gotoAndStop\("([^"]+)"\)', last)
    nxt = nxt.group(1) if nxt and not loop else ('(stop)' if 'stop()' in last else ('(removeMovieClip)' if 'removeMovieClip' in last else None))
    snd = {f - a: re.findall(r'addSound\("Effects","([^"]+)"\)', acts[f]) for f in range(a, b + 1) if f in acts and 'addSound' in acts[f]}
    tracks = []
    for name, d, kids_ in nodes:
        kid_tracks = []
        for kd in kids_:
            if not kd['solo_si_cid'] and kd['tipo'] != 'anim':
                continue
            kv, kf = [], []
            for f in range(a, b + 1):
                o = st[f - 1].get(d)
                on = bool(o) and o.get('ch') == kd['cid']
                kv.append(on)
                kf.append(((f - o['placed_f']) % kd['n']) if (on and kd['tipo'] == 'anim') else 0)
            kid_tracks.append({"hijo": kd['nombre'], "visible": kv, "frame": kf if kd['tipo'] == 'anim' else None})
        tf, vis, mod, add, blur = [], [], [], [], []
        for f in range(a, b + 1):
            o = st[f - 1].get(d)
            if o is None:
                vis.append(False); tf.append(None); mod.append(None); blur.append([0.0, 0.0]); continue
            bl = [0.0, 0.0]
            for fl in o.get('filters') or []:
                if isinstance(fl, dict) and fl.get('type') == 'BLURFILTER':
                    bl = [float(fl.get('blurX', 0)), float(fl.get('blurY', 0))]
            blur.append(bl)
            vis.append(True)
            m = o['matrix']
            tf.append([m[0], m[1], m[2], m[3], m[4] / 20.0, m[5] / 20.0])
            cx = o.get('cx')
            mod.append([cx[0] / 256, cx[1] / 256, cx[2] / 256, cx[3] / 256] if cx else [1, 1, 1, 1])
            if cx and any(cx[4:]): add.append({"f": f, "suma": cx[4:]})
        # rellenar huecos de transform con el último conocido
        lastv = next((x for x in tf if x), [1, 0, 0, 1, 0, 0])
        tf2 = []
        for x in tf:
            lastv = x or lastv; tf2.append(lastv)
        tracks.append({"nodo": name, "hijos": kid_tracks, "transform": tf2, "visible": vis, "modulate": mod, "color_aditivo_no_aplicado": add, "desenfoque_swf_px": blur})
    efectos = []
    for f in range(a, b + 1):
        for dpt, o in st[f - 1].items():
            if dpt not in [n[1] for n in nodes]:
                efectos.append({"f": f, "profundidad": dpt, "characterId": o.get('ch'), "x_px": o['matrix'][4] / 20.0, "y_px": o['matrix'][5] / 20.0})
    ef_ids = sorted({e['characterId'] for e in efectos})
    anims.append({"nombre": l['label'], "fotogramas_swf": [a, b], "n": b - a + 1, "loop": loop, "siguiente": nxt,
                  "sonidos_por_fotograma": snd, "tracks": tracks,
                  "efectos_no_incluidos_en_escena": {"characterIds": ef_ids, "fotogramas": sorted({e['f'] for e in efectos}), "primeras_colocaciones": efectos[:3]}})

# ---------- escribir .tscn ----------
FPS = 30.0
lines = []
subs = []
for k, an in enumerate(anims):
    sid = 'Animation_%d' % k
    n = an['n']; length = n / FPS
    times = ', '.join('%.6g' % (j / FPS) for j in range(n))
    trans = ', '.join(['1'] * n)
    tl = ['[sub_resource type="Animation" id="%s"]' % sid, 'resource_name = "%s"' % an['nombre'],
          'length = %.6g' % length, 'loop_mode = %d' % (1 if an['loop'] else 0), 'step = %.6g' % (1 / FPS)]
    ti = 0
    for tr in an['tracks']:
        vals = ', '.join('Transform2D(%r, %r, %r, %r, %r, %r)' % tuple(v) for v in tr['transform'])
        tl += ['tracks/%d/type = "value"' % ti, 'tracks/%d/imported = false' % ti, 'tracks/%d/enabled = true' % ti,
               'tracks/%d/path = NodePath("Modelo/%s:transform")' % (ti, tr['nodo']), 'tracks/%d/interp = 0' % ti,
               'tracks/%d/loop_wrap = true' % ti,
               'tracks/%d/keys = {\n"times": PackedFloat32Array(%s),\n"transitions": PackedFloat32Array(%s),\n"update": 1,\n"values": [%s]\n}' % (ti, times, trans, vals)]
        ti += 1
        if not all(tr['visible']):
            vals = ', '.join('true' if v else 'false' for v in tr['visible'])
            tl += ['tracks/%d/type = "value"' % ti, 'tracks/%d/imported = false' % ti, 'tracks/%d/enabled = true' % ti,
                   'tracks/%d/path = NodePath("Modelo/%s:visible")' % (ti, tr['nodo']), 'tracks/%d/interp = 0' % ti,
                   'tracks/%d/loop_wrap = true' % ti,
                   'tracks/%d/keys = {\n"times": PackedFloat32Array(%s),\n"transitions": PackedFloat32Array(%s),\n"update": 1,\n"values": [%s]\n}' % (ti, times, trans, vals)]
            ti += 1
        if any(v[0] > 0 or v[1] > 0 for v in tr['desenfoque_swf_px']):
            vals = ', '.join('Vector2(%r, %r)' % tuple(v) for v in tr['desenfoque_swf_px'])
            tl += ['tracks/%d/type = "value"' % ti, 'tracks/%d/imported = false' % ti, 'tracks/%d/enabled = true' % ti,
                   'tracks/%d/path = NodePath("Modelo/%s:metadata/desenfoque_swf")' % (ti, tr['nodo']), 'tracks/%d/interp = 0' % ti,
                   'tracks/%d/loop_wrap = true' % ti,
                   'tracks/%d/keys = {\n"times": PackedFloat32Array(%s),\n"transitions": PackedFloat32Array(%s),\n"update": 1,\n"values": [%s]\n}' % (ti, times, trans, vals)]
            ti += 1
        for kt in tr['hijos']:
            if not all(kt['visible']):
                vals = ', '.join('true' if v else 'false' for v in kt['visible'])
                tl += ['tracks/%d/type = "value"' % ti, 'tracks/%d/imported = false' % ti, 'tracks/%d/enabled = true' % ti,
                       'tracks/%d/path = NodePath("Modelo/%s/%s:visible")' % (ti, tr['nodo'], kt['hijo']), 'tracks/%d/interp = 0' % ti,
                       'tracks/%d/loop_wrap = true' % ti,
                       'tracks/%d/keys = {\n"times": PackedFloat32Array(%s),\n"transitions": PackedFloat32Array(%s),\n"update": 1,\n"values": [%s]\n}' % (ti, times, trans, vals)]
                ti += 1
            if kt['frame'] is not None:
                vals = ', '.join(str(v) for v in kt['frame'])
                tl += ['tracks/%d/type = "value"' % ti, 'tracks/%d/imported = false' % ti, 'tracks/%d/enabled = true' % ti,
                       'tracks/%d/path = NodePath("Modelo/%s/%s:frame")' % (ti, tr['nodo'], kt['hijo']), 'tracks/%d/interp = 0' % ti,
                       'tracks/%d/loop_wrap = true' % ti,
                       'tracks/%d/keys = {\n"times": PackedFloat32Array(%s),\n"transitions": PackedFloat32Array(%s),\n"update": 1,\n"values": [%s]\n}' % (ti, times, trans, vals)]
                ti += 1
        if any(m and m != [1, 1, 1, 1] for m in tr['modulate']):
            vals = ', '.join('Color(%r, %r, %r, %r)' % tuple(m or [1, 1, 1, 1]) for m in tr['modulate'])
            tl += ['tracks/%d/type = "value"' % ti, 'tracks/%d/imported = false' % ti, 'tracks/%d/enabled = true' % ti,
                   'tracks/%d/path = NodePath("Modelo/%s:modulate")' % (ti, tr['nodo']), 'tracks/%d/interp = 0' % ti,
                   'tracks/%d/loop_wrap = true' % ti,
                   'tracks/%d/keys = {\n"times": PackedFloat32Array(%s),\n"transitions": PackedFloat32Array(%s),\n"update": 1,\n"values": [%s]\n}' % (ti, times, trans, vals)]
            ti += 1
    subs.append('\n'.join(tl))
lib = '[sub_resource type="AnimationLibrary" id="AnimationLibrary_1"]\n_data = {\n%s\n}' % ',\n'.join(
    '"%s": SubResource("Animation_%d")' % (an['nombre'], k) for k, an in enumerate(anims))
RT = RES_TEX or ('res://%s/texturas' % nombre)
exts = ['[ext_resource type="Texture2D" path="%s/%s" id="%s"]' % (RT, t['file'], t['id']) for t in tex.values()]
sfs = []
for cid, fr in frames_res.items():
    exts += ['[ext_resource type="Texture2D" path="%s/%s" id="%s"]' % (RT, x['file'], x['id']) for x in fr['frames']]
    sfs.append('[sub_resource type="SpriteFrames" id="%s"]\nanimations = [{\n"frames": [%s],\n"loop": true,\n"name": &"default",\n"speed": 30.0\n}]' % (
        fr['sf_id'], ', '.join('{\n"duration": 1.0,\n"texture": ExtResource("%s")\n}' % x['id'] for x in fr['frames'])))
subs = sfs + subs
hdr = '[gd_scene load_steps=%d format=3]' % (len(exts) + len(subs) + 2)
body = ['[node name="%s" type="Node2D"]' % nombre,
        '[node name="Modelo" type="Node2D" parent="."]',
        'metadata/fuente = "SONNY2.swf I41 %s (MODEL %d); 1 unidad = 1 px SWF; escalar este nodo para HD"' % (rep['spec']['name'], mid)]
f1 = st[0]
for name, d, sprites in nodes:
    o = f1.get(d)
    m = o['matrix'] if o else [1, 0, 0, 1, 0, 0]
    body.append('[node name="%s" type="Node2D" parent="Modelo"]' % name)
    body.append('transform = Transform2D(%r, %r, %r, %r, %r, %r)' % (m[0], m[1], m[2], m[3], m[4] / 20.0, m[5] / 20.0))
    body.append('metadata/profundidad_swf = %d' % d)
    body.append('metadata/desenfoque_swf = Vector2(0, 0)')
    for sp in sprites:
        if sp['tipo'] == 'anim':
            fr = sp['anim']
            body.append('[node name="%s" type="AnimatedSprite2D" parent="Modelo/%s"]' % (sp['nombre'], name))
            body.append('scale = Vector2(%r, %r)' % (1 / ZM, 1 / ZM))
            body.append('sprite_frames = SubResource("%s")' % fr['sf_id'])
            body.append('centered = false')
            body.append('offset = Vector2(%r, %r)' % (-fr['anclaje_png'][0], -fr['anclaje_png'][1]))
            body.append('metadata/characterId = %d' % sp['cid'])
            o1 = f1.get(d)
            if not (o1 and o1.get('ch') == sp['cid']): body.append('visible = false')
            continue
        t = sp['tex']
        body.append('[node name="%s" type="Sprite2D" parent="Modelo/%s"]' % (sp['nombre'], name))
        o1 = f1.get(d)
        if sp.get('solo_si_cid') and not (o1 and o1.get('ch') == sp['cid']): body.append('visible = false')
        body.append('scale = Vector2(%r, %r)' % (1 / Z, 1 / Z))
        body.append('texture = ExtResource("%s")' % t['id'])
        body.append('centered = false')
        body.append('offset = Vector2(%r, %r)' % (-t['anclaje_png'][0], -t['anclaje_png'][1]))
        body.append('metadata/characterId = %d' % sp['cid'])
        body.append('metadata/profundidad_attachMovie = %d' % sp['z'])
body.append('[node name="AnimationPlayer" type="AnimationPlayer" parent="."]')
body.append('libraries = {\n"": SubResource("AnimationLibrary_1")\n}')
body.append('autoplay = "stand"')
txt = '\n\n'.join([hdr] + exts + subs + [lib] + body) + '\n'
open(os.path.join(out, nombre + '.tscn'), 'w').write(txt)
if os.environ.get('NO_JSON'):
    sys.exit(print('nodos', len(nodes), 'texturas', len(tex), 'animaciones', len(anims)))
json.dump({"personaje": rep['spec'], "model": mid, "zoom_texturas": Z, "fps": FPS,
           "zoom_animados": ZM,
           "nodos": [{"nodo": n, "profundidad": d, "sprites": [({"nombre": s['nombre'], "characterId": s['cid'], "tipo": "static", "textura": s['tex']['file'],
                                                                 "anclaje_png": s['tex']['anclaje_png'], "z_attach": s['z']} if s['tipo'] == 'static' else
                                                                {"nombre": s['nombre'], "characterId": s['cid'], "tipo": "anim", "fotogramas": [x['file'] for x in s['anim']['frames']],
                                                                 "anclaje_png": s['anim']['anclaje_png'], "z_attach": 0}) for s in sp]} for n, d, sp in nodes],
           "animaciones": anims}, open(os.path.join(out, 'datos_animacion.json'), 'w'), ensure_ascii=False)
print('nodos', len(nodes), 'texturas', len(tex), 'animaciones', [(a['nombre'], a['n'], 'loop' if a['loop'] else a['siguiente']) for a in anims])
