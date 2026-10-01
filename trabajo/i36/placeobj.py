# Lectura y escritura de PlaceObject2/3 (lo justo para cambiar personaje, matriz y nombre).
import struct, sys
sys.path.insert(0, '/home/claude/w/paso5/tools')
from swfshape import Bits

def _skip_cxform(b, p):
    r = Bits(b, p)
    has_add = r.ub(1); has_mult = r.ub(1); n = r.ub(4)
    if has_mult: [r.sb(n) for _ in range(4)]
    if has_add: [r.sb(n) for _ in range(4)]
    r.align(); return r.p

class PO:
    """Partes: pre (flags+profundidad+clase), char, matriz (bytes), resto antes del nombre, nombre, cola."""
    def __init__(self, code, body):
        self.code = code; b = body; p = 0
        self.f = b[0]; p = 1
        self.f2 = None
        if code == 70:
            self.f2 = b[1]; p = 2
        self.depth = struct.unpack_from('<H', b, p)[0]; p += 2
        self.cls = b''
        if code == 70 and (self.f2 & 0x08):
            j = b.index(b'\0', p); self.cls = b[p:j + 1]; p = j + 1
        self.char = None
        if self.f & 0x02:
            self.char = struct.unpack_from('<H', b, p)[0]; p += 2
        self.mat = None
        if self.f & 0x04:
            r = Bits(b, p); self.m = r.matrix(); r.align(); self.mat = b[p:r.p]; p = r.p
        q = p
        if self.f & 0x08: q = _skip_cxform(b, q)
        if self.f & 0x10: q += 2
        self.mid = b[p:q]; p = q
        self.name = None
        if self.f & 0x20:
            j = b.index(b'\0', p); self.name = b[p:j].decode('latin1'); p = j + 1
        self.tail = b[p:]
    def body(self):
        f = self.f
        f = (f | 0x02) if self.char is not None else (f & ~0x02)
        f = (f | 0x04) if self.mat is not None else (f & ~0x04)
        f = (f | 0x20) if self.name is not None else (f & ~0x20)
        out = bytes([f])
        if self.code == 70: out += bytes([self.f2])
        out += struct.pack('<H', self.depth) + self.cls
        if self.char is not None: out += struct.pack('<H', self.char)
        if self.mat is not None: out += self.mat
        out += self.mid
        if self.name is not None: out += self.name.encode('latin1') + b'\0'
        return out + self.tail

def matrix_bytes(sx, sy, tx, ty):
    """MATRIX con escala (sin rotacion) y traslacion en twips."""
    bits = []
    def ub(v, n): bits.extend((v >> (n - 1 - i)) & 1 for i in range(n))
    def sbits(vals):
        n = 1
        for v in vals:
            while not (-(1 << (n - 1)) <= v < (1 << (n - 1))): n += 1
        return n
    if sx == 1 and sy == 1:
        ub(0, 1)
    else:
        a, d = int(round(sx * 65536)), int(round(sy * 65536)); n = sbits([a, d])
        ub(1, 1); ub(n, 5); ub(a & ((1 << n) - 1), n); ub(d & ((1 << n) - 1), n)
    ub(0, 1)
    n = sbits([tx, ty]) if (tx or ty) else 0
    ub(n, 5)
    if n: ub(tx & ((1 << n) - 1), n); ub(ty & ((1 << n) - 1), n)
    while len(bits) % 8: bits.append(0)
    return bytes(int(''.join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))
