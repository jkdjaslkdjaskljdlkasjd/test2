# Paso 5 — prueba de sensibilidad: se meten errores A PROPOSITO en la version
# recompilada y se comprueba que la ejecucion diferencial los detecta.
# Si la prueba no detectara estos errores, su "todo identico" no valdria nada.
import sys, os, re, json, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(30000)
import diffrun
from as2comp import compile_script


class MemGame(diffrun.Game):
    """Juego armado en memoria compilando los .as del paso 3 (con cambios opcionales)."""
    def __init__(self, p3, override=None):
        self.idx = json.load(open(os.path.join(p3, 'index.json')))
        self.src = {}
        self.cache = {}
        for s in self.idx:
            t = open(os.path.join(p3, s['file']), encoding='utf-8').read()
            if override and s['file'] in override: t = override[s['file']]
            self.src[s['file']] = t
            self.cache[s['file']] = compile_script(t)

    def code(self, s):
        b = self.cache[s['file']]
        return b, 0, len(b)


def run(ga, gb, vivify=False):
    A = diffrun.Runner(ga, vivify); B = diffrun.Runner(gb, vivify)
    A.run_scripts(); B.run_scripts(); A.prepare(); B.prepare(); A.sweep(); B.sweep()
    same, cut, diffs = diffrun.compare(A, B)
    return same, cut, diffs, len(A.steps)


MUTS = [  # (script, texto original exacto, texto mutado, descripcion)
]


def main(p1, p3, out):
    import io, contextlib
    orig = diffrun.Game(p1, p3)
    base = MemGame(p3)
    with contextlib.redirect_stdout(io.StringIO()):
        same, cut, diffs, n = run(orig, base)
    res = dict(base=dict(pasos=n, identicos=same, cortados=cut, distintos=len(diffs)))
    print('original vs recompilado en memoria: %d pasos, %d identicos, %d distintos' % (n, same, len(diffs)))
    muts = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mutantes.json')))
    res['mutantes'] = []
    for m in muts:
        t = base.src[m['script']]
        assert t.count(m['de']) >= 1, m
        g = MemGame(p3, {m['script']: t.replace(m['de'], m['a'], 1)})
        with contextlib.redirect_stdout(io.StringIO()):
            same, cut, diffs, n = run(orig, g)
        first = diffs[0]['paso'] if diffs else None
        print('%-9s %-60s -> %s' % ('DETECTADO' if diffs else 'NO VISTO', m['que'][:60],
                                    ('%d pasos distintos; primero: %s' % (len(diffs), first)) if diffs else ''))
        res['mutantes'].append(dict(m, detectado=bool(diffs), pasos_distintos=len(diffs), primero=first))
    json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main(*sys.argv[1:4])
