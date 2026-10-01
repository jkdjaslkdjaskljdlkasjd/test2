# I26–I29 (sobre I25): rework del lobo (propuesta v4, "Mokoshotar: sangre y escarcha"); I28 ordena el arbol por nivel; I29 escudo del juego.
#
#   python3 build.py SALIDA.swf [--debug] [--sin-rework]
#
# Parte del SONNY2.swf de I25 (37a95f71...), separado con swfsplit.py y descompilado con swfcode.py
# (herramientas del paso 5). Cambios:
#  1. Script principal (fotograma 42, DoAction_2): se agrega al final la capa del rework (src/*.as, en
#     orden). Las capas viejas del lobo quedan en el archivo pero inertes (ver src/rw_00_base.as).
#  2. Reloj de combate (fotograma 217, battleClocker): la esquiva pasa por _root.__rwNoDodge
#     (Hunted y Killer Instinct no se pueden esquivar) y el turno extra de Call of the Ancestors.
#  3. Iconos de prueba: fotogramas nuevos en el sprite de iconos de habilidades (2186), copia del dibujo
#     de una habilidad parecida con un tinte por rama, y etiquetas nuevas en el sprite de estados (1986)
#     sobre fotogramas que ya existen. No se genera ninguna imagen.
import sys, os, re, json, struct, hashlib, glob
AQUI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(AQUI, '..', 'paso5', 'tools')
sys.path.insert(0, TOOLS); sys.path.insert(0, AQUI)
from swfpatch import Patcher

BASE = os.path.join(AQUI, '..', 'i25')
P1 = os.path.join(BASE, 'paso1'); P3 = os.path.join(BASE, 'paso3')
REL = 'escenario/frame_0042/DoAction_2.as'
CLOCK = 'escenario/frame_0217/colocacion_d480_battleClocker/onClipEvent(enterFrame).as'

out = sys.argv[1]
debug = '--debug' in sys.argv
sin_rework = '--sin-rework' in sys.argv
log = []
p = Patcher(P1, P3)


# ------------------------------------------------------------------ utilidades de etiquetas
def tags_of(body, start):
    """(codigo, cuerpo) de las etiquetas internas de un DefineSprite, hasta End incluido."""
    i = start; out = []
    while i < len(body):
        h = struct.unpack_from('<H', body, i)[0]; code = h >> 6; ln = h & 63; hl = 2
        if ln == 63:
            ln = struct.unpack_from('<I', body, i + 2)[0]; hl = 6
        out.append((code, body[i + hl:i + hl + ln]))
        i += hl + ln
        if code == 0:
            break
    return out


def tag_bytes(code, body):
    if len(body) >= 63 or code in (2, 22, 32, 83, 36, 20, 21, 35, 90, 26, 70):
        return struct.pack('<HI', (code << 6) | 63, len(body)) + body
    return struct.pack('<H', (code << 6) | len(body)) + body


def sprite_body(cid):
    t = p.byid[cid]
    code, b = p.tag_body(t)
    return t, code, b


class Bits:
    def __init__(self): self.v = []
    def u(self, x, n):
        for k in range(n - 1, -1, -1): self.v.append((x >> k) & 1)
    def s(self, x, n): self.u(x & ((1 << n) - 1), n)
    def bytes(self):
        v = self.v + [0] * (-len(self.v) % 8)
        return bytes(int(''.join(map(str, v[i:i + 8])), 2) for i in range(0, len(v), 8))


def nbits_signed(vals):
    n = 1
    for x in vals:
        while not (-(1 << (n - 1)) <= x < (1 << (n - 1))): n += 1
    return n


def cxform_alpha(mult, add):
    """CXFORMWITHALPHA con multiplicadores (0..1) y sumas (-255..255) para R, G, B (alfa sin cambios)."""
    mm = [int(round(m * 256)) for m in mult] + [256]
    aa = list(add) + [0]
    n = nbits_signed(mm + aa)
    b = Bits(); b.u(1, 1); b.u(1, 1); b.u(n, 4)
    for x in mm: b.s(x, n)
    for x in aa: b.s(x, n)
    return b.bytes()


def parse_matrix(body, pos):
    """Devuelve (fin_en_bytes) de un MATRIX que empieza en pos."""
    bits = ''.join('{:08b}'.format(x) for x in body[pos:pos + 40])
    k = 0
    if bits[k] == '1':
        k += 1; n = int(bits[k:k + 5], 2); k += 5 + 2 * n
    else:
        k += 1
    if bits[k] == '1':
        k += 1; n = int(bits[k:k + 5], 2); k += 5 + 2 * n
    else:
        k += 1
    n = int(bits[k:k + 5], 2); k += 5 + 2 * n
    return pos + (k + 7) // 8


# ------------------------------------------------------------------ 1. iconos de habilidades (sprite 2186)
# nombre nuevo -> (nombre existente cuyo dibujo se copia, rama para el tinte)
NUEVOS = [
    ("Rupture", "Deep Wounds", "hunt"), ("Killer Instinct", "Werezombie", "hunt"),
    ("Black Ice", "Cold Trail", "winter"), ("Feeding Frenzy", "Pack Tactics", "pack"),
    ("Frostbound Pack", "Winter Heart", "pack"), ("Taste of Blood", "Iron Jaws", "endurance"),
    ("Rime Coat", "Thick Hide", "endurance"), ("Ice Tomb", "Last Stand", "endurance"),
    ("Bloodhound", "Predator's Patience", "hunt"), ("Shardfall", "Shatter Guard", "winter"),
    ("Frozen Blood", "Frost Fang", "winter"), ("Winter's Grip", "Wicked Claws", "winter"),
    ("Cold Snap", "Howl of the Ancestors", "winter"), ("Shared Hunger", "Rallying Cry", "pack"),
    ("Cold Comfort", "Echo Ward", "pack"), ("Blood Drinker", "Second Wind", "endurance"),
    ("Blood Moon Rising", "Scent of Blood", "aspect"), ("Endless Winter", "Cold Trail", "aspect"),
    ("Call of the Ancestors", "Howl of the Ancestors", "aspect"), ("Frozen Maw", "Wicked Claws", "winter"),
]
TINTE = {"hunt": ((1.0, 0.55, 0.55), (45, 0, 0)), "winter": ((0.55, 0.85, 1.0), (0, 25, 60)),
         "pack": ((1.0, 0.85, 0.45), (45, 30, 0)), "endurance": ((0.75, 1.0, 0.75), (0, 35, 10)),
         "aspect": ((0.85, 0.55, 1.0), (45, 0, 65))}
# ids de las habilidades (los mismos que en src/rw_10_data.as) para el mapa fotograma -> id
IDS = {"Werezombie": 809, "Rake": 861, "Canine Instincts": 862, "Howl of the Ancestors": 863, "Iron Jaws": 864,
       "Wicked Claws": 865, "Primal Breath": 808, "Pounce": 810, "Scent of Blood": 811, "Hamstring": 812,
       "Deep Wounds": 814, "Frost Fang": 815, "Shatter Guard": 816, "Predator's Patience": 817,
       "Cold Trail": 818, "Cull the Weak": 819, "Relentless Hunt": 820, "Rallying Cry": 821,
       "Guardian's Call": 822, "Pack Tactics": 823, "Echo Ward": 824, "Thick Hide": 825, "Second Wind": 826,
       "Last Stand": 827, "Unyielding": 828, "Winter Heart": 829, "Undying Will": 830,
       "Rupture": 831, "Killer Instinct": 832, "Black Ice": 833, "Feeding Frenzy": 834, "Frostbound Pack": 835,
       "Taste of Blood": 836, "Rime Coat": 837, "Ice Tomb": 838, "Bloodhound": 839, "Shardfall": 840,
       "Frozen Blood": 841, "Winter's Grip": 842, "Cold Snap": 843, "Shared Hunger": 844, "Cold Comfort": 845,
       "Blood Drinker": 846, "Blood Moon Rising": 854, "Endless Winter": 855, "Call of the Ancestors": 856,
       "Frozen Maw": 857}

t2186, code2186, b2186 = sprite_body(2186)
head = b2186[:4]
nframes = struct.unpack_from('<H', b2186, 2)[0]
tg = tags_of(b2186, 4)
assert tg[-1][0] == 0
# dibujo de cada etiqueta existente: la colocacion en la profundidad 5 de su fotograma
frame = 1; label_frame = {}; place5 = {}; stop_action = None; cur_label = None
for code, body in tg:
    if code == 43:
        cur_label = body.split(b'\0')[0].decode('latin1'); label_frame[cur_label] = frame
    if code == 70 and frame >= 987:
        depth = struct.unpack_from('<H', body, 2)[0]
        if depth == 5 and body[0] & 0x02:
            place5[frame] = body
    if code == 12 and frame >= 987 and stop_action is None:
        stop_action = body
    if code == 1:
        frame += 1; cur_label = None
assert frame - 1 == nframes == 1014, (frame, nframes)
nuevos_tags = []
frame_ids = {}
for nombre, desde in label_frame.items():
    if nombre in IDS and 987 <= desde <= 1014:
        frame_ids[desde] = IDS[nombre]
f = nframes
for nombre, fuente, rama in NUEVOS:
    f += 1
    src = place5[label_frame[fuente]]
    # PlaceObject3 (flags1, flags2, depth, charId, matrix) -> PlaceObject2 con transformacion de color
    assert src[1] in (0, 2), 'PlaceObject3 con extras'   # 0x02: solo modo de mezcla (normal)
    cid = struct.unpack_from('<H', src, 4)[0]
    mend = parse_matrix(src, 6)
    matrix = src[6:mend]
    mult, add = TINTE[rama]
    po2 = bytes([0x0E]) + struct.pack('<HH', 5, cid) + matrix + cxform_alpha(mult, add)
    nuevos_tags += [(43, nombre.encode('latin1') + b'\0'), (28, struct.pack('<H', 5)), (26, po2), (12, stop_action), (1, b'')]
    frame_ids[f] = IDS[nombre]
body = bytearray(head[:2] + struct.pack('<H', f))
for code, bd in tg[:-1] + nuevos_tags + [(0, b'')]:
    body += tag_bytes(code, bd)
p.replace[t2186['file']] = (code2186, bytes(body))
log.append('iconos  sprite 2186: %d fotogramas nuevos (%d-%d)' % (f - nframes, nframes + 1, f))

# ------------------------------------------------------------------ 2. iconos de estado (sprite 1986): etiquetas nuevas
ESTADOS = {
    "RWWOUND": "RAKE", "RWWOUNDH": "RAKE", "RWSCENT": "M10SCENT", "RWHUNTED": "M10EXPOSE",
    "RWSOLID": "M55FROZEN", "RWFRAGILE": "FRAGILE", "RWHEMO": "M10TRAIL", "RWTORN": "M10TRAIL",
    "RWSILENCE": "SILENCED", "RWSTUN": "HOWLOFTHEANCESTORS", "RWCRIPPLE": "M10HAMSTRING",
    "RWDREAD": "M55DREAD", "RWHAM1": "M10HAMSTRING", "RWHAM2": "M10HAMSTRING", "RWJAWS": "IRONJAWS",
    "RWWICKED": "WICKEDCLAWS", "RWBLACKICE": "WICKEDCLAWS", "RWTERROR": "M10EXPOSE", "RWWSLOW": "WICKEDCLAWS",
    "RWRUSH1": "M55COURAGE", "RWRUSH2": "M55COURAGE", "RWRUSH3": "M55COURAGE", "RWKILLER1": "MOKOWEREZOMBIE",
    "RWKILLER2": "MOKOWEREZOMBIE", "RWSHARD": "M10WARD", "RWRIME": "M10STAND", "RWTOMB": "M55FROZEN",
    "RWCANINE1": "CANINEINSTINCTS", "RWCANINE2": "CANINEINSTINCTS", "RWCANINEH": "CANINEINSTINCTS",
    "RWFRENZY": "M10PRIMAL", "RWFROSTPACK": "M10PRIMAL", "RWCOURAGE": "M55COURAGE", "RWGUARD": "M10GUARD",
    "RWGUARDSH": "M55GUARDSELF", "RWWARD": "M10WARD", "RWPRIMAL1": "M10PRIMAL", "RWPRIMAL2": "M10PRIMAL",
    "RWPRIMALEND": "M10PRIMAL", "RWWERE1": "MOKOWEREZOMBIE", "RWWERE2": "MOKOWEREZOMBIE",
    "RWSTAND1": "M10STAND", "RWSTAND2": "M10STAND", "RWANCFORM": "M10WIND", "RWCALL": "M10WIND",
    "RWSPENT": "M10EXPOSE", "RWBLESS": "M10UNDYING", "RWBMOON": "M10SCENT", "RWEWINTER": "WICKEDCLAWS",
    "RWSTUNIMM": "M10STAND", "RWSPIRIT": "M10WIND",
    "RWSH_WARD": "M10WARD", "RWSH_GUARD": "M55GUARDSELF", "RWSH_HEART": "M10WARD", "RWSH_HUNGER": "M10WARD",
    "RWSH_DRINK": "M10WARD", "RWSH_UNDY": "M10UNDYING",
}
for n in range(1, 8):
    ESTADOS["RWFROST%d" % n] = "WICKEDCLAWS"
t1986, code1986, b1986 = sprite_body(1986)
tg = tags_of(b1986, 4)
frame = 1; lab = {}
for code, bd in tg:
    if code == 43: lab[bd.split(b'\0')[0].decode('latin1')] = frame
    if code == 1: frame += 1
por_frame = {}
for nuevo, viejo in ESTADOS.items():
    assert viejo in lab, viejo
    por_frame.setdefault(lab[viejo], []).append(nuevo)
body = bytearray(b1986[:4]); frame = 1; puestas = 0
for code, bd in tg:
    if code == 1 and frame in por_frame:
        for nm in sorted(por_frame[frame]):
            body += tag_bytes(43, nm.encode('latin1') + b'\0'); puestas += 1
    body += tag_bytes(code, bd)
    if code == 1: frame += 1
p.replace[t1986['file']] = (code1986, bytes(body))
log.append('estados sprite 1986: %d etiquetas nuevas' % puestas)

# ------------------------------------------------------------------ 3. script principal
src = open(os.path.join(P3, 'scripts', REL), encoding='utf-8').read()
assert src.rstrip().endswith('});'), 'el final de DoAction_2 cambio'
nuevo = src
if not sin_rework:
    partes = sorted(glob.glob(os.path.join(AQUI, 'src', 'rw_*.as')))
    for parte in partes:
        nuevo += '\n' + open(parte, encoding='utf-8').read()
    mapa = ', '.join('"%d": %d' % (k, v) for k, v in sorted(frame_ids.items()))
    nuevo += '\n_root.__rwFrameIdsSet({%s});\n_root.__v8Sync();\n' % mapa
    log.append('rework  %d archivos: %s' % (len(partes), ' '.join(os.path.basename(x) for x in partes)))
if debug:
    nuevo += '\n' + open(os.path.join(AQUI, 'debug_hook.as'), encoding='utf-8').read()
p.script(REL, nuevo)

# ------------------------------------------------------------------ 4. reloj de combate (fotograma 217)
if not sin_rework:
    txt = open(os.path.join(P3, 'scripts', CLOCK), encoding='utf-8').read()
    a = '''                     if(spdVar3 < 1)
                     {
                        spdVar3 = 0;
                     }
'''
    b = a + '''                     if(_root.__rwNoDodge && _root.__rwNoDodge(mCaster, mTarget, mAry1))
                     {
                        spdVar3 = 0;
                     }
'''
    assert txt.count(a) == 1
    txt = txt.replace(a, b)
    a2 = '''      if(Cycler == 0)
      {
         _root.BattleTimeNow = 0;
         _root.InBattle = false;
         _root.speechDone = false;
         turnTime = 0;
         _root.TurnTime--;'''
    b2 = '''      if(Cycler == 0 && _root.__rwExtraTurn && _root.__rwExtraTurn())
      {
         _root.BattleTimeNow = 0;
         _root.InBattle = false;
         _root.speechDone = true;
         turnTime = 0;
         _root.PlayerToMove -= 3;
         if(_root.PlayerToMove < 0)
         {
            _root.PlayerToMove += 6;
         }
         _root.nextPlayer = false;
      }
      else if(Cycler == 0)
      {
         _root.BattleTimeNow = 0;
         _root.InBattle = false;
         _root.speechDone = false;
         turnTime = 0;
         _root.TurnTime--;'''
    assert txt.count(a2) == 1
    txt = txt.replace(a2, b2)
    p.script(CLOCK, txt)
    log.append('reloj   esquiva por __rwNoDodge y turno extra por __rwExtraTurn')

data, unc = p.build(out)
print('\n'.join(p.log + log))
print(out, len(data), hashlib.sha256(data).hexdigest())
