# Paso 4 — control independiente del descompilador: compara, script por script,
# el ORIGINAL con el RECOMPILADO contando operaciones y valores (sin mirar el
# texto AS2). Si el descompilador hubiera perdido, duplicado o cambiado algo,
# aparece aqui aunque la ida y vuelta de texto salga identica.
#
# Se cuentan: operaciones con efecto (GetMember, CallMethod, Add2, Return...) y
# todos los valores empujados (cadenas, numeros, booleanos, null, undefined).
# No se cuentan: saltos, Not, Pop, registros, ConstantPool y el acceso a
# parametros/this (el original los tiene en registros; la recompilacion, por nombre).
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(20000)
from as2dec import decode, decompile
from as2comp import compile_script

IGNORE = {'Push', 'ConstantPool', 'Jump', 'If', 'Not', 'Pop', 'StoreRegister', 'PushDuplicate',
          'End', 'GetVariable', 'SetVariable', 'DefineFunction', 'DefineFunction2'}


def sig(b, a0=0, a1=None):
    ops = collections.Counter(); vals = collections.Counter(); names = set()

    def walk(s, e, pool):
        for x in decode(b, s, e, pool):
            if x.name == 'Push':
                for v in x.a:
                    if v.kind == 'r': continue
                    if v.kind == 's': vals[('s', v.v)] += 1
                    elif v.kind in ('i', 'n', 'f'): vals[('n', float(v.v))] += 1
                    else: vals[(v.kind, v.v)] += 1
            elif x.name in ('DefineFunction', 'DefineFunction2'):
                ops['function'] += 1
                for r, n in x.a['params']: names.add(n)
                walk(*x.a['body'], list(x.a['pool']))
            elif x.name not in IGNORE:
                ops[x.name] += 1
    walk(a0, a1 if a1 is not None else len(b), [])
    return ops, vals, names


def compare(orig, new):
    o1, v1, n1 = sig(orig); o2, v2, n2 = sig(new)
    skip = n1 | n2 | {'this', 'arguments', 'super', '_root', '_parent', '_global'}
    dv = {}
    for k in set(v1) | set(v2):
        if k[0] == 's' and k[1] in skip: continue
        if v1[k] != v2[k]: dv[k] = (v1[k], v2[k])
    do = {k: (o1[k], o2[k]) for k in set(o1) | set(o2) if o1[k] != o2[k]}
    return do, dv


def main(p1, p3, out=None):
    idx = json.load(open(os.path.join(p3, 'index.json')))
    cache = {}; res = []; tot_o = collections.Counter(); tot_v = collections.Counter()
    for s in idx:
        L = s['loc']; f = L['tag']
        if f not in cache:
            cache.clear(); cache[f] = open(os.path.join(p1, 'tags', f), 'rb').read()
        orig = cache[f][L['a0']:L['a1']]
        a = decompile(orig)[0]
        new = compile_script(a)
        do, dv = compare(orig, new)
        if do or dv:
            res.append(dict(file=s['file'], ops={k: list(v) for k, v in do.items()},
                            vals={repr(k): list(v) for k, v in dv.items()}))
            for k in do: tot_o[k] += 1
            for k in dv: tot_v[k] += 1
    print('scripts con diferencias de operaciones o valores: %d de %d' % (len(res), len(idx)))
    print('operaciones distintas (en cuantos scripts):', dict(tot_o.most_common(20)))
    print('valores distintos (en cuantos scripts):', [(k, n) for k, n in tot_v.most_common(15)])
    if out: json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)
    return res


if __name__ == '__main__':
    main(*sys.argv[1:4])
