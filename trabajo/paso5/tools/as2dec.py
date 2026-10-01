# Paso 3 — descompilador AVM1 -> AS2 legible.
#
# Reconstruye el flujo de control (if/else, while, do-while, for-in, switch,
# break/continue, &&, ||, ?:) a partir de los patrones que emiten el IDE de
# Flash y los compiladores de la epoca. Cuando un salto no encaja en ningun
# patron, no se inventa nada: se emite `goto L_xxx` con su etiqueta, para que
# el codigo siga siendo completo y fiel.
#
# Junto a cada .as se genera un .pcode (desensamblado exacto), que es la fuente
# de verdad para recompilar.
import struct, re, json, math

NAMES = {0x04:'NextFrame',0x05:'PrevFrame',0x06:'Play',0x07:'Stop',0x08:'ToggleQuality',
 0x09:'StopSounds',0x0A:'Add',0x0B:'Subtract',0x0C:'Multiply',0x0D:'Divide',0x0E:'Equals',
 0x0F:'Less',0x10:'And',0x11:'Or',0x12:'Not',0x13:'StringEquals',0x14:'StringLength',
 0x15:'StringExtract',0x17:'Pop',0x18:'ToInteger',0x1C:'GetVariable',0x1D:'SetVariable',
 0x20:'SetTarget2',0x21:'StringAdd',0x22:'GetProperty',0x23:'SetProperty',0x24:'CloneSprite',
 0x25:'RemoveSprite',0x26:'Trace',0x27:'StartDrag',0x28:'EndDrag',0x29:'StringLess',
 0x2A:'Throw',0x2B:'CastOp',0x2C:'ImplementsOp',0x30:'RandomNumber',0x31:'MBStringLength',
 0x32:'CharToAscii',0x33:'AsciiToChar',0x34:'GetTime',0x35:'MBStringExtract',
 0x36:'MBCharToAscii',0x37:'MBAsciiToChar',0x3A:'Delete',0x3B:'Delete2',0x3C:'DefineLocal',
 0x3D:'CallFunction',0x3E:'Return',0x3F:'Modulo',0x40:'NewObject',0x41:'DefineLocal2',
 0x42:'InitArray',0x43:'InitObject',0x44:'TypeOf',0x45:'TargetPath',0x46:'Enumerate',
 0x47:'Add2',0x48:'Less2',0x49:'Equals2',0x4A:'ToNumber',0x4B:'ToString',0x4C:'PushDuplicate',
 0x4D:'StackSwap',0x4E:'GetMember',0x4F:'SetMember',0x50:'Increment',0x51:'Decrement',
 0x52:'CallMethod',0x53:'NewMethod',0x54:'InstanceOf',0x55:'Enumerate2',0x60:'BitAnd',
 0x61:'BitOr',0x62:'BitXor',0x63:'BitLShift',0x64:'BitRShift',0x65:'BitURShift',
 0x66:'StrictEquals',0x67:'Greater',0x68:'StringGreater',0x69:'Extends',0x81:'GotoFrame',
 0x83:'GetURL',0x87:'StoreRegister',0x88:'ConstantPool',0x8A:'WaitForFrame',0x8B:'SetTarget',
 0x8C:'GoToLabel',0x8D:'WaitForFrame2',0x8E:'DefineFunction2',0x8F:'Try',0x94:'With',
 0x96:'Push',0x99:'Jump',0x9A:'GetURL2',0x9B:'DefineFunction',0x9D:'If',0x9E:'Call',
 0x9F:'GotoFrame2',0x00:'End'}

PROPS = ['_x','_y','_xscale','_yscale','_currentframe','_totalframes','_alpha','_visible',
         '_width','_height','_rotation','_target','_framesloaded','_name','_droptarget',
         '_url','_highquality','_focusrect','_soundbuftime','_quality','_xmouse','_ymouse']

IDENT = re.compile(r'^[A-Za-z_$][A-Za-z0-9_$]*$')
PATH = re.compile(r'^[A-Za-z_$][A-Za-z0-9_$]*(\.[A-Za-z_$][A-Za-z0-9_$]*)*$')
RESERVED = {'break','case','continue','default','delete','do','else','for','function','if',
            'in','instanceof','new','return','switch','this','typeof','var','void','while',
            'with','class','extends','true','false','null','undefined'}


# ====================================================================== decodificacion
class Val:
    """Operando de Push."""
    __slots__ = ('kind', 'v')
    def __init__(self, kind, v): self.kind = kind; self.v = v


class Ins:
    __slots__ = ('pos', 'end', 'op', 'name', 'a')
    def __init__(self, pos, end, op, a=None):
        self.pos = pos; self.end = end; self.op = op
        self.name = NAMES.get(op, 'Op_%02X' % op); self.a = a


STATS = {}


def stat(k):
    STATS[k] = STATS.get(k, 0) + 1


def _cstr(b, i):
    j = b.index(b'\0', i)
    raw = b[i:j]
    try:
        return raw.decode('utf-8'), j + 1       # SWF 6+ guarda las cadenas en UTF-8
    except UnicodeDecodeError:
        stat('cadena no UTF-8')
        return raw.decode('latin1'), j + 1


def decode(b, start=0, end=None, pool=None):
    """Lista de instrucciones de [start, end). Las funciones se decodifican
    aparte: su cuerpo se salta aqui y se guarda como (inicio, fin)."""
    end = len(b) if end is None else end
    pool = [] if pool is None else pool
    out = []
    i = start
    while i < end:
        op = b[i]; pos = i
        if op < 0x80:
            out.append(Ins(pos, i + 1, op)); i += 1
            if op == 0:
                continue
            continue
        ln = struct.unpack_from('<H', b, i + 1)[0]
        p = i + 3; q = p + ln
        a = None
        if op == 0x96:
            vals = []
            while p < q:
                t = b[p]; p += 1
                if t == 0: s, p = _cstr(b, p); vals.append(Val('s', s))
                elif t == 1: vals.append(Val('f', struct.unpack_from('<f', b, p)[0])); p += 4
                elif t == 2: vals.append(Val('null', None))
                elif t == 3: vals.append(Val('undef', None))
                elif t == 4: vals.append(Val('r', b[p])); p += 1
                elif t == 5: vals.append(Val('b', bool(b[p]))); p += 1
                elif t == 6:
                    raw = b[p:p + 8]; vals.append(Val('n', struct.unpack('<d', raw[4:] + raw[:4])[0])); p += 8
                elif t == 7: vals.append(Val('i', struct.unpack_from('<i', b, p)[0])); p += 4
                elif t == 8:
                    k = b[p]; p += 1
                    vals.append(Val('s', pool[k]) if k < len(pool) else Val('s', '__pool%d' % k))
                elif t == 9:
                    k = struct.unpack_from('<H', b, p)[0]; p += 2
                    vals.append(Val('s', pool[k]) if k < len(pool) else Val('s', '__pool%d' % k))
                else:
                    vals.append(Val('undef', None)); p = q
            a = vals
        elif op == 0x88:
            c = struct.unpack_from('<H', b, p)[0]; p += 2
            lst = []
            for _ in range(c):
                s, p = _cstr(b, p); lst.append(s)
            pool[:] = lst
            a = len(lst)
        elif op in (0x99, 0x9D):
            a = q + struct.unpack_from('<h', b, p)[0]
        elif op == 0x87:
            a = b[p]
        elif op == 0x9B:
            nm, p = _cstr(b, p)
            np_ = struct.unpack_from('<H', b, p)[0]; p += 2
            ps = []
            for _ in range(np_):
                s, p = _cstr(b, p); ps.append((0, s))
            cs = struct.unpack_from('<H', b, p)[0]; p += 2
            a = dict(name=nm, params=ps, regs=4, flags=0, f2=False, body=(p, p + cs), pool=list(pool))
            q = p + cs
        elif op == 0x8E:
            nm, p = _cstr(b, p)
            np_ = struct.unpack_from('<H', b, p)[0]; p += 2
            rc = b[p]; p += 1
            fl = struct.unpack_from('<H', b, p)[0]; p += 2
            ps = []
            for _ in range(np_):
                r = b[p]; s, p = _cstr(b, p + 1); ps.append((r, s))
            cs = struct.unpack_from('<H', b, p)[0]; p += 2
            a = dict(name=nm, params=ps, regs=rc, flags=fl, f2=True, body=(p, p + cs), pool=list(pool))
            q = p + cs
        elif op == 0x81:
            a = struct.unpack_from('<H', b, p)[0]
        elif op == 0x83:
            u, p2 = _cstr(b, p); t2, _ = _cstr(b, p2); a = (u, t2)
        elif op in (0x8B, 0x8C):
            a, _ = _cstr(b, p)
        elif op == 0x8A:
            a = (struct.unpack_from('<H', b, p)[0], b[p + 2])
        elif op == 0x8D:
            a = b[p]
        elif op == 0x9F:
            fl = b[p]
            bias = struct.unpack_from('<H', b, p + 1)[0] if fl & 2 else 0
            a = (fl, bias)
        elif op == 0x9A:
            a = b[p]
        elif op == 0x94:
            a = struct.unpack_from('<H', b, p)[0]
            q = q  # el cuerpo de With va a continuacion y se decodifica en linea
        elif op == 0x8F:
            fl = b[p]
            ts, cs2, fs = struct.unpack_from('<HHH', b, p + 1)
            pp = p + 7
            if fl & 4:
                cn = b[pp]; pp += 1
            else:
                cn, pp = _cstr(b, pp)
            a = dict(flags=fl, t=ts, c=cs2, f=fs, catch=cn)
        else:
            a = b[p:q]
        out.append(Ins(pos, q, op, a))
        i = q
    return out


def _f32(v):
    if v != v or v in (float('inf'), float('-inf')): return _num(v)
    if v == int(v) and abs(v) < 1e15: return str(int(v))
    want = struct.pack('<f', v)
    for d in range(1, 10):
        t = '%.*g' % (d, v)
        if struct.pack('<f', float(t)) == want:
            return t
    return repr(v)


def _num(v):
    if v == 0 and math.copysign(1, v) < 0: return '-0'
    if v != v: return 'NaN'
    if v in (float('inf'), float('-inf')): return 'Infinity' if v > 0 else '-Infinity'
    if v == int(v) and abs(v) < 1e15: return str(int(v))
    r = repr(v)
    return r


def _str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t') + '"'


def pcode(ins, depth=0):
    """Desensamblado exacto (con dobles correctos)."""
    out = []
    P = '   ' * depth
    for x in ins:
        if x.name == 'Push':
            vs = []
            for v in x.a:
                if v.kind == 's': vs.append(_str(v.v))
                elif v.kind in ('n', 'i'): vs.append(_num(v.v))
                elif v.kind == 'f': vs.append(_f32(v.v))
                elif v.kind == 'r': vs.append('register%d' % v.v)
                elif v.kind == 'b': vs.append('true' if v.v else 'false')
                else: vs.append(v.kind)
            out.append('%s%6d  Push %s' % (P, x.pos, ', '.join(vs)))
        elif x.name in ('Jump', 'If'):
            out.append('%s%6d  %s loc%d' % (P, x.pos, x.name, x.a))
        elif x.name in ('DefineFunction', 'DefineFunction2'):
            ps = ', '.join(('r%d:' % r if r else '') + n for r, n in x.a['params'])
            out.append('%s%6d  %s "%s" (%s) regs=%d flags=0x%x {' % (P, x.pos, x.name, x.a['name'], ps, x.a['regs'], x.a['flags']))
            out.append('%s        }' % P)
        elif x.name == 'StoreRegister':
            out.append('%s%6d  StoreRegister %d' % (P, x.pos, x.a))
        elif x.name == 'ConstantPool':
            out.append('%s%6d  ConstantPool (%d)' % (P, x.pos, x.a))
        elif isinstance(x.a, (bytes, bytearray)) and x.a:
            out.append('%s%6d  %s %s' % (P, x.pos, x.name, x.a.hex()))
        elif x.a is not None and not isinstance(x.a, (bytes, bytearray)):
            out.append('%s%6d  %s %r' % (P, x.pos, x.name, x.a))
        else:
            out.append('%s%6d  %s' % (P, x.pos, x.name))
    return out


# ====================================================================== expresiones
class E:
    """Expresion con precedencia. inner: operando si es una negacion (!x)."""
    __slots__ = ('t', 'p', 'inner', 'lit', 'reg', 'bin', 'inc', 'asg')
    def __init__(self, t, p=20, inner=None, lit=None, reg=None, bin=None, inc=None, asg=None):
        self.asg = asg      # (valor, es_cadena) si es una asignacion usada como valor
        self.t = t; self.p = p; self.inner = inner; self.lit = lit; self.reg = reg
        self.bin = bin      # (simbolo, a, b) si es una operacion binaria
        self.inc = inc      # (operando, +1/-1) si viene de Increment/Decrement
    def __repr__(self): return self.t


def W(e, p):
    return '(' + e.t + ')' if e.p < p else e.t


BIN = {'Add2': ('+', 13), 'Add': ('+', 13), 'Subtract': ('-', 13), 'Multiply': ('*', 14),
       'Divide': ('/', 14), 'Modulo': ('%', 14), 'Less2': ('<', 11), 'Less': ('<', 11),
       'Greater': ('>', 11), 'Equals2': ('==', 10), 'Equals': ('==', 10),
       'StrictEquals': ('===', 10), 'BitAnd': ('&', 9), 'BitXor': ('^', 8), 'BitOr': ('|', 7),
       'BitLShift': ('<<', 12), 'BitRShift': ('>>', 12), 'BitURShift': ('>>>', 12),
       'And': ('and', 6), 'Or': ('or', 5), 'StringEquals': ('eq', 10), 'StringLess': ('lt', 11),
       'StringGreater': ('gt', 11), 'InstanceOf': ('instanceof', 11), 'StringAdd': ('add', 13)}
NEGOP = {'==': '!=', '===': '!==', '!=': '==', '!==': '==='}


def binop(sym, p, a, b):
    return E('%s %s %s' % (W(a, p), sym, W(b, p + 1)), p, bin=(sym, a, b))


def neg(e):
    if e.inner is not None:
        return e.inner
    if e.bin and e.bin[0] in NEGOP:
        r = binop(NEGOP[e.bin[0]], 10, e.bin[1], e.bin[2])
        r.inner = e          # negar de nuevo devuelve la expresion original
        return r
    return E('!' + W(e, 15), 15, inner=e)


def lit(v):
    if v.kind == 's': return E(_str(v.v), 20, lit=v.v)
    if v.kind in ('n', 'i', 'f'):
        t = _f32(v.v) if v.kind == 'f' else _num(v.v)
        return E(t, 20 if not t.startswith('-') else 15, lit=v.v)
    if v.kind == 'b': return E('true' if v.v else 'false', 20, lit=v.v)
    if v.kind == 'null': return E('null', 20, lit=None)
    if v.kind == 'undef': return E('undefined', 20, lit='__undef__')
    return E('?', 20)


SPECIAL = {'this', 'super', 'arguments', 'undefined'}


def name_of(e):
    """Si e es una cadena literal usable como identificador, devuelve el nombre."""
    if isinstance(e.lit, str) and IDENT.match(e.lit):
        if e.lit not in RESERVED or e.lit in SPECIAL:
            return e.lit
    return None


def member(o, k):
    if isinstance(k.lit, str) and IDENT.match(k.lit) and k.lit not in RESERVED:
        return E('%s.%s' % (W(o, 18), k.lit), 18)
    return E('%s[%s]' % (W(o, 18), k.t), 18)


# ====================================================================== descompilador
class Unstructured(Exception):
    pass


class Func:
    def __init__(self, info=None):
        self.regnames = {}
        self.declared = set()
        if info and info['f2']:
            fl = info['flags']; r = 1
            for bit, nm in ((0x01, 'this'), (0x04, 'arguments'), (0x10, 'super'),
                            (0x40, '_root'), (0x80, '_parent'), (0x100, '_global')):
                if fl & bit:
                    self.regnames[r] = nm; r += 1
            for reg, nm in info['params']:
                if reg: self.regnames[reg] = nm
        self.params = set(self.regnames)

    def reg(self, n):
        return self.regnames.get(n, '_loc%d_' % n)


class Decompiler:
    def __init__(self, b, pool=None):
        self.b = b
        self.pool = [] if pool is None else pool
        self.gotos = 0
        self.labels = set()
        self._dohead_active = -1
        self.seen = set()
        self.missing = 0
        self.total = 0

    # ------------------------------------------------------------------
    def script(self, start=0, end=None):
        ins = decode(self.b, start, end, self.pool)
        return self.body(ins, Func())

    def body(self, ins, fn):
        idx = {x.pos: k for k, x in enumerate(ins)}
        if ins: idx[ins[-1].end] = len(ins)
        saved = (getattr(self, 'I', None), getattr(self, 'IX', None), getattr(self, 'FN', None),
                 getattr(self, 'DOHEAD', None), self.labels, self.gotos)
        self.I = ins; self.IX = idx
        # cabezas de do-while: destino de un If hacia atras
        self.DOHEAD = {}
        for k, x in enumerate(ins):
            if x.name == 'If' and x.a in idx and idx[x.a] <= k:
                h = idx[x.a]
                if h not in self.DOHEAD or self.DOHEAD[h] < k:
                    self.DOHEAD[h] = k
        self.labels = set()
        g0 = self.gotos
        declared0 = set(fn.declared)
        for attempt in range(3):
            self.seen = set()
            fn.declared = set(declared0)
            self.FN = fn
            self.gotos = g0
            before = set(self.labels)
            stmts, st = self.block(0, len(ins), [], [])
            if self.labels == before:
                break
        for e in st:
            stat('valor sin usar al final')
            stmts.append('// (valor sin usar) %s;' % e.t)
        skip = ('End', 'ConstantPool')
        miss = [k for k, x in enumerate(ins) if k not in self.seen and x.name not in skip]
        self.missing = getattr(self, 'missing', 0) + len(miss)
        self.total = getattr(self, 'total', 0) + sum(1 for x in ins if x.name not in skip)
        g = self.gotos
        self.I, self.IX, self.FN, self.DOHEAD, self.labels, _ = saved
        self.gotos = g
        return stmts

    def pending_labels(self):
        return False

    def idx(self, pos):
        if pos in self.IX:
            return self.IX[pos]
        raise Unstructured('salto a mitad de instruccion %d' % pos)

    # ------------------------------------------------------------------
    def fn_expr(self, info, as_stmt):
        a0, a1 = info['body']
        sub = Decompiler(self.b, list(info['pool']))
        fn = Func(info)
        inner = decode(self.b, a0, a1, sub.pool)
        stmts = sub.body(inner, fn)
        self.gotos += sub.gotos
        self.missing = getattr(self, 'missing', 0) + getattr(sub, 'missing', 0)
        self.total = getattr(self, 'total', 0) + getattr(sub, 'total', 0)
        params = ', '.join(n for r, n in info['params'])
        nm = info['name']
        head = 'function %s(%s)' % (nm, params) if nm else 'function(%s)' % params
        text = head + '\n{\n' + '\n'.join('   ' + l for s in stmts for l in s.split('\n')) + '\n}'
        if not stmts:
            text = head + '\n{\n}'
        return text

    # ------------------------------------------------------------------
    def pure(self, i0, i1, loops, st_in):
        """Evalua [i0,i1) esperando exactamente un valor y ninguna sentencia."""
        saved = set(self.seen)
        try:
            s, st = self.block(i0, i1, loops, list(st_in), expr_only=True)
        except Unstructured:
            self.seen = saved
            return None
        if s or len(st) != len(st_in) + 1:
            self.seen = saved
            return None
        return st[-1]

    def block(self, i0, i1, loops, st, expr_only=False, stmts=None):
        I = self.I
        out = [] if stmts is None else stmts
        fn = self.FN
        i = i0
        stmt_start = i0

        def pop():
            if st: return st.pop()
            return E('__stack_underflow__', 20)

        def emit(s):
            if expr_only:
                raise Unstructured('sentencia en expresion')
            if st:
                stat('sentencia con valores pendientes en la pila')
                STATS.setdefault('_donde', []).append(s[:80])
            out.append(s)

        skip_r0 = [False]

        def setstmt(target, v, i):
            """Asignacion. Devuelve True si se convirtio en expresion (y no hay sentencia)."""
            if st and not expr_only:
                # x++ dentro de una expresion: el valor viejo ya esta en la pila
                if v.inc and v.inc[0].t == target and st[-1].t == target:
                    st[-1] = E('%s%s' % (target, '++' if v.inc[1] > 0 else '--'), 17)
                    return True
                # a = b = v : b se asigna con el valor guardado en el registro 0
                nx_ = I[i + 1] if i + 1 < i1 else None
                if (v.asg is not None and (v.asg[1] or v.reg == 0) and nx_ is not None
                        and nx_.name == 'Push' and nx_.a and nx_.a[0].kind == 'r' and nx_.a[0].v == 0):
                    val = v.t if v.asg[1] else v.asg[0].t
                    st.append(E('%s = %s' % (target, val), 3, asg=(None, True)))
                    skip_r0[0] = True
                    return True
            emit(self.assign(target, v))
            return False

        while i < i1:
            x = I[i]
            n = x.name
            self.seen.add(i)
            if not st:
                stmt_start = i
            if i in self.labels and not expr_only:
                out.append('L_%d:' % x.pos)

            # ---------------- do-while
            if i in self.DOHEAD and i != getattr(self, '_dohead_active', -1) and not st and not expr_only:
                k = self.DOHEAD[i]
                if k < i1:
                    self._dohead_active = i
                    body, st2 = self.block(i, k, loops + [(i, k + 1, -1)], [])
                    self._dohead_active = -1
                    cond = st2.pop() if st2 else E('true')
                    self.seen.add(k)
                    if st2: stat('valor sobrante en la pila (do-while)')
                    for e in st2: body.append('%s;' % e.t)
                    if not body and cond.t == '__stack_underflow__ != null':
                        pass  # limpieza de for-in al salir con return/break: vacia la pila
                    else:
                        out.append('do\n{\n' + self.ind(body) + '\n}\nwhile(%s);' % cond.t)
                    i = k + 1
                    continue

            if n == 'Push':
                vals = x.a
                if skip_r0[0]:
                    skip_r0[0] = False
                    if vals and vals[0].kind == 'r' and vals[0].v == 0:
                        vals = vals[1:]
                for v in vals:
                    if v.kind == 'r':
                        st.append(E(fn.reg(v.v), 20, reg=v.v))
                    else:
                        st.append(lit(v))
            elif n == 'Pop':
                # Pop con la pila vacia no hace nada en AVM1 (el compilador de
                # clases de Macromedia lo deja tras cada 'if(!_global.x)')
                if st:
                    e = pop()
                    if e.t != 'undefined' and not e.t.startswith('__iter__'):
                        emit(e.t + ';')
            elif n == 'GetVariable':
                k = pop()
                nm = name_of(k)
                st.append(E(nm, 20) if nm and nm not in PROPS else E('eval(%s)' % k.t, 18))
            elif n == 'SetVariable':
                v = pop(); k = pop()
                nm = name_of(k)
                if nm and nm not in PROPS:
                    setstmt(nm, v, i)
                else:
                    emit('set(%s, %s);' % (k.t, v.t))
            elif n == 'DefineLocal':
                v = pop(); k = pop()
                nm = name_of(k)
                if not nm: stat('DefineLocal con nombre no valido')
                emit('var %s = %s;' % (nm or k.t, v.t))
            elif n == 'DefineLocal2':
                k = pop()
                if not name_of(k): stat('DefineLocal2 con nombre no valido')
                emit('var %s;' % (name_of(k) or k.t))
            elif n == 'GetMember':
                k = pop(); o = pop()
                st.append(member(o, k))
            elif n == 'SetMember':
                v = pop(); k = pop(); o = pop()
                setstmt(member(o, k).t, v, i)
            elif n in BIN:
                b2 = pop(); a2 = pop()
                sym, p = BIN[n]
                st.append(binop(sym, p, a2, b2))
            elif n == 'Not':
                st.append(neg(pop()))
            elif n == 'TypeOf':
                st.append(E('typeof ' + W(pop(), 15), 15))
            elif n in ('Increment', 'Decrement'):
                # Increment = Number(x) + 1 (nunca concatena). Si termina en x = ..., se escribe x++
                a_ = pop()
                st.append(E('Number(%s) %s 1' % (a_.t, '+' if n == 'Increment' else '-'), 13,
                            inc=(a_, 1 if n == 'Increment' else -1)))
            elif n == 'ToInteger':
                st.append(E('int(%s)' % pop().t, 18))
            elif n == 'ToNumber':
                st.append(E('Number(%s)' % pop().t, 18))
            elif n == 'ToString':
                st.append(E('String(%s)' % pop().t, 18))
            elif n == 'StringLength' or n == 'MBStringLength':
                st.append(E('length(%s)' % pop().t, 18))
            elif n in ('StringExtract', 'MBStringExtract'):
                c = pop(); ix = pop(); s = pop()
                st.append(E('substring(%s, %s, %s)' % (s.t, ix.t, c.t), 18))
            elif n in ('CharToAscii', 'MBCharToAscii'):
                st.append(E('ord(%s)' % pop().t, 18))
            elif n in ('AsciiToChar', 'MBAsciiToChar'):
                st.append(E('chr(%s)' % pop().t, 18))
            elif n == 'RandomNumber':
                st.append(E('random(%s)' % pop().t, 18))
            elif n == 'GetTime':
                st.append(E('getTimer()', 18))
            elif n == 'TargetPath':
                st.append(E('targetPath(%s)' % pop().t, 18))
            elif n == 'CastOp':
                o = pop(); c = pop()
                st.append(E('__cast(%s, %s)' % (c.t, o.t), 18))
            elif n == 'PushDuplicate':
                # && y || : PushDuplicate [Not] If L ; Pop ; <b> ; L:
                j = i + 1
                is_and = False
                if j < i1 and I[j].name == 'Not':
                    is_and = True; j += 1
                if (j < i1 and I[j].name == 'If' and j + 1 < i1 and I[j + 1].name == 'Pop'
                        and I[j].a in self.IX and self.IX[I[j].a] > j and self.IX[I[j].a] <= i1):
                    t = self.IX[I[j].a]
                    a_ = pop()
                    rhs = self.pure(j + 2, t, loops, [])
                    if rhs is not None:
                        self.seen.update(range(i + 1, j + 2))
                        sym, p = ('&&', 6) if is_and else ('||', 5)
                        st.append(E('%s %s %s' % (W(a_, p), sym, W(rhs, p + 1)), p))
                        i = t
                        continue
                    st.append(a_)
                e = pop(); st.append(e); st.append(e)
                if not (e.reg is not None or e.lit is not None or IDENT.match(e.t)):
                    stat('PushDuplicate de una expresion')
            elif n == 'StackSwap':
                a_ = pop(); b_ = pop(); st.append(a_); st.append(b_)
            elif n == 'StoreRegister':
                e = pop()
                rn = fn.reg(x.a)
                if i + 1 < i1 and I[i + 1].name == 'Pop':
                    if expr_only:
                        raise Unstructured('asignacion en expresion')
                    self.seen.add(i + 1)
                    decl = ''
                    if x.a not in fn.params and rn not in fn.declared and rn.startswith('_loc'):
                        decl = 'var '; fn.declared.add(rn)
                    if st and e.inc and e.inc[0].t == rn and st[-1].t == rn:
                        st[-1] = E('%s%s' % (rn, '++' if e.inc[1] > 0 else '--'), 17)
                    else:
                        emit(decl + self.assign(rn, e))
                    i += 2
                    continue
                # switch: StoreRegister rN ; Push v ; StrictEquals ; If
                sw = self.try_switch(i, i1, e, loops, out, expr_only)
                if sw is not None:
                    i = sw
                    continue
                if e.reg == x.a:
                    st.append(e)
                else:
                    st.append(E('%s = %s' % (rn, e.t), 3, reg=x.a, asg=(e, False)))
            elif n == 'CallFunction':
                f = pop(); c = pop()
                args = [pop() for _ in range(self.cnt(c))]
                nm = name_of(f)
                if not nm and not isinstance(f.lit, str) and f.lit is not None and f.lit != '__undef__':
                    # nombre no textual (p. ej. false): AVM1 lo convierte a cadena y busca esa variable
                    nm = 'eval(%s)' % _str(f.t)
                st.append(E('%s(%s)' % (nm if nm else 'eval(%s)' % f.t, ', '.join(a.t for a in args)), 18))
            elif n == 'CallMethod':
                m = pop(); o = pop(); c = pop()
                args = [pop() for _ in range(self.cnt(c))]
                A = ', '.join(a.t for a in args)
                if m.lit in ('', '__undef__') or m.t == 'undefined':
                    st.append(E('%s(%s)' % (W(o, 18), A), 18))
                else:
                    st.append(E('%s(%s)' % (member(o, m).t, A), 18))
            elif n == 'NewObject':
                f = pop(); c = pop()
                args = [pop() for _ in range(self.cnt(c))]
                nm = name_of(f)
                if not nm:
                    stat('NewObject con nombre no valido'); nm = 'eval(%s)' % f.t
                st.append(E('new %s(%s)' % (nm, ', '.join(a.t for a in args)), 18))
            elif n == 'NewMethod':
                m = pop(); o = pop(); c = pop()
                args = [pop() for _ in range(self.cnt(c))]
                tgt = W(o, 18) if m.lit in ('', '__undef__') else member(o, m).t
                st.append(E('new %s(%s)' % (tgt, ', '.join(a.t for a in args)), 18))
            elif n == 'InitArray':
                c = pop()
                st.append(E('[' + ', '.join(pop().t for _ in range(self.cnt(c))) + ']', 20))
            elif n == 'InitObject':
                c = pop(); kv = []
                for _ in range(self.cnt(c)):
                    v = pop(); k = pop()
                    kk = k.lit if isinstance(k.lit, str) and IDENT.match(k.lit) else k.t
                    kv.append('%s: %s' % (kk, v.t))
                st.append(E('{' + ', '.join(reversed(kv)) + '}', 20))
            elif n == 'Delete':
                k = pop(); o = pop()
                st.append(E('delete ' + member(o, k).t, 15))
            elif n == 'Delete2':
                k = pop()
                if not name_of(k): stat('Delete2 con nombre no valido')
                st.append(E('delete ' + (name_of(k) or k.t), 15))
            elif n == 'Return':
                e = pop()
                emit('return;' if e.t == 'undefined' else 'return %s;' % e.t)
            elif n == 'Throw':
                emit('throw %s;' % pop().t)
            elif n == 'Trace':
                emit('trace(%s);' % pop().t)
            elif n == 'GetProperty':
                ix = pop(); tg = pop()
                pr = PROPS[int(ix.lit)] if isinstance(ix.lit, (int, float)) and 0 <= int(ix.lit) < len(PROPS) else None
                if pr and tg.lit == '':
                    st.append(E(pr, 20))
                else:
                    st.append(E('getProperty(%s, %s)' % (tg.t, pr or ix.t), 18))
            elif n == 'SetProperty':
                v = pop(); ix = pop(); tg = pop()
                pr = PROPS[int(ix.lit)] if isinstance(ix.lit, (int, float)) and 0 <= int(ix.lit) < len(PROPS) else None
                if pr and tg.lit == '':
                    setstmt(pr, v, i)
                else:
                    emit('setProperty(%s, %s, %s);' % (tg.t, pr or ix.t, v.t))
            elif n == 'CloneSprite':
                d = pop(); t = pop(); s = pop()
                emit('duplicateMovieClip(%s, %s, %s);' % (s.t, t.t, d.t))
            elif n == 'RemoveSprite':
                emit('removeMovieClip(%s);' % pop().t)
            elif n == 'StartDrag':
                tg = pop(); lock = pop(); con = pop()
                if con.lit not in (0, False, None) and con.t not in ('0', 'false'):
                    y2 = pop(); x2 = pop(); y1 = pop(); x1 = pop()
                    emit('startDrag(%s, %s, %s, %s, %s, %s);' % (tg.t, lock.t, x1.t, y1.t, x2.t, y2.t))
                else:
                    emit('startDrag(%s, %s);' % (tg.t, lock.t))
            elif n == 'EndDrag': emit('stopDrag();')
            elif n == 'Play': emit('play();')
            elif n == 'Stop': emit('stop();')
            elif n == 'NextFrame': emit('nextFrame();')
            elif n == 'PrevFrame': emit('prevFrame();')
            elif n == 'StopSounds': emit('stopAllSounds();')
            elif n == 'ToggleQuality': emit('toggleHighQuality();')
            elif n == 'GotoFrame': emit('gotoAndStop(%d);' % (x.a + 1))
            elif n == 'GoToLabel': emit('gotoAndStop(%s);' % _str(x.a))
            elif n == 'GotoFrame2':
                f = pop(); fl, bias = x.a
                emit('%s(%s);' % ('gotoAndPlay' if fl & 1 else 'gotoAndStop',
                                   f.t if not bias else '%s + %d' % (f.t, bias)))
            elif n == 'GetURL':
                emit('getURL(%s, %s);' % (_str(x.a[0]), _str(x.a[1])))
            elif n == 'GetURL2':
                tg = pop(); u = pop(); fl = x.a
                meth = ['', ', "GET"', ', "POST"', ''][fl & 3]
                if fl & 0x80:
                    emit('loadVariables(%s, %s%s);' % (u.t, tg.t, meth))
                elif fl & 0x40:
                    emit('loadMovie(%s, %s%s);' % (u.t, tg.t, meth))
                else:
                    emit('getURL(%s, %s%s);' % (u.t, tg.t, meth))
            elif n == 'Call':
                emit('call(%s);' % pop().t)
            elif n == 'SetTarget':
                emit('setTarget(%s);' % _str(x.a))
            elif n == 'SetTarget2':
                emit('setTarget(%s);' % pop().t)
            elif n == 'Extends':
                sup = pop(); sub = pop()
                emit('%s extends %s;' % (sub.t, sup.t))
            elif n == 'ImplementsOp':
                c = pop(); k = pop()
                ifs = [pop().t for _ in range(self.cnt(k))]
                emit('%s implements %s;' % (c.t, ', '.join(ifs)))
            elif n == 'InstanceOf':
                b2 = pop(); a2 = pop()
                st.append(E('%s instanceof %s' % (W(a2, 11), W(b2, 12)), 11))
            elif n == 'ConstantPool':
                pass
            elif n == 'End':
                pass
            elif n in ('DefineFunction', 'DefineFunction2'):
                txt = self.fn_expr(x.a, x.a['name'] != '')
                if x.a['name']:
                    emit(txt)
                else:
                    st.append(E(txt, 19))
            elif n in ('Enumerate', 'Enumerate2'):
                obj = pop()
                if n == 'Enumerate':
                    obj = E(name_of(obj) or 'eval(%s)' % obj.t, 20)
                r = self.try_forin(i, i1, obj, loops, out)
                if r is None:
                    raise Unstructured('for-in no reconocido')
                i = r
                continue
            elif n == 'With':
                o = pop()
                a0 = x.end; a1 = x.end + x.a
                body, st2 = self.block(i + 1, self.idx(a1), loops, [])
                emit('with(%s)\n{\n%s\n}' % (o.t, self.ind(body)))
                i = self.idx(a1)
                continue
            elif n == 'Try':
                i = self.do_try(i, i1, x, loops, out)
                continue
            elif n in ('WaitForFrame', 'WaitForFrame2'):
                if n == 'WaitForFrame':
                    fr, skip = x.a
                    head = 'ifFrameLoaded(%d)' % (fr + 1)
                else:
                    skip = x.a
                    head = 'ifFrameLoaded(%s)' % pop().t
                body, st2 = self.block(i + 1, min(i1, i + 1 + skip), loops, [])
                emit('%s\n{\n%s\n}' % (head, self.ind(body)))
                i = min(i1, i + 1 + skip)
                continue
            elif n == 'Jump':
                t = self.idx(x.a)
                if loops and t == loops[-1][1]:
                    emit('break;')
                elif loops and t == loops[-1][2]:
                    emit('continue;')
                elif t == i1 and not st:
                    pass   # salto al final del propio bloque: no hace nada
                else:
                    if expr_only: raise Unstructured('goto en expresion')
                    self.labels.add(t); self.gotos += 1
                    emit('goto L_%d;' % I[t].pos if t < len(I) else 'goto L_fin;')
            elif n == 'If':
                r = self.do_if(i, i1, x, loops, st, out, stmt_start, expr_only)
                i = r
                continue
            else:
                emit('// instruccion no soportada: %s' % n)
            i += 1
        return out, st

    # ------------------------------------------------------------------
    @staticmethod
    def cnt(c):
        try:
            return max(0, int(float(c.lit)))
        except Exception:
            return 0

    @staticmethod
    def ind(stmts):
        return '\n'.join('   ' + l for s in stmts for l in s.split('\n'))

    @staticmethod
    def assign(lhs, v):
        # x = Increment(x) -> x++ ;  x = x + y -> x += y  (solo si el operando izquierdo es x)
        if v.inc and v.inc[0].t == lhs:
            return '%s%s;' % (lhs, '++' if v.inc[1] > 0 else '--')
        if v.bin and v.bin[0] in ('+', '-', '*', '/') and v.bin[1].t == lhs:
            return '%s %s= %s;' % (lhs, v.bin[0], v.bin[2].t)
        return '%s = %s;' % (lhs, v.t)

    # ------------------------------------------------------------------
    def do_if(self, i, i1, x, loops, st, out, stmt_start, expr_only):
        I = self.I
        t = self.idx(x.a)
        cond = st.pop() if st else E('__stack_underflow__')

        def emit(s):
            if expr_only: raise Unstructured('sentencia en expresion')
            out.append(s)

        # salto hacia atras sin do-while reconocido
        if t <= i and expr_only:
            raise Unstructured('salto atras en expresion')
        if t <= i:
            if loops and t == loops[-1][2]:
                emit('if(%s)\n{\n   continue;\n}' % cond.t)
                return i + 1
            self.labels.add(t); self.gotos += 1
            emit('if(%s) goto L_%d;' % (cond.t, I[t].pos))
            return i + 1
        # salto fuera del bloque: break / continue
        if t > i1:
            if loops and t == loops[-1][1]:
                emit('if(%s)\n{\n   break;\n}' % cond.t)
                return i + 1
            if loops and t == loops[-1][2]:
                emit('if(%s)\n{\n   continue;\n}' % cond.t)
                return i + 1
            if expr_only: raise Unstructured('salto fuera')
            self.labels.add(t); self.gotos += 1
            emit('if(%s) goto L_%s;' % (cond.t, I[t].pos if t < len(I) else 'fin'))
            return i + 1

        last = I[t - 1] if t - 1 > i else None
        # operador ternario: c ? A : B  (If salta a A cuando c es cierto)
        if last is not None and last.name == 'Jump' and last.a in self.IX:
            j = self.IX[last.a]
            if t < j <= i1:
                v_else = self.pure(i + 1, t - 1, loops, st)
                if v_else is not None:
                    v_then = self.pure(t, j, loops, st)
                    if v_then is not None:
                        self.seen.add(t - 1)
                        st.append(E('%s ? %s : %s' % (W(cond, 5), W(v_then, 4), W(v_else, 4)), 4))
                        return j
        if expr_only:
            raise Unstructured('if en expresion')
        # while: ... If fin ; cuerpo ; Jump inicio_condicion
        if last is not None and last.name == 'Jump' and last.a in self.IX and self.IX[last.a] == stmt_start and not st:
            head = stmt_start
            self.seen.add(t - 1)
            body, st2 = self.block(i + 1, t - 1, loops + [(head, t, head)], [])
            if st2: stat('valor sobrante en la pila (while)')
            for e in st2: body.append('%s;' % e.t)
            out.append('while(%s)\n{\n%s\n}' % (neg(cond).t, self.ind(body)))
            return t
        # if / else
        if last is not None and last.name == 'Jump' and last.a in self.IX:
            j = self.IX[last.a]
            if t <= j <= i1 and not (loops and j == loops[-1][1] and j > i1):
                self.seen.add(t - 1)
                then, s1 = self.block(i + 1, t - 1, loops, [])
                if j == t:
                    els, s2 = [], []
                else:
                    els, s2 = self.block(t, j, loops, [])
                if s1 or s2: stat('valor sobrante en la pila (if/else)')
                for e in s1: then.append('%s;' % e.t)
                for e in s2: els.append('%s;' % e.t)
                txt = 'if(%s)\n{\n%s\n}' % (neg(cond).t, self.ind(then))
                if els:
                    if len(els) == 1 and els[0].startswith('if('):
                        txt += '\nelse ' + els[0]
                    else:
                        txt += '\nelse\n{\n%s\n}' % self.ind(els)
                out.append(txt)
                return j
        # if simple
        then, s1 = self.block(i + 1, t, loops, [])
        if s1: stat('valor sobrante en la pila (if)')
        for e in s1: then.append('%s;' % e.t)
        out.append('if(%s)\n{\n%s\n}' % (neg(cond).t, self.ind(then)))
        return t

    # ------------------------------------------------------------------
    def try_forin(self, i, i1, obj, loops, out):
        """Enumerate2 ; H: StoreRegister r ; Push null ; Equals2 ; If fin ; cuerpo ; Jump H"""
        I = self.I
        h = i + 1
        if not (h + 3 < i1 and I[h].name == 'StoreRegister' and I[h + 1].name == 'Push'
                and I[h + 1].a and I[h + 1].a[0].kind == 'null' and I[h + 2].name in ('Equals2', 'StrictEquals')
                and I[h + 3].name == 'If'):
            return None
        reg = I[h].a
        t = self.idx(I[h + 3].a)
        if t > i1 or I[t - 1].name != 'Jump' or self.idx(I[t - 1].a) != h:
            return None
        fn = self.FN
        self.seen.update(range(h, h + 4)); self.seen.add(t - 1)
        old = fn.regnames.get(reg)
        fn.regnames[reg] = '__iter__'
        body, st2 = self.block(h + 4, t - 1, loops + [(h, t, h)], [])
        if old is None: fn.regnames.pop(reg, None)
        else: fn.regnames[reg] = old
        var = '__iter__'
        if st2: stat('valor sobrante en la pila (for-in)')
        if body:
            m = re.match(r'^(var )?([A-Za-z_$][\w$.]*) = __iter__;$', body[0])
            if m:
                var = (m.group(1) or '') + m.group(2)
                body = body[1:]
        if var == '__iter__' or any('__iter__' in s for s in body):
            stat('for-in sin variable reconocible')
        body = [s.replace('__iter__', 'k') for s in body]
        out.append('for(%s in %s)\n{\n%s\n}' % (var if var != '__iter__' else 'var k', obj.t, self.ind(body)))
        return t

    # ------------------------------------------------------------------
    def try_switch(self, i, i1, subj, loops, out, expr_only):
        """StoreRegister rN ; Push v ; StrictEquals ; If c1 ; [Push rN ; Push v ; StrictEquals ; If c2]* ; Jump def"""
        I = self.I
        if expr_only: return None
        reg = I[i].a
        j = i + 1
        cases = []
        first = True
        while j + 2 < i1:
            if first:
                if not (I[j].name == 'Push' and len(I[j].a) == 1 and I[j + 1].name == 'StrictEquals' and I[j + 2].name == 'If'):
                    break
                val = lit(I[j].a[0]); j += 3
            else:
                if not (I[j].name == 'Push' and len(I[j].a) == 2 and I[j].a[0].kind == 'r' and I[j].a[0].v == reg
                        and I[j + 1].name == 'StrictEquals' and I[j + 2].name == 'If'):
                    break
                val = lit(I[j].a[1]); j += 3
            cases.append((val, self.idx(I[j - 1].a)))
            first = False
        if not cases or j >= i1 or I[j].name != 'Jump':
            return None
        dflt = self.idx(I[j].a)
        starts = sorted(set([c[1] for c in cases] + [dflt]))
        # fin del switch: el mayor destino de break dentro de los cuerpos
        end = dflt
        for k in range(j + 1, i1):
            if I[k].name == 'Jump':
                tt = self.IX.get(I[k].a)
                if tt is not None and tt > end and tt <= i1:
                    end = tt
        if end < max(starts):
            end = max(starts)
            # el ultimo caso llega hasta el final del bloque si no hay break
            for k in range(end, i1):
                pass
        if end > i1 or starts[0] != j + 1:
            return None
        self.seen.update(range(i, j + 1))
        lines = []
        bounds = starts + [end] if end not in starts else starts
        by_start = {}
        for v, s in cases:
            by_start.setdefault(s, []).append(v)
        for a, b2 in zip(bounds, bounds[1:]):
            labels = ['case %s:' % v.t for v in by_start.get(a, [])]
            if a == dflt and dflt != end:
                labels.append('default:')
            body, st2 = self.block(a, b2, loops + [(a, end, loops[-1][2] if loops else -1)], [])
            lines += labels
            lines += ['   ' + l for s in body for l in s.split('\n')]
        out.append('switch(%s)\n{\n%s\n}' % (subj.t, '\n'.join('   ' + l for l in lines)))
        return end

    # ------------------------------------------------------------------
    def do_try(self, i, i1, x, loops, out):
        a = x.a
        p0 = x.end
        t_end = p0 + a['t']; c_end = t_end + a['c']; f_end = c_end + a['f']
        tb, _ = self.block(i + 1, self.idx(t_end), loops, [])
        txt = 'try\n{\n%s\n}' % self.ind(tb)
        k = self.idx(t_end)
        # el IDE pone un Jump al final del try para saltar el catch
        if a['flags'] & 1:
            cb, _ = self.block(self.idx(t_end), self.idx(c_end), loops, [])
            cn = a['catch'] if isinstance(a['catch'], str) else self.FN.reg(a['catch'])
            txt += '\ncatch(%s)\n{\n%s\n}' % (cn, self.ind(cb))
        if a['flags'] & 2:
            fb, _ = self.block(self.idx(c_end), self.idx(f_end), loops, [])
            txt += '\nfinally\n{\n%s\n}' % self.ind(fb)
        out.append(txt)
        return self.idx(f_end)


def decompile(b, start=0, end=None):
    """Devuelve (texto_as2, texto_pcode, n_gotos, error)."""
    pc = pcode_tree(b, start, end)
    d = Decompiler(b, [])
    try:
        stmts = d.body(decode(b, start, end, d.pool), Func())
        decompile.last = (d.total, d.missing)
        return '\n'.join(stmts) + '\n', pc, d.gotos, None
    except RecursionError:
        return None, pc, 0, 'RecursionError: anidamiento demasiado profundo'
    except Exception as ex:
        import traceback
        return None, pc, 0, '%s: %s' % (type(ex).__name__, ex)


def pcode_tree(b, start=0, end=None, depth=0, pool=None):
    pool = [] if pool is None else pool
    ins = decode(b, start, end, pool)
    out = []
    for x in ins:
        out += pcode([x], depth)
        if x.name in ('DefineFunction', 'DefineFunction2'):
            a0, a1 = x.a['body']
            sub = pcode_tree(b, a0, a1, depth + 1, list(x.a['pool']))
            out = out[:-1] + sub.split('\n') + [out[-1]]
    return '\n'.join(out)
