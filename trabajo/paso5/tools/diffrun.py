# Paso 5 — ejecucion diferencial: corre el juego ORIGINAL y el RECOMPILADO en la
# maquina con grabadora (avmdiff.py) con exactamente el mismo guion y compara
# los efectos paso por paso.
#
# Guion (el mismo para las dos versiones):
#   1. DoInitAction de todos los sprites (clases mx, SWFBridge...).
#   2. Scripts del escenario en orden de fotograma (motor del juego, datos, mod).
#   3. Scripts de todos los sprites, eventos de clips y botones.
#   4. Barrido: se llama a CADA funcion alcanzable desde _root y _global con
#      varios juegos de argumentos.
# Se hace dos veces: con clips "vacios" y con clips que crean hijos al vuelo
# (para entrar en ramas que dependen de que exista un clip).
#
# Uso: python3 diffrun.py P1_ORIG P3_ORIG P1_NUEVO P3_NUEVO [salida.json]
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(30000)
from avmdiff import VM, Obj, Budget, Throw, UNDEF, NULL, is_fn, mkarr, tostr

ARGSETS = ['vacio', 'ceros', 'unos', 'clips', 'texto', 'unidades', 'numeros', 'arreglos', 'mixto', 'jugada']
UNIT = dict(plevel=30.0, LIFEN=1000.0, LIFEU=1000.0, LIFE=1000.0, FOCUSN=300.0, FOCUSU=300.0, FOCUS=300.0,
            STRENGTH=100.0, STRENGTHU=100.0, MAGIC=50.0, MAGICU=50.0, SPEED=60.0, SPEEDU=60.0,
            DEFENSE=40.0, DEFENSEU=40.0, DEF=40.0, DEFU=40.0, PER=30.0, PERU=30.0, SHIELD=0.0,
            SHIELDCOUNTER=0.0, SSWITCH=0.0, DMG=0.0, DMG2=0.0, IDMG=0.0, IDMG2=0.0, IDMGP=0.0,
            IDMGP2=1.0, STUN=0.0, REFLECT=0.0, SILENCED=0.0, FOCUSCHANGE=0.0, HEALMOD=1.0,
            abilityCoolDown=0.0, deadKrin=0.0, isBoss=0.0, playerID=1.0, teamSide=1.0,
            playerName='Sonny', active=True, AIType=1.0)


class Game:
    def __init__(self, p1, p3):
        self.p1 = p1
        self.idx = json.load(open(os.path.join(p3, 'index.json')))
        self.cache = {}

    def code(self, s):
        f = s['loc']['tag']
        if f not in self.cache:
            self.cache[f] = open(os.path.join(self.p1, 'tags', f), 'rb').read()
        return self.cache[f], s['loc']['a0'], s['loc']['a1']


def order(idx):
    init = [s for s in idx if s['file'].startswith('scripts/DoInitAction/')]
    esc = [s for s in idx if s['file'].startswith('scripts/escenario/')]
    rest = [s for s in idx if s not in init and s not in esc]
    return init, esc, rest


class Runner:
    def __init__(self, game, vivify, seed=7, instr=150_000, effects=2000):
        self.g = game
        self.vm = VM(seed=seed, vivify=vivify, max_effects=10 ** 9, max_instr=10 ** 12)
        self.instr = instr; self.effects = effects
        self.steps = []          # (nombre, efectos, resultado)
        self.clips = []          # clips creados para correr scripts (raices del barrido)
        self.byfile = {}
        self.called = set()

    def step(self, name, fn, big=False):
        vm = self.vm
        vm.log = []
        vm.max_effects = self.effects * (1000 if big else 1)
        vm.instr = 0; vm.max_instr = self.instr * (200 if big else 1)
        vm.depth = 0
        res = 'ok'
        try:
            r = fn()
            if r is not None and r is not UNDEF:
                res = 'ok ' + vm.rep(r)
        except Budget as ex:
            res = 'corte:' + str(ex)
        except Throw as ex:
            res = 'throw'
        except RecursionError:
            res = 'corte:recursion'
        self.steps.append((name, vm.log, res))

    def run_scripts(self):
        vm = self.vm
        init, esc, rest = order(self.g.idx)
        for s in init:
            b, a0, a1 = self.g.code(s)
            c = vm.clip('init'); c.props['_parent'] = vm.root
            self.step(s['file'], lambda: vm.run_script(b, a0, a1, vm.root, vm.root), big=True)
        for s in esc:
            b, a0, a1 = self.g.code(s)
            if '/colocacion_' in s['file']:
                c = vm.clip(s['file'].split('/')[3]); c.props['_parent'] = vm.root
                self.clips.append(c); self.byfile[s['file']] = c
                self.step(s['file'], lambda: vm.run_script(b, a0, a1, c, c), big=True)
            else:
                self.step(s['file'], lambda: vm.run_script(b, a0, a1, vm.root, vm.root), big=True)
        for s in rest:
            b, a0, a1 = self.g.code(s)
            c = vm.clip(s['file'].split('/')[1]); c.props['_parent'] = vm.root
            self.clips.append(c); self.byfile[s['file']] = c
            self.step(s['file'], lambda: vm.run_script(b, a0, a1, c, c), big=True)

    def functions(self):
        """Funciones alcanzables desde _root y _global, en orden de ruta."""
        vm = self.vm
        seen = set(); out = []
        queue = [('_root', vm.root, vm.root), ('_global', vm.glob, vm.glob)]
        queue += [('clip%d' % i, c, c) for i, c in enumerate(self.clips)]
        while queue:
            path, o, own = queue.pop(0)
            if id(o) in seen or not isinstance(o, Obj): continue
            seen.add(id(o))
            if is_fn(o) and o.code is not None:
                out.append((path, o, own))
            if path.count('.') > 6: continue
            items = list(o.props.items())
            if o.arr is not None and len(o.arr) < 200:
                items += [(str(i), v) for i, v in enumerate(o.arr)]
            for k, v in sorted(items, key=lambda kv: kv[0]):
                if k in ('_parent', '__constructor__', 'constructor', '_level0'): continue
                if isinstance(v, Obj):
                    queue.append((path + '.' + k, v, o))
        return out

    def owner(self, path):
        vm = self.vm
        parts = path.split('.')
        o = vm.root if parts[0] == '_root' else vm.glob
        for k in parts[1:-1]:
            o = vm.getmember(o, k, vivify_ok=False) if not (isinstance(o, Obj) and o.arr is not None) else o.arr[int(k)] if k.isdigit() and int(k) < len(o.arr) else UNDEF
        return o if isinstance(o, Obj) else vm.root

    def args(self, kind):
        vm = self.vm
        if kind == 'vacio': return []
        if kind == 'ceros': return [0.0] * 6
        if kind == 'unos': return [1.0] * 6
        if kind == 'clips':
            a = []
            for i in range(4):
                c = vm.clip('arg%d' % i); c.props['_parent'] = vm.root; a.append(c)
            return a + [1.0, 2.0]
        if kind == 'numeros': return [5.0, 100.0, -1.0, 0.5, 2.0, 7.0]
        if kind == 'arreglos':
            return [mkarr([1.0, 2.0, 3.0]), mkarr(['a', 'b', 'c']), mkarr([self.unit(1.0)]), 2.0, 1.0, 0.0]
        if kind == 'jugada':
            r = vm.root.props
            return [624.0, 0.0, r.get('playerKrin1', UNDEF), r.get('playerKrin4', UNDEF), 1.0, 4.0]
        if kind == 'mixto':
            return [500.0, self.unit(1.0), self.unit(4.0), True, 1.0, 'player1']
        if kind == 'unidades':
            us = []
            for pid in (1.0, 4.0):
                u = Obj()
                for k2, v2 in UNIT.items(): u.props[k2] = v2
                u.props['playerID'] = pid; u.props['teamSide'] = 1.0 if pid < 4 else 2.0
                bl = []
                for j in range(3):
                    bb = Obj(); bb.props.update(CD=0.0, buffId=float(j + 1), buffValue=0.0); bl.append(bb)
                u.props['BUFFARRAYK'] = mkarr(bl)
                us.append(u)
            return [us[0], us[1], 1.0, 1.0, 0.0, 'player1']
        return ['player1', 2.0, 'enemy1', 1.0, 'HEAL', 3.0]

    def unit(self, pid):
        u = Obj()
        for k2, v2 in UNIT.items(): u.props[k2] = v2
        u.props['playerID'] = pid; u.props['teamSide'] = 1.0 if pid < 4 else 2.0
        bl = []
        for j in range(3):
            bb = Obj(); bb.props.update(CD=1.0, buffId=float(j + 1), buffValue=5.0); bl.append(bb)
        u.props['BUFFARRAYK'] = mkarr(bl)
        return u

    def prepare(self):
        """Estado de partida tipico (como el banco del mod): jugador, equipo y enemigos."""
        vm = self.vm; r = vm.root.props
        K = r.get('Krin')
        if not isinstance(K, Obj):
            K = Obj(); r['Krin'] = K
        base = dict(talentMainArray=mkarr([0.0] * 60), skillPoints=3.0, abilityCoolDown=mkarr([0.0] * 60),
                    moveMatrix=mkarr([623.0, 808.0, 624.0, 1.0, 2.0, 3.0]),
                    moveMatrix2=mkarr([624.0, 625.0, 5.0, 6.0, 809.0]), BattlePick=1.0, totalXP=50.0,
                    LevelStats=mkarr([5.0] * 6), NameSets=mkarr(['Sonny', 'Veradux', 'Roald', 'a', 'b', 'c']),
                    dataMode='none', EnemyXPFinal=10.0)
        for k, v in base.items():
            K.props[k] = v
        r['KRS'] = mkarr([float(i * 37 % 100) for i in range(100)]); r['KRSC'] = 0.0
        for pid in range(1, 7):
            u = self.unit(float(pid)); u.kind = 'movieclip'; u.name = 'playerKrin%d' % pid
            slots = []
            for _ in range(7):
                sl = Obj(); sl.props.update(CD=0.0, buffId='', changeArray=mkarr([0.0] * 14)); slots.append(sl)
            u.props['BUFFARRAYK'] = mkarr(slots); u.props['changeArray'] = mkarr([0.0] * 14)
            r['playerKrin%d' % pid] = u
        self.step('(estado de partida)', lambda: None)
        # fotogramas de combate: se repiten los enterFrame y botones con el combate en marcha
        r['InBattle'] = True
        init, esc, rest = order(self.g.idx)
        for fr in range(3):
            for s in esc + rest:
                if 'enterFrame' not in s['file'] and 'on(' not in s['file']: continue
                b, a0, a1 = self.g.code(s)
                c = self.byfile.get(s['file']) or vm.root
                self.step('combate f%d %s' % (fr, s['file']), lambda b=b, a0=a0, a1=a1, c=c: vm.run_script(b, a0, a1, c, c), big=True)
        r['InBattle'] = False

    def sweep(self, rounds=4):
        vm = self.vm
        total = 0
        for rnd in range(rounds):
            # cada CUERPO de funcion se barre una sola vez (las closures se recrean en cada llamada)
            body = lambda f: (id(f.code), f.start)
            fns = []; ids = set()
            for x in self.functions():
                if body(x[1]) in self.called or body(x[1]) in ids: continue
                fns.append(x); ids.add(body(x[1]))
            # ademas: toda funcion creada que nadie alcanzo (closures, handlers de clips...)
            for k, f in enumerate(list(vm.allfns)):
                if body(f) in self.called or body(f) in ids: continue
                own, key = vm.fowner.get(id(f), (vm.root, ''))
                fns.append(('fn%d.%s' % (k, key or f.name or 'anon'), f, own)); ids.add(body(f))
            if not fns: break
            for path, f, own in fns:
                self.called.add(body(f))
                for k in ARGSETS:
                    def go(path=path, f=f, k=k, own=own):
                        return vm.call(f, own, self.args(k), path)
                    self.step('r%d %s (%s)' % (rnd + 1, path, k), go)
            total += len(fns)
            print('      ronda %d: %d funciones, %d pasos' % (rnd + 1, len(fns), len(self.steps)), flush=True)
        return total


def coverage(game, vm):
    """Instrucciones y funciones del juego que llegaron a ejecutarse."""
    from as2dec import decode
    tot = hit = 0; ftot = fhit = 0; per = {}
    for s in game.idx:
        b, a0, a1 = game.code(s)
        ex = vm.cover.get(id(b), set())
        pos = []; fstarts = []

        def walk(x0, x1, pool):
            for x in decode(b, x0, x1, pool):
                pos.append(x.pos)
                if x.name in ('DefineFunction', 'DefineFunction2'):
                    fstarts.append(x.a['body'][0] if x.a['body'][1] > x.a['body'][0] else None)
                    walk(*x.a['body'], list(x.a['pool']))
        walk(a0, a1, [])
        h = sum(1 for p in pos if p in ex)
        tot += len(pos); hit += h
        ftot += len(fstarts); fhit += sum(1 for p in fstarts if p is not None and p in ex)
        per[s['file']] = [h, len(pos)]
    return hit, tot, fhit, ftot, per


def compare(A, B):
    same = 0; cut = 0; diffs = []
    for (na, la, ra), (nb, lb, rb) in zip(A.steps, B.steps):
        if na != nb:
            diffs.append(dict(paso=na, otro=nb, motivo='guion distinto')); continue
        if ra.startswith('corte:instr') or rb.startswith('corte:instr'):
            n = min(len(la), len(lb))
            if la[:n] == lb[:n]:
                cut += 1; continue
        if la == lb and ra == rb:
            same += 1; continue
        k = next((i for i, (x, y) in enumerate(zip(la, lb)) if x != y), min(len(la), len(lb)))
        diffs.append(dict(paso=na, efecto=k, original=la[k:k + 3], recompilado=lb[k:k + 3],
                          res_original=ra, res_recompilado=rb, n_original=len(la), n_recompilado=len(lb)))
    if len(A.steps) != len(B.steps):
        diffs.append(dict(paso='(fin)', motivo='cantidad de pasos distinta %d vs %d' % (len(A.steps), len(B.steps))))
    return same, cut, diffs


def main(p1a, p3a, p1b, p3b, out=None):
    ga = Game(p1a, p3a); gb = Game(p1b, p3b)
    report = {}
    for vivify in (False, True):
        t0 = time.time()
        A = Runner(ga, vivify); B = Runner(gb, vivify)
        A.run_scripts(); B.run_scripts(); A.prepare(); B.prepare()
        nfa = A.sweep(); nfb = B.sweep()
        same, cut, diffs = compare(A, B)
        eff = sum(len(s[1]) for s in A.steps)
        tag = 'clips que crean hijos' if vivify else 'clips vacios'
        ha, ta, fha, fta, per_a = coverage(ga, A.vm)
        hb, tb, fhb, ftb, per_b = coverage(gb, B.vm)
        print('   cobertura original: %.1f%% de las instrucciones, %d de %d funciones | recompilado: %.1f%%, %d de %d'
              % (100.0 * ha / ta, fha, fta, 100.0 * hb / tb, fhb, ftb))
        print('[%s] pasos %d | identicos %d | cortados por tiempo (iguales hasta el corte) %d | '
              'distintos %d | funciones barridas %d/%d | efectos comparados %d | %.0fs'
              % (tag, len(A.steps), same, cut, len(diffs), nfa, nfb, eff, time.time() - t0))
        for d in diffs[:10]:
            print('   X', json.dumps(d, ensure_ascii=False)[:400])
        report[tag] = dict(pasos=len(A.steps), identicos=same, cortados=cut, distintos=len(diffs),
                           funciones=[nfa, nfb], efectos=eff, diferencias=diffs[:200],
                           resultados=[[s[0], s[2], len(s[1])] for s in A.steps],
                           cobertura=dict(original=[ha, ta, fha, fta], recompilado=[hb, tb, fhb, ftb]),
                           cobertura_por_script=per_a)
        report[tag]['_runners'] = None
        globals()['_last'] = (A, B)
    if out:
        json.dump(report, open(out, 'w'), indent=1, ensure_ascii=False)
    return report


if __name__ == '__main__':
    main(*sys.argv[1:6])
