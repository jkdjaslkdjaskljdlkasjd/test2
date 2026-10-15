#!/usr/bin/env python3
"""Tabla de objetos KRINITEM<id> -> {nombre_interno, ranura(b), rareza, looks, linea}
extraída del código AS2 decompilado (frame_42/DoAction_2.as).
Reglas copiadas del código: createNewItemKrin incrementa itemKrinIDnow; si b>1, looks="NINJA" por defecto;
una asignación posterior 'gghhjjuu.looks = "X"' (o _root["KRINITEM"+n].looks) lo sustituye.
uso: items.py DoAction_2.as salida.json
"""
import re, sys, json
src, out = sys.argv[1], sys.argv[2]
cur = None
items = {}
re_set = re.compile(r'^\s*itemKrinIDnow\s*=\s*(-?\d+)\s*;')
re_new = re.compile(r'^\s*createNewItemKrin\((.*)\);\s*$')
re_looks = re.compile(r'^\s*gghhjjuu\.looks\s*=\s*"([^"]*)"\s*;')
re_looks2 = re.compile(r'_root\["KRINITEM"\s*\+\s*(\d+)\]\.looks\s*=\s*"([^"]*)"|_root\.KRINITEM(\d+)\.looks\s*=\s*"([^"]*)"')
inside_func = False
for ln, line in enumerate(open(src, encoding='utf-8', errors='replace'), 1):
    if line.startswith('function createNewItemKrin'):
        inside_func = True
    if inside_func:
        if line.startswith('}'):
            inside_func = False
        continue
    m = re_set.match(line)
    if m:
        cur = int(m.group(1))
        continue
    m = re_new.match(line)
    if m and cur is not None:
        cur += 1
        args = [a.strip() for a in re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', m.group(1))]
        name = args[0].strip('"')
        b = int(args[1]) if args[1].lstrip('-').isdigit() else args[1]
        items[cur] = {"id": cur, "nombre_interno": name, "ranura_b": b, "rareza": args[2].strip('"'),
                      "args": args, "looks": "NINJA" if isinstance(b, int) and b > 1 else None,
                      "looks_origen": "defecto createNewItemKrin (b>1)" if isinstance(b, int) and b > 1 else None,
                      "linea": ln}
        continue
    m = re_looks.match(line)
    if m and cur in items:
        items[cur]["looks"] = m.group(1)
        items[cur]["looks_origen"] = "gghhjjuu.looks l.%d" % ln
        continue
    for m in re_looks2.finditer(line):
        i = int(m.group(1) or m.group(3)); v = m.group(2) or m.group(4)
        if i in items:
            items[i].setdefault("looks_reasignado", []).append({"looks": v, "linea": ln})
json.dump({str(k): v for k, v in sorted(items.items())}, open(out, 'w'), indent=1, ensure_ascii=False)
print(len(items), "objetos")
