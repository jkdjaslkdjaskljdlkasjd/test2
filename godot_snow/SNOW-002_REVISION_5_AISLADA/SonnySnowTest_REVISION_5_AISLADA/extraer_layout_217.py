# extraer_layout_217.py
# Extractor binario fiel para SNOW-002 (Segunda revision corregida).
# - Soporta PlaceObject2 (tag 26) y PlaceObject3 (tag 70, con flags2, ClassName, FilterList, BlendMode, etc.)
#   tanto en la linea de tiempo principal (fotograma 217) como dentro de DefineSprite_3343 (BATTLESCREEN)
#   y recursivamente dentro de todos los sprites hijos para el calculo de bounds.
# - Conserva campos omitidos en Move (flag 0x01) sin pisar matrices ni CharacterID previos.
# - Separa explicitamente la procedencia de posicion (pos_verified), escala (scale_verified) y
#   dimensiones (size_verified / size_source: "SWF_F1", "SWF_REF_MODEL" o "NONE").

import os
import sys
import json
import zlib
import struct

ROOT = os.path.dirname(os.path.abspath(__file__))


class BitReader:
    def __init__(self, data, byte_offset=0):
        self.data = data
        self.byte_pos = byte_offset
        self.bit_pos = 0

    def align(self):
        if self.bit_pos > 0:
            self.bit_pos = 0
            self.byte_pos += 1

    def read_ub(self, n):
        if n == 0:
            return 0
        val = 0
        for _ in range(n):
            b = self.data[self.byte_pos]
            bit = (b >> (7 - self.bit_pos)) & 1
            val = (val << 1) | bit
            self.bit_pos += 1
            if self.bit_pos == 8:
                self.bit_pos = 0
                self.byte_pos += 1
        return val

    def read_sb(self, n):
        if n == 0:
            return 0
        val = self.read_ub(n)
        if val & (1 << (n - 1)):
            val -= (1 << n)
        return val

    def read_matrix(self):
        self.align()
        a = d = 1.0
        b = c = 0.0
        if self.read_ub(1):  # HasScale
            nb = self.read_ub(5)
            a = self.read_sb(nb) / 65536.0
            d = self.read_sb(nb) / 65536.0
        if self.read_ub(1):  # HasRotate
            nb = self.read_ub(5)
            b = self.read_sb(nb) / 65536.0  # RotateSkew0
            c = self.read_sb(nb) / 65536.0  # RotateSkew1
        nb = self.read_ub(5)
        tx = self.read_sb(nb) / 20.0
        ty = self.read_sb(nb) / 20.0
        self.align()
        return {
            "a": round(a, 6),
            "b": round(b, 6),
            "c": round(c, 6),
            "d": round(d, 6),
            "tx": round(tx, 3),
            "ty": round(ty, 3),
            "xscale": round(a * 100.0, 3),
            "yscale": round(d * 100.0, 3),
        }

    def read_rect(self):
        self.align()
        nb = self.read_ub(5)
        xmin = self.read_sb(nb) / 20.0
        xmax = self.read_sb(nb) / 20.0
        ymin = self.read_sb(nb) / 20.0
        ymax = self.read_sb(nb) / 20.0
        self.align()
        return {
            "xMin": round(xmin, 3),
            "xMax": round(xmax, 3),
            "yMin": round(ymin, 3),
            "yMax": round(ymax, 3),
            "w": round(xmax - xmin, 3),
            "h": round(ymax - ymin, 3),
        }

    def skip_cxform_with_alpha(self):
        self.align()
        has_add = self.read_ub(1)
        has_mult = self.read_ub(1)
        nb = self.read_ub(4)
        if has_mult:
            for _ in range(4):
                self.read_sb(nb)
        if has_add:
            for _ in range(4):
                self.read_sb(nb)
        self.align()


def identity_matrix():
    return {"a": 1.0, "b": 0.0, "c": 0.0, "d": 1.0, "tx": 0.0, "ty": 0.0, "xscale": 100.0, "yscale": 100.0}


def transform_rect_affine(rect, mat):
    a, b, c, d = mat["a"], mat["b"], mat["c"], mat["d"]
    tx, ty = mat["tx"], mat["ty"]
    corners = [
        (rect["xMin"], rect["yMin"]),
        (rect["xMax"], rect["yMin"]),
        (rect["xMin"], rect["yMax"]),
        (rect["xMax"], rect["yMax"]),
    ]
    xs = [a * x + c * y + tx for x, y in corners]
    ys = [b * x + d * y + ty for x, y in corners]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    return {
        "xMin": round(xmin, 3),
        "xMax": round(xmax, 3),
        "yMin": round(ymin, 3),
        "yMax": round(ymax, 3),
        "w": round(xmax - xmin, 3),
        "h": round(ymax - ymin, 3),
    }


def read_c_string(body, pos):
    end = body.find(b"\x00", pos)
    if end == -1:
        return "", len(body)
    return body[pos:end].decode("latin1", errors="ignore"), end + 1


def parse_place_object2_or_3(code, body):
    """
    Parsea PlaceObject2 (tag 26) y PlaceObject3 (tag 70) segun la especificacion SWF.
    En PlaceObject3:
      - byte 0: flags1 (igual que PlaceObject2)
      - byte 1: flags2 (0x01 HasFilterList, 0x02 HasBlendMode, 0x04 HasCacheAsBitmap,
                        0x08 HasClassName, 0x10 HasImage, 0x20 HasVisible, 0x40 HasOpaqueBackground)
      - bytes 2..3: Depth (UI16)
    """
    flags1 = body[0]
    if code == 70:
        flags2 = body[1]
        depth = struct.unpack_from("<H", body, 2)[0]
        pos = 4
    else:
        flags2 = 0
        depth = struct.unpack_from("<H", body, 1)[0]
        pos = 3

    move = bool(flags1 & 0x01)
    has_character = bool(flags1 & 0x02)
    has_matrix = bool(flags1 & 0x04)
    has_cxform = bool(flags1 & 0x08)
    has_ratio = bool(flags1 & 0x10)
    has_name = bool(flags1 & 0x20)
    has_clip_depth = bool(flags1 & 0x40)

    has_class_name = bool(flags2 & 0x08)
    has_image = bool(flags2 & 0x10)

    class_name = None
    if code == 70 and (has_class_name or (has_image and has_character)):
        class_name, pos = read_c_string(body, pos)

    cid = None
    if has_character:
        cid = struct.unpack_from("<H", body, pos)[0]
        pos += 2

    mat = None
    if has_matrix:
        br = BitReader(body, pos)
        mat = br.read_matrix()
        pos = br.byte_pos

    if has_cxform:
        br = BitReader(body, pos)
        br.skip_cxform_with_alpha()
        pos = br.byte_pos

    if has_ratio:
        pos += 2

    name = None
    if has_name:
        name, pos = read_c_string(body, pos)

    clip_depth = None
    if has_clip_depth:
        clip_depth = struct.unpack_from("<H", body, pos)[0]
        pos += 2

    return {
        "tag": code,
        "depth": depth,
        "move": move,
        "cid": cid,
        "matrix": mat,
        "name": name,
        "clip_depth": clip_depth,
        "class_name": class_name,
    }


def apply_display_tag(display_list, code, body):
    """Actualiza la display_list soportando PlaceObject2 (26), PlaceObject3 (70) y RemoveObject/2 (5, 28)."""
    if code in (26, 70):
        po = parse_place_object2_or_3(code, body)
        d = po["depth"]
        if po["move"] and d in display_list:
            entry = dict(display_list[d])
            entry["tag"] = code
            if po["cid"] is not None:
                entry["cid"] = po["cid"]
            if po["matrix"] is not None:
                entry["matrix"] = po["matrix"]
            if po["name"] is not None:
                entry["name"] = po["name"]
            if po["clip_depth"] is not None:
                entry["clip_depth"] = po["clip_depth"]
            display_list[d] = entry
        elif not po["move"] and d in display_list:
            # Colocacion sin Move en profundidad ocupada: Flash/AIR la ignora
            pass
        else:
            display_list[d] = {
                "tag": code,
                "depth": d,
                "cid": po["cid"],
                "matrix": po["matrix"] if po["matrix"] is not None else identity_matrix(),
                "name": po["name"],
                "clip_depth": po["clip_depth"],
            }
    elif code == 28:  # RemoveObject2
        d = struct.unpack_from("<H", body, 0)[0]
        display_list.pop(d, None)
    elif code == 5:  # RemoveObject
        _, d = struct.unpack_from("<HH", body, 0)
        display_list.pop(d, None)


def iter_tags_from_bytes(buf, start_pos=0):
    pos = start_pos
    n = len(buf)
    while pos < n:
        hdr = struct.unpack_from("<H", buf, pos)[0]
        pos += 2
        code = hdr >> 6
        length = hdr & 0x3F
        if length == 0x3F:
            length = struct.unpack_from("<I", buf, pos)[0]
            pos += 4
        if code == 0:
            break
        yield code, buf[pos:pos + length]
        pos += length


def cargar_fuente_swf_o_paso1():
    candidatos = []
    if len(sys.argv) > 1:
        candidatos.append(sys.argv[1])
    candidatos.extend([
        os.path.join(ROOT, "SONNY2.swf"),
        os.path.join(ROOT, "../SONNY2.swf"),
        os.path.join(ROOT, "../sonny2mod/SONNY2.swf"),
        os.path.join(ROOT, "../../sonny2mod/SONNY2.swf"),
        os.path.join(ROOT, "i41/SONNY2.swf"),
        os.path.join(ROOT, "../i41/SONNY2.swf"),
        os.path.join(ROOT, "trabajo/act1"),
        os.path.join(ROOT, "../trabajo/act1"),
        os.path.join(ROOT, "trabajo/paso5/paso1"),
        os.path.join(ROOT, "../trabajo/paso5/paso1"),
    ])

    elegido = next((c for c in candidatos if os.path.exists(c)), None)
    if not elegido:
        raise FileNotFoundError(
            "No se encontro SONNY2.swf ni carpeta paso1/act1. "
            "Ejecuta: python extraer_layout_217.py RUTA_A_SONNY2.swf"
        )

    byid = {}
    main_tags = []
    def_codes = {2, 22, 32, 83, 11, 33, 37, 39, 7, 34, 46, 84}

    if os.path.isfile(elegido) and elegido.lower().endswith(".swf"):
        raw = open(elegido, "rb").read()
        sha = __import__("hashlib").sha256(raw).hexdigest()
        print(f"[OK] Leyendo SWF: {elegido} ({len(raw)} bytes, SHA-256: {sha})")
        sig = raw[:3]
        body = zlib.decompress(raw[8:]) if sig == b"CWS" else raw[8:]
        br = BitReader(body, 0)
        _ = br.read_rect()
        pos = br.byte_pos + 4
        for code, tb in iter_tags_from_bytes(body, pos):
            main_tags.append((code, tb))
            if code in def_codes and len(tb) >= 2:
                cid = struct.unpack_from("<H", tb, 0)[0]
                byid[cid] = (code, tb)
    else:
        print(f"[OK] Leyendo carpeta de tags: {elegido}")
        manifest = json.load(open(os.path.join(elegido, "manifest.json"), encoding="utf-8"))
        tags_dir = os.path.join(elegido, "tags")
        for t in manifest["tags"]:
            code = t["code"]
            tb = open(os.path.join(tags_dir, t["file"]), "rb").read()
            main_tags.append((code, tb))
            if "id" in t:
                byid[t["id"]] = (code, tb)

    return elegido, main_tags, byid


def calcular_bounds_fotograma_n(cid, byid, target_frame=1, visitados=None):
    """
    Calcula el bounding box del fotograma `target_frame` (por defecto 1) de un CharacterID,
    soportando PlaceObject2 (26) y PlaceObject3 (70).
    """
    if visitados is None:
        visitados = set()
    if cid is None or cid in visitados or cid not in byid:
        return None
    visitados.add(cid)

    code, body = byid[cid]
    if code in (2, 22, 32, 83, 11, 33, 37):
        br = BitReader(body, 2)
        return br.read_rect()

    if code in (46, 84):  # DefineMorphShape / DefineMorphShape2: StartBounds en offset 2
        br = BitReader(body, 2)
        return br.read_rect()

    if code == 39:  # DefineSprite
        dlist = {}
        cur_frame = 1
        for scode, sbody in iter_tags_from_bytes(body, 4):
            if scode == 1:  # ShowFrame
                if cur_frame >= target_frame:
                    break
                cur_frame += 1
            else:
                apply_display_tag(dlist, scode, sbody)

        xmin, ymin, xmax, ymax = 1e9, 1e9, -1e9, -1e9
        found = False
        for item in dlist.values():
            sub = calcular_bounds_fotograma_n(item["cid"], byid, 1, set(visitados))
            if sub and (sub["w"] > 0 or sub["h"] > 0):
                tr = transform_rect_affine(sub, item["matrix"])
                found = True
                xmin = min(xmin, tr["xMin"])
                xmax = max(xmax, tr["xMax"])
                ymin = min(ymin, tr["yMin"])
                ymax = max(ymax, tr["yMax"])
        if found:
            return {
                "xMin": round(xmin, 3),
                "xMax": round(xmax, 3),
                "yMin": round(ymin, 3),
                "yMax": round(ymax, 3),
                "w": round(xmax - xmin, 3),
                "h": round(ymax - ymin, 3),
            }
    return None


def inspeccionar_modelo_referencia_jugador(cid, byid):
    """
    Si el contenedor del jugador (ej. DefineSprite_2503) tiene su primer fotograma vacio o
    con un clip 'inner' que carga modelos en fotogramas posteriores, busca el primer fotograma
    no vacio de ese sprite para reportarlo por separado como 'reference_pose_bounds' (sin
    mezclarlo con bounds_local del fotograma 1).
    """
    if cid not in byid or byid[cid][0] != 39:
        return None
    _, body = byid[cid]
    _, nframes = struct.unpack_from("<HH", body, 0)
    for fr in range(1, min(nframes + 1, 30)):
        b = calcular_bounds_fotograma_n(cid, byid, target_frame=fr)
        if b and b["w"] >= 10.0 and b["h"] >= 20.0:
            return {"frame": fr, **b}
    return None


def serializar_item(item, byid, check_ref_pose=False):
    cid = item["cid"]
    mat = item["matrix"]
    bnds_local = calcular_bounds_fotograma_n(cid, byid, target_frame=1) if cid else None
    has_valid_f1_size = bool(bnds_local and (bnds_local["w"] > 0.0 or bnds_local["h"] > 0.0))
    bnds_parent = transform_rect_affine(bnds_local, mat) if has_valid_f1_size else None

    ref_pose_local = None
    ref_pose_parent = None
    if check_ref_pose and not has_valid_f1_size and cid:
        ref_pose_local = inspeccionar_modelo_referencia_jugador(cid, byid)
        if ref_pose_local:
            ref_pose_parent = transform_rect_affine(ref_pose_local, mat)

    if has_valid_f1_size:
        size_source = "SWF_F1"
    elif ref_pose_parent is not None:
        size_source = "SWF_REF_POSE"
    else:
        size_source = "NONE"

    return {
        "tag": item.get("tag", 26),
        "depth": item["depth"],
        "cid": cid,
        "name": item["name"],
        "x": mat["tx"],
        "y": mat["ty"],
        "xscale": mat["xscale"],
        "yscale": mat["yscale"],
        "matrix": mat,
        "pos_verified": True,
        "scale_verified": True,
        "size_verified": has_valid_f1_size,
        "size_source": size_source,
        "bounds_local": bnds_local if has_valid_f1_size else None,
        "bounds_in_parent": bnds_parent,
        "reference_pose_local": ref_pose_local,
        "reference_pose_in_parent": ref_pose_parent,
    }


def localizar_carpeta_assets():
    candidatos = [
        os.path.join(ROOT, "03_Proyecto_Godot/SonnySnowTest/assets"),
        os.path.join(ROOT, "SonnySnowTest/assets"),
        os.path.join(ROOT, "assets"),
    ]
    for c in candidatos:
        if os.path.isdir(c):
            return c
    out = os.path.join(ROOT, "assets")
    os.makedirs(out, exist_ok=True)
    return out


def main():
    fuente, main_tags, byid = cargar_fuente_swf_o_paso1()

    # 1. Extraer el fotograma 1 de DefineSprite_3343 (BATTLESCREEN), incluyendo PlaceObject3 (tag 70)
    if 3343 not in byid:
        raise RuntimeError("No se encontro DefineSprite_3343 (BATTLESCREEN) en la fuente.")
    _, b3343 = byid[3343]
    bs_dlist = {}
    for scode, sbody in iter_tags_from_bytes(b3343, 4):
        if scode == 1:  # Primer ShowFrame
            break
        apply_display_tag(bs_dlist, scode, sbody)

    players = {}
    for item in sorted(bs_dlist.values(), key=lambda x: x["depth"]):
        nm = item.get("name")
        if nm in ("player1", "player2", "player3", "player4", "player5", "player6"):
            players[nm] = serializar_item(item, byid, check_ref_pose=True)

    # 2. Simular la linea de tiempo principal desde el fotograma 1 hasta el fotograma 217
    frame = 1
    stage_dlist = {}
    for code, tb in main_tags:
        if code == 1:  # ShowFrame
            if frame == 217:
                break
            frame += 1
        else:
            apply_display_tag(stage_dlist, code, tb)

    if 89 not in stage_dlist:
        raise RuntimeError("No se encontro la profundidad 89 (BATTLESCREEN) en el fotograma 217.")
    bs_stage = serializar_item(stage_dlist[89], byid)

    top_bars = {}
    bottom_panel = {}
    top_bar_depths = {342, 360, 378, 396, 414, 432}
    bottom_depths = {60, 65, 480, 484, 498, 628, 634, 644, 646}
    bottom_names = {
        "UI_BAR", "battleClocker", "krinToMove", "krinToMove2",
        "moveSelectBoomer", "combatScript", "__hdSkipX", "__hdSkipXbg"
    }

    for d, item in sorted(stage_dlist.items()):
        nm = item.get("name") or f"depth_{d}"
        if nm in ("p1BAR", "p2BAR", "p3BAR", "p4BAR", "p5BAR", "p6BAR") or d in top_bar_depths:
            top_bars[nm] = serializar_item(item, byid)
        if d in bottom_depths or nm in bottom_names:
            bottom_panel[nm] = serializar_item(item, byid)

    resultado = {
        "source": os.path.basename(fuente),
        "battlescreen_d89": bs_stage,
        "players": players,
        "top_bars": top_bars,
        "bottom_panel": bottom_panel,
        "hd_battle_layout": {"s": 0.62, "ax": 400.0, "ay": 575.0, "dy": -12.0},
    }

    assets_dir = localizar_carpeta_assets()
    out_file = os.path.join(assets_dir, "battle_layout_217.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"[OK] Escrito en: {out_file}")
    print(f"     Slots extraidos: {len(players)}/6 -> {sorted(players.keys())}")
    for k in sorted(players.keys()):
        p = players[k]
        print(f"       - {k} (tag {p['tag']}, d={p['depth']}): pos=({p['x']}, {p['y']}) scale=({p['xscale']}%, {p['yscale']}%) size_source={p['size_source']} bounds_f1={p['bounds_in_parent']}")
    print(f"     Barras superiores extraidas: {len(top_bars)}/6 -> {sorted(top_bars.keys())}")
    for k in sorted(top_bars.keys()):
        b = top_bars[k]
        print(f"       - {k} (tag {b['tag']}, d={b['depth']}): pos=({b['x']}, {b['y']}) size_source={b['size_source']} bounds_f1={b['bounds_in_parent']}")
    print(f"     Piezas inferiores extraidas: {len(bottom_panel)} -> {sorted(bottom_panel.keys())}")


if __name__ == "__main__":
    main()
