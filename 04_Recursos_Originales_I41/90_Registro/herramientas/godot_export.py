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
os.makedirs(os.path.join(out, 'texturas'), exist_ok=True)


def find(d, cid):
    g = glob.glob(os.path.join(d, 'DefineSprite_%d' % cid)) + glob.glob(os.path.join(d, 'DefineSprite_%d_*' % cid))
    return g[0] if g else None


def anchor(cid):
    p = find(tpng, cid); s = find(tsvg, cid)
    im = Image.open(os.path.join(p, '1.png'))
    t = open(os.path.join(s, '1.svg')).read(2000)
    H, W = map(float, re.search(r'height="([\d.]+)px" width="([\d.]+)px"', t).groups())
    tx, ty = map(float, re.search(r'matrix\(1\.0, 0\.0, 0\.0, 1\.0, ([-\d.]+), ([-\d.]+)\)', t).groups())
    return os.path.join(p, '1.png'), ((im.width - W * Z) / 2 + tx * Z, (im.height - H * Z) / 2 + ty * Z), im.size


# instancias del MODEL: profundidad -> nombre / carácter
inst = {}
for ev in M['timeline']:
    if ev.get('name') and 'ch' in ev:
        inst[ev['depth']] = (ev['name'], ev['ch'])
bones = {}
for b, v in rep['huesos'].items():
    for d in v['profundidades_en_model']:
        bones[d] = (b, v['contenido'])
# otros objetos con nombre que no son huesos (sombra)
extra = {d: n for d, (n, ch) in inst.items() if d not in bones}
used_depths = sorted(set(bones) | set(extra))
tex = {}
ext_id = 0


def texture(cid, link):
    global ext_id
    if cid in tex: return tex[cid]
    p, anc, size = anchor(cid)
    fn = '%s_%d_x%d.png' % (link or 'chid', cid, int(Z))
    shutil.copy(p, os.path.join(out, 'texturas', fn))
    ext_id += 1
    tex[cid] = {"id": "%d_tex" % ext_id, "file": fn, "anclaje_png": anc, "size": size}
    return tex[cid]


nodes = []  # (path, depth, [sprites])
for d in used_depths:
    if d in bones:
        name, cont = bones[d]
        sprites = []
        for it in sorted(cont, key=lambda x: x['profundidad_timeline']):
            t = texture(it['characterId'], it['linkage'])
            sprites.append({"nombre": '%s_%s' % (it['nombre'], it['linkage']), "tex": t, "z": it['profundidad_as2'], "cid": it['characterId']})
        nodes.append((name, d, sprites))
    else:
        name = extra[d]
        cid = inst[d][1]
        t = texture(cid, '_'.join(C[str(cid)]['exports']) or name)
        nodes.append((name, d, [{"nombre": name + '_grafico', "tex": t, "z": 0, "cid": cid}]))

# animaciones por etiqueta
labels = sorted(M['labels'], key=lambda l: l['f'])
acts = {}
for p in glob.glob(os.path.join(sdir, 'DefineSprite_%d*' % mid, 'frame_*', '*.as')):
    acts[int(re.search(r'frame_(\d+)', p).group(1))] = open(p, encoding='utf-8', errors='replace').read()
anims = []
for i, l in enumerate(labels):
    a = l['f']; b = (labels[i + 1]['f'] - 1) if i + 1 < len(labels) else M['frames']
    last = acts.get(b, '')
    loop = bool(re.search(r'gotoAndStop\("%s"\)' % re.escape(l['label']), last))
    nxt = re.search(r'gotoAndStop\("([^"]+)"\)', last)
    nxt = nxt.group(1) if nxt and not loop else ('(stop)' if 'stop()' in last else ('(removeMovieClip)' if 'removeMovieClip' in last else None))
    snd = {f - a: re.findall(r'addSound\("Effects","([^"]+)"\)', acts[f]) for f in range(a, b + 1) if f in acts and 'addSound' in acts[f]}
    tracks = []
    for name, d, _ in nodes:
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
        tracks.append({"nodo": name, "transform": tf2, "visible": vis, "modulate": mod, "color_aditivo_no_aplicado": add, "desenfoque_swf_px": blur})
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
hdr = '[gd_scene load_steps=%d format=3]' % (len(tex) + len(anims) + 2)
exts = ['[ext_resource type="Texture2D" path="res://%s/texturas/%s" id="%s"]' % (nombre, t['file'], t['id']) for t in tex.values()]
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
        t = sp['tex']
        body.append('[node name="%s" type="Sprite2D" parent="Modelo/%s"]' % (sp['nombre'], name))
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
json.dump({"personaje": rep['spec'], "model": mid, "zoom_texturas": Z, "fps": FPS,
           "nodos": [{"nodo": n, "profundidad": d, "sprites": [{"nombre": s['nombre'], "characterId": s['cid'], "textura": s['tex']['file'],
                                                                 "anclaje_png": s['tex']['anclaje_png'], "z_attach": s['z']} for s in sp]} for n, d, sp in nodes],
           "animaciones": anims}, open(os.path.join(out, 'datos_animacion.json'), 'w'), ensure_ascii=False)
print('nodos', len(nodes), 'texturas', len(tex), 'animaciones', [(a['nombre'], a['n'], 'loop' if a['loop'] else a['siguiente']) for a in anims])
