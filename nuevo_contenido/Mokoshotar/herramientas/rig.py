#!/usr/bin/env python3
"""Rig 2D de un personaje exportado (datos_animacion.json de godot_export.py).

- poses: dict hueso -> [a,b,c,d,tx,ty] (px SWF), tomado de cualquier fotograma de las animaciones originales
- operaciones sobre poses: rotar un hueso alrededor de un punto (su pivote), trasladar/rotar todo el cuerpo,
  interpolar entre poses (componente a componente)
- render con la misma semántica que la escena Godot (Node2D.transform · Sprite2D(scale=1/Z, offset=-anclaje)),
  con modulate por hueso y capas extra (efectos) en coordenadas del modelo.
"""
import json, math, os
from PIL import Image, ImageDraw


class Rig:
    def __init__(self, scene_dir):
        self.dir = scene_dir
        self.D = json.load(open(os.path.join(scene_dir, 'datos_animacion.json')))
        self.Z = self.D['zoom_texturas']
        self.nodes = [n for n in self.D['nodos']]
        self.order = [n['nodo'] for n in self.nodes]
        self.anims = {a['nombre']: a for a in self.D['animaciones']}
        self._tex = {}

    # ---------- poses ----------
    def pose(self, anim, i=0):
        a = self.anims[anim]
        p, mod = {}, {}
        for tr in a['tracks']:
            if tr['visible'][i]:
                p[tr['nodo']] = list(tr['transform'][i])
                mod[tr['nodo']] = list(tr['modulate'][i] or [1, 1, 1, 1])
        return p, mod

    @staticmethod
    def lerp(p1, p2, t):
        out = {}
        for k in p1:
            if k in p2:
                out[k] = [x + (y - x) * t for x, y in zip(p1[k], p2[k])]
            else:
                out[k] = list(p1[k])
        return out

    @staticmethod
    def apply(m, n):
        """m · n (aplicar n y luego m)."""
        a1, b1, c1, d1, x1, y1 = m
        a2, b2, c2, d2, x2, y2 = n
        return [a1 * a2 + c1 * b2, b1 * a2 + d1 * b2, a1 * c2 + c1 * d2, b1 * c2 + d1 * d2,
                a1 * x2 + c1 * y2 + x1, b1 * x2 + d1 * y2 + y1]

    @staticmethod
    def rot_about(deg, px, py):
        r = math.radians(deg)
        c, s = math.cos(r), math.sin(r)
        # T(p) R T(-p)
        return [c, s, -s, c, px - c * px + s * py, py - s * px - c * py]

    def rotate_bone_local(self, p, bone, deg, lx=0.0, ly=0.0):
        """Rota el hueso alrededor de un punto en SUS coordenadas locales (0,0 = su origen/pivote)."""
        m = p[bone]
        wx = m[0] * lx + m[2] * ly + m[4]
        wy = m[1] * lx + m[3] * ly + m[5]
        p[bone] = self.apply(self.rot_about(deg, wx, wy), m)

    def rotate_world(self, p, bones, deg, px, py):
        R = self.rot_about(deg, px, py)
        for b in bones:
            if b in p:
                p[b] = self.apply(R, p[b])

    def translate(self, p, bones, dx, dy):
        for b in bones:
            if b in p:
                p[b][4] += dx; p[b][5] += dy

    def scale_world(self, p, bones, sx, sy, px, py):
        S = [sx, 0, 0, sy, px - sx * px, py - sy * py]
        for b in bones:
            if b in p:
                p[b] = self.apply(S, p[b])

    # ---------- render ----------
    def tex(self, fn):
        if fn not in self._tex:
            self._tex[fn] = Image.open(os.path.join(self.dir, 'texturas', fn)).convert('RGBA')
        return self._tex[fn]

    def render(self, pose, mod=None, size=(900, 520), origin=(380, 330), scale=4.0, extras=None, bg=(0, 0, 0, 0), skip=()):
        """extras: lista de (z_index_despues_de_nodo, PIL RGBA imagen, matriz en px modelo, ancla_px_imagen, escala_img)"""
        can = Image.new('RGBA', size, bg)
        extras = extras or []
        for n in self.nodes:
            name = n['nodo']
            if name in skip or name not in pose:
                pass
            else:
                a, b, c, d, ox, oy = pose[name]
                md = (mod or {}).get(name, [1, 1, 1, 1])
                for sp in sorted(n['sprites'], key=lambda s: s['z_attach']):
                    if sp.get('tipo') == 'anim' or not sp.get('textura'):
                        continue
                    im = self.tex(sp['textura'])
                    self._blit(can, im, [a, b, c, d, ox, oy], sp['anclaje_png'], 1.0 / self.Z, md, origin, scale)
            for (after, im, m, anc, k) in extras:
                if after == name:
                    self._blit(can, im, m, anc, k, [1, 1, 1, 1], origin, scale)
        return can

    @staticmethod
    def _blit(can, im, m, anc, k, md, origin, scale):
        a, b, c, d, ox, oy = m
        A2, B2, C2, D2 = a * k * scale, b * k * scale, c * k * scale, d * k * scale
        ex = scale * ox + origin[0]; ey = scale * oy + origin[1]
        det = A2 * D2 - B2 * C2
        if abs(det) < 1e-9:
            return
        ia, ib, ic, idd = D2 / det, -B2 / det, -C2 / det, A2 / det
        coeffs = (ia, ic, -(ia * ex + ic * ey) + anc[0], ib, idd, -(ib * ex + idd * ey) + anc[1])
        lay = im.transform(can.size, Image.AFFINE, coeffs, resample=Image.BICUBIC)
        if md != [1, 1, 1, 1]:
            r_, g_, b_, a_ = lay.split()
            lay = Image.merge('RGBA', [ch.point(lambda v, kk=kk: int(max(0, min(255, v * kk)))) for ch, kk in zip((r_, g_, b_, a_), md)])
        can.alpha_composite(lay)

    def debug_pivots(self, pose, path, scale=6.0):
        im = self.render(pose, size=(1100, 650), origin=(560, 380), scale=scale, bg=(60, 60, 60, 255))
        dr = ImageDraw.Draw(im)
        for name, m in pose.items():
            x = scale * m[4] + 560; y = scale * m[5] + 380
            dr.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(255, 50, 50), width=2)
            # eje x local
            dr.line([x, y, x + 25 * m[0], y + 25 * m[1]], fill=(255, 220, 0), width=2)
            dr.text((x + 7, y - 14), name, fill=(255, 255, 255))
        im.save(path)
