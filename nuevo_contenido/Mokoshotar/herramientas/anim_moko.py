#!/usr/bin/env python3
"""Animaciones nuevas para Mokoshotar sobre el rig MODEL5 original (sin piezas nuevas en el cuerpo).

  Attack_Moko  "Mordisco Glacial"  28 f @30fps  impacto en f13 (sonido de ataque + golpe)
  cast_Moko    "Aullido de Escarcha" 42 f @30fps  liberación en f16 (sonido de hechizo)

Todo se construye a partir de la pose 'stand' original: rotaciones en las articulaciones (encadenando
muslo->pata porque el rig es plano), movimiento del cuerpo completo y modulate de color. Los efectos
(estela de hielo, anillo de escarcha) son imágenes nuevas generadas aquí.
Salida: frames.json (pose por fotograma, modulate, efectos) + efectos/*.png + preview/*.png
uso: anim_moko.py rig_dir out_dir
"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
from rig import Rig
from PIL import Image, ImageDraw, ImageFilter

rig_dir, out = sys.argv[1:3]
os.makedirs(os.path.join(out, 'efectos'), exist_ok=True)
os.makedirs(os.path.join(out, 'preview'), exist_ok=True)
R = Rig(rig_dir)
STAND, MOD0 = R.pose('stand', 0)
BODY = ['chest', 'foot1', 'head', 'hand1', 'hand2', 'arm1', 'arm2', 'leg1', 'leg2', 'leg3', 'leg4']
FRONT = [('hand1', 'arm1'), ('hand2', 'arm2')]
REAR = [('leg3', 'leg1'), ('leg4', 'leg2')]
NECK = (24.0, -4.0)        # pivote del cuello (px modelo, pose stand)
HIP = (-27.0, 10.0)
CENTER = (0.0, 12.0)
GROUND = 35.8


def ease(t):  # ease in-out
    return t * t * (3 - 2 * t)


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_in(t):
    return t ** 3


def seg(f, f0, f1, fn=ease):
    if f <= f0: return 0.0
    if f >= f1: return 1.0
    return fn((f - f0) / float(f1 - f0))


def limb(p, upper, lower, a_up, a_low):
    """Rota el muslo alrededor de su origen (arrastrando la pata) y luego la pata en su origen."""
    m = p[upper]
    R.rotate_world(p, [upper, lower], a_up, m[4], m[5])
    R.rotate_bone_local(p, lower, a_low)


def build(spec):
    """spec(f) -> dict de parámetros; devuelve pose, modulate."""
    frames = []
    for f in range(spec['n']):
        k = spec['fn'](f)
        p = {b: list(v) for b, v in STAND.items()}
        md = {b: list(v) for b, v in MOD0.items()}
        # extremidades
        for (u, l) in FRONT:
            limb(p, u, l, k.get('front_up', 0), k.get('front_low', 0))
        for (u, l) in REAR:
            limb(p, u, l, k.get('rear_up', 0), k.get('rear_low', 0))
        # cuello / cabeza
        R.rotate_world(p, ['head'], k.get('head', 0), NECK[0], NECK[1])
        R.rotate_world(p, ['foot1', 'head'], k.get('neck', 0), 12.0, 8.0)
        # cuerpo entero
        piv = k.get('body_pivot', CENTER)
        R.rotate_world(p, BODY, k.get('body_rot', 0), piv[0], piv[1])
        R.translate(p, BODY, k.get('dx', 0), k.get('dy', 0))
        # sombra: sigue en x, se encoge con la altura
        h = -k.get('dy', 0)
        sh = list(STAND['shadower'])
        s = max(0.55, 1 - h * 0.03)
        p['shadower'] = [sh[0] * s, sh[1] * s, sh[2] * s, sh[3] * s, sh[4] + k.get('dx', 0), sh[5]]
        # modulate (brillo helado)
        for b, g in k.get('glow', {}).items():
            base = md.get(b, [1, 1, 1, 1])
            md[b] = [base[0] * (1 + 0.25 * g), base[1] * (1 + 0.55 * g), base[2] * (1 + 0.9 * g), base[3]]
        frames.append({"f": f, "pose": p, "mod": md, "fx": k.get('fx', [])})
    return frames


# ---------- efectos (imágenes nuevas) ----------
def fx_claw(path):
    """Tres zarpazos diagonales de hielo, afilados en los extremos."""
    W = 512
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, off in enumerate((-95, 0, 95)):
        x0, y0, x1, y1 = 120 + off, 60, 330 + off, 450
        for w, col in ((30, (60, 170, 255, 130)), (16, (160, 235, 255, 230)), (6, (255, 255, 255, 255))):
            n = 24
            pts = []
            for j in range(n + 1):
                t = j / n
                # curva ligera
                x = x0 + (x1 - x0) * t + 40 * math.sin(math.pi * t)
                y = y0 + (y1 - y0) * t
                pts.append((x, y, w * math.sin(math.pi * t) ** 0.8))
            for j in range(n):
                xa, ya, wa = pts[j]; xb, yb, wb = pts[j + 1]
                d.line([xa, ya, xb, yb], fill=col, width=max(1, int((wa + wb) / 2)))
    im = Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(8)), im)
    im.save(path); return im


def fx_ring(path):
    W = 768
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = W / 2
    for r, w, col in ((330, 26, (70, 170, 255, 110)), (330, 10, (190, 240, 255, 230)), (250, 6, (120, 210, 255, 180))):
        d.ellipse([c - r, c - r, c + r, c + r], outline=col, width=w)
    for i in range(24):  # marcas rúnicas
        a = 2 * math.pi * i / 24
        r1, r2 = 262, 300 if i % 3 else 318
        d.line([c + r1 * math.cos(a), c + r1 * math.sin(a), c + r2 * math.cos(a), c + r2 * math.sin(a)], fill=(220, 250, 255, 255), width=8)
    for i in range(6):  # cristales de hielo
        a = 2 * math.pi * i / 6 + 0.3
        x, y = c + 290 * math.cos(a), c + 290 * math.sin(a)
        d.polygon([(x, y - 46), (x + 16, y), (x, y + 46), (x - 16, y)], fill=(230, 250, 255, 240))
    im = Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(12)), im)
    im.save(path); return im


def fx_breath(path):
    """Cono de aliento helado con cristales."""
    W = 512
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 60, W / 2
    for r in range(40, 460, 6):
        spread = 0.08 + r / 900.0
        a = int(170 * (1 - r / 470.0))
        d.ellipse([cx + r - 18, cy - r * spread - 18, cx + r + 18, cy + r * spread + 18], fill=(170, 225, 255, a))
    im = im.filter(ImageFilter.GaussianBlur(14))
    d = ImageDraw.Draw(im)
    import random
    rnd = random.Random(7)
    for i in range(18):
        r = rnd.uniform(90, 430); a = rnd.uniform(-0.25, 0.25)
        x, y = cx + r, cy + r * a; L = rnd.uniform(8, 18)
        d.polygon([(x, y - L), (x + L * 0.35, y), (x, y + L), (x - L * 0.35, y)], fill=(240, 252, 255, 235))
    im.save(path); return im


FXI = {"claw": fx_claw(os.path.join(out, 'efectos', 'fx_mordisco_glacial.png')),
       "ring": fx_ring(os.path.join(out, 'efectos', 'fx_anillo_escarcha.png')),
       "breath": fx_breath(os.path.join(out, 'efectos', 'fx_aliento_aullido.png'))}
FX_SCALE = 1 / 8.0  # px imagen -> px modelo


# ---------- ATAQUE: Mordisco Glacial ----------
def attack(f):
    k = {}
    a = seg(f, 0, 7)                       # anticipación
    l = seg(f, 7, 12, ease_out)            # salto
    b = seg(f, 12, 14, ease_out)           # mordisco
    r = seg(f, 15, 27, ease)               # regreso
    lunge = l * (1 - r)
    crouch = a * (1 - l)
    k['dx'] = -7 * crouch + 34 * lunge + 4 * b * (1 - r)
    k['dy'] = 4 * crouch - 9 * math.sin(math.pi * min(1, (f - 7) / 7.0)) * (1 if 7 <= f <= 14 else 0)
    k['body_rot'] = 6 * crouch - 9 * lunge * (1 - b) + 4 * b * (1 - r)
    k['front_up'] = 10 * crouch - 38 * lunge * (1 - b) + 8 * b * (1 - r)
    k['front_low'] = -6 * crouch - 25 * lunge * (1 - b)
    k['rear_up'] = -12 * crouch + 32 * lunge
    k['rear_low'] = 10 * crouch + 18 * lunge
    k['head'] = 14 * crouch - 20 * lunge * (1 - b) + 28 * b * (1 - r)
    k['neck'] = 4 * crouch - 6 * lunge
    glow = (1 if 11 <= f <= 16 else 0) * (1 - abs(f - 13) / 4.0)
    k['glow'] = {'head': glow * 1.6, 'foot1': glow, 'hand1': glow * 0.6, 'hand2': glow * 0.6}
    if 12 <= f <= 19:
        t = (f - 12) / 7.0
        alpha = 1 - t
        sc = (0.7 + 0.6 * t) * FX_SCALE
        k['fx'] = [{"img": "claw", "after": "head", "x": 50 + 34 * lunge, "y": 2, "rot": 0, "scale": sc, "alpha": alpha}]
    return k


# ---------- HECHIZO: Aullido de Escarcha ----------
def cast(f):
    k = {}
    s = seg(f, 0, 9)                       # sentarse y alzar hocico
    r = seg(f, 32, 41)                     # regreso
    hold = s * (1 - r)
    trem = math.sin(f * 2.1) * (1 if 12 <= f <= 30 else 0)
    k['body_pivot'] = HIP
    k['body_rot'] = -14 * hold
    k['dy'] = 2 * hold
    k['rear_up'] = -28 * hold
    k['rear_low'] = 34 * hold
    k['front_up'] = 10 * hold
    k['front_low'] = -4 * hold
    k['neck'] = -12 * hold
    k['head'] = -34 * hold + 2.2 * trem
    pulse = (0.5 + 0.5 * math.sin((f - 10) * 0.55)) if 10 <= f <= 32 else 0
    g = seg(f, 6, 14) * (1 - r)
    k['glow'] = {'chest': g * (0.6 + 0.8 * pulse), 'foot1': g * (0.6 + 0.8 * pulse), 'head': g * (0.4 + 0.6 * pulse)}
    fx = []
    if 16 <= f <= 36:
        t = (f - 16) / 20.0
        fx.append({"img": "ring", "after": "shadower", "x": 4, "y": 30, "rot": f * 4, "scale": (0.25 + 1.25 * ease_out(t)) * FX_SCALE,
                   "alpha": (1 - t) ** 1.2, "squash": 0.32})
    if 13 <= f <= 30:
        t = (f - 13) / 17.0
        fx.append({"img": "breath", "after": "head", "x": 40, "y": -36, "rot": -62, "scale": (0.45 + 0.75 * t) * FX_SCALE, "alpha": math.sin(math.pi * t) ** 0.7})
    k['fx'] = fx
    return k


ANIMS = {"Attack_Moko": {"n": 28, "fn": attack, "evento": {"f": 13, "tipo": "impacto", "sonido": "SonidoAtaque"},
                         "siguiente": "stand", "nombre_es": "Mordisco Glacial"},
         "cast_Moko": {"n": 42, "fn": cast, "evento": {"f": 16, "tipo": "liberacion", "sonido": "SonidoHechizo"},
                       "siguiente": "stand", "nombre_es": "Aullido de Escarcha"}}
result = {}
for name, spec in ANIMS.items():
    fr = build(spec)
    result[name] = {"n": spec['n'], "evento": spec['evento'], "siguiente": spec['siguiente'], "nombre_es": spec['nombre_es'],
                    "frames": fr}
    os.makedirs(os.path.join(out, 'preview', name), exist_ok=True)
    for x in fr:
        extras = []
        for e in x['fx']:
            im = FXI[e['img']].copy()
            if e['alpha'] < 1:
                im.putalpha(im.getchannel('A').point(lambda v, a=e['alpha']: int(v * max(0, a))))
            r_ = math.radians(e['rot']); c, s_ = math.cos(r_), math.sin(r_); sc = e['scale']; sq = e.get('squash', 1.0)
            m = [c * sc, s_ * sc * sq, -s_ * sc, c * sc * sq, e['x'], e['y']]
            extras.append((e['after'], im, m, (im.width / 2, im.height / 2), 1.0))
        img = R.render(x['pose'], x['mod'], size=(900, 520), origin=(380, 300), scale=4.0, extras=extras, bg=(38, 44, 56, 255))
        img.save(os.path.join(out, 'preview', name, '%03d.png' % x['f']))
json.dump({k: {kk: vv for kk, vv in v.items()} for k, v in result.items()}, open(os.path.join(out, 'frames.json'), 'w'))
print({k: v['n'] for k, v in result.items()})
