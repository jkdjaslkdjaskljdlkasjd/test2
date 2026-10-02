# I31 — fondos de zona (sprite 2908 = KrinScreen)
# Zona 1 (PRISON) y Zona 5 (CITY/Hew): vuelven al arte original (sin HD).
# Zona 4 (TUNNELS/Labyrinth) y Zona 6 (ROME/Il Sanctus): imagen HD a pantalla completa.
import sys, os, struct, json, shutil, io
sys.path.insert(0, '/home/claude/w/paso5/tools')
from swfsplit import read_tags

HD_TUNNELS = (4319, 4320)   # se reutilizan los ids del Pawn Shop (ya no se usa)
HD_ROME    = (4323, 4324)   # se reutilizan los ids de la prision HD (ya no se usa)

def raw_tags(body):
    """[(code, bytes_cuerpo)] de los tags internos de un DefineSprite."""
    out = []
    for code, lh, o, ln in read_tags(body, 4, len(body)):
        out.append((code, body[o:o+ln], lh))
    return out

def frames_of(tags):
    fr = [[]]
    for t in tags:
        code = t[0]
        if code == 0:
            continue
        fr[-1].append(t)
        if code == 1:
            fr.append([])
    return fr  # cada fotograma termina con su ShowFrame; el ultimo queda vacio

def pack(code, b, long_hdr=False):
    if long_hdr or len(b) >= 63:
        return struct.pack('<HI', (code << 6) | 63, len(b)) + b
    return struct.pack('<H', (code << 6) | len(b)) + b

def place(depth, char):          # PlaceObject2 con personaje y matriz identidad
    return (26, bytes([0x06]) + struct.pack('<HH', depth, char) + b'\x00', False)

def remove(depth):               # RemoveObject2
    return (28, struct.pack('<H', depth), False)

def is_place(t, depth=None, char=None):
    code, b = t[0], t[1]
    if code not in (26, 70):
        return False
    f = b[0]; i = 1 + (1 if code == 70 else 0)
    d = struct.unpack_from('<H', b, i)[0]; i += 2
    if code == 70 and (b[1] & 8):
        i = b.index(b'\0', i) + 1
    c = struct.unpack_from('<H', b, i)[0] if f & 2 else None
    return (depth is None or d == depth) and (char is None or c == char)

def is_remove(t, depth):
    return t[0] == 28 and struct.unpack_from('<H', t[1], 0)[0] == depth

def insert_before_showframe(frame, items):
    return frame[:-1] + items + frame[-1:]

def build_sprite(act_body, base_body):
    sid, nfr = struct.unpack_from('<HH', act_body, 0)
    A = frames_of(raw_tags(act_body))
    B = frames_of(raw_tags(base_body))
    # Fotograma 1 (PRISON) y 16 (CITY/Hew): exactamente como el juego base.
    for n in (1, 16):
        A[n-1] = B[n-1]
    # Fotograma 60 (TUNNELS): sin borde 2812 (prof. 47) y con la imagen HD en la prof. 26.
    f = A[59]
    assert any(is_remove(t, 26) for t in f), 'TUNNELS deberia quitar la prof. 26'
    A[59] = insert_before_showframe(f, [remove(47), place(26, HD_TUNNELS[1])])
    # Fotograma 73 (ROME): quitar lo que haya en 26 (HD de TUNNELS) y poner la HD de ROME.
    A[72] = insert_before_showframe(A[72], [remove(26), place(26, HD_ROME[1])])
    # Fotograma 86 (CASINO, primera zona sin HD despues de ROME): quitar la HD y reponer el borde.
    A[85] = insert_before_showframe(A[85], [remove(26), place(47, 2812)])
    body = struct.pack('<HH', sid, nfr)
    for fr in A:
        for t in fr:
            body += pack(*t)
    body += b'\x00\x00'   # End
    return body

def village_shape(body4320):
    """Forma 4318 (pueblo HD) con la geometria de pantalla completa de 4320: la de I23 quedaba
    2,5 unidades corta a la derecha y 1,15 abajo (6 px y 3 px en 2560x1440)."""
    import struct
    b = bytearray(body4320)
    assert struct.unpack_from('<H', b, 0)[0] == 4320
    struct.pack_into('<H', b, 0, 4318)
    old = bytes([0x01, 0x41]) + struct.pack('<H', 4319)
    assert bytes(b).count(old) == 1
    i = bytes(b).index(old)
    b[i:i + 4] = bytes([0x01, 0x41]) + struct.pack('<H', 4317)
    return bytes(b)
