# Lista de visualizacion de un sprite en un fotograma de I25 (profundidad, personaje, nombre, matriz, forma):
#   python3 dl.py ID FOTOGRAMA
# Con esto se midieron las piezas del menu (sprite 3239, fotograma 25) para el menu 2K. Usa las mismas carpetas
# que build.py (../i25 y ../paso5/tools).
import sys, os, json, struct
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'paso5', 'tools'))
from swfpatch import Patcher
from swfshape import Bits
P1 = os.path.join(AQUI, '..', 'i25', 'paso1'); P3 = os.path.join(AQUI, '..', 'i25', 'paso3')
p = Patcher(P1, P3)
SYM = json.load(open(os.path.join(P1, 'symbols.json')))

def tags_of(body, start):
    i = start; out = []
    while i < len(body):
        h = struct.unpack_from('<H', body, i)[0]; code = h >> 6; ln = h & 63; hl = 2
        if ln == 63:
            ln = struct.unpack_from('<I', body, i + 2)[0]; hl = 6
        out.append((code, body[i + hl:i + hl + ln]))
        i += hl + ln
        if code == 0: break
    return out

def cxform(r):
    r.align(); has_add = r.ub(1); has_mult = r.ub(1); n = r.ub(4)
    m = [1, 1, 1, 1]; a = [0, 0, 0, 0]
    if has_mult: m = [r.sb(n) / 256.0 for _ in range(4)]
    if has_add: a = [r.sb(n) for _ in range(4)]
    r.align(); return (m, a)

def place(code, body):
    r = Bits(body, 0)
    f = r.u8(); f2 = 0
    if code == 70: f2 = r.u8()
    d = {'move': f & 1}
    d['depth'] = r.u16()
    if code == 70 and (f2 & 0x08 or (f2 & 0x10 and f & 0x02)):
        s = b''
        while body[r.p] != 0: s += bytes([body[r.p]]); r.p += 1
        r.p += 1; d['class'] = s.decode('latin1')
    if f & 0x02: d['char'] = r.u16()
    if f & 0x04: d['matrix'] = r.matrix()
    if f & 0x08: d['cx'] = cxform(r)
    if f & 0x10: d['ratio'] = r.u16()
    if f & 0x20:
        s = b''
        while body[r.p] != 0: s += bytes([body[r.p]]); r.p += 1
        r.p += 1; d['name'] = s.decode('latin1')
    if f & 0x40: d['clip'] = r.u16()
    if code == 70:
        if f2 & 0x01: d['filters'] = True
        if f2 & 0x02: r.align(); d['blend'] = body[r.p] if not (f2 & 0x01) else '?'
        if f2 & 0x04: d['cache'] = True
    return d

def display(tags, frame_want):
    dl = {}; frame = 1; labels = {}
    for code, body in tags:
        if code in (26, 70):
            d = place(code, body)
            if d['move'] and d['depth'] in dl:
                old = dl[d['depth']]; old.update({k: v for k, v in d.items() if k != 'move'})
            else:
                dl[d['depth']] = dict(d)
        elif code == 28:
            dep = struct.unpack_from('<H', body, 0)[0]; dl.pop(dep, None)
        elif code == 5:
            dep = struct.unpack_from('<H', body, 2)[0]; dl.pop(dep, None)
        elif code == 43:
            labels[frame] = body.split(b'\0')[0].decode('latin1')
        elif code == 1:
            if frame == frame_want: return dl
            frame += 1
    return dl

def shape_rect(cid):
    t = p.byid.get(cid)
    if not t or not t['name'].startswith('DefineShape'): return None
    code, b = p.tag_body(t)
    r = Bits(b, 2); x0, x1, y0, y1 = r.rect()
    return (x0 / 20, y0 / 20, x1 / 20, y1 / 20)

def body_of(cid):
    t = p.byid[cid]; code, b = p.tag_body(t); return b

if __name__ == '__main__':
    cid = int(sys.argv[1]); fr = int(sys.argv[2])
    tags = tags_of(body_of(cid), 4)
    dl = display(tags, fr)
    for dep in sorted(dl):
        d = dl[dep]; c = d.get('char'); t = p.byid.get(c)
        kind = t['name'] if t else '?'
        ex = SYM.get(str(c), {}).get('exports')
        m = d.get('matrix'); ms = ''
        if m: ms = 'sx=%.3f sy=%.3f r=%.3f,%.3f t=(%.1f,%.1f)' % (m[0], m[3], m[1], m[2], m[4] / 20, m[5] / 20)
        rc = shape_rect(c) if c else None
        print(dep, c, kind, d.get('name', ''), ex or '', ms, 'clip=%s' % d['clip'] if 'clip' in d else '', 'rect=%s' % (rc,) if rc else '', 'cx' if 'cx' in d else '', 'filt' if d.get('filters') else '')
