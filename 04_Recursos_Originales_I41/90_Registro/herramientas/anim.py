#!/usr/bin/env python3
"""Intérprete de líneas de tiempo SWF (datos del inventario) -> estado por fotograma.

frame_states(timeline, nframes) -> lista (índice 0 = fotograma 1) de dict depth -> objeto:
  {"ch","name","matrix":[a,b,c,d,tx,ty],"cx":[rm,gm,bm,am,ra,ga,ba,aa]|None,"ratio","clipDepth",
   "filters","blend","placed_f"}
Semántica SWF: place = objeto nuevo; move = modifica propiedades; replace (move+character) = cambia
carácter conservando lo no especificado; remove = elimina. Matriz por defecto: identidad.
Se aplica en orden lineal desde el fotograma 1 (equivale a reproducir hacia delante).
"""
import copy

IDENT = [1.0, 0.0, 0.0, 1.0, 0, 0]


def frame_states(timeline, nframes):
    by_f = {}
    for ev in timeline:
        by_f.setdefault(ev["f"], []).append(ev)
    state = {}
    out = []
    for f in range(1, nframes + 1):
        for ev in by_f.get(f, []):
            d = ev["depth"]
            op = ev["op"]
            if op == "remove":
                state.pop(d, None)
                continue
            if op == "place":
                o = {"ch": ev.get("ch"), "matrix": IDENT[:], "cx": None, "placed_f": f}
                state[d] = o
            else:
                o = state.get(d)
                if o is None:
                    o = {"ch": ev.get("ch"), "matrix": IDENT[:], "cx": None, "placed_f": f}
                    state[d] = o
                if op == "replace" and "ch" in ev:
                    o["ch"] = ev["ch"]
            for k_src, k_dst in (("matrix", "matrix"), ("cx", "cx"), ("name", "name"), ("ratio", "ratio"),
                                 ("clipDepth", "clipDepth"), ("filters", "filters"), ("blend", "blend"),
                                 ("visible", "visible")):
                if k_src in ev:
                    o[k_dst] = ev[k_src]
            if ev.get("clipActions"):
                o["clipActions"] = True
        out.append(copy.deepcopy(state))
    return out


def mul(m1, m2):
    """Composición: aplicar m2 y después m1 (m1 * m2). Matrices [a,b,c,d,tx,ty] (tx,ty en twips)."""
    a1, b1, c1, d1, x1, y1 = m1
    a2, b2, c2, d2, x2, y2 = m2
    return [a1 * a2 + c1 * b2, b1 * a2 + d1 * b2, a1 * c2 + c1 * d2, b1 * c2 + d1 * d2,
            a1 * x2 + c1 * y2 + x1, b1 * x2 + d1 * y2 + y1]
