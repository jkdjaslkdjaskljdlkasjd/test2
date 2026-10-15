#!/usr/bin/env python3
"""Inventario estructural del SWF a partir del XML de JPEXS (-swf2xml).

Salida: inventory.json con
  characters[id] = {id, tag, tag_index, exports[], bounds, frames, labels, timeline, children, ...}
  root = {frames, labels, timeline}
La línea de tiempo se guarda como lista de eventos por fotograma, sin interpretar:
  {"f":frame,"op":"place|move|remove","depth":d,"ch":id,"name":..,"matrix":[a,b,c,d,tx,ty],
   "cx":[rm,gm,bm,am,ra,ga,ba,aa],"ratio":..,"clipDepth":..,"clipActions":bool,"blend":..,"filters":n}
Matrices en unidades SWF: a,b,c,d como float (escala/rotación), tx,ty en twips.
"""
import sys, json
import xml.etree.ElementTree as ET

src, out = sys.argv[1], sys.argv[2]

DEF_ID_ATTR = {
    "DefineSpriteTag": "spriteId", "DefineShapeTag": "shapeId", "DefineShape2Tag": "shapeId",
    "DefineShape3Tag": "shapeId", "DefineShape4Tag": "shapeId", "DefineSoundTag": "soundId",
    "DefineBitsLosslessTag": "characterID", "DefineBitsLossless2Tag": "characterID",
    "DefineBitsJPEG2Tag": "characterID", "DefineBitsJPEG3Tag": "characterID",
    "DefineBitsJPEG4Tag": "characterID", "DefineBitsTag": "characterID",
    "DefineButton2Tag": "buttonId", "DefineButtonTag": "buttonId",
    "DefineEditTextTag": "characterID", "DefineTextTag": "characterID", "DefineText2Tag": "characterID",
    "DefineFont3Tag": "fontID", "DefineFont2Tag": "fontID", "DefineFontTag": "fontId",
    "DefineMorphShapeTag": "characterId", "DefineMorphShape2Tag": "characterId",
    "DefineVideoStreamTag": "characterID",
}


def fnum(v):
    try:
        return float(v)
    except Exception:
        return None


def matrix(el):
    if el is None:
        return None
    a = d = 1.0
    b = c = 0.0
    if el.get("hasScale") == "true":
        a = float(el.get("scaleX"))
        d = float(el.get("scaleY"))
    if el.get("hasRotate") == "true":
        b = float(el.get("rotateSkew0"))
        c = float(el.get("rotateSkew1"))
    return [a, b, c, d, int(el.get("translateX", 0)), int(el.get("translateY", 0))]


def cxform(el):
    if el is None:
        return None
    g = lambda k, dflt: int(el.get(k, dflt))
    hm = el.get("hasMultTerms") == "true"
    ha = el.get("hasAddTerms") == "true"
    return [g("redMultTerm", 256) if hm else 256, g("greenMultTerm", 256) if hm else 256,
            g("blueMultTerm", 256) if hm else 256, g("alphaMultTerm", 256) if hm else 256,
            g("redAddTerm", 0) if ha else 0, g("greenAddTerm", 0) if ha else 0,
            g("blueAddTerm", 0) if ha else 0, g("alphaAddTerm", 0) if ha else 0]


def rect(el):
    if el is None:
        return None
    return [int(el.get("Xmin")), int(el.get("Ymin")), int(el.get("Xmax")), int(el.get("Ymax"))]


def filt(x):
    """Filtro con todos sus parámetros (atributos + colores/matrices hijos)."""
    d = {k: v for k, v in x.attrib.items()}
    for ch in x:
        if ch.get("type") == "RGBA":
            d[ch.tag] = "#%02x%02x%02x/%s" % (int(ch.get("red")), int(ch.get("green")), int(ch.get("blue")), ch.get("alpha"))
        else:
            d[ch.tag] = [dict(g.attrib) if len(g) == 0 and g.attrib else (g.text or "") for g in ch] or dict(ch.attrib)
    return d


def deps(el):
    """Dependencias por ID que no están en la lista de visualización (bitmaps de rellenos, fuentes)."""
    out = set()
    for e in el.iter():
        b = e.get("bitmapId")
        if b is not None and b != "65535":
            out.add(int(b))
        f = e.get("fontId")
        if f is not None and e is not el:
            out.add(int(f))
    return sorted(out)


def timeline(items):
    """items: lista de elementos <item> hijos de un sprite o del escenario."""
    f = 1
    events, labels, actions = [], [], []
    sounds = []
    for it in items:
        t = it.get("type")
        if t == "ShowFrameTag":
            f += 1
        elif t in ("PlaceObjectTag", "PlaceObject2Tag", "PlaceObject3Tag"):
            ev = {"f": f, "depth": int(it.get("depth"))}
            hasch = it.get("placeFlagHasCharacter") == "true" or (t == "PlaceObjectTag")
            move = it.get("placeFlagMove") == "true"
            ev["op"] = "replace" if (hasch and move) else ("place" if hasch else "move")
            if hasch and it.get("characterId") is not None:
                ev["ch"] = int(it.get("characterId"))
            if it.get("placeFlagHasName") == "true":
                ev["name"] = it.get("name")
            if it.get("placeFlagHasClassName") == "true" and it.get("className"):
                ev["className"] = it.get("className")
            m = matrix(it.find("matrix"))
            if m is not None and (it.get("placeFlagHasMatrix") == "true" or t == "PlaceObjectTag"):
                ev["matrix"] = m
            c = cxform(it.find("colorTransform"))
            if c is not None and it.get("placeFlagHasColorTransform") == "true":
                ev["cx"] = c
            if it.get("placeFlagHasRatio") == "true":
                ev["ratio"] = int(it.get("ratio"))
            if it.get("placeFlagHasClipDepth") == "true":
                ev["clipDepth"] = int(it.get("clipDepth"))
            if it.get("placeFlagHasClipActions") == "true":
                ev["clipActions"] = True
            if it.get("placeFlagHasBlendMode") == "true":
                ev["blend"] = int(it.get("blendMode"))
            if it.get("placeFlagHasFilterList") == "true":
                fl = it.find("surfaceFilterList")
                ev["filters"] = [filt(x) for x in fl] if fl is not None else "?"
            if it.get("placeFlagHasCacheAsBitmap") == "true":
                ev["cacheAsBitmap"] = True
            if it.get("placeFlagHasVisible") == "true":
                ev["visible"] = it.get("visible")
            events.append(ev)
        elif t in ("RemoveObjectTag", "RemoveObject2Tag"):
            events.append({"f": f, "op": "remove", "depth": int(it.get("depth"))})
        elif t == "FrameLabelTag":
            labels.append({"f": f, "label": it.get("name"), "anchor": it.get("namedAnchor") == "true"})
        elif t in ("DoActionTag",):
            actions.append(f)
        elif t == "StartSoundTag":
            sounds.append({"f": f, "soundId": int(it.get("soundId"))})
    total = f - 1 if items and items[-1].get("type") in ("ShowFrameTag", "EndTag") else f
    return events, labels, actions, sounds


def main():
    tree_iter = ET.iterparse(src, events=("start", "end"))
    depth = 0
    chars = {}
    exports = {}
    root_items = []
    tag_index = -1
    init_actions = []
    for ev, el in tree_iter:
        if ev == "start":
            depth += 1
            continue
        depth -= 1
        # depth: swf=1, tags=2, top items=3
        if depth == 2 and el.tag == "item":
            tag_index += 1
            t = el.get("type")
            idattr = DEF_ID_ATTR.get(t)
            if idattr and el.get(idattr) is not None:
                cid = int(el.get(idattr))
                c = {"id": cid, "tag": t.replace("Tag", ""), "tag_index": tag_index, "exports": []}
                if t == "DefineSpriteTag":
                    sub = el.find("subTags")
                    items = list(sub) if sub is not None else []
                    evs, labs, acts, snds = timeline(items)
                    c["frames"] = int(el.get("frameCount"))
                    c["labels"] = labs
                    c["timeline"] = evs
                    c["doaction_frames"] = acts
                    c["start_sounds"] = snds
                    c["children"] = sorted({e["ch"] for e in evs if "ch" in e})
                elif t.startswith("DefineShape"):
                    c["bounds"] = rect(el.find("shapeBounds"))
                    if el.find("edgeBounds") is not None:
                        c["edgeBounds"] = rect(el.find("edgeBounds"))
                elif t.startswith("DefineMorphShape"):
                    c["bounds"] = rect(el.find("startBounds"))
                    c["endBounds"] = rect(el.find("endBounds"))
                elif t == "DefineSoundTag":
                    fmt = {0: "PCM-native", 1: "ADPCM", 2: "MP3", 3: "PCM-LE", 4: "Nellymoser16k",
                           5: "Nellymoser8k", 6: "Nellymoser", 11: "Speex"}
                    c["soundFormat"] = fmt.get(int(el.get("soundFormat")), el.get("soundFormat"))
                    c["soundRate"] = [5512, 11025, 22050, 44100][int(el.get("soundRate"))]
                    c["soundSize16"] = el.get("soundSize") == "true"
                    c["stereo"] = el.get("soundType") == "true"
                    c["sampleCount"] = int(el.get("soundSampleCount"))
                elif t in ("DefineButton2Tag", "DefineButtonTag"):
                    recs = el.find("characters")
                    kids = []
                    if recs is not None:
                        for r in recs:
                            if r.get("characterId"):
                                kids.append({"ch": int(r.get("characterId")), "depth": int(r.get("placeDepth", 0)),
                                             "up": r.get("buttonStateUp") == "true", "over": r.get("buttonStateOver") == "true",
                                             "down": r.get("buttonStateDown") == "true", "hit": r.get("buttonStateHitTest") == "true",
                                             "matrix": matrix(r.find("placeMatrix"))})
                    c["records"] = kids
                    c["children"] = sorted({k["ch"] for k in kids})
                elif t == "DefineEditTextTag":
                    c["bounds"] = rect(el.find("bounds"))
                    c["variableName"] = el.get("variableName")
                    c["initialText"] = el.get("initialText")
                    if el.get("fontId"):
                        c["fontId"] = int(el.get("fontId"))
                elif t.startswith("DefineFont"):
                    c["fontName"] = (el.get("fontName") or "").replace("\\u0000", "").rstrip("\x00")
                    gst = el.find("glyphShapeTable")
                    c["numGlyphs"] = len(gst) if gst is not None else 0
                elif t.startswith("DefineText"):
                    c["bounds"] = rect(el.find("textBounds"))
                if not t == "DefineSpriteTag":
                    dp = deps(el)
                    if t == "DefineEditTextTag" and el.get("fontId") and el.get("hasFont") == "true":
                        dp = sorted(set(dp) | {int(el.get("fontId"))})
                    if dp:
                        c["deps"] = dp
                chars[cid] = c
            elif t == "ExportAssetsTag":
                tags_el = el.find("tags")
                names_el = el.find("names")
                ids = [int(x.text) for x in tags_el] if tags_el is not None else []
                nms = [x.text for x in names_el] if names_el is not None else []
                for i, n in zip(ids, nms):
                    exports.setdefault(i, []).append(n)
            elif t == "DoInitActionTag":
                init_actions.append({"spriteId": int(el.get("spriteId")), "tag_index": tag_index})
            else:
                root_items.append(el)
                continue  # keep for root timeline
            el.clear()
    for i, ns in exports.items():
        if i in chars:
            chars[i]["exports"] = ns
    for ia in init_actions:
        if ia["spriteId"] in chars:
            chars[ia["spriteId"]]["has_initaction"] = True
    evs, labs, acts, snds = timeline(root_items)
    root = {"labels": labs, "timeline": evs, "doaction_frames": acts, "start_sounds": snds,
            "children": sorted({e["ch"] for e in evs if "ch" in e})}
    # Referencias inversas: quién usa a quién (incluye shapes con fills de bitmap no, solo display list)
    parents = {}
    for c in chars.values():
        for k in c.get("children", []) + c.get("deps", []):
            parents.setdefault(k, []).append(c["id"])
    for k in root["children"]:
        parents.setdefault(k, []).append(0)
    for c in chars.values():
        c["parents"] = sorted(set(parents.get(c["id"], [])))
    json.dump({"characters": {str(k): v for k, v in sorted(chars.items())}, "root": root,
               "exports_by_id": {str(k): v for k, v in sorted(exports.items())},
               "init_actions": init_actions}, open(out, "w"))
    print("characters", len(chars), "exports", sum(len(v) for v in exports.values()),
          "root frames events", len(evs), "labels", len(labs))


main()
