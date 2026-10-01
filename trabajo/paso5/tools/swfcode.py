# Paso 3 — extrae y descompila todo el codigo AVM1 del SWF.
#
# Uso:  python3 swfcode.py CARPETA_PASO1 CARPETA_SALIDA
#
# Estructura de salida (parecida a JPEXS):
#   scripts/escenario/frame_0042/DoAction.as           (+ .pcode)
#   scripts/escenario/frame_0001/colocacion_d12/onClipEvent(load).as
#   scripts/DefineSprite_1234_nombre/frame_0003/DoAction.as
#   scripts/DoInitAction/DefineSprite_1234_nombre.as
#   scripts/DefineButton2_567_nombre/on(release).as
#   index.json   lista de todos los scripts con su origen exacto (etiqueta,
#                desplazamiento), gotos y error si lo hubo
import sys, os, json, struct, re
sys.path.insert(0, os.path.dirname(__file__))
from swfsplit import read_tags
from swfshape import Bits
from as2dec import decompile

CLIP_EVENTS = [  # bit (en UI32 little-endian) -> nombre
    (0x00000001, 'onClipEvent(load)'), (0x00000002, 'onClipEvent(enterFrame)'),
    (0x00000004, 'onClipEvent(unload)'), (0x00000008, 'onClipEvent(mouseMove)'),
    (0x00000010, 'onClipEvent(mouseDown)'), (0x00000020, 'onClipEvent(mouseUp)'),
    (0x00000040, 'onClipEvent(keyDown)'), (0x00000080, 'onClipEvent(keyUp)'),
    (0x00000100, 'onClipEvent(data)'), (0x00000200, 'onClipEvent(initialize)'),
    (0x00000400, 'on(press)'), (0x00000800, 'on(release)'),
    (0x00001000, 'on(releaseOutside)'), (0x00002000, 'on(rollOver)'),
    (0x00004000, 'on(rollOut)'), (0x00008000, 'on(dragOver)'),
    (0x00010000, 'on(dragOut)'), (0x00020000, 'on(keyPress)'),
    (0x00040000, 'onClipEvent(construct)')]

BTN_EVENTS = [  # (byte, mascara) -> nombre
    (0, 0x08, 'release'), (0, 0x04, 'press'), (0, 0x02, 'rollOut'), (0, 0x01, 'rollOver'),
    (0, 0x10, 'dragOut'), (0, 0x20, 'dragOver'), (0, 0x40, 'releaseOutside'),
    (0, 0x80, 'dragOver'), (1, 0x01, 'dragOut')]

KEYS = {1: '<Left>', 2: '<Right>', 3: '<Home>', 4: '<End>', 5: '<Insert>', 6: '<Delete>',
        8: '<Backspace>', 13: '<Enter>', 14: '<Up>', 15: '<Down>', 16: '<PageUp>',
        17: '<PageDown>', 18: '<Tab>', 19: '<Escape>', 32: '<Space>'}


def safe(s):
    return re.sub(r'[^A-Za-z0-9_.()<>-]+', '_', s)[:60]


def skip_filters(b, p):
    n = b[p]; p += 1
    for _ in range(n):
        fid = b[p]; p += 1
        if fid == 0: p += 23
        elif fid == 1: p += 9
        elif fid == 2: p += 15
        elif fid == 3: p += 27
        elif fid in (4, 7):
            k = b[p]; p += 1 + 5 * k + 19
        elif fid == 5:
            mx, my = b[p], b[p + 1]; p += 2 + 8 + 4 * mx * my + 5
        elif fid == 6: p += 80
    return p


def place_actions(b, off, ln, code):
    """Devuelve (profundidad, nombre, [(evento, ini, fin)]) de un PlaceObject2/3."""
    f1 = b[off]
    if not f1 & 0x80:
        return None
    p = off + 1
    f2 = 0
    if code == 70:
        f2 = b[p]; p += 1
    depth = struct.unpack_from('<H', b, p)[0]; p += 2
    if code == 70 and (f2 & 0x08 or (f2 & 0x10 and f1 & 0x02)):
        while b[p]: p += 1
        p += 1
    if f1 & 0x02: p += 2
    r = Bits(b, p)
    if f1 & 0x04: r.matrix()
    if f1 & 0x08:
        r.align(); ha = r.ub(1); hm = r.ub(1); nb = r.ub(4)
        if hm: [r.sb(nb) for _ in range(4)]
        if ha: [r.sb(nb) for _ in range(4)]
        r.align()
    p = r.p
    if f1 & 0x10: p += 2
    name = ''
    if f1 & 0x20:
        j = b.index(b'\0', p); name = b[p:j].decode('latin1'); p = j + 1
    if f1 & 0x40: p += 2
    if code == 70:
        if f2 & 0x01: p = skip_filters(b, p)
        if f2 & 0x02: p += 1
        if f2 & 0x04: p += 1
        if f2 & 0x20: p += 5
    p += 2            # reservado
    p += 4            # AllEventFlags (SWF6+)
    evs = []
    end = off + ln
    while p + 4 <= end:
        fl = struct.unpack_from('<I', b, p)[0]; p += 4
        if fl == 0: break
        size = struct.unpack_from('<I', b, p)[0]; p += 4
        a0 = p
        key = None
        if fl & 0x00020000:
            key = b[p]; a0 = p + 1
        names = [nm for bit, nm in CLIP_EVENTS if fl & bit]
        if key is not None:
            names = [nm.replace('keyPress', 'keyPress "%s"' % KEYS.get(key, chr(key) if 32 < key < 127 else key)) for nm in names]
        evs.append((' '.join(names) or 'evento_%x' % fl, a0, p + size, p - 4))
        p += size
    return depth, name, evs


def button_actions(b):
    """DefineButton2 -> [(evento, ini, fin)]"""
    off = struct.unpack_from('<H', b, 3)[0]
    if off == 0: return []
    p = 3 + off
    out = []
    while p + 4 <= len(b):
        size = struct.unpack_from('<H', b, p)[0]
        c0, c1 = b[p + 2], b[p + 3]
        names = [nm for byte, mask, nm in BTN_EVENTS if (c0 if byte == 0 else c1) & mask]
        key = c1 >> 1
        if key:
            names.append('keyPress "%s"' % KEYS.get(key, chr(key) if 32 < key < 127 else key))
        a0 = p + 4
        a1 = p + size if size else len(b)
        out.append(('on(%s)' % ', '.join(dict.fromkeys(names)) if names else 'on(?)', a0, a1, p if size else None))
        if size == 0: break
        p += size
    return out


class Walker:
    def __init__(self, p1, out):
        self.p1 = p1; self.out = out
        self.m = json.load(open(os.path.join(p1, 'manifest.json')))
        self.sy = json.load(open(os.path.join(p1, 'symbols.json')))
        self.index = []
        os.makedirs(os.path.join(out, 'scripts'), exist_ok=True)

    def label(self, cid):
        e = self.sy.get(str(cid), {}).get('exports') or []
        return '%d%s' % (cid, ('_' + safe(e[0])) if e else '')

    def write(self, rel, b, a0, a1, origin, loc=None):
        decompile.last = (0, 0)
        txt, pc, gotos, err = decompile(b, a0, a1)
        tot, miss = decompile.last
        path = os.path.join(self.out, 'scripts', rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        base = path[:-3]
        k = 1
        while os.path.exists(base + '.as') or os.path.exists(base + '.pcode'):
            k += 1
            base = path[:-3] + '_%d' % k
        header = '// %s\n// origen: %s\n' % (os.path.basename(base), origin)
        if err:
            header += '// NO SE PUDO ESTRUCTURAR (%s). El .pcode de al lado es el codigo exacto.\n' % err
            txt = ''
        elif gotos:
            header += '// %d salto(s) sin patron reconocible se dejaron como goto.\n' % gotos
        open(base + '.as', 'w').write(header + '\n' + (txt or ''))
        open(base + '.pcode', 'w').write(header + '\n' + pc + '\n')
        self.index.append(dict(file=os.path.relpath(base + '.as', self.out), origin=origin,
                               bytes=a1 - a0, gotos=gotos, error=err, ins=tot, missing=miss,
                               lines=(txt or '').count('\n'), loc=loc))

    def timeline(self, where, items, get_body):
        """items: lista de (codigo, off, ln, etiqueta_idx) de una linea de tiempo."""
        frame = 1
        for code, off, ln, origin, hdr in items:
            b = get_body(origin)
            src = origin['file'] if isinstance(origin, dict) else '%s, byte %d' % (origin, off)
            tagf = origin['file'] if isinstance(origin, dict) else origin
            # campos de largo que contienen al script (para poder reemplazarlo en el paso 4)
            fx = [] if hdr is None else [['taghdr', hdr[0]]]
            if code == 12:
                self.write('%s/frame_%04d/DoAction.as' % (where, frame), b, off, off + ln,
                           '%s fotograma %d, DoAction (%s)' % (where, frame, src),
                           dict(tag=tagf, a0=off, a1=off + ln, fix=fx))
            elif code in (26, 70):
                r = place_actions(b, off, ln, code)
                if r:
                    depth, nm, evs = r
                    for ev, a0, a1, szo in evs:
                        self.write('%s/frame_%04d/colocacion_d%d%s/%s.as' % (
                            where, frame, depth, ('_' + safe(nm)) if nm else '', safe(ev)),
                            b, a0, a1, '%s fotograma %d, clip en profundidad %d (%s)' % (where, frame, depth, src),
                            dict(tag=tagf, a0=a0, a1=a1, fix=fx + [['u32', szo]]))
            elif code == 1:
                frame += 1

    def run(self):
        import shutil
        shutil.rmtree(os.path.join(self.out, 'scripts'), ignore_errors=True)  # regenerar limpio
        tags = self.m['tags']
        cache = {}

        def top_body(t):
            if t['file'] not in cache:
                cache.clear()
                cache[t['file']] = open(os.path.join(self.p1, 'tags', t['file']), 'rb').read()
            return cache[t['file']]

        # escenario principal
        items = []
        for t in tags:
            if t['code'] in (12, 26, 70, 1):
                items.append((t['code'], 0, t['len'], t, None))
        self.timeline('escenario', items,
                      lambda t: open(os.path.join(self.p1, 'tags', t['file']), 'rb').read())
        # sprites, DoInitAction y botones
        for t in tags:
            c = t['code']
            if c == 39:
                b = open(os.path.join(self.p1, 'tags', t['file']), 'rb').read()
                inner = [(c2, o2, l2, t['file'], (o2 - (6 if lh else 2), lh)) for c2, lh, o2, l2 in read_tags(b, 4, len(b))
                         if c2 in (12, 26, 70, 1)]
                if any(x[0] in (12, 26, 70) for x in inner):
                    self.timeline('DefineSprite_%s' % self.label(t['id']), inner, lambda f, b=b: b)
            elif c == 59:
                b = open(os.path.join(self.p1, 'tags', t['file']), 'rb').read()
                sid = struct.unpack_from('<H', b, 0)[0]
                self.write('DoInitAction/DefineSprite_%s.as' % self.label(sid), b, 2, len(b),
                           'DoInitAction del sprite %d (%s)' % (sid, t['file']),
                           dict(tag=t['file'], a0=2, a1=len(b), fix=[]))
            elif c == 34:
                b = open(os.path.join(self.p1, 'tags', t['file']), 'rb').read()
                for ev, a0, a1, szo in button_actions(b):
                    self.write('DefineButton2_%s/%s.as' % (self.label(t['id']), safe(ev)), b, a0, a1,
                               'boton %d (%s)' % (t['id'], t['file']),
                               dict(tag=t['file'], a0=a0, a1=a1, fix=[['u16', szo]] if szo is not None else []))
            elif c == 7:
                b = open(os.path.join(self.p1, 'tags', t['file']), 'rb').read()
                p = 2
                while b[p]:
                    r = Bits(b, p + 5); r.matrix(); p = r.p
                self.write('DefineButton_%s/on(release).as' % self.label(t['id']), b, p + 1, len(b),
                           'boton %d (%s)' % (t['id'], t['file']),
                           dict(tag=t['file'], a0=p + 1, a1=len(b), fix=[]))
        json.dump(self.index, open(os.path.join(self.out, 'index.json'), 'w'), indent=1, ensure_ascii=False)
        return self.index


if __name__ == '__main__':
    sys.setrecursionlimit(20000)
    idx = Walker(sys.argv[1], sys.argv[2]).run()
    n = len(idx)
    err = [x for x in idx if x['error']]
    g = [x for x in idx if x['gotos']]
    print('scripts:', n)
    print('estructurados sin goto:', n - len(err) - len(g))
    print('con algun goto:', len(g), '| gotos totales:', sum(x['gotos'] for x in idx))
    print('sin estructurar (solo pcode):', len(err))
    for x in err[:12]: print('   ', x['file'], '->', x['error'][:110])
    print('lineas de AS2:', sum(x['lines'] for x in idx))
    tot = sum(x.get('ins', 0) for x in idx); mis = sum(x.get('missing', 0) for x in idx)
    print('instrucciones: %d | reflejadas en el AS2: %d (%.3f%%)' % (tot, tot - mis, 100.0 * (tot - mis) / max(tot, 1)))
    for x in sorted(idx, key=lambda x: -x.get('missing', 0))[:8]:
        if x.get('missing'): print('   sin reflejar %d en %s' % (x['missing'], x['file']))
