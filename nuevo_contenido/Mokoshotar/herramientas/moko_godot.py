#!/usr/bin/env python3
"""Ensambla la escena Godot de Mokoshotar con las animaciones y sonidos nuevos.

Entrada: escena base generada por godot_export.py (con texturas), frames.json de anim_moko.py,
         efectos PNG y sonidos OGG.
Salida (carpeta autónoma res://Mokoshotar/):
  Mokoshotar.tscn       escena: animaciones originales + Attack_Moko + cast_Moko,
                        nodos de efectos, 3 AudioStreamPlayer2D, script
  mokoshotar.gd         atacar(critico) / lanzar_hechizo(critico), encadenado a 'stand', teclas 1-4
  texturas/ efectos/ sonidos/
uso: moko_godot.py base_dir nuevo_dir sonidos_dir out_dir
"""
import sys, os, re, json, shutil, math

base, nuevo, snd, out = sys.argv[1:5]
NAME = 'Mokoshotar'
RES = 'res://%s' % NAME
os.makedirs(out, exist_ok=True)
for d in ('texturas', 'efectos', 'sonidos'):
    os.makedirs(os.path.join(out, d), exist_ok=True)
for f in os.listdir(os.path.join(base, 'texturas')):
    shutil.copy(os.path.join(base, 'texturas', f), os.path.join(out, 'texturas', f))
for f in os.listdir(os.path.join(nuevo, 'efectos')):
    shutil.copy(os.path.join(nuevo, 'efectos', f), os.path.join(out, 'efectos', f))
for f in os.listdir(snd):
    if f.endswith('.ogg') or f.endswith('.wav') or f.endswith('.json'):
        shutil.copy(os.path.join(snd, f), os.path.join(out, 'sonidos', f))

txt = open(os.path.join(base, NAME + '.tscn')).read()
blocks = re.split(r'\n\n(?=\[)', txt)
hdr = blocks[0]
ext = [b for b in blocks if b.startswith('[ext_resource')]
subs = [b for b in blocks if b.startswith('[sub_resource') and 'AnimationLibrary' not in b]
lib = [b for b in blocks if 'type="AnimationLibrary"' in b][0]
nodes = [b for b in blocks if b.startswith('[node')]
FR = json.load(open(os.path.join(nuevo, 'frames.json')))
FPS = 30.0

# ---------- recursos nuevos ----------
eid = 1000


def new_ext(typ, path):
    global eid
    eid += 1
    i = '%d_new' % eid
    ext.append('[ext_resource type="%s" path="%s" id="%s"]' % (typ, path, i))
    return i


fx_files = {"claw": "fx_mordisco_glacial.png", "ring": "fx_anillo_escarcha.png", "breath": "fx_aliento_aullido.png"}
fx_ids = {k: new_ext('Texture2D', '%s/efectos/%s' % (RES, v)) for k, v in fx_files.items()}
s_ids = {k: new_ext('AudioStream', '%s/sonidos/%s.ogg' % (RES, k)) for k in
         ('moko_ataque_mordisco_1', 'moko_ataque_mordisco_2', 'moko_hechizo_escarcha_1', 'moko_hechizo_escarcha_2', 'moko_critico_aullido')}
script_id = new_ext('Script', '%s/mokoshotar.gd' % RES)
subs.append('''[sub_resource type="AudioStreamRandomizer" id="Aleatorio_ataque"]
playback_mode = 1
random_pitch = 1.04
streams_count = 2
stream_0/stream = ExtResource("%s")
stream_0/weight = 1.0
stream_1/stream = ExtResource("%s")
stream_1/weight = 1.0''' % (s_ids['moko_ataque_mordisco_1'], s_ids['moko_ataque_mordisco_2']))
subs.append('''[sub_resource type="AudioStreamRandomizer" id="Aleatorio_hechizo"]
playback_mode = 1
random_pitch = 1.03
streams_count = 2
stream_0/stream = ExtResource("%s")
stream_0/weight = 1.0
stream_1/stream = ExtResource("%s")
stream_1/weight = 1.0''' % (s_ids['moko_hechizo_escarcha_1'], s_ids['moko_hechizo_escarcha_2']))

# ---------- nodos de efectos (insertados en el orden de dibujo) ----------
FX_NODES = {"claw": ("fx_mordisco", "head"), "breath": ("fx_aliento", "head"), "ring": ("fx_anillo", "shadower")}
node_names = [re.search(r'name="([^"]+)"', n).group(1) for n in nodes]
new_nodes = []
for n in nodes:
    new_nodes.append(n)
    m = re.match(r'\[node name="([^"]+)" type="Node2D" parent="Modelo"\]', n)
    if m:
        pass
# insertar tras el último bloque perteneciente al hueso indicado (el hueso y sus hijos)
def insert_after(lst, bone, block):
    idx = None
    for i, b in enumerate(lst):
        if re.search(r'parent="Modelo/%s"' % re.escape(bone), b) or re.match(r'\[node name="%s" type="Node2D" parent="Modelo"\]' % re.escape(bone), b):
            idx = i
    lst.insert(idx + 1, block)


for key, (nn, after) in FX_NODES.items():
    insert_after(new_nodes, after, '[node name="%s" type="Sprite2D" parent="Modelo"]\nvisible = false\ntexture = ExtResource("%s")\nmetadata/efecto_nuevo = true' % (nn, fx_ids[key]))
# raíz con script
new_nodes[0] = new_nodes[0] + '\nscript = ExtResource("%s")' % script_id
# reproductores de audio antes del AnimationPlayer
ap_i = [i for i, b in enumerate(new_nodes) if 'type="AnimationPlayer"' in b][0]
audio = ['[node name="SonidoAtaque" type="AudioStreamPlayer2D" parent="."]\nstream = SubResource("Aleatorio_ataque")',
         '[node name="SonidoHechizo" type="AudioStreamPlayer2D" parent="."]\nstream = SubResource("Aleatorio_hechizo")',
         '[node name="SonidoCritico" type="AudioStreamPlayer2D" parent="."]\nstream = ExtResource("%s")' % s_ids['moko_critico_aullido']]
new_nodes[ap_i:ap_i] = audio

# ---------- animaciones nuevas ----------
bones = [re.match(r'\[node name="([^"]+)" type="Node2D" parent="Modelo"\]', b).group(1) for b in nodes
         if re.match(r'\[node name="([^"]+)" type="Node2D" parent="Modelo"\]', b)]


def track(i, path, values, n, interp=1, kind='value'):
    times = ', '.join('%.6g' % (j / FPS) for j in range(n))
    trans = ', '.join(['1'] * n)
    return ['tracks/%d/type = "%s"' % (i, kind), 'tracks/%d/imported = false' % i, 'tracks/%d/enabled = true' % i,
            'tracks/%d/path = NodePath("%s")' % (i, path), 'tracks/%d/interp = %d' % (i, interp), 'tracks/%d/loop_wrap = true' % i,
            'tracks/%d/keys = {\n"times": PackedFloat32Array(%s),\n"transitions": PackedFloat32Array(%s),\n"update": %d,\n"values": [%s]\n}'
            % (i, times, trans, 0 if interp else 1, ', '.join(values))]


def method_track(i, path, t, method='play'):
    return ['tracks/%d/type = "method"' % i, 'tracks/%d/imported = false' % i, 'tracks/%d/enabled = true' % i,
            'tracks/%d/path = NodePath("%s")' % (i, path), 'tracks/%d/interp = 1' % i, 'tracks/%d/loop_wrap = true' % i,
            'tracks/%d/keys = {\n"times": PackedFloat32Array(%.6g),\n"transitions": PackedFloat32Array(1),\n"values": [{\n"args": [],\n"method": &"%s"\n}]\n}' % (i, t, method)]


SOUND_AT = {"Attack_Moko": ("SonidoAtaque", 7), "cast_Moko": ("SonidoHechizo", 9)}
new_anim_ids = []
for name, a in FR.items():
    n = a['n']; sid = 'Animation_%s' % name
    tl = ['[sub_resource type="Animation" id="%s"]' % sid, 'resource_name = "%s"' % name, 'length = %.6g' % (n / FPS),
          'loop_mode = 0', 'step = %.6g' % (1 / FPS)]
    ti = 0
    for b in bones:
        fr = a['frames']
        if all(b not in x['pose'] for x in fr):
            tl += track(ti, 'Modelo/%s:visible' % b, ['false'] * n, n, interp=0); ti += 1
            continue
        tl += track(ti, 'Modelo/%s:transform' % b, ['Transform2D(%r, %r, %r, %r, %r, %r)' % tuple(x['pose'][b]) for x in fr], n); ti += 1
        tl += track(ti, 'Modelo/%s:visible' % b, ['true'] * n, n, interp=0); ti += 1
        tl += track(ti, 'Modelo/%s:modulate' % b, ['Color(%r, %r, %r, %r)' % tuple(x['mod'].get(b, [1, 1, 1, 1])) for x in fr], n); ti += 1
    for key, (nn, after) in FX_NODES.items():
        vis, tf, md = [], [], []
        for x in a['frames']:
            e = [q for q in x['fx'] if q['img'] == key]
            if e:
                e = e[0]; r = math.radians(e['rot']); c, s_ = math.cos(r), math.sin(r); sc = e['scale']; sq = e.get('squash', 1.0)
                vis.append('true'); tf.append('Transform2D(%r, %r, %r, %r, %r, %r)' % (c * sc, s_ * sc * sq, -s_ * sc, c * sc * sq, e['x'], e['y']))
                md.append('Color(1, 1, 1, %r)' % max(0.0, e['alpha']))
            else:
                vis.append('false'); tf.append(tf[-1] if tf else 'Transform2D(1, 0, 0, 1, 0, 0)'); md.append('Color(1, 1, 1, 0)')
        tl += track(ti, 'Modelo/%s:visible' % nn, vis, n, interp=0); ti += 1
        tl += track(ti, 'Modelo/%s:transform' % nn, tf, n); ti += 1
        tl += track(ti, 'Modelo/%s:modulate' % nn, md, n); ti += 1
    player, f = SOUND_AT[name]
    tl += method_track(ti, player, f / FPS); ti += 1
    subs.append('\n'.join(tl))
    new_anim_ids.append((name, sid))
# las animaciones originales deben ocultar los efectos nuevos
fixed = []
for b in subs:
    if b.startswith('[sub_resource type="Animation"') and 'Animation_Attack_Moko' not in b and 'Animation_cast_Moko' not in b:
        nt = len(re.findall(r'^tracks/\d+/type', b, re.M))
        n = int(round(float(re.search(r'^length = ([\d.e-]+)', b, re.M).group(1)) * FPS))
        extra = []
        for k, (nn, _) in enumerate(FX_NODES.values()):
            extra += track(nt + k, 'Modelo/%s:visible' % nn, ['false'] * max(n, 1), max(n, 1), interp=0)
        b = b + '\n' + '\n'.join(extra)
    fixed.append(b)
subs = fixed
lib = lib.rstrip('}').rstrip() + ',\n' + ',\n'.join('"%s": SubResource("%s")' % (nm, sid) for nm, sid in new_anim_ids) + '\n}'
hdr = '[gd_scene load_steps=%d format=3]' % (len(ext) + len(subs) + 2)
open(os.path.join(out, NAME + '.tscn'), 'w').write('\n\n'.join([hdr] + ext + subs + [lib] + new_nodes) + '\n')

gd = '''extends Node2D
## Mokoshotar (I41, rig MODEL5) con animaciones y sonidos nuevos.
## - atacar(critico): "Attack_Moko" (Mordisco Glacial). Sonido aleatorio entre 2 (SonidoAtaque) en el fotograma 7;
##   el mordisco impacta en el fotograma 13. Si es crítico, suena el aullido (SonidoCritico) en el impacto.
## - lanzar_hechizo(critico): "cast_Moko" (Aullido de Escarcha). Sonido aleatorio entre 2 (SonidoHechizo) en el
##   fotograma 9; la escarcha se libera en el fotograma 16.
## Al terminar, ambas vuelven a "stand". Teclas de prueba: 1 ataque, 2 ataque crítico, 3 hechizo, 4 hechizo crítico.

const FPS := 30.0
const IMPACTO_ATAQUE := 13.0 / FPS
const LIBERACION_HECHIZO := 16.0 / FPS

signal impacto(critico: bool)

@onready var anim: AnimationPlayer = $AnimationPlayer
@onready var sonido_critico: AudioStreamPlayer2D = $SonidoCritico

func _ready() -> void:
	anim.animation_finished.connect(_al_terminar)
	anim.play("stand")

func atacar(critico: bool = false) -> void:
	anim.play("Attack_Moko")
	await get_tree().create_timer(IMPACTO_ATAQUE).timeout
	impacto.emit(critico)
	if critico:
		sonido_critico.play()

func lanzar_hechizo(critico: bool = false) -> void:
	anim.play("cast_Moko")
	await get_tree().create_timer(LIBERACION_HECHIZO).timeout
	impacto.emit(critico)
	if critico:
		sonido_critico.play()

func _al_terminar(nombre: StringName) -> void:
	if nombre in [&"Attack_Moko", &"cast_Moko", &"runback", &"hit", &"cast", &"outofstun"]:
		anim.play("stand")

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: atacar(false)
			KEY_2: atacar(true)
			KEY_3: lanzar_hechizo(false)
			KEY_4: lanzar_hechizo(true)
'''
open(os.path.join(out, 'mokoshotar.gd'), 'w').write(gd)
print('animaciones nuevas', [x[0] for x in new_anim_ids], 'ext', len(ext), 'subs', len(subs))
