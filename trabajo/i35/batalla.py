# I32-I35 - piezas nuevas del SWF para los fondos de combate HD.
#   ids nuevos: 4325 contenedor __hdBattleBG, 4326 mascara de la escena como sprite (__hdMask),
#               4327 fondo rojo de la X (__hdSkipXbg), 4328 linea negra de la ventana (__hdMarco),
#               4329-4340 envoltorios de los suelos originales de BATTLESCREEN (__hdSuelo<personaje>),
#               4341+ por cada fondo: bitmap cielo, forma cielo, bitmap suelo (JPEG3), forma suelo, sprite suelo
import os, sys, struct
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D); sys.path.insert(0, '/home/claude/w/paso5/tools')
from placeobj import PO, matrix_bytes
from as2comp import compile_script

import capas
# Fondos: etiqueta del contenedor = nombre de la imagen (combate_<ETIQUETA>.png). Que combate usa cada una
# lo decide _root.__hdBattleMap en hd_batalla.as (ZoneBG|SkyBG -> etiqueta).
CONT, MASK, XBG, MARCO = 4325, 4326, 4327, 4328
# suelos originales de BATTLESCREEN (3343) que se ocultan con HD (personajes del suelo de cada escenario)
SUELOS = [3330, 3331, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3342]
SUELO0 = 4329
FONDOS = []
_id = 4341
for _lab in sorted(capas.BORDES):
    FONDOS.append((_lab, _id, _id + 1, 'build/combate_%s_2560x1440.jpg' % _lab, _id + 2, _id + 3, _id + 4))
    _id += 5

def tag(code, body, long_hdr=False):
    if long_hdr or len(body) >= 63:
        return struct.pack('<HI', (code << 6) | 63, len(body)) + body
    return struct.pack('<H', (code << 6) | len(body)) + body

def po2(depth, char, mat=b'\x00'):
    return tag(26, bytes([0x06]) + struct.pack('<HH', depth, char) + mat)

def sprite(cid, frames):
    """frames: lista de listas de bytes de etiquetas (sin ShowFrame)."""
    body = struct.pack('<HH', cid, len(frames))
    for f in frames:
        body += b''.join(f) + tag(1, b'')
    return body + b'\x00\x00'

def shape_from_4320(body4320, sid, bid):
    b = bytearray(body4320)
    struct.pack_into('<H', b, 0, sid)
    old = bytes([0x01, 0x41]) + struct.pack('<H', 4319)
    assert bytes(b).count(old) == 1
    i = bytes(b).index(old); b[i + 2:i + 4] = struct.pack('<H', bid)
    return bytes(b)

def aplicar(p, P1):
    m = p.m['tags']
    # --- etiquetas nuevas, justo despues del ShowFrame del fotograma 216
    f = 1; pos = None
    for k, t in enumerate(m):
        if t['name'] == 'ShowFrame':
            f += 1
            if f == 217:
                pos = k + 1; break
    t4320 = p.byid[4320]
    b4320 = open(os.path.join(P1, 'tags', t4320['file']), 'rb').read()
    nuevos = []
    frames = [[tag(12, compile_script('stop();\n_root.__hdBattleSetup(this);\n'))]]
    from PIL import Image
    for label, bid, sid, jpg, gbid, gsid, gspr in FONDOS:
        nuevos.append((21, struct.pack('<H', bid) + open(os.path.join(D, jpg), 'rb').read(), bid, 'DefineBitsJPEG2'))
        nuevos.append((2, shape_from_4320(b4320, sid, bid), sid, 'DefineShape'))
        # la forma 4320 esta en coordenadas de KrinScreen (zona en 400; 222,9): se lleva al escenario
        # suelo: misma imagen JPEG con alfa por encima del pie de las montanas
        imj = Image.open(os.path.join(D, jpg)).convert('RGB')
        a = capas.alfa(capas.borde(imj, capas.BORDES[label]))
        nuevos.append((35, capas.jpeg3(gbid, imj, a), gbid, 'DefineBitsJPEG3'))
        nuevos.append((2, shape_from_4320(b4320, gsid, gbid), gsid, 'DefineShape'))
        nuevos.append((39, sprite(gspr, [[po2(1, gsid, matrix_bytes(1, 1, 8000, 4458))]]), gspr, 'DefineSprite'))
        suelo = PO(26, bytes([0x06]) + struct.pack('<HH', 2, gspr) + b'\x00'); suelo.name = '__hdGround'
        frames.append([tag(43, label.encode() + b'\0'), po2(1, sid, matrix_bytes(1, 1, 8000, 4458)),
                       tag(26, suelo.body()), tag(12, compile_script('stop();\n'))])
    nuevos.append((39, sprite(CONT, frames), CONT, 'DefineSprite'))
    nuevos.append((39, sprite(MASK, [[po2(1, 213)]]), MASK, 'DefineSprite'))
    nuevos.append((39, sprite(XBG, [[po2(1, 2919)]]), XBG, 'DefineSprite'))
    nuevos.append((39, sprite(MARCO, [[po2(1, 3349)]]), MARCO, 'DefineSprite'))
    # envoltorio del suelo: se oculta solo si el combate actual tiene HD
    aviso = 'if(_root.__hdHideSuelo == true)\n{\n   this._visible = false;\n}\n'
    for k, ch in enumerate(SUELOS):
        nuevos.append((39, sprite(SUELO0 + k, [[po2(1, ch), tag(12, compile_script(aviso))]]), SUELO0 + k, 'DefineSprite'))
    ents = []
    for code, body, cid, name in nuevos:
        fn = 'nuevo_I32_%d.bin' % cid
        ents.append({'code': code, 'name': name, 'long': True, 'len': len(body), 'id': cid, 'file': fn})
        p.replace[fn] = (code, body)
        p.log.append('nuevo   %s %d' % (name, cid))
    # orden: primero los envoltorios del suelo (los usa 3343) y las piezas, despues los fondos y el contenedor
    m[pos:pos] = ents
    # --- BATTLESCREEN (3343): el suelo de cada escenario HD pasa a su envoltorio con nombre __hdSuelo
    t3343 = p.byid[3343]
    body = open(os.path.join(P1, 'tags', t3343['file']), 'rb').read()
    out = bytearray(body[:4]); i = 4; hechos = 0
    sue = dict((ch, SUELO0 + k) for k, ch in enumerate(SUELOS))
    while i < len(body):
        h = struct.unpack_from('<H', body, i)[0]; code = h >> 6; ln = h & 63; hl = 2
        if ln == 63:
            ln = struct.unpack_from('<I', body, i + 2)[0]; hl = 6
        bd = body[i + hl:i + hl + ln]
        if code in (26, 70):
            o = PO(code, bd)
            if o.char in sue:
                nombre = '__hdSuelo%d' % o.char
                if o.f & 1:
                    # "move" que cambia de personaje (STREETS3): se quita y se vuelve a poner, sin matriz
                    out += tag(28, struct.pack('<H', o.depth))
                    o = PO(26, bytes([0x06]) + struct.pack('<HH', o.depth, sue[o.char]) + b'\x00')
                else:
                    o.char = sue[o.char]
                o.name = nombre; bd = o.body(); code = o.code; hechos += 1
        out += struct.pack('<HI', (code << 6) | 63, len(bd)) + bd if hl == 6 else tag(code, bd)
        i += hl + ln
        if code == 0:
            break
    assert hechos == len(SUELOS), hechos
    p.replace[t3343['file']] = (39, bytes(out))
    p.log.append('sprite  3343 BATTLESCREEN: %d suelos envueltos como __hdSuelo<personaje>' % len(SUELOS))
    # --- fotograma 217: mascara, X, contenedor; fotograma 218: quitar el contenedor
    f = 1; fin217 = None; ini218 = None
    for k, t in enumerate(m):
        if t['name'] == 'ShowFrame':
            if f == 217: fin217 = k
            f += 1
            if f == 218: ini218 = k + 1
            if f > 218: break
            continue
        if f == 217 and t['name'] in ('PlaceObject2', 'PlaceObject3'):
            body = open(os.path.join(P1, 'tags', t['file']), 'rb').read()
            o = PO(t['code'], body)
            if o.depth == 72 and o.char == 213:
                o.char = MASK; o.name = '__hdMask'
            elif o.depth == 644 and o.char == 3408:
                o.name = '__hdSkipX'
            elif o.depth == 646 and o.char == 2919:
                o.char = XBG; o.name = '__hdSkipXbg'
            elif o.depth == 341 and o.char == 3349:
                o.char = MARCO; o.name = '__hdMarco'
            else:
                continue
            p.replace[t['file']] = (t['code'], o.body())
            p.log.append('fot.217 profundidad %d -> %s' % (o.depth, o.name))
    cont = PO(26, bytes([0x06]) + struct.pack('<HH', 58, CONT) + b'\x00')
    cont.name = '__hdBattleBG'
    e1 = {'code': 26, 'name': 'PlaceObject2', 'long': False, 'len': 0, 'id': None, 'file': 'nuevo_I32_place58.bin'}
    p.replace[e1['file']] = (26, cont.body())
    m.insert(fin217, e1)
    e2 = {'code': 28, 'name': 'RemoveObject2', 'long': False, 'len': 2, 'id': None, 'file': 'nuevo_I32_remove58.bin'}
    p.replace[e2['file']] = (28, struct.pack('<H', 58))
    m.insert(ini218 + 1, e2)
    p.log.append('fot.217 contenedor __hdBattleBG en la profundidad 58; fot.218 lo quita')
    return ['__hdSuelo%d' % ch for ch in SUELOS]
