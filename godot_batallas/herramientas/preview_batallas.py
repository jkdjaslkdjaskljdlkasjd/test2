#!/usr/bin/env python3
"""Vista previa (Python, misma semántica que BattleViewer.gd en reposo, cámara en reposo = identidad):
cielo + suelo de la zona HD + personajes originales (rig de la escena Godot) en el origen de cada slot,
espejo en enemigos, MODEL5 x0.8 y +10, orden por profundidad del frame 217. Pose: fotograma 1 de 'stand'.
uso: preview_batallas.py proyecto_dir chkall_dir out_dir KBR51 KBR1 ...
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from rig import Rig
from PIL import Image, ImageDraw, ImageFont
proj, chk, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
D = json.load(open(os.path.join(proj, 'datos/combates.json')))
PX = 1440 / 575; LEFT = -1000 / 9
DEPTH = {"player5": 40, "player6": 80, "player1": 120, "player2": 160, "player3": 200, "player4": 240}
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
rigs = {}
for kbr in sys.argv[4:]:
    b = next(c for c in D['combates'] if c['combate'] == kbr)
    z = b['zona_hd']
    can = Image.open(os.path.join(proj, 'assets/zonas/%s_sky.png' % z)).convert('RGBA')
    can.alpha_composite(Image.open(os.path.join(proj, 'assets/zonas/%s_ground.png' % z)).convert('RGBA'))
    lab = []
    for slot in sorted(DEPTH, key=DEPTH.get):
        s = b['slots'][slot]; sl = D['slots'][slot]
        if not s['apariencia']:
            continue
        ap = s['apariencia']
        if ap not in rigs:
            rigs[ap] = Rig(os.path.join(chk, ap))
        R = rigs[ap]
        p, m = R.pose('stand', 0)
        sx = sl['xscale']; k = 0.8 if s['model'] == 'MODEL5' else 1.0; dy = 10.0 if s['model'] == 'MODEL5' else 0.0
        for n in p:
            a, bb, c, d, x, y = p[n]
            p[n] = [a * k * sx, bb * k, c * k * sx, d * k, x * k * sx, y * k + dy]
        ox = (sl['x_stage'] - LEFT) * PX; oy = sl['y_stage'] * PX
        can.alpha_composite(R.render(p, m, size=can.size, origin=(ox, oy), scale=PX))
        lab.append('%s %s' % (slot.replace('player', 'F'), ap))
    d = ImageDraw.Draw(can)
    d.rectangle((0, 1380, 2560, 1440), fill=(0, 0, 0, 170))
    d.text((20, 1392), '%s | fondo %s | %s | vista previa Python (NO es captura de Godot)' % (kbr, z, '  '.join(lab)), fill=(255, 255, 255), font=font)
    can.convert('RGB').save(os.path.join(out, 'preview_%s_%s.png' % (kbr, z)))
    print(kbr, z, lab)
