#!/usr/bin/env python3
"""Vídeo de demostración (MP4 con audio) de las animaciones y sonidos nuevos de Mokoshotar.
Secuencia: stand -> Attack_Moko (sonido 1) -> stand -> Attack_Moko (sonido 2) -> stand ->
cast_Moko (1) -> stand -> cast_Moko (2) -> stand -> Attack_Moko CRÍTICO (sonido 1 + aullido en el impacto) -> stand
Los fotogramas se renderizan con la misma semántica que la escena Godot (rig.py).
uso: demo_moko.py rig_dir nuevo_dir sonidos_dir out.mp4
"""
import sys, os, json, subprocess, math
import numpy as np
from scipy.io import wavfile
sys.path.insert(0, os.path.dirname(__file__))
from rig import Rig
from PIL import Image, ImageDraw, ImageFont

rig_dir, nuevo, snd, out = sys.argv[1:5]
R = Rig(rig_dir)
tmp = os.path.join(os.path.dirname(out), 'demo_frames'); os.makedirs(tmp, exist_ok=True)
FPS = 30
SR = 44100
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
stand = R.anims['stand']


def stand_frames(n, start=0):
    res = []
    for i in range(n):
        j = (start + i) % stand['n']
        p, m = R.pose('stand', j)
        res.append(('stand', p, m, []))
    return res


fr_new = {}
for name in ('Attack_Moko', 'cast_Moko'):
    fr_new[name] = sorted(os.listdir(os.path.join(nuevo, 'preview', name)))
seq = []   # (titulo, imagen_path|pose)
events = []  # (frame_index, wav)
def add_stand(n):
    for (_, p, m, _) in stand_frames(n):
        seq.append(('Reposo (stand original)', ('pose', p, m)))
def add_new(name, title, snd_name, crit=False):
    start = len(seq)
    for f in fr_new[name]:
        seq.append((title, ('img', os.path.join(nuevo, 'preview', name, f))))
    events.append((start + (7 if name == 'Attack_Moko' else 9), snd_name))
    if crit:
        events.append((start + 13, 'moko_critico_aullido'))

add_stand(24)
add_new('Attack_Moko', 'Ataque: Mordisco Glacial  (sonido 1/2)', 'moko_ataque_mordisco_1'); add_stand(18)
add_new('Attack_Moko', 'Ataque: Mordisco Glacial  (sonido 2/2)', 'moko_ataque_mordisco_2'); add_stand(18)
add_new('cast_Moko', 'Hechizo: Aullido de Escarcha  (sonido 1/2)', 'moko_hechizo_escarcha_1'); add_stand(24)
add_new('cast_Moko', 'Hechizo: Aullido de Escarcha  (sonido 2/2)', 'moko_hechizo_escarcha_2'); add_stand(24)
add_new('Attack_Moko', 'GOLPE CRITICO: mordisco + aullido', 'moko_ataque_mordisco_1', crit=True); add_stand(75)

for i, (title, src) in enumerate(seq):
    if src[0] == 'img':
        im = Image.open(src[1]).convert('RGBA')
    else:
        im = R.render(src[1], src[2], size=(900, 520), origin=(380, 300), scale=4.0, bg=(38, 44, 56, 255))
    d = ImageDraw.Draw(im)
    d.text((18, 14), title, fill=(230, 240, 255), font=font)
    d.text((18, 488), 'Mokoshotar (I41, rig MODEL5) - vista previa de la escena Godot', fill=(150, 165, 190), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14))
    im.convert('RGB').save(os.path.join(tmp, '%05d.png' % i))
dur = len(seq) / FPS
mix = np.zeros((int((dur + 3) * SR), 2))
for fi, name in events:
    sr, x = wavfile.read(os.path.join(snd, name + '.wav'))
    x = x.astype(float) / 32768
    i = int(fi / FPS * SR)
    n = min(len(x), len(mix) - i)
    mix[i:i + n] += x[:n] * (0.9 if 'aullido' in name else 1.0)
mix = mix[:int(dur * SR)]
mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
wav = os.path.join(os.path.dirname(out), 'demo_audio.wav')
wavfile.write(wav, SR, np.int16(mix * 32767))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%05d.png'), '-i', wav,
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
json.dump({"eventos_sonido": [{"fotograma": f, "segundo": round(f / FPS, 3), "sonido": s} for f, s in events], "duracion_s": round(dur, 2)},
          open(out[:-4] + '_eventos.json', 'w'), indent=1)
print('frames', len(seq), 'dur', round(dur, 2), 'eventos', events)
