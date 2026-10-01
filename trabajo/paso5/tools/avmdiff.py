# Paso 5 — maquina AVM1 "con grabadora" para comparar dos versiones del juego.
#
# Ejecuta el bytecode real de cada script y anota cada efecto observable:
#   escrituras en objetos y en el timeline, llamadas a funciones nativas o a
#   metodos de clips (gotoAndPlay, attachMovie...), trace() y valores devueltos.
# Las variables locales y los registros NO se anotan (son internos a cada
# funcion; justamente ahi es donde original y recompilado pueden diferir sin
# que cambie nada).
#
# Dos ejecuciones son equivalentes si producen la misma lista de efectos.
import struct, math, random

class _U:
    def __repr__(self): return 'undefined'
    def __bool__(self): return False
class _N:
    def __repr__(self): return 'null'
    def __bool__(self): return False
UNDEF = _U(); NULL = _N()

HIDDEN = {'__proto__', 'constructor', '__constructor__', 'prototype'}


class Obj:
    __slots__ = ('props', 'arr', 'kind', 'native', 'code', 'start', 'end', 'params', 'nregs',
                 'scope', 'pool', 'f2', 'flags', 'name', 'oid', 'this_', 'home', 'hidden')
    def __init__(self, kind='object'):
        self.props = {}; self.arr = None; self.kind = kind; self.native = None; self.code = None
        self.name = ''; self.oid = None; self.hidden = None


def mkarr(lst=None):
    o = Obj('array'); o.arr = list(lst or []); return o

def is_fn(v): return isinstance(v, Obj) and (v.native is not None or v.code is not None)


def tonum(v):
    if v is True: return 1.0
    if v is False: return 0.0
    if isinstance(v, float): return v
    if isinstance(v, str):
        s = v.strip()
        if s == '': return 0.0
        try:
            if s[:2].lower() == '0x': return float(int(s, 16))
            return float(s)
        except ValueError: return float('nan')
    if v is NULL: return 0.0
    return float('nan')


def fmtnum(v):
    if v != v: return 'NaN'
    if v == float('inf'): return 'Infinity'
    if v == float('-inf'): return '-Infinity'
    if v == int(v) and abs(v) < 1e15: return str(int(v))
    s = '%.15g' % v
    if 'e' in s:
        m, e = s.split('e'); return m + 'e' + ('+' if int(e) > 0 else '-') + str(abs(int(e)))
    return s


def tostr(v):
    if isinstance(v, str): return v
    if v is UNDEF: return 'undefined'
    if v is NULL: return 'null'
    if v is True: return 'true'
    if v is False: return 'false'
    if isinstance(v, float): return fmtnum(v)
    if isinstance(v, Obj):
        if v.arr is not None: return ','.join(tostr(x) for x in v.arr)
        if is_fn(v): return '[type Function]'
        if v.kind == 'movieclip': return v.name or '_level0'
        return '[object Object]'
    return str(v)


def tobool(v):
    if v is True or v is False: return v
    if v is UNDEF or v is NULL: return False
    if isinstance(v, float): return v == v and v != 0.0
    if isinstance(v, str): return v != ''
    return True


def typeof(v):
    if v is UNDEF: return 'undefined'
    if v is NULL: return 'null'
    if v is True or v is False: return 'boolean'
    if isinstance(v, float): return 'number'
    if isinstance(v, str): return 'string'
    if is_fn(v): return 'function'
    if isinstance(v, Obj) and v.kind == 'movieclip': return 'movieclip'
    return 'object'


class Budget(Exception): pass
class Throw(Exception):
    def __init__(self, v): self.v = v


def _cstr(b, i):
    j = b.index(b'\0', i)
    raw = b[i:j]
    try: return raw.decode('utf-8'), j + 1
    except UnicodeDecodeError: return raw.decode('latin1'), j + 1


MC_RET_CLIP = {'attachMovie', 'createEmptyMovieClip', 'duplicateMovieClip'}
PROPS = ['_x', '_y', '_xscale', '_yscale', '_currentframe', '_totalframes', '_alpha', '_visible',
         '_width', '_height', '_rotation', '_target', '_framesloaded', '_name', '_droptarget',
         '_url', '_highquality', '_focusrect', '_soundbuftime', '_quality', '_xmouse', '_ymouse']


class VM:
    def __init__(self, seed=1, vivify=False, max_effects=4000, max_instr=8_000_000):
        self.rng = random.Random(seed)
        self.vivify = vivify
        self.log = []
        self.next_id = 0
        self.max_effects = max_effects; self.max_instr = max_instr
        self.instr = 0
        self.depth = 0
        self.gregs = [UNDEF] * 4
        self.time = 0
        self.cover = {}          # id(buffer) -> set de posiciones ejecutadas
        self.allfns = []         # todas las funciones creadas, en orden
        self.fowner = {}         # id(funcion) -> (objeto, nombre) de la ultima asignacion
        self.glob = Obj(); self.glob.name = '_global'
        self.root = self.clip('_root')
        self.root.props['_level0'] = self.root
        self._builtins()

    # ------------------------------------------------------------ registro
    def rid(self, o):
        if o.oid is None:
            self.next_id += 1; o.oid = self.next_id
        return o.oid

    def rep(self, v):
        if isinstance(v, Obj):
            return '#%d%s' % (self.rid(v), 'f' if is_fn(v) else ('c' if v.kind == 'movieclip' else ''))
        if isinstance(v, float): return fmtnum(v)
        if isinstance(v, str): return repr(v)
        return repr(v) if v not in (True, False) else ('true' if v else 'false')

    def eff(self, *parts):
        self.log.append(' '.join(parts))
        if len(self.log) > self.max_effects:
            raise Budget('efectos')

    # ------------------------------------------------------------ objetos
    def clip(self, name=''):
        c = Obj('movieclip'); c.name = name
        return c

    def nf(self, name, fn):
        o = Obj('function'); o.native = fn; o.name = name; return o

    def proto_of(self, o):
        p = o.props.get('__proto__')
        return p if isinstance(p, Obj) else None

    def fn_prototype(self, f):
        p = f.props.get('prototype')
        if not isinstance(p, Obj):
            p = Obj(); p.props['constructor'] = f
            f.props['prototype'] = p
        return p

    def getmember(self, o, name, vivify_ok=True):
        name = tostr(name)
        if isinstance(o, str):
            if name == 'length': return float(len(o))
            return self.strmethod(o, name)
        if isinstance(o, float) or o is True or o is False:
            if name == 'toString': return self.nf('toString', lambda t, a, v=o: tostr(v))
            return UNDEF
        if not isinstance(o, Obj): return UNDEF
        if o.arr is not None:
            if name == 'length': return float(len(o.arr))
            if name.isdigit():
                i = int(name); return o.arr[i] if i < len(o.arr) else UNDEF
            m = self.arrmethod(o, name)
            if m is not None: return m
        if is_fn(o) and name == 'prototype':
            return self.fn_prototype(o)
        k = o; n = 0
        while k is not None and n < 50:
            if name in k.props: return k.props[name]
            k = self.proto_of(k); n += 1
        if is_fn(o) and name in ('call', 'apply'):
            if name == 'call':
                return self.nf('call', lambda t, a, f=o: self.call(f, a[0] if a else UNDEF, list(a[1:])))
            return self.nf('apply', lambda t, a, f=o: self.call(
                f, a[0] if a else UNDEF, list(a[1].arr) if len(a) > 1 and isinstance(a[1], Obj) and a[1].arr is not None else []))
        if name in ('hasOwnProperty',):
            return self.nf(name, lambda t, a, oo=o: tostr(a[0]) in oo.props if a else False)
        if o.kind == 'movieclip':
            if name in PROPS: return self.clipprop(o, name)
            if self.vivify and vivify_ok and not name.startswith('on') and name[:1] != '_':
                c = self.clip(name); o.props[name] = c
                return c
        return UNDEF

    def clipprop(self, c, name):
        d = {'_x': 0.0, '_y': 0.0, '_xscale': 100.0, '_yscale': 100.0, '_currentframe': 1.0,
             '_totalframes': 1.0, '_alpha': 100.0, '_visible': True, '_width': 0.0, '_height': 0.0,
             '_rotation': 0.0, '_framesloaded': 1.0, '_name': c.name, '_xmouse': 0.0, '_ymouse': 0.0}
        return d.get(name, UNDEF)

    def setmember(self, o, name, v):
        name = tostr(name)
        if not isinstance(o, Obj): return
        self.eff('set', self.rep(o), name, self.rep(v))
        if isinstance(v, Obj) and v.code is not None:
            self.fowner[id(v)] = (o, name)
        if o.arr is not None:
            if name == 'length':
                n = int(tonum(v)) if tonum(v) == tonum(v) else 0
                del o.arr[n:]
                while len(o.arr) < n: o.arr.append(UNDEF)
                return
            if name.isdigit():
                i = int(name)
                if i < 100000:
                    while len(o.arr) <= i: o.arr.append(UNDEF)
                    o.arr[i] = v
                return
        o.props[name] = v

    def strmethod(self, s, name):
        nf = self.nf
        def I(a, k, d=0):
            if len(a) <= k: return d
            x = tonum(a[k]); return int(x) if x == x else 0
        if name == 'charAt': return nf(name, lambda t, a: s[I(a, 0)] if 0 <= I(a, 0) < len(s) else '')
        if name == 'charCodeAt': return nf(name, lambda t, a: float(ord(s[I(a, 0)])) if 0 <= I(a, 0) < len(s) else float('nan'))
        if name == 'indexOf': return nf(name, lambda t, a: float(s.find(tostr(a[0]) if a else 'undefined', max(0, I(a, 1)))))
        if name == 'lastIndexOf': return nf(name, lambda t, a: float(s.rfind(tostr(a[0]) if a else 'undefined')))
        if name == 'substring':
            def f(t, a):
                i = max(0, I(a, 0)); j = max(0, I(a, 1, len(s)))
                if i > j: i, j = j, i
                return s[i:j]
            return nf(name, f)
        if name == 'substr':
            def f(t, a):
                i = I(a, 0)
                if i < 0: i = max(0, len(s) + i)
                n = I(a, 1, len(s))
                return s[i:i + max(0, n)]
            return nf(name, f)
        if name == 'slice': return nf(name, lambda t, a: s[I(a, 0):I(a, 1, len(s))])
        if name == 'toUpperCase': return nf(name, lambda t, a: s.upper())
        if name == 'toLowerCase': return nf(name, lambda t, a: s.lower())
        if name == 'split':
            def f(t, a):
                if not a or a[0] is UNDEF: return mkarr([s])
                d = tostr(a[0])
                return mkarr(list(s) if d == '' else s.split(d))
            return nf(name, f)
        if name in ('toString', 'valueOf'): return nf(name, lambda t, a: s)
        if name == 'concat': return nf(name, lambda t, a: s + ''.join(tostr(x) for x in a))
        return UNDEF

    def arrmethod(self, o, name):
        nf = self.nf; A = o.arr
        def I(a, k, d):
            if len(a) <= k: return d
            x = tonum(a[k]); return int(x) if x == x else 0
        if name == 'push':
            def f(t, a):
                self.eff('push', self.rep(o), *[self.rep(x) for x in a]); A.extend(a); return float(len(A))
            return nf(name, f)
        if name == 'pop':
            def f(t, a):
                self.eff('pop', self.rep(o)); return A.pop() if A else UNDEF
            return nf(name, f)
        if name == 'shift':
            def f(t, a):
                self.eff('shift', self.rep(o)); return A.pop(0) if A else UNDEF
            return nf(name, f)
        if name == 'unshift':
            def f(t, a):
                self.eff('unshift', self.rep(o), *[self.rep(x) for x in a])
                A[0:0] = list(a); return float(len(A))
            return nf(name, f)
        if name == 'slice':
            def f(t, a):
                i = I(a, 0, 0); j = I(a, 1, len(A))
                return mkarr(A[i:j])
            return nf(name, f)
        if name == 'splice':
            def f(t, a):
                i = I(a, 0, 0)
                if i < 0: i += len(A)
                n = I(a, 1, len(A) - i)
                self.eff('splice', self.rep(o), str(i), str(n), *[self.rep(x) for x in a[2:]])
                cut = A[i:i + n]; A[i:i + n] = list(a[2:]); return mkarr(cut)
            return nf(name, f)
        if name == 'join': return nf(name, lambda t, a: (tostr(a[0]) if a and a[0] is not UNDEF else ',').join(tostr(x) for x in A))
        if name == 'concat': return nf(name, lambda t, a: mkarr(A + [y for x in a for y in (x.arr if isinstance(x, Obj) and x.arr is not None else [x])]))
        if name == 'reverse':
            def f(t, a):
                self.eff('reverse', self.rep(o)); A.reverse(); return o
            return nf(name, f)
        if name == 'sort' or name == 'sortOn':
            def f(t, a):
                self.eff(name, self.rep(o))
                import functools
                if name == 'sort' and a and is_fn(a[0]):
                    A.sort(key=functools.cmp_to_key(lambda x, y: (lambda r: 0 if r != r else (1 if r > 0 else (-1 if r < 0 else 0)))(tonum(self.call(a[0], UNDEF, [x, y])))))
                elif name == 'sortOn' and a:
                    k = tostr(a[0])
                    A.sort(key=lambda x: tostr(self.getmember(x, k)))
                else:
                    A.sort(key=tostr)
                return o
            return nf(name, f)
        if name == 'toString': return nf(name, lambda t, a: tostr(o))
        return None

    # ------------------------------------------------------------ nativos del entorno
    def _builtins(self):
        g = self.glob.props; nf = self.nf
        M = Obj(); M.name = 'Math'
        def w(f):
            def h(t, a):
                x = tonum(a[0]) if a else float('nan')
                try: return float(f(x))
                except (ValueError, OverflowError): return float('nan')
            return h
        for n, f in (('floor', math.floor), ('ceil', math.ceil), ('abs', abs), ('sqrt', math.sqrt),
                     ('sin', math.sin), ('cos', math.cos), ('tan', math.tan), ('atan', math.atan),
                     ('log', math.log), ('exp', math.exp), ('asin', math.asin), ('acos', math.acos)):
            M.props[n] = nf(n, w(f))
        M.props['round'] = nf('round', w(lambda x: math.floor(x + 0.5)))
        M.props['pow'] = nf('pow', lambda t, a: self._pow(a))
        M.props['atan2'] = nf('atan2', lambda t, a: math.atan2(tonum(a[0]), tonum(a[1])))
        M.props['random'] = nf('random', lambda t, a: self.rng.random())
        M.props['max'] = nf('max', lambda t, a: (lambda v: float('nan') if any(x != x for x in v) else max(v))([tonum(x) for x in a] or [float('-inf')]))
        M.props['min'] = nf('min', lambda t, a: (lambda v: float('nan') if any(x != x for x in v) else min(v))([tonum(x) for x in a] or [float('inf')]))
        M.props['PI'] = math.pi
        g['Math'] = M
        def mkobj(t, a):
            return Obj()
        g['Object'] = nf('Object', mkobj)
        self.fn_prototype(g['Object'])
        g['Object'].props['registerClass'] = nf('registerClass', lambda t, a: self._rec('Object.registerClass', a, True))
        g['Array'] = nf('Array', lambda t, a: mkarr(a) if len(a) != 1 or not isinstance(a[0], float) else mkarr([UNDEF] * max(0, min(100000, int(a[0])))))
        g['String'] = nf('String', lambda t, a: tostr(a[0]) if a else '')
        g['String'].props['fromCharCode'] = nf('fromCharCode', lambda t, a: ''.join(chr(int(tonum(x)) & 0xFFFF) for x in a))
        g['Number'] = nf('Number', lambda t, a: tonum(a[0]) if a else 0.0)
        g['Boolean'] = nf('Boolean', lambda t, a: tobool(a[0]) if a else False)
        g['isNaN'] = nf('isNaN', lambda t, a: tonum(a[0]) != tonum(a[0]) if a else True)
        g['isFinite'] = nf('isFinite', lambda t, a: math.isfinite(tonum(a[0])) if a else False)
        def pint(t, a):
            s = tostr(a[0]).strip() if a else ''
            import re
            m = re.match(r'^[+-]?\d+', s)
            return float(int(m.group(0))) if m else float('nan')
        def pfl(t, a):
            s = tostr(a[0]).strip() if a else ''
            import re
            m = re.match(r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?', s)
            return float(m.group(0)) if m else float('nan')
        g['parseInt'] = nf('parseInt', pint); g['parseFloat'] = nf('parseFloat', pfl)
        g['ASSetPropFlags'] = nf('ASSetPropFlags', lambda t, a: UNDEF)
        g['NaN'] = float('nan'); g['Infinity'] = float('inf')
        # todo lo demas del entorno Flash se simula grabando la llamada
        for n in ('setInterval', 'clearInterval', 'escape', 'unescape', 'fscommand', 'getVersion',
                  'updateAfterEvent', 'showRedrawRegions', 'setTimeout', 'clearTimeout'):
            g[n] = nf(n, (lambda n: lambda t, a: self._rec(n, a))(n))
        for cls in ('Sound', 'TextFormat', 'Color', 'Date', 'LoadVars', 'XML', 'LocalConnection',
                    'ColorTransform', 'Matrix', 'Point', 'Rectangle', 'BitmapData', 'GlowFilter',
                    'DropShadowFilter', 'BlurFilter', 'TextField', 'MovieClip', 'Transform',
                    'ContextMenu', 'ContextMenuItem', 'Button', 'Function', 'Error'):
            g[cls] = self.mock_class(cls)
        for n in ('Key', 'Mouse', 'Stage', 'Selection', 'System', 'SharedObject', 'Accessibility',
                  'ExternalInterface', 'Camera', 'Microphone', 'Video'):
            g[n] = self.mock_static(n)

    def _pow(self, a):
        try: return float(tonum(a[0]) ** tonum(a[1]))
        except (OverflowError, ZeroDivisionError, ValueError): return float('nan')
        except TypeError: return float('nan')

    def _rec(self, name, a, ret_undef=True):
        self.eff('call', name, *[self.rep(x) for x in a])
        return UNDEF

    def mock_class(self, cls):
        def ctor(t, a):
            o = Obj('mock'); o.name = cls
            self.eff('new', cls, self.rep(o), *[self.rep(x) for x in a])
            return o
        return self.nf(cls, ctor)

    def mock_static(self, n):
        o = Obj('mock'); o.name = n
        return o

    # ------------------------------------------------------------ variables
    def getvar(self, name, ctx):
        if name == 'this': return ctx['this']
        if name == '_root' or name == '_level0': return self.root
        if name == '_global': return self.glob
        if name == '_parent':
            t = ctx['this']
            return t.props.get('_parent', self.root) if isinstance(t, Obj) else UNDEF
        if name == 'arguments': return ctx.get('args', UNDEF)
        if name == 'super': return ctx.get('super', UNDEF)
        if '.' in name or '/' in name or ':' in name:
            return self.path(name, ctx)
        for sc in ctx['scope']:
            if isinstance(sc, dict):
                if name in sc: return sc[name]
            else:
                v = self.getmember(sc, name, vivify_ok=False)
                if v is not UNDEF or (isinstance(sc, Obj) and name in sc.props): return v
        if name in self.glob.props: return self.glob.props[name]
        return UNDEF

    def path(self, p, ctx):
        parts = [x for x in p.replace('/', '.').replace(':', '.').split('.') if x]
        if not parts: return ctx['this']
        v = self.getvar(parts[0], ctx)
        for k in parts[1:]:
            v = self.getmember(v, k)
        return v

    def setvar(self, name, v, ctx):
        if '.' in name or '/' in name or ':' in name:
            parts = [x for x in name.replace('/', '.').replace(':', '.').split('.') if x]
            o = self.path('.'.join(parts[:-1]), ctx) if len(parts) > 1 else ctx['tl']
            self.setmember(o, parts[-1], v); return
        for sc in ctx['scope']:
            if isinstance(sc, dict):
                if name in sc: sc[name] = v; return
            elif isinstance(sc, Obj) and name in sc.props:
                self.setmember(sc, name, v); return
        self.setmember(ctx['tl'], name, v)

    # ------------------------------------------------------------ llamadas
    def call(self, f, this, args, name=''):
        if not is_fn(f):
            if isinstance(this, Obj) and this.kind in ('movieclip', 'mock') and name:
                self.eff('mc', self.rep(this), name, *[self.rep(x) for x in args])
                if name in MC_RET_CLIP:
                    c = self.clip(tostr(args[1]) if len(args) > 1 else 'clip')
                    c.props['_parent'] = this
                    if len(args) > 1: this.props[tostr(args[1])] = c
                    return c
                if name == 'hitTest': return False
                if name in ('getDepth', 'getNextHighestDepth', 'getBytesLoaded', 'getBytesTotal'): return 1.0
                return UNDEF
            self.eff('callmissing', name or '?', *[self.rep(x) for x in args])
            return UNDEF
        if f.native is not None:
            r = f.native(this, args)
            return r
        self.depth += 1
        if self.depth > 100:
            self.depth -= 1
            raise Throw('recursion')
        try:
            locs = {}
            argo = mkarr(args)
            if f.f2:
                regs = [UNDEF] * max(1, f.nregs)
                fl = f.flags; r = 1
                sup = self.superobj(f, this)
                pre = []
                if fl & 0x01: pre.append(this)
                if fl & 0x04: pre.append(argo)
                if fl & 0x10: pre.append(sup)
                if fl & 0x40: pre.append(self.root)
                if fl & 0x80: pre.append(this.props.get('_parent', self.root) if isinstance(this, Obj) else self.root)
                if fl & 0x100: pre.append(self.glob)
                for v in pre:
                    if r < len(regs): regs[r] = v
                    r += 1
                for i, (rg, pn) in enumerate(f.params):
                    v = args[i] if i < len(args) else UNDEF
                    if rg and rg < len(regs): regs[rg] = v
                    else: locs[pn] = v
            else:
                regs = self.gregs          # DefineFunction clasico: registros globales
                sup = self.superobj(f, this)
                for i, pn in enumerate(f.params):
                    locs[pn] = args[i] if i < len(args) else UNDEF
            ctx = {'this': this, 'scope': [locs] + f.scope, 'regs': regs, 'pool': f.pool,
                   'args': argo, 'super': sup, 'tl': f.home if f.home is not None else self.root}
            return self.run(f.code, f.start, f.end, ctx)
        finally:
            self.depth -= 1

    def superobj(self, f, this):
        s = Obj('super'); s.this_ = this
        s.home = f
        return s

    def construct(self, f, args, name):
        if is_fn(f) and f.native is not None:
            return f.native(UNDEF, args)
        o = Obj()
        if is_fn(f):
            o.props['__proto__'] = self.fn_prototype(f)
            o.props['__constructor__'] = f
            r = self.call(f, o, args, name)
            if isinstance(r, Obj): return r
        else:
            self.eff('newmissing', name)
        return o

    def call_super(self, s, name, args):
        # super.metodo(...) o super(...): busca en el prototipo del padre
        this = s.this_
        f = s.home
        # clase actual: el prototipo que contiene a la funcion en ejecucion
        proto = self.proto_of(this) if isinstance(this, Obj) else None
        k = proto; home = None; n = 0
        while k is not None and n < 50:
            if any(v is f for v in k.props.values()) or k.props.get('constructor') is f:
                home = k; break
            k = self.proto_of(k); n += 1
        base = self.proto_of(home) if home is not None else (self.proto_of(proto) if proto else None)
        if name is None:
            ctor = home.props.get('__constructor__') if home is not None else None
            if ctor is None and base is not None: ctor = base.props.get('constructor')
            if is_fn(ctor): return self.call(ctor, this, args, 'super')
            return UNDEF
        m = self.getmember(base, name) if base is not None else UNDEF
        if is_fn(m): return self.call(m, this, args, name)
        self.eff('supermissing', name)
        return UNDEF

    def instanceof(self, o, c):
        if not isinstance(o, Obj) or not is_fn(c): return False
        p = self.fn_prototype(c); k = self.proto_of(o); n = 0
        while k is not None and n < 50:
            if k is p: return True
            k = self.proto_of(k); n += 1
        return False

    # ------------------------------------------------------------ interprete
    def run_script(self, b, a0, a1, this, tl=None):
        ctx = {'this': this, 'scope': [this] if isinstance(this, Obj) else [], 'regs': self.gregs,
               'pool': [[]], 'args': UNDEF, 'super': UNDEF, 'tl': tl or this}
        return self.run(b, a0, a1, ctx)

    def run(self, b, start, end, ctx):
        st = []
        push = st.append
        def pop():
            return st.pop() if st else UNDEF
        regs = ctx['regs']
        cov = self.cover.setdefault(id(b), set())
        i = start
        while i < end:
            self.instr += 1
            if self.instr > self.max_instr: raise Budget('instrucciones')
            cov.add(i)
            op = b[i]
            if op == 0: return UNDEF
            if op < 0x80:
                i += 1
                if op == 0x17: pop()
                elif op == 0x4C: v = pop(); push(v); push(v)
                elif op == 0x4D:
                    a = pop(); c = pop(); push(a); push(c)
                elif op == 0x1C: push(self.getvar(tostr(pop()), ctx))
                elif op == 0x1D:
                    v = pop(); self.setvar(tostr(pop()), v, ctx)
                elif op == 0x4E:
                    n = pop(); o = pop()
                    if isinstance(o, Obj) and o.kind == 'super':
                        push(self.nf('super.' + tostr(n), lambda t, a, s=o, nm=tostr(n): self.call_super(s, nm, a)))
                    else:
                        push(self.getmember(o, n))
                elif op == 0x4F:
                    v = pop(); n = pop(); o = pop(); self.setmember(o, n, v)
                elif op == 0x3C:
                    v = pop(); n = tostr(pop())
                    sc = ctx['scope'][0] if ctx['scope'] else None
                    if isinstance(sc, dict): sc[n] = v
                    else: self.setmember(ctx['tl'], n, v)
                elif op == 0x41:
                    n = tostr(pop())
                    sc = ctx['scope'][0] if ctx['scope'] else None
                    if isinstance(sc, dict): sc.setdefault(n, UNDEF)
                elif op == 0x3D:
                    n = pop(); na = self.cnt(pop())
                    args = [pop() for _ in range(na)]
                    nm = tostr(n)
                    f = self.getvar(nm, ctx)
                    push(self.call(f, ctx['this'] if False else UNDEF, args, nm))
                elif op == 0x52:
                    n = pop(); o = pop(); na = self.cnt(pop())
                    args = [pop() for _ in range(na)]
                    if isinstance(o, Obj) and o.kind == 'super':
                        push(self.call_super(o, None if (n is UNDEF or tostr(n) == '') else tostr(n), args))
                    elif n is UNDEF or tostr(n) == '':
                        push(self.call(o, UNDEF, args, '<expr>'))
                    else:
                        f = self.getmember(o, n, vivify_ok=False)
                        push(self.call(f, o, args, tostr(n)))
                elif op == 0x40:
                    n = tostr(pop()); na = self.cnt(pop())
                    args = [pop() for _ in range(na)]
                    push(self.construct(self.getvar(n, ctx), args, n))
                elif op == 0x53:
                    n = pop(); o = pop(); na = self.cnt(pop())
                    args = [pop() for _ in range(na)]
                    f = o if (n is UNDEF or tostr(n) == '') else self.getmember(o, n)
                    push(self.construct(f, args, tostr(n)))
                elif op == 0x3E:
                    return pop()
                elif op == 0x42:
                    na = self.cnt(pop()); push(mkarr([pop() for _ in range(na)]))
                elif op == 0x43:
                    na = self.cnt(pop()); o = Obj(); kv = []
                    for _ in range(na):
                        v = pop(); k = tostr(pop()); kv.append((k, v))
                    for k, v in reversed(kv): o.props[k] = v
                    push(o)
                elif op == 0x47:
                    r = pop(); l = pop()
                    l2 = self.prim(l); r2 = self.prim(r)
                    if isinstance(l2, str) or isinstance(r2, str): push(tostr(l2) + tostr(r2))
                    else: push(tonum(l2) + tonum(r2))
                elif op == 0x0A: r = pop(); push(tonum(pop()) + tonum(r))
                elif op == 0x0B: r = pop(); push(tonum(pop()) - tonum(r))
                elif op == 0x0C: r = pop(); push(tonum(pop()) * tonum(r))
                elif op == 0x0D:
                    r = tonum(pop()); l = tonum(pop())
                    if r == 0: push(float('nan') if l == 0 or l != l else math.copysign(float('inf'), l) * math.copysign(1, r))
                    else: push(l / r)
                elif op == 0x3F:
                    r = tonum(pop()); l = tonum(pop())
                    push(float('nan') if r == 0 or r != r or l != l or math.isinf(l) else math.fmod(l, r))
                elif op == 0x50: push(tonum(pop()) + 1)
                elif op == 0x51: push(tonum(pop()) - 1)
                elif op == 0x12: push(not tobool(pop()))
                elif op == 0x10: r = pop(); l = pop(); push(tobool(l) and tobool(r))
                elif op == 0x11: r = pop(); l = pop(); push(tobool(l) or tobool(r))
                elif op in (0x49, 0x0E): r = pop(); l = pop(); push(self.looseeq(l, r))
                elif op == 0x66: r = pop(); l = pop(); push(self.stricteq(l, r))
                elif op in (0x48, 0x0F): r = pop(); l = pop(); push(self.lt(l, r))
                elif op == 0x67: r = pop(); l = pop(); push(self.lt(r, l))
                elif op == 0x13: r = pop(); l = pop(); push(tostr(l) == tostr(r))
                elif op == 0x29: r = pop(); l = pop(); push(tostr(l) < tostr(r))
                elif op == 0x68: r = pop(); l = pop(); push(tostr(l) > tostr(r))
                elif op == 0x21: r = pop(); l = pop(); push(tostr(l) + tostr(r))
                elif op == 0x44: push(typeof(pop()))
                elif op == 0x54: c = pop(); o = pop(); push(self.instanceof(o, c))
                elif op == 0x2B:
                    o = pop(); c = pop(); push(o if self.instanceof(o, c) else NULL)
                elif op in (0x55, 0x46):
                    o = pop()
                    if op == 0x46: o = self.getvar(tostr(o), ctx)
                    push(NULL)
                    if isinstance(o, Obj):
                        keys = []
                        if o.arr is not None: keys += [str(k) for k in range(len(o.arr))]
                        k = o; seen = set(); n = 0
                        while k is not None and n < 50:
                            for kk in k.props:
                                if kk not in seen and kk not in HIDDEN:
                                    seen.add(kk); keys.append(kk)
                            k = self.proto_of(k); n += 1
                        for kk in reversed(keys): push(kk)
                elif op == 0x26: self.eff('trace', repr(tostr(pop())))
                elif op == 0x30:
                    n = tonum(pop()); push(float(self.rng.randrange(max(1, int(n)))) if n == n and n >= 1 else 0.0)
                elif op in (0x60, 0x61, 0x62, 0x63, 0x64, 0x65):
                    r = self.i32(pop()); l = self.i32(pop())
                    if op == 0x60: v = l & r
                    elif op == 0x61: v = l | r
                    elif op == 0x62: v = l ^ r
                    elif op == 0x63: v = self.i32(float((l << (r & 31)) & 0xFFFFFFFF))
                    elif op == 0x64: v = l >> (r & 31)
                    else: v = (l & 0xFFFFFFFF) >> (r & 31)
                    push(float(v))
                elif op == 0x18:
                    n = tonum(pop()); push(0.0 if n != n or math.isinf(n) else float(int(n)))
                elif op == 0x4A: push(tonum(self.prim(pop())))
                elif op == 0x4B: push(tostr(pop()))
                elif op in (0x14, 0x31): push(float(len(tostr(pop()))))
                elif op in (0x15, 0x35):
                    c = int(tonum(pop()) or 0); ix = int(tonum(pop()) or 0); s = tostr(pop())
                    push(s[max(0, ix - 1):max(0, ix - 1) + max(0, c)])
                elif op in (0x32, 0x36):
                    s = tostr(pop()); push(float(ord(s[0])) if s else 0.0)
                elif op in (0x33, 0x37): push(chr(int(tonum(pop())) & 0xFFFF))
                elif op == 0x34:
                    self.time += 33; push(float(self.time))
                elif op == 0x45: push(tostr(pop()))
                elif op == 0x3A:
                    n = tostr(pop()); o = pop()
                    ok = isinstance(o, Obj) and n in o.props
                    if ok:
                        self.eff('delete', self.rep(o), n); del o.props[n]
                    push(ok)
                elif op == 0x3B:
                    n = tostr(pop()); ok = False
                    for sc in ctx['scope']:
                        if isinstance(sc, dict) and n in sc:
                            del sc[n]; ok = True; break
                        if isinstance(sc, Obj) and n in sc.props:
                            self.eff('delete', self.rep(sc), n); del sc.props[n]; ok = True; break
                    push(ok)
                elif op == 0x22:
                    ix = pop(); t = pop()
                    o = self.target(t, ctx)
                    k = int(tonum(ix)) if tonum(ix) == tonum(ix) else -1
                    nm = PROPS[k] if 0 <= k < len(PROPS) else ''
                    push(self.getmember(o, nm) if isinstance(o, Obj) and nm else UNDEF)
                elif op == 0x23:
                    v = pop(); ix = pop(); t = pop()
                    o = self.target(t, ctx)
                    k = int(tonum(ix)) if tonum(ix) == tonum(ix) else -1
                    nm = PROPS[k] if 0 <= k < len(PROPS) else '?%s' % tostr(ix)
                    if isinstance(o, Obj): self.setmember(o, nm, v)
                    else: self.eff('setprop', tostr(t), nm, self.rep(v))
                elif op == 0x25: self.eff('removeMovieClip', self.rep(pop()))
                elif op == 0x24:
                    d = pop(); t = pop(); s = pop()
                    self.eff('duplicateMovieClip', self.rep(s), self.rep(t), self.rep(d))
                elif op == 0x27:
                    tg = pop(); lock = pop(); con = pop()
                    ex = [pop() for _ in range(4)] if tobool(con) else []
                    self.eff('startDrag', self.rep(tg), self.rep(lock), *[self.rep(x) for x in ex])
                elif op in (0x06, 0x07, 0x04, 0x05, 0x09, 0x08, 0x28):
                    self.eff({6: 'play', 7: 'stop', 4: 'nextFrame', 5: 'prevFrame', 9: 'stopAllSounds',
                              8: 'toggleQuality', 0x28: 'stopDrag'}[op], self.rep(ctx['tl']))
                elif op == 0x69:
                    sup = pop(); sub = pop()
                    if is_fn(sub) and is_fn(sup):
                        p = Obj(); p.props['__proto__'] = self.fn_prototype(sup)
                        p.props['__constructor__'] = sup
                        sub.props['prototype'] = p
                    self.eff('extends', self.rep(sub), self.rep(sup))
                elif op == 0x2C:
                    c = pop(); n = self.cnt(pop())
                    for _ in range(n): pop()
                elif op == 0x2A: raise Throw(pop())
                elif op == 0x20: self.eff('setTarget', self.rep(pop()))
                elif op == 0x9E: self.eff('call', self.rep(pop()))
                else:
                    self.eff('op?', hex(op))
                continue
            ln = struct.unpack_from('<H', b, i + 1)[0]
            p = i + 3; q = p + ln
            if op == 0x96:
                pool = ctx['pool'][0]
                while p < q:
                    t = b[p]; p += 1
                    if t == 0: s, p = _cstr(b, p); push(s)
                    elif t == 1: push(float(struct.unpack_from('<f', b, p)[0])); p += 4
                    elif t == 2: push(NULL)
                    elif t == 3: push(UNDEF)
                    elif t == 4: push(regs[b[p]] if b[p] < len(regs) else UNDEF); p += 1
                    elif t == 5: push(bool(b[p])); p += 1
                    elif t == 6:
                        raw = b[p:p + 8]; push(struct.unpack('<d', raw[4:] + raw[:4])[0]); p += 8
                    elif t == 7: push(float(struct.unpack_from('<i', b, p)[0])); p += 4
                    elif t == 8: k = b[p]; push(pool[k] if k < len(pool) else UNDEF); p += 1
                    elif t == 9:
                        k = struct.unpack_from('<H', b, p)[0]; push(pool[k] if k < len(pool) else UNDEF); p += 2
                    else: push(UNDEF); p = q
                i = q; continue
            if op == 0x88:
                c = struct.unpack_from('<H', b, p)[0]; p += 2; lst = []
                for _ in range(c):
                    s, p = _cstr(b, p); lst.append(s)
                ctx['pool'] = [lst]
                i = q; continue
            if op == 0x99:
                i = q + struct.unpack_from('<h', b, p)[0]; continue
            if op == 0x9D:
                t = q + struct.unpack_from('<h', b, p)[0]
                i = t if tobool(pop()) else q; continue
            if op == 0x87:
                r = b[p]
                if r < len(regs): regs[r] = st[-1] if st else UNDEF
                i = q; continue
            if op in (0x9B, 0x8E):
                nm, p = _cstr(b, p)
                npar = struct.unpack_from('<H', b, p)[0]; p += 2
                f = Obj('function'); f.name = nm
                if op == 0x8E:
                    f.nregs = b[p]; p += 1
                    f.flags = struct.unpack_from('<H', b, p)[0]; p += 2
                    ps = []
                    for _ in range(npar):
                        r = b[p]; s, p = _cstr(b, p + 1); ps.append((r, s))
                    f.f2 = True
                else:
                    ps = []
                    for _ in range(npar):
                        s, p = _cstr(b, p); ps.append(s)
                    f.f2 = False; f.nregs = 4; f.flags = 0
                cs = struct.unpack_from('<H', b, p)[0]; p += 2
                f.code = b; f.start = p; f.end = p + cs; f.params = ps
                f.scope = ctx['scope']; f.pool = [ctx['pool'][0]]
                f.home = ctx['tl']
                self.allfns.append(f)
                if nm:
                    sc = ctx['scope'][0] if ctx['scope'] else None
                    if isinstance(sc, dict) and ctx.get('args') is not UNDEF: sc[nm] = f
                    else: self.setmember(ctx['tl'], nm, f)
                else:
                    push(f)
                i = p + cs; continue
            if op == 0x94:      # With
                o = pop()
                sub = dict(ctx); sub['scope'] = [o] + ctx['scope']
                self.run(b, q, q + struct.unpack_from('<H', b, p)[0], sub)
                i = q + struct.unpack_from('<H', b, p)[0]; continue
            if op == 0x9A:
                tg = pop(); u = pop()
                self.eff('getURL2', self.rep(u), self.rep(tg), str(b[p])); i = q; continue
            if op == 0x83:
                u, p2 = _cstr(b, p); t2, _ = _cstr(b, p2)
                self.eff('getURL2', repr(u), repr(t2), '0'); i = q; continue
            if op == 0x81:
                self.eff('gotoAndStop', self.rep(ctx['tl']), repr(float(struct.unpack_from('<H', b, p)[0] + 1)))
                i = q; continue
            if op == 0x8C:
                s, _ = _cstr(b, p); self.eff('gotoAndStop', self.rep(ctx['tl']), repr(s)); i = q; continue
            if op == 0x9F:
                fr = pop()
                self.eff('gotoAndPlay' if b[p] & 1 else 'gotoAndStop', self.rep(ctx['tl']),
                         repr(tonum(fr)) if isinstance(fr, float) else self.rep(fr))
                i = q; continue
            if op == 0x8B:
                s, _ = _cstr(b, p); self.eff('setTarget', repr(s)); i = q; continue
            i = q
        return UNDEF

    # ------------------------------------------------------------ util
    def prim(self, v):
        if isinstance(v, Obj):
            if v.arr is not None or is_fn(v) or v.kind in ('movieclip',): return tostr(v)
            vo = self.getmember(v, 'valueOf', vivify_ok=False)
            if is_fn(vo) and vo.code is not None: return self.prim(self.call(vo, v, [], 'valueOf'))
            ts = self.getmember(v, 'toString', vivify_ok=False)
            if is_fn(ts) and ts.code is not None: return tostr(self.call(ts, v, [], 'toString'))
            return tostr(v)
        return v

    def target(self, t, ctx):
        if isinstance(t, Obj): return t
        s = tostr(t)
        if s == '': return ctx['tl']
        v = self.path(s, ctx)
        return v if isinstance(v, Obj) else None

    @staticmethod
    def cnt(v):
        n = tonum(v)
        return max(0, min(10000, int(n))) if n == n and not math.isinf(n) else 0

    @staticmethod
    def i32(v):
        n = tonum(v)
        if n != n or math.isinf(n): return 0
        n = int(n) & 0xFFFFFFFF
        return n - 0x100000000 if n >= 0x80000000 else n

    def looseeq(self, l, r):
        if l is UNDEF or l is NULL: return r is UNDEF or r is NULL
        if r is UNDEF or r is NULL: return False
        if isinstance(l, Obj) and isinstance(r, Obj): return l is r
        if isinstance(l, Obj): l = self.prim(l)
        if isinstance(r, Obj): r = self.prim(r)
        if isinstance(l, str) and isinstance(r, str): return l == r
        return tonum(l) == tonum(r)

    def stricteq(self, l, r):
        if typeof(l) != typeof(r): return False
        if isinstance(l, Obj): return l is r
        return self.looseeq(l, r)

    def lt(self, l, r):
        l = self.prim(l); r = self.prim(r)
        if isinstance(l, str) and isinstance(r, str): return l < r
        a, c = tonum(l), tonum(r)
        if a != a or c != c: return UNDEF
        return a < c
