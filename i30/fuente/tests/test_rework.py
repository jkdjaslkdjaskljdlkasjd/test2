# Pruebas del rework (banco AVM1 fiel). Cada prueba arma un combate a mano y compara con la cuenta
# hecha a mano a partir de la propuesta v4. Sin criticos al azar; Piercing = Defensa (el golpe no cambia).
#   python3 test_rework.py [filtro]
import sys, math, traceback
from rwbench import RW
from avmvm import tonum, tostr, Obj

OK = []; BAD = []
def check(name, got, want, tol=0):
    good = abs(got - want) <= tol if isinstance(want, (int, float)) and isinstance(got, (int, float)) else got == want
    (OK if good else BAD).append(name)
    if not good:
        print('  FALLA %-58s obtenido=%r esperado=%r' % (name, got, want))
    return good

def ceil(x):
    return math.ceil(x - 1e-9)

def fresh(learn=None, level=20, aspect=0, STR=200, MAG=50, SPD=70, wolfLife=5000, enemies=1, ally=False, elife=20000):
    b = RW(level=level)
    b.unit(1, 'Sonny', STR=STR, MAG=MAG, SPD=SPD, LIFE=wolfLife, FOC=200)
    b.unit(2, 'Brute', STR=100, SPD=50, LIFE=elife)
    if enemies > 1:
        b.unit(4, 'Grunt', STR=100, SPD=50, LIFE=elife)
    if enemies > 2:
        b.unit(6, 'Imp', STR=100, SPD=50, LIFE=elife)
    if ally:
        b.unit(3, 'Veradux', STR=150, SPD=60, LIFE=6000)
    for sid, r in (learn or {}).items():
        b.learn(sid, r)
    if aspect:
        b.aspect(aspect)
    b.start()
    b.units[1].props['FOCUSN'] = 100.0     # a medio Focus: las ganancias no chocan con el tope
    return b

def U(b, pid, k):
    return tonum(b.units[pid].props[k])

TESTS = []
def test(f):
    TESTS.append(f); return f

# ================================================================== puntos y fichas
@test
def puntos_ancestral():
    b = RW(level=1)
    b.unit(1, 'Sonny')
    K = b.R['Krin'].props
    for L, want in ((1, 0), (2, 1), (4, 3), (5, 5), (9, 9), (10, 11), (15, 17), (20, 23), (30, 33)):
        K['Level'] = float(L)
        b.learn(811, 1)
        check('bonus Ancestral nivel %d' % L, tonum(b.call('__rwBonusTarget')), want)
    # total a nivel 30: 5 iniciales + 29 del juego + 33 extra = 67
    check('puntos totales nivel 30', 5 + 29 + 33, 67)
    b.learn(811, 0)
    check('sin Scent of Blood no hay bonus', tonum(b.call('__rwBonusTarget')), 0)

@test
def puntos_sync_y_migracion():
    b = RW(level=10)
    b.unit(1, 'Sonny')
    K = b.R['Krin'].props
    K['skillPoints'] = 3.0
    tal = K['talentMainArray']
    while len(tal.arr) < 65: tal.arr.append(0.0)
    tal.arr[40] = 2.0; tal.arr[60] = 1.0; tal.arr[48] = 3.0   # arbol viejo: 6 puntos gastados
    b.call('__rwMigrate')
    check('migracion devuelve 6 puntos', tonum(K['skillPoints']), 9)
    check('ranura vieja 40 en 0', tonum(tal.arr[40]), 0)
    b.call('__rwMigrate')
    check('no devuelve dos veces', tonum(K['skillPoints']), 9)
    ok = b.call('__rwLearn', 811.0)
    check('aprender Scent of Blood', ok is True, True)
    # 9 - 1 = 8; bonus nivel 10 = 11 -> 19
    check('bonus sumado al aprender Scent', tonum(K['skillPoints']), 19)
    b.call('__rwRefundAll')
    # devuelve 1 y quita los 11 del bonus: 19 + 1 - 11 = 9
    check('reinicio devuelve y retira el bonus', tonum(K['skillPoints']), 9)

@test
def fichas_y_barra():
    b = fresh(learn={811: 1, 831: 0})
    K = b.R['Krin'].props
    mm2 = [int(tonum(x)) for x in K['moveMatrix2'].arr]
    check('libres en la lista (Rake, Iron Jaws, Wicked, Howl, Canine, Werezombie)', all(x in mm2 for x in (861, 864, 865, 863, 862, 809)), True)
    check('Frozen Maw siempre en la lista', 857 in mm2, True)
    check('Rupture sin aprender no esta', 831 in mm2, False)
    check('pasivas no estan', 811 in mm2, False)
    a = b.R['KRINABILITY819'].arr
    b.learn(819, 2)
    check('Cull R2 cuesta 20', tonum(b.R['KRINABILITY819'].arr[5]), 20)
    check('Cull R2 CD 4', tonum(b.R['KRINABILITY819'].arr[7]), 4)
    b.learn(854, 1)
    mm2 = [int(tonum(x)) for x in K['moveMatrix2'].arr]
    check('definitiva sin su Aspecto no esta', 854 in mm2, False)
    b.aspect(1)
    mm2 = [int(tonum(x)) for x in K['moveMatrix2'].arr]
    check('definitiva con su Aspecto esta', 854 in mm2, True)
    K['moveMatrix'].arr[0] = 854.0
    b.aspect(2)
    check('al cambiar de Aspecto sale de la barra', tonum(K['moveMatrix'].arr[0]), 0)
    check('Expose Throat ya no existe en el arbol', b.R['__rwS'].props.get('813') is None, True)

@test
def barra_de_i25():
    b = RW(level=10)
    b.unit(1, 'Sonny')
    K = b.R['Krin'].props
    from avmvm import mkarr
    K['moveMatrix'] = mkarr([624.0, 628.0, 813.0, 810.0, 623.0, 626.0, 0.0, 5.0])
    b.call('__v8Sync')
    got = [int(tonum(x)) for x in K['moveMatrix'].arr]
    # 624->861, 628->865, 813 (Expose Throat) sale, 810 sin aprender sale, 623->809, 626->863, 5 (otra clase) queda
    check('barra de I25: ids nuevos y Expose Throat fuera', got, [861, 865, 0, 0, 809, 863, 0, 5])

E1 = 'You do not have enough Ability Points.'
E2 = 'This Ability cannot be developed further.'
E3 = 'Your Level is not high enough.'
E4 = "You don't have the required abilites to access this one."
TIERS = [1, 2, 3, 5, 6, 8, 10]

@test
def requisitos():
    # los avisos son los del arbol de clase (KrinLang): los requisitos pesan mas que el nivel, y el nivel mas que
    # los puntos; los requisitos no se escriben con su nombre
    b = RW(level=20)
    b.unit(1, 'Sonny')
    K = b.R['Krin'].props
    K['skillPoints'] = 10.0
    cl = lambda sid: tostr(b.call('__rwCanLearn', float(sid)))
    check('los avisos salen de KrinLang', (tostr(b.call('__rwErr', 1.0)), tostr(b.call('__rwErr', 3.0)), tostr(b.call('__rwErr', 4.0))), (E1, E3, E4))
    check('Rupture sin Hamstring (conexion)', cl(831), E4)
    b.learn(812, 1)
    check('Rupture sin Deep Wounds (otra pagina)', cl(831), E4)
    b.learn(811, 1)
    b.learn(814, 1)
    check('Rupture con Hamstring y Deep Wounds', cl(831), '')
    check('Black Ice sin Cold Trail (conexion)', cl(833), E4)
    for sid in (815, 816, 818):
        b.learn(sid, 1)
    check('Black Ice sin Shardfall (otra pagina)', cl(833), E4)
    b.learn(840, 1)
    check('Black Ice con Cold Trail y Shardfall', cl(833), '')
    K['Level'] = 2.0
    check('Pounce (fila Lvl. 3) a nivel 2', cl(810), E3)
    check('sin requisito y sin nivel: pesa el requisito', cl(824), E4)
    K['Level'] = 3.0
    check('Pounce a nivel 3', cl(810), '')
    K['skillPoints'] = 0.0
    check('sin puntos', cl(810), E1)
    K['skillPoints'] = 10.0
    b.learn(810, 2)
    check('rango maximo', cl(810), E2)
    K['Level'] = 20.0
    check('definitiva sin Aspecto', cl(856), 'Requires Aspect of the Ancestors.')
    b.aspect(4)
    check('definitiva con Aspecto', cl(856), '')

@test
def arbol_forma():
    # como el arbol de clase, ordenado por nivel: cada fila es un escalon (Lvl. 1, 2, 3, 5, 6, 8, 10) y el primer
    # rango de cada habilidad pide el nivel de su fila. Cada conexion es un requisito real y sube de fila: en la
    # misma columna (puede pasar por casillas vacias) o en diagonal a la columna vecina de la fila de arriba, sin
    # cruzarse. Las 6 gratis estan arriba y son las unicas raices de la pagina 1.
    b = RW(level=20)
    b.unit(1, 'Sonny')
    S = b.R['__rwS'].props
    celdas = {}
    malas = []
    nodos = []
    for d in b.R['__rwList'].arr:
        P = d.props
        pg = int(tonum(P['pg']))
        if pg not in (1, 2):
            continue
        sid = int(tonum(P['id'])); c = int(tonum(P['col'])); r = int(tonum(P['row']))
        if (pg, c, r) in celdas:
            malas.append('casilla repetida %d %d' % (sid, celdas[(pg, c, r)]))
        celdas[(pg, c, r)] = sid
        pre = [int(tonum(x)) for x in P['pre'].arr]
        free = tonum(P.get('free', 0.0)) > 0
        lv = [tonum(x) for x in P['lv'].arr]
        nodos.append((pg, sid, c, r, pre, free))
        if any(lv[k + 1] < lv[k] for k in range(len(lv) - 1)):
            malas.append('niveles de rango %d' % sid)
        if free:
            if r > 1 or any(tonum(S[str(q)].props.get('free', 0.0)) <= 0 for q in pre):
                malas.append('gratis fuera de arriba %d' % sid)
        elif lv[0] != TIERS[r]:
            malas.append('nivel %d fila %d: %s' % (sid, r, lv[0]))
        if pg == 1 and not free and not pre:
            malas.append('raiz suelta %d' % sid)
    diag = []
    for pg, sid, c, r, pre, free in nodos:
        for q in pre:
            Q = S[str(q)].props
            qc = int(tonum(Q['col'])); qr = int(tonum(Q['row']))
            if int(tonum(Q['pg'])) != pg or qr >= r:
                malas.append('conexion %d->%d' % (q, sid))
            elif qc == c:
                if any((pg, c, k) in celdas for k in range(qr + 1, r)):
                    malas.append('conexion tapada %d->%d' % (q, sid))
            elif abs(qc - c) == 1 and qr == r - 1:
                diag.append((pg, r, qc, c))
            else:
                malas.append('conexion %d->%d' % (q, sid))
    for x in diag:
        if (x[0], x[1], x[3], x[2]) in diag:
            malas.append('diagonales cruzadas %s' % (x,))
    check('forma del arbol (filas por nivel, conexiones y casillas)', malas, [])
    check('26 activas y 17 pasivas', (sum(1 for k in celdas if k[0] == 1), sum(1 for k in celdas if k[0] == 2)), (26, 17))
    raices2 = sorted(sid for pg, sid, c, r, pre, free in nodos if pg == 2 and not pre)
    check('raices de Instincts: Scent of Blood, Pack Tactics y Thick Hide', raices2, [811, 823, 825])
    K = b.R['Krin'].props
    K['skillPoints'] = 10.0
    cl = lambda sid: tostr(b.call('__rwCanLearn', float(sid)))
    check('Killer Instinct pide Cull the Weak', cl(832), E4)
    check('Frost Fang cuelga de Hamstring', cl(815), E4)
    check('Feeding Frenzy cuelga de Hamstring (diagonal)', cl(834), E4)
    check('Shardfall cuelga de Deep Wounds (diagonal)', cl(840), E4)
    check('Pounce cuelga de Iron Jaws (gratis): se puede', cl(810), '')
    b.learn(819, 1)
    check('con Cull the Weak, Killer Instinct se puede', cl(832), '')

@test
def pocas_al_principio():
    # al principio se abren pocas: a nivel 1 solo Scent of Blood y Thick Hide; despues, fila por fila
    def abiertas(level, learned=()):
        b = RW(level=level)
        b.unit(1, 'Sonny')
        b.R['Krin'].props['skillPoints'] = 10.0
        for sid in learned:
            b.learn(sid, 1)
        out = []
        for d in b.R['__rwList'].arr:
            P = d.props
            sid = int(tonum(P['id']))
            if int(tonum(P['pg'])) in (1, 2) and b.rank(sid) < 1 and tostr(b.call('__rwCanLearn', float(sid))) == '':
                out.append(sid)
        return sorted(out)
    check('nivel 1', abiertas(1), [811, 825])
    check('nivel 2', abiertas(2), [811, 821, 825, 826])
    check('nivel 3 con Scent of Blood', abiertas(3, (811,)), [810, 812, 814, 821, 825, 826])

@test
def menu_2k():
    # menu de habilidades en 2K (rw_80_2k.as): fuera de la pagina de habilidades el arbol usa la grilla del menu de
    # 800; en la pagina (KRINMENU en el fotograma 25) la del 2K, centrada en el recuadro del arbol y dentro de el
    b = RW(level=20)
    b.unit(1, 'Sonny')
    check('sin menu: grilla de 800 (columna 0)', tonum(b.call('__rwColX', 0.0)), 87)
    check('sin menu: grilla de 800 (fila 1)', tonum(b.call('__rwRowY', 1.0)), 164)
    K = Obj(); K.props['_currentframe'] = 25.0
    b.R['KRINMENU'] = K
    check('pagina de habilidades: grilla 2K', b.call('__rw2kPage'), True)
    G = b.R['__rw2kGrid'].props; L = b.R['__rw2kL'].props
    g = lambda k: tonum(G[k])
    box = [tonum(x) for x in L['left'].arr]
    check('columna 0 en 2K', tonum(b.call('__rwColX', 0.0)), g('x0'))
    check('grilla centrada en el recuadro del arbol', g('x0') + 1.5 * g('dx'), (box[0] + box[2]) / 2, 0.01)
    r = 12 * g('ns') / 100                      # medio icono (24 unidades al 100 %)
    check('iconos dentro del recuadro (izquierda)', g('x0') - r > box[0] + 20, True)
    check('niveles a la derecha de la grilla y dentro del recuadro', (g('x0') + 3 * g('dx') + r < g('tx'), g('tx') + g('tw') <= box[2]), (True, True))
    check('ultima fila por encima del selector de pagina', g('y0') + 6 * g('dy') + r < g('py'), True)
    check('selector de pagina dentro del recuadro', g('pbar') < box[3], True)
    check('filas separadas (sin tocarse)', g('dy') > 2 * r + 6, True)
    panel = [tonum(x) for x in L['panel'].arr]
    check('panel dentro del 16:9 y por encima de la barra de navegacion', (panel[0] >= -111.11, panel[2] <= 911.11, panel[3] < 480), (True, True, True))
    check('recuadros dentro del panel', (box[0] > panel[0], tonum(L['right'].arr[2]) < panel[2], box[3] < panel[3]), (True, True, True))
    K.props['_currentframe'] = 1.0
    check('otra pagina: grilla de 800', tonum(b.call('__rwColX', 0.0)), 87)
    b.R['__rw2kEnabled'] = False
    K.props['_currentframe'] = 25.0
    check('__rw2kEnabled = false: grilla de 800', tonum(b.call('__rwColX', 0.0)), 87)

@test
def ancestral_bono():
    # +10% de Health, Strength, Instinct y Speed con Scent of Blood, como en I26. No depende de la llave de la base
    # (_root.__i1AncBonus, que la capa night deja en 0) y no se suma dos veces
    b = RW(level=20)
    check('la capa night deja la llave de la base en 0', tonum(b.R['__i1AncBonus']), 0)
    b.unit(1, 'Sonny', STR=200, MAG=100, SPD=80, LIFE=5000)
    b.unit(2, 'Brute')
    b.learn(811, 1)
    b.start()
    check('con Scent of Blood: +10% de Strength', U(b, 1, 'STRENGTHU'), 220, 1)
    check('con Scent of Blood: +10% de Instinct', U(b, 1, 'MAGICU'), 110, 1)
    check('con Scent of Blood: +10% de Speed', U(b, 1, 'SPEEDU'), 88, 1)
    check('con Scent of Blood: +10% de vida', U(b, 1, 'LIFEU'), 5500, 1)
    check('los puntos extra siguen', tonum(b.call('__rwBonusTarget')), 23)
    b = RW(level=20)
    b.R['__i1AncBonus'] = 0.1
    b.unit(1, 'Sonny', STR=200, LIFE=5000)
    b.unit(2, 'Brute')
    b.learn(811, 1)
    b.start()
    check('con la llave de la base en 0,1 no se suma dos veces', U(b, 1, 'STRENGTHU'), 220, 1)
    b = RW(level=20)
    b.unit(1, 'Sonny', STR=200, LIFE=5000)
    b.unit(2, 'Brute')
    b.start()
    check('sin Scent of Blood no hay bono', (U(b, 1, 'STRENGTHU'), U(b, 1, 'LIFEU')), (200.0, 5000.0))

@test
def rake():
    b = fresh(learn={861: 1})
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(861, 2)
    check('Rake R1 dano 170%', d[2], ceil(S * 1.7))
    st = b.st(2)
    check('Rake R1 pone 2 Wounds', st['W'], 2)
    check('sin Scent of Blood no hay Scent', st['Sc'], 0)
    b = fresh(learn={861: 2, 811: 1})
    b.cast(861, 2); b.cast(861, 2)
    check('Rake R2 sobre herido: 2+3 = 5 -> tope 3 sin Deep Wounds', b.st(2)['W'], 3)
    check('Scent: 1 y luego 2 = 3 -> tope 2 con R1', b.st(2)['Sc'], 2)
    b = fresh(learn={861: 3, 811: 2, 814: 1})
    b.cast(861, 2)
    check('Rake R3: 3 Wounds', b.st(2)['W'], 3)
    b.cast(861, 2)
    check('Rake R3 dos veces: tope 5 con Deep Wounds', b.st(2)['W'], 5)
    check('3 Scent -> Hunted', b.has(2, 'RWHUNTED'), True)

@test
def rake_maestria():
    b = fresh(learn={861: 3, 811: 2, 814: 1})
    b.cast(861, 2); b.cast(861, 2)          # queda Hunted
    b.call('__rwTakeWounds', b.units[2], 99.0)
    b.cast(861, 2)
    check('Rake maestria contra Hunted: 3+1 Wounds', b.st(2)['W'], 4)
    check('Rake maestria: duran 5 turnos', tonum(b.call('__rwWoundLeft', b.units[2])), 5)

@test
def pounce():
    b = fresh(learn={810: 2, 811: 2})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    f0 = U(b, 1, 'FOCUSN')
    d = b.cast(810, 2)
    check('Pounce R2: 190% x (1 + 0.3 x 2 Scent)', d[2], ceil(S * 1.9 * 1.6))
    check('Pounce R2: +10 Focus por Scent', U(b, 1, 'FOCUSN') - b.paid, 20)
    check('Blood Rush 1', b.has(1, 'RWRUSH1'), True)
    b.cast(810, 2); b.cast(810, 2)
    check('Blood Rush 3', b.has(1, 'RWRUSH3'), True)
    # maestria: 1 Wound y 1 Scent; ese Scent es el 3.o -> Hunted, y la maestria de Scent of Blood (R2) suma 2 Wounds
    check('Pounce maestria: a 3 Blood Rush pone 1 Wound y 1 Scent (-> Hunted +2 Wounds)', (b.st(2)['W'], b.has(2, 'RWHUNTED')), (3.0, True))
    # Blood Rush +15%: DMG2
    check('Blood Rush 3 = +15% dano directo', round(U(b, 1, 'DMG2'), 4), 0.15)

@test
def hamstring():
    b = fresh(learn={812: 2, 811: 2})
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(812, 2)
    check('Hamstring R2 205%', d[2], ceil(S * 2.05))
    check('Hamstring -40% Speed', round(U(b, 2, 'SPEEDU')), ceil(50 * 0.6))
    st = b.st(2)
    check('Hamstring 1 Wound', st['W'], 1)
    check('Hamstring 1 Scent (no estaba herido)', st['Sc'], 1)
    b.cast(812, 2)
    check('Hamstring sobre herido: +2 Scent', b.st(2)['Sc'], 3)
    check('Hamstring maestria: Hunted y mas lento -> pierde el turno', b.has(2, 'RWCRIPPLE'), True)
    b.call('__rwDel', b.units[2], 'RWCRIPPLE')
    b.cast(812, 2)
    check('maestria una vez cada 4 turnos', b.has(2, 'RWCRIPPLE'), False)

@test
def rupture():
    b = fresh(learn={831: 2, 814: 2, 811: 1})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddWounds', b.units[2], 5.0, b.units[1])
    per = S * 0.15 * 1.35
    left = tonum(b.call('__rwWoundLeft', b.units[2]))
    d = b.cast(831, 2)
    want = ceil(S * 1.8) + ceil(5 * per * left * 1.5)
    check('Rupture R2: 180% + 150% del sangrado que queda (5 Wounds x 4 turnos)', d[2], want, 1)
    st = b.st(2)
    check('Rupture consume los Wounds', st['W'], 0)
    check('Rupture: 1 Scent cada 2 Wounds (tope 2 con R1)', st['Sc'], 2)
    check('Hemorrhage 3 turnos (maestria con 5)', tonum(b.call('__rwLeft', b.units[2], 'RWHEMO')), 3)
    check('Torn (maestria)', b.has(2, 'RWTORN'), True)
    check('Hemorrhage -20% Defensa Fisica', round(U(b, 2, 'DEFU') if False else tonum(b.units[2].props['DEFU'].props['Physical'])), round(400 * 0.8))
    check('Hemorrhage -15% dano infligido', round(U(b, 2, 'DMG2'), 4), -0.15)
    check('Torn +20% dano recibido', round(U(b, 2, 'IDMG2'), 4), 0.2)
    b = fresh(learn={831: 1, 814: 1})
    b.call('__rwAddWounds', b.units[2], 2.0, b.units[1])
    b.cast(831, 2)
    check('Rupture con 2 Wounds: sin Hemorrhage', b.has(2, 'RWHEMO'), False)

@test
def killer_instinct():
    b = fresh(learn={832: 2})
    S0 = U(b, 1, 'STRENGTH')
    l0 = U(b, 1, 'LIFEN'); f0 = U(b, 1, 'FOCUSN')
    b.cast(832, None)
    check('KI: -10% de la vida actual', l0 - U(b, 1, 'LIFEN'), math.floor(l0 * 0.1))
    check('KI: 2 Wounds sobre el lobo', b.st(1)['W'], 2)
    check('KI: +25 Focus', U(b, 1, 'FOCUSN') - b.paid, 25)
    check('KI R2: +40% Strength', U(b, 1, 'STRENGTHU'), ceil(S0 * 1.4))
    check('KI: +15% dano recibido', round(U(b, 1, 'IDMG2'), 4), 0.15)
    check('KI: dura 3 turnos (CD 4 al ponerlo en su turno)', tonum(b.call('__rwLeft', b.units[1], 'RWKILLER2')), 4)
    b.learn(861, 1)
    b.cast(861, 2)
    check('KI: +1 Wound por habilidad (Rake R1: 2+1)', b.st(2)['W'], 3)
    check('KI: no se puede esquivar', b.call('__rwNoDodge', b.units[1], b.units[2], b.R['KRINABILITY861']) is True, True)
    lt = b.tick(1)
    check('KI: el lobo sangra 2 x 15% de su Strength base', lt, ceil(2 * 0.15 * S0 * 1.15))

@test
def iron_jaws():
    b = fresh(learn={864: 2, 811: 1})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddScent', b.units[2], 1.0, b.units[1])
    d = b.cast(864, 2)
    check('Iron Jaws R2 320%', d[2], ceil(S * 3.2))
    check('Iron Jaws destruye 30 Focus', U(b, 2, 'FOCUSN'), 170)
    check('Iron Jaws: -25% Speed', round(U(b, 2, 'SPEEDU')), ceil(50 * 0.75))
    check('Iron Jaws: +15% dano recibido', round(U(b, 2, 'IDMG2'), 4), 0.15)
    check('consume el Scent -> Silenced', b.has(2, 'RWSILENCE'), True)
    check('Silenced bloquea Focus', U(b, 2, 'SILENCED'), 1)
    b2 = fresh(learn={864: 2, 811: 2})
    b2.call('__rwAddScent', b2.units[2], 3.0, b2.units[1])
    f0 = U(b2, 1, 'FOCUSN')
    b2.cast(864, 2)
    check('contra Hunted destruye 60', U(b2, 2, 'FOCUSN'), 140)
    check('maestria: el Scent devuelve 25 Focus', U(b2, 1, 'FOCUSN') - b2.paid, 25)

@test
def cull():
    b = fresh(learn={819: 3, 811: 2, 814: 1})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    b.call('__rwAddWounds', b.units[2], 4.0, b.units[1])
    d = b.cast(819, 2)
    check('Cull R3: 340% x (1 + 0.8x2 + 0.25x4)', d[2], ceil(S * 3.4 * (1 + 1.6 + 1.0)))
    check('Cull consume el Scent', b.st(2)['Sc'], 0)
    check('Cull no consume los Wounds', b.st(2)['W'], 4)
    # por debajo del 35%
    b = fresh(learn={819: 1}, elife=20000)
    b.units[2].props['LIFEN'] = 6000.0
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(819, 2)
    check('Cull +40% bajo 35%', d[2], ceil(S * 2.6 * 1.4))

@test
def cull_maestria():
    b = fresh(learn={819: 3, 814: 1}, enemies=2)
    b.call('__rwAddWounds', b.units[2], 3.0, b.units[1])
    b.units[2].props['LIFEN'] = 10.0
    b.units[4].props['LIFEN'] = 9000.0
    f0 = U(b, 1, 'FOCUSN')
    b.cast(819, 2)
    check('Cull mata', b.units[2].props['active'], False)
    check('maestria: devuelve el Focus (20)', U(b, 1, 'FOCUSN') - b.paid, 20)
    check('maestria: los Wounds saltan al de menos vida', b.st(4)['W'], 3)

# ================================================================== Winter
@test
def howl():
    b = fresh(learn={863: 3, 811: 2})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    d = b.cast(863, 2)
    check('Howl R3 280%', d[2], ceil(S * 2.8))
    check('Howl: stun 2 turnos', tonum(b.call('__rwLeft', b.units[2], 'RWSTUN')), 2)
    check('Howl R3: 3 Frostbite', b.st(2)['FB'], 3)
    check('Howl consume 2 Scent', b.st(2)['Sc'], 0)
    check('Ancestral Dread (25 Focus por turno)', b.has(2, 'RWDREAD'), True)
    b.tick(2)
    check('Dread: -25 Focus al terminar su turno', U(b, 2, 'FOCUSN'), 175)
    b2 = fresh(learn={863: 1})
    b2.units[2].props['STUN'] = 0.0
    b2.R['Krin'].props['bossFight'] = True
    b2.cast(863, 2)
    check('Howl aturde tambien a jefes', U(b2, 2, 'STUN') > 0, True)

@test
def howl_maestria():
    b = fresh(learn={863: 3, 811: 2}, enemies=3)
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    b.cast(863, 2)
    check('maestria: los otros enemigos +1 Frostbite', (b.st(4)['FB'], b.st(6)['FB']), (1.0, 1.0))
    check('maestria: los otros -15 Focus', (U(b, 4, 'FOCUSN'), U(b, 6, 'FOCUSN')), (185.0, 185.0))

@test
def wicked_claws():
    b = fresh(learn={865: 3, 814: 1})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddWounds', b.units[2], 5.0, b.units[1])
    d = b.cast(865, 2)
    check('Wicked Claws R3 245% hielo', d[2], ceil(S * 2.45), 1)
    check('R3: 2 Frostbite +2 por 5 Wounds (tope +2)', b.st(2)['FB'], 4)
    check('-20% curacion recibida', round(U(b, 2, 'HEALMOD_MINUS'), 4), 0.8)
    # maestria contra Brittle
    b = fresh(learn={865: 3})
    b.call('__rwSetFrost', b.units[2], 3.0, b.units[1])
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(865, 2)
    first = ceil(S * 2.45 * 1.2)
    check('maestria contra Brittle: +60% del golpe en un segundo golpe', d[2], first + ceil(first * 0.6), 1)
    check('3 + 2 + 1 Frostbite = 6 -> se congela (0)', (b.st(2)['FB'], b.has(2, 'RWSOLID')), (0.0, True))

@test
def instinto():
    # Instinct x1.4 mayor que Strength: usa Instinct
    b = fresh(learn={865: 1}, STR=100, MAG=200)
    I = U(b, 1, 'MAGICU')
    d = b.cast(865, 2)
    check('Wicked Claws con Instinct: 185% x1.4 de Instinct', d[2], ceil(I * 1.85 * 1.4))
    d = b.cast(861, 2)
    check('Rake (Hunt) siempre con Strength', d[2], ceil(U(b, 1, 'STRENGTHU') * 1.7))

@test
def frost_fang():
    b = fresh(learn={815: 3, 814: 2})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddWounds', b.units[2], 4.0, b.units[1])
    per = S * 0.15 * 1.35; left = tonum(b.call('__rwWoundLeft', b.units[2]))
    d = b.cast(815, 2)
    want = ceil(S * 2.6) + ceil(3 * per * left)
    check('Frost Fang R3: 260% + sangrado de 3 Wounds como hielo', d[2], want, 1)
    check('quedan 1 Wound', b.st(2)['W'], 1)
    check('3 Wounds -> 3 Frostbite', b.st(2)['FB'], 3)
    # maestria: si congela, +20 Focus y no consume
    b = fresh(learn={815: 3, 814: 1})
    b.call('__rwSetFrost', b.units[2], 4.0, b.units[1])
    b.call('__rwAddWounds', b.units[2], 3.0, b.units[1])
    f0 = U(b, 1, 'FOCUSN')
    b.cast(815, 2)
    check('maestria: congela', b.has(2, 'RWSOLID'), True)
    check('maestria: +20 Focus (el costo ya se pago)', U(b, 1, 'FOCUSN') - b.paid, 20)
    check('maestria: los Wounds no se consumen', b.st(2)['W'], 3)

@test
def shatter_guard():
    b = fresh(learn={816: 2})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwSetFrost', b.units[2], 5.0, b.units[1])
    d = b.cast(816, 2)
    check('Shatter Guard R2: 145% x 5 (Brittle +20%)', d[2], ceil(S * 1.45 * 5 * 1.2))
    st = b.st(2)
    check('consume todo el Frostbite', st['FB'], 0)
    check('1 Wound cada 2 Frostbite', st['W'], 2)
    check('1 Ice Shard cada 2 Frostbite', b.st(1)['Sh'], 2)
    check('maestria con 5: Fragile', b.has(2, 'RWFRAGILE'), True)
    b = fresh(learn={816: 1})
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(816, 2)
    check('sin Frostbite golpea una vez', d[2], ceil(S * 1.15))

@test
def cold_trail():
    b = fresh(learn={818: 3, 814: 1}, enemies=3)
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwSetFrost', b.units[4], 1.0, b.units[1])
    b.call('__rwAddWounds', b.units[6], 1.0, b.units[1])
    d = b.cast(818, 2)
    check('Cold Trail golpea a todos 180%', (d.get(2), d.get(4), d.get(6)), (ceil(S * 1.8),) * 3)
    check('1 Frostbite y 1 Wound', (b.st(2)['FB'], b.st(2)['W']), (1.0, 1.0))
    check('maestria: ya tenia Frostbite -> +2', b.st(4)['FB'], 3)
    check('maestria: ya tenia Wounds -> +2', b.st(6)['W'], 3)

@test
def black_ice():
    b = fresh(learn={833: 2, 840: 2, 816: 2, 818: 1}, enemies=2)
    b.call('__rwAddShards', 4.0)
    S = U(b, 1, 'STRENGTHU')
    b.cast(833, 2)
    check('Black Ice consume los Shards', b.st(1)['Sh'], 0)
    check('Black Ice en todos los enemigos 3 turnos', (tonum(b.call('__rwLeft', b.units[2], 'RWBLACKICE')), tonum(b.call('__rwLeft', b.units[4], 'RWBLACKICE'))), (3.0, 3.0))
    # el enemigo actua sobre el hielo
    l0 = U(b, 2, 'LIFEN')
    b.enemy_hit(2, 1, 0.5)
    check('al actuar: 1 Frostbite', b.st(2)['FB'], 1)
    check('al actuar: 20% x 4 Shards', l0 - U(b, 2, 'LIFEN'), ceil(S * 0.2 * 4))
    b.cast(818, 2)
    check('Cold Trail sobre el hielo: 2 Frostbite', b.st(4)['FB'], 2)
    check('Cold Trail alarga el hielo 1 turno', tonum(b.call('__rwLeft', b.units[4], 'RWBLACKICE')), 4)

# ================================================================== Pack
@test
def canine():
    b = fresh(learn={862: 2, 814: 1, 811: 1}, ally=True)
    b.call('__rwAddWounds', b.units[2], 4.0, b.units[1])
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    S0 = U(b, 3, 'STRENGTH')
    b.cast(862, 3)
    check('Canine R2 +25% Strength', U(b, 3, 'STRENGTHU'), ceil(S0 * 1.25))
    # regla del usuario (26/09): sube por Wounds o por Scent, no por los dos; Canine solo cuenta Wounds
    check('Canine: 2 + 4 Wounds/2 = 4 turnos (el Scent no cuenta)', tonum(b.call('__rwLeft', b.units[3], 'RWCANINE2')), 4)
    check('maestria: el lobo recibe la mitad', b.has(1, 'RWCANINEH'), True)
    # el aliado pega +5% por Wound
    l0 = U(b, 2, 'LIFEN')
    a = b.R['KRINABILITY624']; bb = b.R['KRINABILITYB624']
    b.call('executeMove', a, bb, b.units[3], b.units[2])
    got = l0 - U(b, 2, 'LIFEN')
    base = U(b, 3, 'STRENGTHU') * tonum(bb.arr[2])
    check('aliado con Canine: +20% por 4 Wounds (+2x3% Pack Tactics no aprendida)', got, ceil(base * 1.2), 1)

@test
def feeding_frenzy_y_frostbound():
    b = fresh(learn={834: 2, 835: 2, 814: 1}, ally=True)
    b.cast(834, None); b.cast(835, None)
    check('Frenzy y Frostbound en el aliado', (b.has(3, 'RWFRENZY'), b.has(3, 'RWFROSTPACK')), (True, True))
    check('no en el lobo', b.has(1, 'RWFRENZY'), False)
    b.call('__rwAddWounds', b.units[2], 5.0, b.units[1])
    b.call('__rwSetFrost', b.units[2], 2.0, b.units[1])
    b.units[3].props['LIFEN'] = 3000.0
    l0 = U(b, 2, 'LIFEN'); h0 = U(b, 3, 'LIFEN')
    a = b.R['KRINABILITY624']; bb = b.R['KRINABILITYB624']
    b.call('executeMove', a, bb, b.units[3], b.units[2])
    got = l0 - U(b, 2, 'LIFEN')
    base = U(b, 3, 'STRENGTHU') * tonum(bb.arr[2])
    # Frenzy R2: 8% x 5 = 40%; Frostbound R2: 6% x 2 = 12%; maestria Frenzy (5 Wounds) x1.5
    check('aliado: (1 + 0.40 + 0.12) x 1.5', got, ceil(base * 1.52 * 1.5), 2)
    check('Frenzy maestria consume 1 Wound', b.st(2)['W'], 4)
    check('Frostbound: primer ataque +1 Frostbite', b.st(2)['FB'], 3)
    check('Frenzy R2 cura 15% del dano', U(b, 3, 'LIFEN') - h0, ceil(got * 0.15), 1)

@test
def rallying_cry():
    b = fresh(learn={821: 3, 814: 1, 811: 2}, ally=True)
    b.call('__rwAddWounds', b.units[2], 3.0, b.units[1])
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    b.call('__rwSetFrost', b.units[2], 2.0, b.units[1])
    b.units[3].props['LIFEN'] = 1000.0     # por debajo del 30% de 6000
    S = U(b, 1, 'STRENGTHU')
    amt = (S * 3.6 + 6000 * 0.15) * (1 + 0.5)    # 3 Wounds + 2 Frostbite (el Scent no cuenta)
    b.cast(821, 3)
    check('Rallying Cry R3 + maestria (cura otra vez 50%)', U(b, 3, 'LIFEN') - 1000, min(5000, ceil(amt) + ceil(amt * 0.5)), 2)
    check('Courage +25%', (b.has(3, 'RWCOURAGE'), round(tonum(b.units[3].props['__rwCourage']), 2)), (True, 0.25))

@test
def guardian():
    b = fresh(learn={822: 2, 811: 1}, ally=True)
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    b.cast(822, 3)
    sh = S * 2.2 * 1.7
    check('Guardian R2: escudo 220% +35% x2 Scent', U(b, 1, 'SHIELD'), ceil(sh), 1)
    check('guardia 2 + 2 turnos', tonum(b.call('__rwLeft', b.units[3], 'RWGUARD')), 4)
    lost, _ = b.enemy_hit(2, 3, 2.0)
    raw = 100 * 2.0
    check('el aliado recibe 60% (40% va al escudo)', lost, ceil(raw * 0.6), 1)
    check('quien golpea al aliado +1 Frostbite', b.st(2)['FB'], 1)
    check('el escudo del lobo absorbio 40%', ceil(sh) - U(b, 1, 'SHIELD'), round(raw * 0.4), 2)

@test
def echo_ward():
    b = fresh(learn={824: 3, 811: 1}, ally=True)
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    b.cast(824, 2)
    check('Echo Ward R3 escudo 200% a todos', (U(b, 1, 'SHIELD'), U(b, 3, 'SHIELD')), (ceil(S * 2.0), ceil(S * 2.0)))
    check('consume 2 Scent', b.st(2)['Sc'], 0)
    check('maestria: 2 Frostbite por Scent', b.st(2)['FB'], 4)
    b.enemy_hit(2, 3, 0.5)
    check('quien golpea a un aliado con escudo sufre 1 Wound', b.st(2)['W'], 1)

@test
def primal_breath():
    b = fresh(learn={808: 2, 811: 1}, ally=True)
    b.call('__rwAddScent', b.units[2], 2.0, b.units[1])
    b.units[3].props['FOCUSN'] = 50.0
    b.cast(808, None)
    check('Primal R2: +20 Focus al instante', U(b, 3, 'FOCUSN'), 70)
    check('3 + 2 turnos (2 Scent)', tonum(b.call('__rwLeft', b.units[3], 'RWPRIMAL2')), 5)
    check('+20% Speed', round(U(b, 3, 'SPEEDU')), ceil(60 * 1.2))
    b.tick(3)
    check('+15 Focus por turno', U(b, 3, 'FOCUSN'), 85)
    # al terminar (maestria): cura 15% y +15% dano
    b.call('__rwSetLeft', b.units[3], 'RWPRIMAL2', 1.0)
    b.units[3].props['LIFEN'] = 3000.0
    b.tick(3)
    check('maestria: al terminar cura 15%', U(b, 3, 'LIFEN'), 3900)
    check('maestria: +15% dano 2 turnos', tonum(b.call('__rwLeft', b.units[3], 'RWPRIMALEND')), 2)

# ================================================================== Endurance
@test
def werezombie():
    b = fresh(learn={809: 2, 811: 1, 814: 1})
    S0 = U(b, 1, 'STRENGTH')
    b.cast(809, None)
    anc = tonum(b.call('__rwAncBonus'))  # +10% de Ancestral Wolf (con Scent of Blood)
    check('Werezombie R2 +35% Strength (+10% de Ancestral Wolf)', U(b, 1, 'STRENGTHU'), ceil(S0 * (1.35 + anc)), 1)
    b.units[1].props['LIFEN'] = 2000.0
    b.tick(1)
    check('regenera 12% de la vida maxima', U(b, 1, 'LIFEN'), 2000 + ceil(U(b, 1, 'LIFEU') * 0.12))
    b.cast(857, 2)
    check('golpes directos ponen 1 Wound', b.st(2)['W'], 1)
    # maestria: Scent consumido alarga y cura
    b.learn(864, 1)
    b.call('__rwAddScent', b.units[2], 1.0, b.units[1])
    left0 = tonum(b.call('__rwLeft', b.units[1], 'RWWERE2'))
    b.cast(864, 2)
    check('maestria: +1 turno por Scent consumido', tonum(b.call('__rwLeft', b.units[1], 'RWWERE2')), left0 + 1)

@test
def taste_of_blood():
    b = fresh(learn={836: 2, 814: 1})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddWounds', b.units[2], 3.0, b.units[1])
    b.units[1].props['LIFEN'] = 1000.0
    d = b.cast(836, 2)
    check('Taste of Blood R2 210%', d[2], ceil(S * 2.1))
    check('bebe 1 Wound', b.st(2)['W'], 2)
    check('cura 80% del dano + 5% por Wound que queda (2)', U(b, 1, 'LIFEN') - 1000, ceil(d[2] * 0.8 + 5000 * 0.05 * 2), 1)

@test
def rime_coat_y_escarcha_defensiva():
    b = fresh(learn={837: 2, 840: 2})
    b.call('__rwAddShards', 3.0)
    b.cast(837, None)
    check('Rime Coat consume 3 Shards', b.st(1)['Sh'], 0)
    check('Rime Coat R2: 25% + 3 x 5% = 40%', round(tonum(b.units[1].props['__rwRimeRed']), 2), 0.4)
    lost, _ = b.enemy_hit(2, 1, 2.0)
    check('el lobo recibe 60%', lost, ceil(200 * 0.6), 1)
    check('quien golpea +1 Frostbite', b.st(2)['FB'], 1)

@test
def second_wind():
    b = fresh(learn={826: 2, 814: 1}, enemies=2)
    b.call('__rwAddWounds', b.units[2], 1.0, b.units[1])
    b.call('__rwAddWounds', b.units[4], 4.0, b.units[1])
    b.units[1].props['LIFEN'] = 500.0
    b.cast(826, None)
    check('Second Wind R2: 15% + 3 x 20% = 75%', U(b, 1, 'LIFEN'), 500 + 5000 * 0.75, 1)
    check('bebe del mas herido', (b.st(4)['W'], b.st(2)['W']), (1.0, 1.0))

@test
def last_stand():
    b = fresh(learn={827: 2, 811: 2})
    b.call('__rwAddScent', b.units[2], 3.0, b.units[1])
    b.cast(827, None)
    check('Last Stand R2: 70% + 3 x 5% = 85%', round(tonum(b.units[1].props['__rwStandRed']), 2), 0.85)
    check('dura 1 turno (CD 2 en su turno)', tonum(b.call('__rwLeft', b.units[1], 'RWSTAND2')), 2)
    lost, _ = b.enemy_hit(2, 1, 2.0)
    check('recibe 15%', lost, ceil(200 * 0.15), 1)
    check('maestria: el atacante +2 Frostbite', b.st(2)['FB'], 2)
    b.call('__rwSetFrost', b.units[2], 3.0, b.units[1])
    b.enemy_hit(2, 1, 0.5)
    check('maestria: atacante Brittle queda congelado', b.has(2, 'RWSOLID'), True)

@test
def ice_tomb():
    b = fresh(learn={838: 1}, ally=True)
    b.call('__rwAddWounds', b.units[3], 1.0, b.units[1])
    b.units[3].props['LIFEN'] = 3000.0
    b.cast(838, 3)
    check('Ice Tomb: aturdido', U(b, 3, 'STUN') > 0, True)
    lost, _ = b.enemy_hit(2, 3, 2.0)
    check('Ice Tomb: -90% dano', lost, ceil(200 * 0.1), 1)
    b.tick(3)
    check('al romperse cura 15%', U(b, 3, 'LIFEN'), 3000 - ceil(200 * 0.1) + 900, 1)
    check('maestria: los enemigos +1 Frostbite', b.st(2)['FB'], 1)

# ================================================================== Wounds, Frostbite, congelado
@test
def wounds_turnos():
    b = fresh(learn={861: 1, 814: 1})
    S = U(b, 1, 'STRENGTHU')
    b.cast(861, 2)
    ticks = []
    for k in range(5):
        ticks.append(b.tick(2))
    per = ceil(2 * S * 0.15 * 1.2)
    check('Wounds (Deep Wounds R1): 3 tics y se van', ticks, [per, per, per, 0, 0])

@test
def frozen_blood_y_scent():
    b = fresh(learn={841: 2, 811: 1, 814: 1})
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddWounds', b.units[2], 2.0, b.units[1])
    b.call('__rwSetFrost', b.units[2], 2.0, b.units[1])
    t = b.tick(2)
    check('Frozen Blood R2: +10% por Frostbite (2) a los Wounds', t, ceil(2 * S * 0.15 * 1.2 * 1.2), 1)
    check('Scent of Blood: un Wound sobre un congelado da 1 Scent', b.st(2)['Sc'], 1)

@test
def relentless_hunt():
    # Relentless Hunt cuenta Scent y Frostbite consumidos, no Wounds
    b = fresh(learn={820: 2, 811: 2, 814: 1, 831: 1, 864: 1})
    b.call('__rwAddWounds', b.units[2], 4.0, b.units[1])
    b.units[1].props['FOCUSN'] = 50.0
    f0 = U(b, 1, 'FOCUSN')
    b.cast(831, 2)
    spent = tonum(b.R['__rwS'].props['831'].props['foc'].arr[0])
    check('Rupture consume 4 Wounds: sin Focus de Relentless Hunt', U(b, 1, 'FOCUSN') - f0, -spent)
    b = fresh(learn={820: 2, 811: 2, 864: 1})
    b.call('__rwAddScent', b.units[2], 1.0, b.units[1])
    b.units[1].props['FOCUSN'] = 50.0
    f0 = U(b, 1, 'FOCUSN')
    b.cast(864, 2)
    spent = tonum(b.R['__rwS'].props['864'].props['foc'].arr[0])
    check('Iron Jaws consume 1 Scent: +9 Focus', U(b, 1, 'FOCUSN') - f0, 9 - spent)

@test
def congelar_y_winters_grip():
    b = fresh(learn={842: 2, 840: 1, 820: 2, 829: 2})
    f0 = U(b, 1, 'FOCUSN')
    b.call('__rwSetFrost', b.units[2], 5.0, b.units[1])
    b.call('__rwAddFrost', b.units[2], 1.0, b.units[1])
    check('6.o Frostbite congela', b.has(2, 'RWSOLID'), True)
    check('al congelar: +2 Ice Shards', b.st(1)['Sh'], 2)
    check('Relentless R2: +15 Focus al congelar', U(b, 1, 'FOCUSN') - f0, 15)
    check('Winter Heart maestria: escudo 15%', U(b, 1, 'SHIELD'), ceil(5000 * 0.15 * 1.0), 60)
    check('maestria Winter\'s Grip: 2 turnos (no jefe)', tonum(b.call('__rwLeft', b.units[2], 'RWSOLID')), 2)
    b.tick(2); b.tick(2)
    check('al descongelarse conserva 2 Frostbite', b.st(2)['FB'], 2)
    b.call('__rwAddFrost', b.units[2], 4.0, b.units[1])
    check('inmune a congelarse 3 turnos: se queda en 5', (b.has(2, 'RWSOLID'), b.st(2)['FB']), (False, 5.0))

@test
def cold_snap():
    b = fresh(learn={843: 2, 814: 1})
    S = U(b, 1, 'STRENGTHU')
    l0 = U(b, 2, 'LIFEN'); f0 = U(b, 2, 'FOCUSN')
    b.call('__rwAddFrost', b.units[2], 3.0, b.units[1])
    check('Cold Snap: -15 Focus al quedar Brittle', f0 - U(b, 2, 'FOCUSN'), 15)
    check('Cold Snap R2: 60% de hielo', l0 - U(b, 2, 'LIFEN'), ceil(S * 0.6), 1)
    check('maestria: 1 Wound', b.st(2)['W'], 1)

@test
def deep_wounds_estallido():
    b = fresh(learn={814: 2}, enemies=3)
    S = U(b, 1, 'STRENGTHU')
    b.call('__rwAddWounds', b.units[2], 4.0, b.units[1])
    per = S * 0.15 * 1.35
    left = tonum(b.call('__rwWoundLeft', b.units[2]))
    b.units[2].props['LIFEN'] = 5.0
    l4 = U(b, 4, 'LIFEN')
    b.cast(857, 2)
    check('muere', b.units[2].props['active'], False)
    check('Deep Wounds R2: los otros reciben 50% del sangrado que quedaba', l4 - U(b, 4, 'LIFEN'), ceil(4 * per * left * 0.5), 1)

@test
def bloodhound():
    b = fresh(learn={839: 2, 814: 1})
    b.call('__rwAddWounds', b.units[2], 4.0, b.units[1])
    b.units[2].props['FOCUSN'] = 25.0
    b.enemy_hit(2, 1, 0.5)
    check('Bloodhound R2: -3 x 4 Wounds = -12 Focus al actuar', U(b, 2, 'FOCUSN'), 13)
    check('maestria: Terrified bajo 20 Focus', b.has(2, 'RWTERROR'), True)
    check('Terrified -20% dano', round(U(b, 2, 'DMG2'), 4), -0.2)
    f0 = U(b, 1, 'FOCUSN')
    b.cast(857, 2)
    check('atacar a un Terrified devuelve 5 Focus (+5 de Frozen Maw)', U(b, 1, 'FOCUSN') - b.paid, 10)

@test
def predators_patience():
    b = fresh(learn={817: 2, 811: 2, 814: 1})
    b.call('__rwAddScent', b.units[2], 3.0, b.units[1])
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(861, 2)
    # Piercing +30%: PER/DEF = 1.3 -> coef = 1 + 0.07 x (1.3 - 1) = 1.021; Hunted +15%
    check('Predator\'s Patience R2 +30% Piercing (3 Scent)', d[2], ceil(S * 1.7 * 1.021 * 1.15), 1)

@test
def pack_tactics():
    b = fresh(learn={823: 2, 811: 2, 814: 1}, ally=True)
    b.call('__rwAddScent', b.units[2], 3.0, b.units[1])
    b.call('__rwAddWounds', b.units[2], 5.0, b.units[1])
    b.units[3].props['LIFEN'] = 3000.0
    f0 = U(b, 1, 'FOCUSN')
    l0 = U(b, 2, 'LIFEN'); h0 = U(b, 3, 'LIFEN')
    a = b.R['KRINABILITY624']; bb = b.R['KRINABILITYB624']
    b.call('executeMove', a, bb, b.units[3], b.units[2])
    got = l0 - U(b, 2, 'LIFEN')
    base = U(b, 3, 'STRENGTHU') * tonum(bb.arr[2])
    check('Pack Tactics R2: +15% (5 Wounds; el Scent no suma), Hunted +15%', got, ceil(base * 1.15 * 1.15), 2)
    check('R2: cura 15% contra Hunted', U(b, 3, 'LIFEN') - h0, ceil(got * 0.15), 1)
    check('maestria: +5 Focus al lobo', U(b, 1, 'FOCUSN') - f0, 5)

@test
def shared_hunger_y_blood_drinker():
    b = fresh(learn={844: 2, 846: 2, 814: 1}, ally=True)
    b.call('__rwAddWounds', b.units[2], 3.0, b.units[1])
    b.units[3].props['LIFEN'] = 1000.0
    b.units[1].props['LIFEN'] = 4000.0
    t = b.tick(2)
    check('Shared Hunger R2: el aliado mas herido cura 30%', U(b, 3, 'LIFEN') - 1000, ceil(t * 0.3), 1)
    check('Blood Drinker R2: el lobo cura 25%', U(b, 1, 'LIFEN') - 4000, ceil(t * 0.25), 1)

@test
def cold_comfort_y_thick_hide():
    b = fresh(learn={845: 2, 825: 2}, ally=True)
    b.call('__rwSetFrost', b.units[2], 5.0, b.units[1])
    lost, _ = b.enemy_hit(2, 3, 2.0)
    # atacante con 5 Frostbite: -15% dano infligido (Frostbite) y Cold Comfort -15%
    check('Cold Comfort R2: -3% x 5', lost, ceil(200 * 0.85 * 0.85), 1)
    lost, _ = b.enemy_hit(2, 1, 2.0)
    # Thick Hide R2: +28% Defensa (el golpe baja por Piercing/Defensa) y -12%; maestria -10%
    coef = 400 / (400 * 1.28)
    check('Thick Hide R2 + maestria', lost, ceil(200 * 0.85 * coef * 0.88 * 0.9), 1)

@test
def unyielding_y_winter_heart():
    # consumir un Scent ya no activa Unyielding ni Winter Heart (sube por Wounds o por Scent, no por los dos)
    b = fresh(learn={828: 2, 829: 2, 811: 2, 864: 1})
    b.call('__rwAddScent', b.units[2], 1.0, b.units[1])
    b.call('__rwAddWounds', b.units[1], 2.0, b.units[1])
    b.cast(864, 2)
    check('Unyielding: consumir un Scent no quita el DoT', b.st(1)['W'], 2)
    check('Winter Heart: consumir un Scent no da escudo', U(b, 1, 'SHIELD'), 0)
    b = fresh(learn={828: 2, 829: 2, 811: 2, 814: 1, 836: 1})
    b.call('__rwAddWounds', b.units[2], 3.0, b.units[1])
    b.call('__rwAddWounds', b.units[1], 2.0, b.units[1])
    b.cast(836, 2)
    check('Unyielding: beber un Wound quita un DoT (Wounds propios)', b.st(1)['W'], 0)
    check('Winter Heart R2: escudo 10% por Wound consumido', U(b, 1, 'SHIELD'), ceil(U(b, 1, 'LIFEU') * 0.1))
    f0 = U(b, 1, 'FOCUSN')
    b.tick(1)
    check('Unyielding R2: +5 Focus por turno', U(b, 1, 'FOCUSN') - f0, 5)

@test
def undying_will():
    b = fresh(learn={830: 1}, wolfLife=1000)
    b.units[1].props['LIFEN'] = 50.0
    b.call('__rwAddWounds', b.units[1], 1.0, b.units[1])
    b.enemy_hit(2, 1, 5.0)
    check('Undying Will: queda en 25%', U(b, 1, 'LIFEN'), 250)
    check('Undying Will: escudo 20%', U(b, 1, 'SHIELD'), 200)
    check('Undying Will: limpio', b.st(1)['W'], 0)
    check('maestria: el atacante 3 Scent/3 Frostbite/3 Wounds (sin pasivas: 0 Scent)', (b.st(2)['FB'], b.st(2)['W']), (3.0, 3.0))
    b.units[1].props['SHIELD'] = 0.0
    b.enemy_hit(2, 1, 50.0)
    check('una sola vez por combate', b.units[1].props['active'], False)

@test
def shardfall():
    b = fresh(learn={840: 2, 816: 2})
    b.call('__rwAddShards', 5.0)
    check('Shardfall R2: tope 5', b.st(1)['Sh'], 5)
    f0 = U(b, 1, 'FOCUSN')
    b.tick(1)
    check('+2 Focus por Shard', U(b, 1, 'FOCUSN') - f0, 10)
    lost, _ = b.enemy_hit(2, 1, 2.0)
    check('-3% dano por Shard', lost, ceil(200 * 0.85), 1)
    check('R2: con 3+ Shards el atacante +1 Frostbite', b.st(2)['FB'], 1)
    b2 = fresh(learn={816: 1})
    b2.call('__rwAddShards', 5.0)
    check('sin Shardfall el tope es 2', b2.st(1)['Sh'], 2)

# ================================================================== Aspectos y definitivas
@test
def aspectos_basicos():
    b = fresh(learn={814: 1}, aspect=1)
    b.call('__rwAddWounds', b.units[2], 9.0, b.units[1])
    check('Blood Moon: tope 7 Wounds', b.st(2)['W'], 7)
    b.call('__rwAddFrost', b.units[2], 3.0, b.units[1])
    check('Blood Moon: cada Frostbite 1 menos (3 -> 2)', b.st(2)['FB'], 2)
    b = fresh(aspect=2)
    b.call('__rwAddFrost', b.units[2], 7.0, b.units[1])
    check('Long Winter: tope 7 Frostbite', (b.st(2)['FB'], b.has(2, 'RWSOLID')), (7.0, False))
    check('Long Winter: Wounds 1 turno menos', tonum(b.call('__rwWoundTurns')), 2)
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(857, 2)
    check('Long Winter: Brittle +30%', d[2], ceil(S * tonum(b.call('__rwMawMult')) * 1.3), 1)
    b = fresh(aspect=3, ally=True)
    S0 = U(b, 3, 'STRENGTH')
    check('Pack Leader: aliados +10%', U(b, 3, 'STRENGTHU'), ceil(S0 * 1.1))
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(861, 2)
    check('Pack Leader: el lobo -15% directo', d[2], ceil(S * 1.7 * 0.85), 1)

@test
def aspecto_ancestros():
    b = fresh(aspect=4, wolfLife=1000)
    b.units[1].props['LIFEN'] = 600.0
    b.enemy_hit(2, 1, 3.3)                 # 600 - 330 = 270: cruza el 40%
    check('baja del 40%: Ancestral Form', b.has(1, 'RWANCFORM'), True)
    check('3 turnos', tonum(b.call('__rwLeft', b.units[1], 'RWANCFORM')), 3)
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(861, 2)
    check('+40% dano', d[2], ceil(S * 1.7 * 1.4), 1)
    for k in range(3):
        b.tick(1)
    check('al terminar: Spent 2 turnos', tonum(b.call('__rwLeft', b.units[1], 'RWSPENT')), 2)

@test
def blood_moon_rising():
    b = fresh(learn={814: 2, 854: 1, 846: 1}, aspect=1, enemies=2)
    S = U(b, 1, 'STRENGTHU')
    b.cast(854, 2)
    b.start_turn(2)
    check('al empezar su turno: 1 Wound', b.st(2)['W'], 1)
    b.units[1].props['LIFEN'] = 3000.0
    t = b.tick(2)
    check('los Wounds pegan doble', t, 2 * ceil(S * 0.15 * 1.35), 1)
    check('y curan 30% (+15% Blood Drinker R1)', U(b, 1, 'LIFEN') - 3000, ceil(t * 0.3) + ceil(t * 0.15), 2)
    b.call('__rwAddWounds', b.units[4], 3.0, b.units[1])
    per = S * 0.15 * 1.35; left = tonum(b.call('__rwWoundLeft', b.units[4]))
    l4 = U(b, 4, 'LIFEN')
    for k in range(4):
        b.tick(1)
    check('al ponerse la luna: estallan al 100%', l4 - U(b, 4, 'LIFEN'), ceil(3 * per * left), 2)

@test
def endless_winter():
    b = fresh(learn={855: 1}, aspect=2, enemies=2)
    b.cast(855, 2)
    check('5 Ice Shards', b.st(1)['Sh'], 5)
    b.start_turn(2)
    check('al empezar su turno: +2 Frostbite', b.st(2)['FB'], 2)
    check('-30% Speed', round(U(b, 2, 'SPEEDU')), ceil(50 * (1 - 0.3 - 0.08)), 1)
    b.call('__rwSetFrost', b.units[2], 7.0, b.units[1])
    b.call('__rwAddFrost', b.units[2], 1.0, b.units[1])
    check('congelados 2 turnos (no jefe)', tonum(b.call('__rwLeft', b.units[2], 'RWSOLID')), 2)
    b.call('__rwSetFrost', b.units[4], 4.0, b.units[1])
    S = U(b, 1, 'STRENGTHU')
    l4 = U(b, 4, 'LIFEN')
    for k in range(4):
        b.tick(1)
    check('los Shards no vencen mientras dura', b.st(1)['Sh'] >= 0, True)
    check('al terminar: 60% por Frostbite', l4 - U(b, 4, 'LIFEN'), ceil(S * 0.6 * 4), 2)

@test
def call_of_the_ancestors():
    b = fresh(learn={856: 1}, aspect=4, ally=True, wolfLife=4000)
    b.units[1].props['LIFEN'] = 1000.0
    b.units[1].props['FOCUSN'] = 10.0
    b.units[3].props['LIFEN'] = 500.0
    b.cast(856, None)
    check('cura 65%', U(b, 1, 'LIFEN'), 1000 + 2600)
    check('todo el Focus', U(b, 1, 'FOCUSN'), 200)
    check('turno extra pendiente', b.R['__rwExtraPending'] is True, True)
    check('bendicion en el aliado mas herido', b.has(3, 'RWBLESS'), True)
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(861, 2)
    check('+100% dano', d[2], ceil(S * 1.7 * 2), 1)
    b.enemy_hit(2, 3, 50.0)
    check('el aliado caido vuelve como lobo ancestral', (b.units[3].props['active'], tostr(b.units[3].props['playerName'])), (True, 'Ancestral Wolf'))
    check('con 50% de vida', U(b, 3, 'LIFEN'), 3000)
    check('turno extra: se concede una vez', (b.call('__rwExtraTurn') is True, b.call('__rwExtraTurn') is True, b.call('__rwExtraTurn') is True), (True, False, False))

@test
def frozen_maw():
    b = fresh(level=1)
    S = U(b, 1, 'STRENGTHU')
    d = b.cast(857, 2)
    check('Frozen Maw nivel 1: 160%', d[2], ceil(S * 1.6))
    b = fresh(level=20)
    b.call('__rwSetFrost', b.units[2], 3.0, b.units[1])
    S = U(b, 1, 'STRENGTHU')
    f0 = U(b, 1, 'FOCUSN')
    d = b.cast(857, 2)
    check('nivel 20: 240% x Brittle', d[2], ceil(S * 2.4 * 1.2), 1)
    check('nivel 10+: 2 Frostbite contra Brittle', b.st(2)['FB'], 5)
    check('+10 Focus contra Brittle', U(b, 1, 'FOCUSN') - b.paid, 10)

# ================================================================== Mokoshotar NPC (KNU55)
@test
def mokoshotar_npc():
    # un Mokoshotar que no es el jugador usa 624/626/627/628 nativos; las capas viejas los descartaban con rango 0
    for mid, coef in ((624, 1.7), (627, 2.8), (628, 1.85)):
        b = fresh(ally=True)
        a = b.R['KRINABILITY%d' % mid]; bb = b.R['KRINABILITYB%d' % mid]
        l0 = U(b, 1, 'LIFEN'); l3 = U(b, 3, 'LIFEN')
        b.call('executeMove', a, bb, b.units[2], b.units[1])
        check('NPC %d contra el lobo' % mid, l0 - U(b, 1, 'LIFEN'), ceil(100 * coef), 1)
        b.call('executeMove', a, bb, b.units[2], b.units[3])
        check('NPC %d contra el aliado' % mid, l3 - U(b, 3, 'LIFEN'), ceil(100 * coef), 1)
    b = fresh(ally=True)
    a = b.R['KRINABILITY624']; bb = b.R['KRINABILITYB624']
    l0 = U(b, 2, 'LIFEN')
    b.call('executeMove', a, bb, b.units[3], b.units[2])
    check('un aliado con 624 pega (150 x 1.7)', l0 - U(b, 2, 'LIFEN'), ceil(150 * 1.7), 1)

# ================================================================== textos
@test
def textos():
    b = fresh(learn={814: 2, 840: 1})
    S = b.R['__rwS'].props
    malos = []
    for k, d in S.items():
        if not isinstance(d, Obj): continue
        sid = int(k); mx = int(tonum(d.props['max']))
        for r in range(1, mx + 1):
            t = tostr(b.call('__rwFullDesc', float(sid), float(r)))
            if t == '' or 'undefined' in t or 'NaN' in t or 'null' in t:
                malos.append((sid, r, t[:60]))
    check('todas las descripciones sin undefined/NaN', malos, [])
    for sid in (861, 831, 815, 816):
        t = tostr(b.call('__rwCostText', float(sid), 1.0))
        check('costo %d' % sid, 'Focus' in t or 'nothing' in t, True)
    for k in range(1, 5):
        check('aspecto %d con texto' % k, len(tostr(b.call('__rwAspectText', float(k)))) > 40, True)


if __name__ == '__main__':
    filtro = sys.argv[1] if len(sys.argv) > 1 else ''
    for f in TESTS:
        if filtro and filtro not in f.__name__:
            continue
        n0 = len(BAD)
        try:
            f()
        except Exception as ex:
            BAD.append(f.__name__)
            print('  ERROR en %s: %s' % (f.__name__, ex))
            traceback.print_exc(limit=3)
        print('%-32s %s' % (f.__name__, 'ok' if len(BAD) == n0 else 'FALLA'))
    print('\n%d comprobaciones: %d bien, %d mal' % (len(OK) + len(BAD), len(OK), len(BAD)))
