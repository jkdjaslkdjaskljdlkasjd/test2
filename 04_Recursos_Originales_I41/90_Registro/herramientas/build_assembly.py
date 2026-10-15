#!/usr/bin/env python3
"""Reconstrucción estática del ensamblaje de un personaje a partir de la lógica original
(__nzRawDress / dressChar, rama STANDARD; DoAction del fotograma 217 de I41).

Copia SIN MODIFICAR los bytes de todas las definiciones originales necesarias y crea:
  - un sprite nuevo por instancia-hueso del MODEL (head, chest, arm1...), que contiene lo que
    attachMovie colocaría en tiempo de ejecución:
        piel   G_S<RANURA>_<skin>   -> profundidad AS2 -1  (timeline 16383)  nombre innerX
        equipo G_<RANURA>_<set>     -> profundidad AS2  0  (timeline 16384)  nombre inner
        pelo   HAIR_<hair>          -> profundidad AS2  2  (timeline 16386)  nombre hair (solo head)
    El marcador original del hueso (onClipEvent(load){unloadMovie(this);}) se omite porque el
    juego lo descarga al cargarse.
  - una copia del sprite MODEL con los PlaceObject de los huesos apuntando a esos sprites nuevos.
Todo lo demás del MODEL (matrices, color, profundidades, etiquetas, efectos de prof. 33, sombra,
acciones de fotograma) se conserva byte a byte.

uso: build_assembly.py I41.swf inventory.json spec.json salida.swf salida_informe.json
spec.json: {"name":"VERADUX_ZPCI3","model":"MODEL1","skin":"METABII","gender":"M","hair":"",
            "equip":["ZPCI3","ZPCI3","ZPCI3","ZPCI3","ZPCI3",0,0]}
"""
import sys, json, struct
sys.path.insert(0, __import__('os').path.dirname(__file__))
import swftags as S

swf_path, inv_path, spec_path, out_path, rep_path = sys.argv[1:6]
spec = json.load(open(spec_path))
inv = json.load(open(inv_path))
C = inv['characters']
by_name = {}
for k, c in C.items():
    for n in c['exports']:
        by_name[n] = int(k)

# --- lógica original (copiada de __nzRawDress, rama STANDARD) ---
dollPartsArray = ["head", "chest", "arm1", "arm2", "hand1", "hand2", "leg1", "leg2", "leg3", "leg4",
                  "foot1", "foot2", "weapon1", "weapon2", "shoulder"]
dollPartsCores = [0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 6, 1]
dollPartsCores2 = ["HEAD", "CHEST", "ARM", "ARM", "HAND", "HAND", "ARM", "ARM", "LEG2", "LEG2", "FOOT", "FOOT",
                   "WEAPON", "WEAPON", "SHOULDER"]
model, skin, hair, gender = spec['model'], spec['skin'], spec['hair'], spec['gender']
equip = spec['equip']
DEPTH_OFF = 16384

attach = {}   # instancia -> {depth_as2: linkage}
log = []


def do_attach(inst, linkage, depth):
    ok = linkage in by_name
    log.append({"instancia": inst, "attachMovie": linkage, "profundidad_as2": depth,
                "existe_en_biblioteca": ok, "characterId": by_name.get(linkage)})
    if ok:
        attach.setdefault(inst, {})[depth] = linkage
    # Si no existe, attachMovie no crea nada (no se borra lo que hubiera en esa profundidad).


standard = spec.get('standard', 'STANDARD')
w1, w2 = spec.get('weapon1', ''), spec.get('weapon2', '')
notas = []
for h in range(len(dollPartsArray)):
    inst = dollPartsArray[h]
    do_attach(inst, gender + "_S" + dollPartsCores2[h] + "_" + skin, -1)
    e = equip[dollPartsCores[h]]
    if standard == "STANDARD":
        if e != 0:
            do_attach(inst, gender + "_" + dollPartsCores2[h] + "_" + str(e), 0)
        if equip[0] == 0 or gender == "F":
            do_attach("head", "HAIR_" + hair, 2)
        if h in (12, 13):
            do_attach(inst, "M_" + dollPartsCores2[h] + "_" + str(e), 0)
    else:
        # rama de formas (dressChar con standard != "STANDARD"), __nzRawDress l.43-62
        do_attach(inst, gender + "_" + dollPartsCores2[h] + "_" + standard, 0)
        if hair != "":
            do_attach("head", "HAIR_" + hair, 2)
        if h in (12, 13):
            if h == 12 and w1 != "":
                do_attach(inst, "M_" + dollPartsCores2[h] + "_" + w1, 0)
            elif h == 13 and w2 != "":
                do_attach(inst, "M_" + dollPartsCores2[h] + "_" + w2, 0)
            else:
                do_attach(inst, "M_" + dollPartsCores2[h] + "_" + str(e), 0)
                notas.append("%s: arma tomada del equipo actual del jugador (equip[%d]=%r en esta especificacion)" % (inst, dollPartsCores[h], e))
if model == "MODEL5":
    notas.append("El juego reduce 'inner' al 80%% y lo baja 10 px cuando el modelo es MODEL5 (frame_217/DoAction.as l.19-24); no aplicado dentro del sprite.")

# --- SWF ---
s = S.read_swf(swf_path)
tags = s['tags']
model_id = by_name[model]
mc = C[str(model_id)]
inst_depth = {}
for ev in mc['timeline']:
    if 'name' in ev:
        inst_depth.setdefault(ev['name'], set()).add(ev['depth'])
for inst in dollPartsArray:
    if inst not in inst_depth:
        log.append({"instancia": inst, "aviso": "el MODEL no tiene instancia con este nombre"})

needed = set()


def closure(i):
    if i in needed:
        return
    needed.add(i)
    c = C[str(i)]
    for k in c.get('children', []) + c.get('deps', []):
        closure(k)


closure(model_id)
for inst, d in attach.items():
    for lk in d.values():
        closure(by_name[lk])

next_id = max(int(k) for k in C) + 1
new_tags = []
bone_sprite = {}  # depth en MODEL -> nuevo id
report_bones = {}
for inst, depths in inst_depth.items():
    if inst not in dollPartsArray:
        continue
    sid = next_id
    next_id += 1
    sub = []
    contents = []
    for d_as2 in sorted(attach.get(inst, {})):
        lk = attach[inst][d_as2]
        cid = by_name[lk]
        name = {-1: "innerX", 0: "inner", 2: "hair"}[d_as2]
        # PlaceObject2: flags HasName(0x20)|HasMatrix(0x04)|HasCharacter(0x02)
        body = struct.pack('<BHH', 0x26, d_as2 + DEPTH_OFF, cid) + b'\x00' + S.string_z(name)
        sub.append((26, body, False))
        contents.append({"profundidad_as2": d_as2, "profundidad_timeline": d_as2 + DEPTH_OFF,
                         "nombre": name, "linkage": lk, "characterId": cid})
    sub.append((1, b'', False))
    sub.append((0, b'', False))
    new_tags.append((39, S.make_sprite(sid, 1, sub), True))
    for dp in depths:
        bone_sprite[dp] = sid
    report_bones[inst] = {"sprite_reconstruido": sid, "profundidades_en_model": sorted(depths),
                          "contenido": contents}


def patch_place(code, body, newid):
    if code == 26:
        flags = body[0]
        if not flags & 0x02:
            return body
        return body[:3] + struct.pack('<H', newid) + body[5:]
    if code == 70:
        flags = body[0]
        flags2 = body[1]
        if not flags & 0x02:
            return body
        off = 4
        if flags2 & 0x08 or (flags2 & 0x10 and flags & 0x02):  # HasClassName / HasImage+HasCharacter
            if flags2 & 0x08:
                while body[off] != 0:
                    off += 1
                off += 1
        return body[:off] + struct.pack('<H', newid) + body[off + 2:]
    return body


# Copia del MODEL con huesos sustituidos
model_tag = next(t for t in tags if t[0] == 39 and S.char_id(t[0], t[1]) == model_id)
mid, mfc, msub = S.sprite_subtags(model_tag[1])
new_model_id = next_id
next_id += 1
patched = []
n_patched = 0
for code, body, lf in msub:
    if code in (26, 70):
        depth = struct.unpack_from('<H', body, 1 if code == 26 else 2)[0]
        if depth in bone_sprite and (body[0] & 0x02):
            body = patch_place(code, body, bone_sprite[depth])
            n_patched += 1
    patched.append((code, body, lf))
new_tags.append((39, S.make_sprite(new_model_id, mfc, patched), True))

# Etiquetas finales
out = []
for code, body, lf in tags:
    if code == 69:  # FileAttributes
        out.append((code, body, lf))
    elif code == 9:
        out.append((code, body, lf))
for code, body, lf in tags:
    cid = S.char_id(code, body)
    if cid is not None and cid in needed:
        out.append((code, body, lf))
    elif code in (73, 88, 74):  # FontAlignZones / FontName / CSMTextSettings de fuentes incluidas
        ref = struct.unpack_from('<H', body, 0)[0]
        if ref in needed:
            out.append((code, body, lf))
out += new_tags
export_name = "RECON_" + spec['name']
out.append((56, S.export_assets([(new_model_id, export_name)]), False))
# escenario: el modelo reconstruido en el centro de un escenario de 800x575 (como I41)
po = struct.pack('<BHH', 0x26, 1, new_model_id) + b'\x00' + S.string_z("inner")
# matriz: traslación (400,400) px = (8000,8000) twips
def matrix_translate(tx, ty):
    # MATRIX: HasScale0 HasRotate0 NTranslateBits
    nb = max(abs(tx), abs(ty)).bit_length() + 1
    bits = '0' + '0' + format(nb, '05b') + format(tx & ((1 << nb) - 1), '0%db' % nb) + format(ty & ((1 << nb) - 1), '0%db' % nb)
    bits += '0' * ((8 - len(bits) % 8) % 8)
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
po = struct.pack('<BHH', 0x26, 1, new_model_id) + matrix_translate(8000, 8000) + S.string_z("inner")
out.append((26, po, False))
out.append((1, b'', False))
out.append((0, b'', False))
S.write_swf(out_path, s['version'], s['rect'], s['rate_raw'], 1, out, compress=True)

json.dump({"spec": spec, "model_id_original": model_id, "model_reconstruido_id": new_model_id,
           "export_reconstruido": export_name, "huesos": report_bones, "attachMovie_log": log,
           "placeobject_parcheados": n_patched, "notas": notas, "definiciones_copiadas": len(needed),
           "nota": "Bytes de definiciones originales copiados sin cambios; solo se añaden sprites-hueso "
                   "y una copia del MODEL con characterId de huesos sustituido."},
          open(rep_path, 'w'), indent=1, ensure_ascii=False)
print("modelo reconstruido", new_model_id, "huesos", len(report_bones), "placeobject parcheados", n_patched,
      "definiciones", len(needed))
