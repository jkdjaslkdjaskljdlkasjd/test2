# I40 - Zona 3 (Ivory Line, el tren; etiqueta TRAIN, fotograma 46 de KrinScreen 2908) con imagen HD.
#
# En el original, el vagon parpadea entre luz calida y luz azul: el sprite 2846 (dentro de 2847) le aplica a la
# imagen un ColorMatrixFilter distinto en cada uno de sus 56 fotogramas. El usuario mando las dos versiones HD
# (calida y azul). Aca se arma un sprite nuevo de 56 fotogramas con las dos imagenes (la azul encima) que sigue
# la misma secuencia: en cada fotograma se lee el filtro del original, se decide si es azul o calido (aplicandolo
# a un naranja del vagon) y su brillo, y se pone con transformacion de color (alfa de la azul y brillo).
#
# Las luces que pasan por las ventanas (2837, en 2847) quedan debajo de la imagen HD: el usuario va a decidir si
# se rehacen.
#
# ids nuevos: 4402/4403 (bitmap y forma calida), 4404/4405 (azul), 4406 (sprite). Van antes de la definicion de 2908.
# En 2908, fotograma 46: la colocacion de 2848 en la 26 pasa a ser 4406, y se quita el marco 47.
import os, sys, struct
D = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(D)
sys.path.insert(0, os.path.join(W, 'i31'))
import zonas, calidad
from PIL import Image

BMP_C, SHP_C, BMP_A, SHP_A, SPR = 4402, 4403, 4404, 4405, 4406
IMG_C = os.path.join(D, 'fuente/zonas/TRAIN_Z3_calido_2560x1440_esrgan.png')
IMG_A = os.path.join(D, 'fuente/zonas/TRAIN_Z3_azul_2560x1440_esrgan.png')
NARANJA = (0.60, 0.35, 0.15)   # color tipico del vagon calido, para clasificar cada filtro
FUERZA_BRILLO = 0.6            # cuanto del cambio de brillo del original se copia (1 = todo)

def tag(code, body):
    if len(body) >= 63:
        return struct.pack('<HI', (code << 6) | 63, len(body)) + body
    return struct.pack('<H', (code << 6) | len(body)) + body

class Bits:
    def __init__(self): self.v = 0; self.n = 0
    def put(self, val, n):
        val &= (1 << n) - 1
        self.v = (self.v << n) | val; self.n += n
    def bytes(self):
        pad = (-self.n) % 8
        v = self.v << pad
        return v.to_bytes((self.n + pad) // 8, 'big')

def cxform(r, g, b, a):
    """CXFORMWITHALPHA solo con multiplicadores (8.8; 256 = 1)."""
    vals = [int(round(x)) for x in (r, g, b, a)]
    nb = max(max(abs(v) for v in vals).bit_length() + 1, 2)
    bt = Bits(); bt.put(0, 1); bt.put(1, 1); bt.put(nb, 4)
    for v in vals:
        bt.put(v, nb)
    return bt.bytes()

def secuencia(P1, byid):
    """[(azul?, brillo)] de los 56 fotogramas de 2846, leyendo su ColorMatrixFilter."""
    b = open(os.path.join(P1, 'tags', byid[2846]['file']), 'rb').read()
    F = zonas.frames_of(zonas.raw_tags(b))
    out = []; m = None
    for fr in F[:-1]:
        for t in fr:
            if t[0] == 70:
                k = t[1].index(bytes([1, 6]), 4)        # lista de filtros: 1 filtro, id 6 = ColorMatrix
                m = struct.unpack_from('<20f', t[1], k + 2)
        o = [sum(m[r * 5 + j] * NARANJA[j] for j in range(3)) + m[r * 5 + 4] / 255 for r in range(3)]
        azul = o[2] > o[0]
        out.append((azul, o[2] if azul else o[0]))
    base_a = min(v for z, v in out if z); base_c = min(v for z, v in out if not z)
    return [(z, 1 + (v / (base_a if z else base_c) - 1) * FUERZA_BRILLO) for z, v in out]

def sprite(seq):
    body = struct.pack('<HH', SPR, len(seq))
    for n, (azul, s) in enumerate(seq):
        k = 256 * s
        c1 = cxform(k, k, k, 256)
        c2 = cxform(k, k, k, 256 if azul else 0)
        if n == 0:
            fr = tag(26, bytes([0x0E]) + struct.pack('<HH', 1, SHP_C) + b'\x00' + c1)
            fr += tag(26, bytes([0x0E]) + struct.pack('<HH', 2, SHP_A) + b'\x00' + c2)
        else:
            fr = tag(26, bytes([0x09]) + struct.pack('<H', 1) + c1)
            fr += tag(26, bytes([0x09]) + struct.pack('<H', 2) + c2)
        body += fr + tag(1, b'')
    return body + b'\x00\x00'

def forma(b4320, sid, bid):
    sh = bytearray(b4320); struct.pack_into('<H', sh, 0, sid)
    old = bytes([0x01, 0x41]) + struct.pack('<H', 4319); assert bytes(sh).count(old) == 1
    i = bytes(sh).index(old); sh[i + 2:i + 4] = struct.pack('<H', bid)
    return bytes(sh)

def aplicar(p, P1):
    m = p.m['tags']
    seq = secuencia(P1, p.byid)
    # 2908, fotograma 46: 2848 -> 4406 en la 26 y sin marco 47
    t2908 = p.byid[2908]
    code, body = p.replace[t2908['file']]
    sid, nfr = struct.unpack_from('<HH', body, 0)
    F = zonas.frames_of(zonas.raw_tags(body))
    f46 = F[45]
    assert any(t[0] == 43 and t[1].rstrip(b'\0') == b'TRAIN' for t in f46)
    hecho = False
    for i, t in enumerate(f46):
        if zonas.is_place(t, 26, 2848):
            f46[i] = zonas.place(26, SPR); hecho = True
    assert hecho
    F[45] = zonas.insert_before_showframe(f46, [zonas.remove(47)])
    nb = struct.pack('<HH', sid, nfr)
    for fr in F:
        for t in fr:
            nb += zonas.pack(*t)
    nb += b'\x00\x00'
    p.replace[t2908['file']] = (39, nb)
    b4320 = open(os.path.join(P1, 'tags', p.byid[4320]['file']), 'rb').read()
    nuevos = [(21, calidad.jpeg2(BMP_C, Image.open(IMG_C)), BMP_C, 'DefineBitsJPEG2'),
              (2, forma(b4320, SHP_C, BMP_C), SHP_C, 'DefineShape'),
              (21, calidad.jpeg2(BMP_A, Image.open(IMG_A)), BMP_A, 'DefineBitsJPEG2'),
              (2, forma(b4320, SHP_A, BMP_A), SHP_A, 'DefineShape'),
              (39, sprite(seq), SPR, 'DefineSprite')]
    pos = next(k for k, t in enumerate(m) if t.get('id') == 2908 and t['name'] == 'DefineSprite')
    ents = []
    for c, b, cid, name in nuevos:
        fn = 'nuevo_I40_%d.bin' % cid
        ents.append({'code': c, 'name': name, 'long': True, 'len': len(b), 'id': cid, 'file': fn})
        p.replace[fn] = (c, b)
    m[pos:pos] = ents
    azules = sum(1 for z, s in seq if z)
    p.log.append('I40: TRAIN (Zona 3) HD: sprite %d de %d fotogramas (%d azules, %d calidos), brillo %.2f-%.2f; '
                 'quita el 47' % (SPR, len(seq), azules, len(seq) - azules, min(s for z, s in seq), max(s for z, s in seq)))
