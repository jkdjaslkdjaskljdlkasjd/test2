# I38 - prueba: New Alcatraz (Zona 1, PRISON, fotograma 1 de KrinScreen 2908) con imagen HD a pantalla completa.
#   - fotograma 1: quita el marco 47 y pone la forma HD en la profundidad 26 (los anillos 27/31/35 y los botones quedan);
#   - fotograma 16 (CITY/Hew): ANTES de colocar su fondo 2818 en la 26, quita la 26 y repone el marco 47.
#     Sin esto vuelve el bug de Hew (I31): el salto hacia adelante pasa por el fotograma 1 y Flash/AIR ignora la
#     colocacion de CITY en una profundidad ocupada. VILLAGE (31) ya quita 26 y 47.
#   - ids nuevos 4400 (bitmap) y 4401 (forma, copia de 4320 con otro bitmap), antes de la definicion de 2908.
import os, sys, struct, io
D = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(D)
sys.path.insert(0, os.path.join(W, 'i31'))
import zonas
from PIL import Image
BMP, SHP = 4400, 4401
# fuente: la imagen del usuario (1672x941) ampliada x4 con Real-ESRGAN realesr-animevideov3 (herramientas/esrgan_np.py)
# y bajada con Lanczos a 2560x1440
SRC = os.path.join(D, 'fuente/zonas/PRISON_Z1_v2_2560x1440_esrgan.png')   # I41: version 2 del usuario (02/10)

def preparar():
    import calidad
    im = Image.open(SRC).convert('RGB')
    assert im.size == (2560, 1440)
    return calidad.jpeg2(BMP, im)   # I40: JPEG 97 4:4:4

def tag(code, body):
    return {'code': code, 'body': body}

def aplicar(p, P1):
    m = p.m['tags']
    t2908 = p.byid[2908]
    code, body = p.replace[t2908['file']]          # el 2908 que ya armo I31
    sid, nfr = struct.unpack_from('<HH', body, 0)
    F = zonas.frames_of(zonas.raw_tags(body))
    assert any(zonas.is_place(t, 47, 2812) for t in F[0]) and any(zonas.is_place(t, 26, 2818) for t in F[15])
    F[0] = zonas.insert_before_showframe(F[0], [zonas.remove(47), zonas.place(26, SHP)])
    F[15] = [zonas.remove(26), zonas.place(47, 2812)] + F[15]
    nb = struct.pack('<HH', sid, nfr)
    for fr in F:
        for t in fr:
            nb += zonas.pack(*t)
    nb += b'\x00\x00'
    p.replace[t2908['file']] = (39, nb)
    # bitmap y forma nuevos, justo antes de la definicion de 2908
    b4320 = open(os.path.join(P1, 'tags', p.byid[4320]['file']), 'rb').read()
    sh = bytearray(b4320); struct.pack_into('<H', sh, 0, SHP)
    old = bytes([0x01, 0x41]) + struct.pack('<H', 4319); assert bytes(sh).count(old) == 1
    i = bytes(sh).index(old); sh[i + 2:i + 4] = struct.pack('<H', BMP)
    pos = next(k for k, t in enumerate(m) if t.get('id') == 2908 and t['name'] == 'DefineSprite')
    ents = []
    for c, b, cid, name in ((21, preparar(), BMP, 'DefineBitsJPEG2'), (2, bytes(sh), SHP, 'DefineShape')):
        fn = 'nuevo_I38_%d.bin' % cid
        ents.append({'code': c, 'name': name, 'long': True, 'len': len(b), 'id': cid, 'file': fn})
        p.replace[fn] = (c, b)
    m[pos:pos] = ents
    p.log.append('I38: PRISON (Zona 1) con HD %d/%d en la 26 del fotograma 1; CITY quita la 26 y repone el 47' % (BMP, SHP))
