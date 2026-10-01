# Paso 4 — prueba de ida y vuelta de TODOS los scripts:
#   original --descompilar--> A  --compilar--> bytecode nuevo --descompilar--> B
# Pasa si A == B (el compilador es el inverso exacto del descompilador).
#
# Uso: python3 roundtrip.py CARPETA_PASO1 CARPETA_PASO3 [salida.json]
import sys, os, re, json, time, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(20000)
from as2dec import decompile
from as2comp import compile_script, CompileError


def norm_labels(t):
    # las etiquetas L_n llevan la posicion en bytes: se renumeran por orden de aparicion
    # '// (valor sin usar)' marca un valor que el original dejaba olvidado en la pila;
    # al recompilar ese valor ya no se deja, asi que la linea desaparece (esperado)
    t = re.sub(r'\n *// \(valor sin usar\)[^\n]*', '', t)
    m = {}
    return re.sub(r'\bL_(\d+|fin)\b', lambda x: m.setdefault(x.group(0), 'L_%d' % (len(m) + 1)), t)


def main(p1, p3, out=None):
    idx = json.load(open(os.path.join(p3, 'index.json')))
    cache = {}
    res = []
    t0 = time.time()
    for s in idx:
        L = s['loc']; f = L['tag']
        if f not in cache:
            cache.clear(); cache[f] = open(os.path.join(p1, 'tags', f), 'rb').read()
        orig = cache[f][L['a0']:L['a1']]
        a, _, _, err = decompile(orig)
        r = dict(file=s['file'], orig=len(orig))
        if err:
            r.update(ok=False, why='descompilar: ' + err); res.append(r); continue
        try:
            nb = compile_script(a)
        except (CompileError, RecursionError) as ex:
            r.update(ok=False, why='compilar: %s' % ex); res.append(r); continue
        b, _, _, err2 = decompile(nb)
        r['new'] = len(nb)
        if err2:
            r.update(ok=False, why='re-descompilar: ' + err2)
        elif norm_labels(a) != norm_labels(b):
            d = list(difflib.unified_diff(a.split('\n'), b.split('\n'), lineterm='', n=1))
            r.update(ok=False, why='distinto', diff=d[:40])
        else:
            r['ok'] = True
        res.append(r)
    ok = sum(1 for r in res if r['ok'])
    print('scripts: %d | ida y vuelta identica: %d | fallan: %d | %.1fs' % (len(res), ok, len(res) - ok, time.time() - t0))
    print('bytes originales: %d | recompilados: %d' % (sum(r['orig'] for r in res), sum(r.get('new', 0) for r in res)))
    for r in [r for r in res if not r['ok']][:15]:
        print('  X', r['file'], '->', r['why'][:150])
        for l in r.get('diff', [])[:12]: print('      ', l[:160])
    if out:
        json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)
    return res


if __name__ == '__main__':
    main(*sys.argv[1:4])
