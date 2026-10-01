# Banco del rework: arma un combate a mano (lobo, enemigos y aliados) sobre el interprete AVM1 fiel
# (bench2.Bench3 + motor.Sim) y deja lanzar habilidades del lobo y avanzar turnos como el reloj.
import sys, os, math
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'banco'))
from motor import Sim
from avmvm import Obj, mkarr, tonum, tostr, is_arr, is_fn, UNDEF

SWF = os.path.join(AQUI, '..', 'i26.swf')
EL = ["Physical", "Magic", "Ice", "Fire", "Lightning", "Earth", "Shadow", "Poison"]


class RW:
    def __init__(self, swf=SWF, seed=7, level=20):
        self.s = Sim(swf, seed=seed)
        self.R = self.s.R
        self.vm = self.s.vm
        K = self.R['Krin'].props
        K['Level'] = float(level)
        K['skillPoints'] = 0.0
        K['talentMainArray'] = mkarr([0.0] * 38)
        K['abilityCoolDown'] = mkarr([0.0] * 8)
        K['moveMatrix'] = mkarr([0.0] * 8)
        K['moveMatrix2'] = mkarr([])
        K['bossFight'] = False
        K['BattlePick'] = 1.0
        self.R['KBR1'] = Obj()
        self.R['KBR1'].props['phases'] = mkarr([])
        self.R['maxBuffLimit'] = 40.0
        self.R['firstUpdate'] = False
        # sin criticos al azar (KRSO = 99); un critico forzado (B[7] = 1000) sigue entrando
        def krrr(this, args):
            self.R['KRSO'] = 99.0
            return UNDEF
        self.R['KRRR'] = self.vm.nf('KRRR', krrr)
        self.units = {}
        for i in range(1, 7):
            u = self.s.blank(i)
            self.R['playerKrin%d' % i] = u
            self.units[i] = u
            bar = Obj('movieclip')
            for k in range(8):
                n = Obj('movieclip'); n.props['buffCounter'] = ''; bar.props['bshr%d' % k] = n
            self.R['p%dBAR' % i] = bar

    # ---------------------------------------------------------------- unidades
    def unit(self, pid, name='U', STR=100, MAG=50, SPD=60, LIFE=5000, FOC=200, lvl=20, per=None, deff=None):
        u = self.units[pid]; P = u.props
        P.update(active=True, playerName=name, plevel=float(lvl), AION=pid != 1)
        P['STRENGTH'] = P['STRENGTHU'] = float(STR)
        P['MAGIC'] = P['MAGICU'] = float(MAG)
        P['SPEED'] = P['SPEEDU'] = float(SPD)
        P['LIFE'] = P['LIFEU'] = P['LIFEN'] = float(LIFE)
        P['FOCUS'] = P['FOCUSU'] = P['FOCUSN'] = float(FOC)
        base = 100 + 15 * lvl
        for el in EL:
            for k in ('PER', 'PERU'): P[k].props[el] = float((per or {}).get(el, base))
            for k in ('DEF', 'DEFU'): P[k].props[el] = float((deff or {}).get(el, base))
        return u

    def call(self, name, *args):
        self.vm.budget = 50_000_000
        return self.vm.call(self.R[name], self.s.r, list(args), name)

    def start(self):
        self.call('__rwBattleStart')

    # ---------------------------------------------------------------- arbol
    def learn(self, sid, rank):
        d = self.R['__rwS'].props[str(sid)].props
        slot = int(tonum(d['slot'])); free = int(tonum(d.get('free', 0.0)))
        tal = self.R['Krin'].props['talentMainArray']
        while len(tal.arr) <= slot: tal.arr.append(0.0)
        tal.arr[slot] = float(max(0, rank - free))
        self.call('__v8Sync')

    def aspect(self, k):
        tal = self.R['Krin'].props['talentMainArray']
        while len(tal.arr) <= 160: tal.arr.append(0.0)
        tal.arr[160] = float(k)
        self.call('__v8Sync')

    def rank(self, sid):
        return tonum(self.call('__rwRank', float(sid)))

    # ---------------------------------------------------------------- acciones
    def cast(self, sid, target=None, caster=1):
        c = self.units[caster]; t = self.units[target] if target else c
        a = self.R['KRINABILITY%d' % sid]; b = self.R['KRINABILITYB%d' % sid]
        P = c.props
        P['FOCUSN'] = tonum(P['FOCUSN']) - tonum(a.arr[5])
        self.paid = tonum(P['FOCUSN'])        # Focus ya pagado: las ganancias se miden desde aqui
        l0 = {i: tonum(u.props.get('LIFEN', 0.0)) for i, u in self.units.items()}
        self.call('executeMove', a, b, c, t)
        self.call('applyChangesKrin', t)
        return {i: round(l0[i] - tonum(u.props.get('LIFEN', 0.0))) for i, u in self.units.items() if l0[i] != tonum(u.props.get('LIFEN', 0.0))}

    def enemy_hit(self, attacker, target, coef=1.0, el='Physical'):
        """ataque directo generico de un enemigo (movimiento nativo 624 = Rake nativo)"""
        a = self.R['KRINABILITY624']; b = self.R['KRINABILITYB624'].arr[:]
        bb = mkarr(b); bb.arr[2] = float(coef); bb.arr[13] = 0.0; bb.arr[0] = el
        u = self.units[target]
        l0 = tonum(u.props.get('LIFEN', 0.0)); s0 = tonum(u.props['SHIELD'])
        self.call('executeMove', a, bb, self.units[attacker], u)
        self.call('applyChangesKrin', u)
        return round(l0 - tonum(u.props.get('LIFEN', 0.0))), round(s0 - tonum(u.props['SHIELD']))

    def tick(self, pid):
        u = self.units[pid]
        l0 = tonum(u.props.get('LIFEN', 0.0))
        self.call('buffTicker', u)
        return round(l0 - tonum(u.props.get('LIFEN', 0.0)))

    def start_turn(self, pid):
        self.call('LowerCD', float(pid))

    # ---------------------------------------------------------------- lectura
    def n(self, fn, pid):
        return tonum(self.call(fn, self.units[pid]))

    def st(self, pid):
        u = self.units[pid]
        return dict(W=self.n('__rwWounds', pid), FB=self.n('__rwFrost', pid), Sc=self.n('__rwScent', pid),
                    Sh=self.n('__rwShards', pid), life=round(tonum(u.props.get('LIFEN', 0.0))), foc=round(tonum(u.props['FOCUSN'])),
                    buffs=self.buffs(pid))

    def buffs(self, pid):
        out = []
        for s in self.units[pid].props['BUFFARRAYK'].arr:
            if isinstance(s, Obj) and tonum(s.props.get('CD', 0)) > 0:
                out.append('%s:%d' % (tostr(s.props.get('buffId')), tonum(s.props.get('CD'))))
        return out

    def has(self, pid, bid):
        return self.call('__rwHas', self.units[pid], bid) is True

    def text(self, sid, r):
        return tostr(self.call('__rwFullDesc', float(sid), float(r)))
