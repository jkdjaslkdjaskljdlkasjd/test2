# Paso 4 — Compilador ActionScript 2 -> bytecode AVM1 (SWF 6+).
#
# Es el inverso de as2dec.py: acepta todo lo que el descompilador escribe
# (incluidos _locN_ = registro N, goto/etiquetas L_n, eval/set, __cast) y
# genera el bytecode con los mismos patrones que el compilador de Macromedia
# (if -> cond Not If, &&/|| con PushDuplicate, for-in con registro 0, etc.).
#
#   from as2comp import compile_script
#   codigo = compile_script(texto_as2)          # bytes, terminados en End (0x00)
#
# Reglas de funciones (siempre DefineFunction2, como el compilador de AS2):
#   - this/arguments/super: se precargan en registros si se usan; si no, se suprimen.
#   - _root/_parent/_global: se precargan si se usan.
#   - Si una precarga chocara con un _locN_ del cuerpo, no se precarga nada y se
#     accede por nombre (mismo resultado).
#   - Los parametros van por nombre (registro 0): asi los ven tambien las
#     funciones anidadas.
import re, struct

__all__ = ['compile_script', 'CompileError']


class CompileError(Exception):
    pass


# ====================================================================== lexer
TOKRE = re.compile(r'''
   (?P<ws>\s+)
 | (?P<lc>//[^\n]*)
 | (?P<bc>/\*.*?\*/)
 | (?P<num>0[xX][0-9a-fA-F]+|(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?)
 | (?P<str>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')
 | (?P<id>[A-Za-z_$][A-Za-z0-9_$]*)
 | (?P<op>>>>=|>>>|===|!==|<<=|>>=|==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<|>>|[-+*/%<>=!?:;,.(){}\[\]&|^~])
''', re.S | re.X)

ESC = {'n': '\n', 'r': '\r', 't': '\t', 'b': '\b', 'f': '\f', 'v': '\v', '0': '\0'}


def unescape(s):
    out = []; i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            d = s[i + 1]
            if d in ESC: out.append(ESC[d]); i += 2; continue
            if d == 'u' and re.match(r'[0-9a-fA-F]{4}', s[i + 2:i + 6]):
                out.append(chr(int(s[i + 2:i + 6], 16))); i += 6; continue
            if d == 'x' and re.match(r'[0-9a-fA-F]{2}', s[i + 2:i + 4]):
                out.append(chr(int(s[i + 2:i + 4], 16))); i += 4; continue
            out.append(d); i += 2; continue
        out.append(c); i += 1
    return ''.join(out)


class Tok:
    __slots__ = ('k', 'v', 'line')
    def __init__(self, k, v, line): self.k = k; self.v = v; self.line = line
    def __repr__(self): return '%s:%r' % (self.k, self.v)


def lex(src):
    out = []; i = 0; line = 1; n = len(src)
    while i < n:
        m = TOKRE.match(src, i)
        if not m:
            raise CompileError('linea %d: caracter inesperado %r' % (line, src[i:i + 20]))
        k = m.lastgroup; t = m.group(k)
        if k == 'num':
            if t[:2] in ('0x', '0X'): v = int(t, 16)
            elif re.fullmatch(r'\d+', t): v = int(t)
            else: v = float(t)
            out.append(Tok('num', v, line))
        elif k == 'str':
            out.append(Tok('str', unescape(t[1:-1]), line))
        elif k == 'id':
            out.append(Tok('id', t, line))
        elif k == 'op':
            out.append(Tok('op', t, line))
        line += t.count('\n')
        i = m.end()
    out.append(Tok('eof', None, line))
    return out


# ====================================================================== AST
# Expresiones: tuplas ('tipo', ...). Sentencias: tuplas ('tipo', ...).
BINPREC = {'*': 14, '/': 14, '%': 14, '+': 13, '-': 13, 'add': 13,
           '<<': 12, '>>': 12, '>>>': 12,
           '<': 11, '>': 11, '<=': 11, '>=': 11, 'instanceof': 11, 'lt': 11, 'gt': 11, 'le': 11, 'ge': 11,
           '==': 10, '!=': 10, '===': 10, '!==': 10, 'eq': 10, 'ne': 10,
           '&': 9, '^': 8, '|': 7, '&&': 6, 'and': 6, '||': 5, 'or': 5}
WORDOPS = {'instanceof', 'add', 'lt', 'gt', 'le', 'ge', 'eq', 'ne', 'and', 'or'}
ASSIGNOPS = {'=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>='}
RESERVED = {'break', 'case', 'continue', 'default', 'delete', 'do', 'else', 'for', 'function', 'if',
            'in', 'instanceof', 'new', 'return', 'switch', 'typeof', 'var', 'void', 'while',
            'with', 'try', 'catch', 'finally', 'throw', 'goto'}


class Parser:
    def __init__(self, toks):
        self.t = toks; self.i = 0

    def pk(self, k=0): return self.t[self.i + k]
    def nx(self): x = self.t[self.i]; self.i += 1; return x
    def isop(self, o, k=0): x = self.t[self.i + k]; return x.k == 'op' and x.v == o
    def isid(self, w, k=0): x = self.t[self.i + k]; return x.k == 'id' and x.v == w

    def err(self, msg):
        x = self.pk()
        raise CompileError('linea %d: %s (cerca de %r)' % (x.line, msg, x.v))

    def ex(self, o):
        if not self.isop(o): self.err('se esperaba %r' % o)
        self.i += 1

    def exid(self, w):
        if not self.isid(w): self.err('se esperaba %r' % w)
        self.i += 1

    def ident(self):
        x = self.nx()
        if x.k != 'id': self.i -= 1; self.err('se esperaba un nombre')
        return x.v

    # ------------------------------------------------------------ sentencias
    def program(self):
        out = []
        while self.pk().k != 'eof':
            out.append(self.stmt())
        return out

    def block_or_stmt(self):
        if self.isop('{'):
            self.nx(); b = []
            while not self.isop('}'):
                if self.pk().k == 'eof': self.err('falta }')
                b.append(self.stmt())
            self.nx(); return b
        return [self.stmt()]

    def semi(self):
        if self.isop(';'): self.nx()

    def stmt(self):
        x = self.pk()
        line = x.line
        s = self._stmt()
        return s + (line,) if isinstance(s, tuple) else s

    def _stmt(self):
        x = self.pk()
        if x.k == 'op':
            if x.v == '{':
                return ('block', self.block_or_stmt())
            if x.v == ';':
                self.nx(); return ('empty',)
        if x.k == 'id':
            w = x.v
            # etiqueta  L_123:
            if self.isop(':', 1) and w not in RESERVED and w not in ('default',):
                self.nx(); self.nx(); return ('label', w)
            if w == 'var':
                self.nx(); decls = []
                while True:
                    nm = self.ident(); v = None
                    if self.isop(':'):            # anotacion de tipo AS2  var x:Number
                        self.nx(); self.ident()
                        while self.isop('.'): self.nx(); self.ident()
                    if self.isop('='): self.nx(); v = self.assign()
                    decls.append((nm, v))
                    if self.isop(','): self.nx(); continue
                    break
                self.semi(); return ('var', decls)
            if w == 'if':
                self.nx(); self.ex('('); c = self.expr(); self.ex(')')
                then = self.block_or_stmt(); els = None
                if self.isid('else'):
                    self.nx(); els = self.block_or_stmt()
                return ('if', c, then, els)
            if w == 'while':
                self.nx(); self.ex('('); c = self.expr(); self.ex(')')
                return ('while', c, self.block_or_stmt())
            if w == 'do':
                self.nx(); body = self.block_or_stmt(); self.exid('while')
                self.ex('('); c = self.expr(); self.ex(')'); self.semi()
                return ('dowhile', body, c)
            if w == 'for':
                self.nx(); self.ex('(')
                # for-in
                j = self.i
                isvar = False
                if self.isid('var'): self.nx(); isvar = True
                if self.pk().k == 'id':
                    save = self.i
                    try:
                        lhs = self.postfix()
                        if self.isid('in'):
                            self.nx(); o = self.expr(); self.ex(')')
                            return ('forin', isvar, lhs, o, self.block_or_stmt())
                    except CompileError:
                        pass
                    self.i = save
                self.i = j
                init = None
                if not self.isop(';'):
                    init = self._stmt() if self.isid('var') else ('expr', self.expr())
                    if init[0] == 'var':
                        pass
                    else:
                        self.semi()
                else:
                    self.nx()
                cond = None if self.isop(';') else self.expr(); self.ex(';')
                step = None if self.isop(')') else self.expr(); self.ex(')')
                return ('for', init, cond, step, self.block_or_stmt())
            if w == 'switch':
                self.nx(); self.ex('('); subj = self.expr(); self.ex(')'); self.ex('{')
                cases = []   # [(valor|None si default, [sentencias])]
                while not self.isop('}'):
                    if self.isid('case'):
                        self.nx(); v = self.expr(); self.ex(':'); cases.append([('case', v), []])
                    elif self.isid('default'):
                        self.nx(); self.ex(':'); cases.append([('default',), []])
                    else:
                        if not cases: self.err('sentencia fuera de case')
                        cases[-1][1].append(self.stmt())
                self.nx()
                return ('switch', subj, cases)
            if w == 'break':
                self.nx(); self.semi(); return ('break',)
            if w == 'continue':
                self.nx(); self.semi(); return ('continue',)
            if w == 'return':
                self.nx()
                v = None
                if not self.isop(';') and not self.isop('}'):
                    v = self.expr()
                self.semi(); return ('return', v)
            if w == 'goto':
                self.nx(); nm = self.ident(); self.semi(); return ('goto', nm)
            if w == 'throw':
                self.nx(); v = self.expr(); self.semi(); return ('throw', v)
            if w == 'with':
                self.nx(); self.ex('('); o = self.expr(); self.ex(')')
                return ('with', o, self.block_or_stmt())
            if w == 'try':
                self.nx(); tb = self.block_or_stmt(); cn = None; cb = None; fb = None
                if self.isid('catch'):
                    self.nx(); self.ex('('); cn = self.ident()
                    if self.isop(':'): self.nx(); self.ident()
                    self.ex(')'); cb = self.block_or_stmt()
                if self.isid('finally'):
                    self.nx(); fb = self.block_or_stmt()
                return ('try', tb, cn, cb, fb)
            if w == 'function' and self.pk(1).k == 'id':
                f = self.function()
                return ('fundecl', f)
        # expresion (o  A extends B;  A implements I, J;)
        e = self.expr()
        if self.isid('extends'):
            self.nx(); sup = self.expr(); self.semi(); return ('extends', e, sup)
        if self.isid('implements'):
            self.nx(); ifs = [self.expr()]
            while self.isop(','): self.nx(); ifs.append(self.expr())
            self.semi(); return ('implements', e, ifs)
        self.semi()
        return ('expr', e)

    def function(self):
        self.exid('function')
        nm = ''
        if self.pk().k == 'id': nm = self.nx().v
        self.ex('('); ps = []
        while not self.isop(')'):
            ps.append(self.ident())
            if self.isop(':'):
                self.nx(); self.ident()
                while self.isop('.'): self.nx(); self.ident()
            if self.isop(','): self.nx()
        self.nx()
        if self.isop(':'):
            self.nx(); self.ident()
            while self.isop('.'): self.nx(); self.ident()
        self.ex('{'); body = []
        while not self.isop('}'):
            if self.pk().k == 'eof': self.err('falta } de la funcion')
            body.append(self.stmt())
        self.nx()
        return ('func', nm, ps, body)

    # ------------------------------------------------------------ expresiones
    def expr(self):
        return self.assign()

    def assign(self):
        lhs = self.ternary()
        x = self.pk()
        if x.k == 'op' and x.v in ASSIGNOPS:
            self.nx()
            rhs = self.assign()
            if lhs[0] not in ('name', 'member', 'index', 'prop'):
                self.err('no se puede asignar a esta expresion')
            return ('assign', x.v, lhs, rhs)
        return lhs

    def ternary(self):
        c = self.binary(5)
        if self.isop('?'):
            self.nx(); a = self.assign(); self.ex(':'); b = self.assign()
            return ('cond', c, a, b)
        return c

    def binop_here(self):
        x = self.pk()
        if x.k == 'op' and x.v in BINPREC: return x.v
        if x.k == 'id' and x.v in WORDOPS: return x.v
        return None

    def binary(self, minp):
        a = self.unary()
        while True:
            op = self.binop_here()
            if op is None or BINPREC[op] < minp: return a
            self.nx()
            b = self.binary(BINPREC[op] + 1)
            a = ('bin', op, a, b)

    def unary(self):
        x = self.pk()
        if x.k == 'op':
            if x.v == '!': self.nx(); return ('not', self.unary())
            if x.v == '-':
                self.nx()
                if self.pk().k == 'num':
                    v = self.nx().v
                    return self.postfix_ops(('num', -v if v != 0 else -0.0))
                if self.isid('Infinity'):
                    self.nx(); return ('num', float('-inf'))
                return ('neg', self.unary())
            if x.v == '+': self.nx(); return ('pos', self.unary())
            if x.v == '~': self.nx(); return ('bnot', self.unary())
            if x.v in ('++', '--'):
                self.nx(); t = self.unary(); return ('preinc', 1 if x.v == '++' else -1, t)
        if x.k == 'id':
            if x.v == 'typeof': self.nx(); return ('typeof', self.unary())
            if x.v == 'delete': self.nx(); return ('delete', self.unary())
            if x.v == 'void': self.nx(); return ('void', self.unary())
        return self.postfix()

    def postfix(self):
        e = self.call_member()
        if self.isop('++') or self.isop('--'):
            op = self.nx().v
            return ('postinc', 1 if op == '++' else -1, e)
        return e

    def args(self):
        self.ex('('); a = []
        while not self.isop(')'):
            a.append(self.assign())
            if self.isop(','): self.nx()
            elif not self.isop(')'): self.err('se esperaba , o )')
        self.nx(); return a

    def member_name(self):
        x = self.nx()
        if x.k != 'id': self.i -= 1; self.err('se esperaba un nombre tras el punto')
        return x.v

    def call_member(self):
        if self.isid('new'):
            self.nx()
            # new Objetivo(args): el objetivo es una cadena de miembros sin llamadas
            if self.isid('eval') and self.isop('(', 1):
                self.nx(); tgt = ('evalname', self.args()[0])
            else:
                tgt = self.primary()
            while True:
                if self.isop('.'): self.nx(); tgt = ('member', tgt, self.member_name())
                elif self.isop('['): self.nx(); k = self.expr(); self.ex(']'); tgt = ('index', tgt, k)
                else: break
            a = self.args() if self.isop('(') else []
            e = ('new', tgt, a)
        else:
            e = self.primary()
        return self.postfix_ops(e)

    def postfix_ops(self, e):
        while True:
            if self.isop('.'):
                self.nx(); e = ('member', e, self.member_name())
            elif self.isop('['):
                self.nx(); k = self.expr(); self.ex(']'); e = ('index', e, k)
            elif self.isop('('):
                e = ('call', e, self.args())
            else:
                return e

    def primary(self):
        x = self.nx()
        if x.k == 'num': return ('num', x.v)
        if x.k == 'str': return ('str', x.v)
        if x.k == 'op':
            if x.v == '(':
                e = self.expr(); self.ex(')'); return e
            if x.v == '[':
                items = []
                while not self.isop(']'):
                    items.append(self.assign())
                    if self.isop(','): self.nx()
                self.nx(); return ('array', items)
            if x.v == '{':
                pairs = []
                while not self.isop('}'):
                    k = self.nx()
                    if k.k in ('id', 'str'): key = k.v
                    elif k.k == 'num': key = k.v
                    else: self.i -= 1; self.err('clave de objeto invalida')
                    self.ex(':'); pairs.append((key, self.assign()))
                    if self.isop(','): self.nx()
                self.nx(); return ('object', pairs)
            self.i -= 1; self.err('expresion invalida')
        if x.k == 'id':
            w = x.v
            if w == 'true': return ('bool', True)
            if w == 'false': return ('bool', False)
            if w == 'null': return ('null',)
            if w == 'undefined': return ('undef',)
            if w == 'NaN': return ('num', float('nan'))
            if w == 'Infinity': return ('num', float('inf'))
            if w == 'function':
                self.i -= 1; return self.function()
            if w in RESERVED and w not in ('typeof',):
                self.i -= 1; self.err('palabra reservada inesperada')
            return ('name', w)
        self.i -= 1; self.err('fin inesperado')


# ====================================================================== generacion
PROPS = ['_x', '_y', '_xscale', '_yscale', '_currentframe', '_totalframes', '_alpha', '_visible',
         '_width', '_height', '_rotation', '_target', '_framesloaded', '_name', '_droptarget',
         '_url', '_highquality', '_focusrect', '_soundbuftime', '_quality', '_xmouse', '_ymouse']
PROPIDX = {p: i for i, p in enumerate(PROPS)}
LOCRE = re.compile(r'^_loc(\d+)_$')
SPECIALS = ['this', 'arguments', 'super', '_root', '_parent', '_global']
SPFLAG = {'this': (0x01, 0x02), 'arguments': (0x04, 0x08), 'super': (0x10, 0x20),
          '_root': (0x40, 0), '_parent': (0x80, 0), '_global': (0x100, 0)}

OPS = {'Add2': 0x47, 'Subtract': 0x0B, 'Multiply': 0x0C, 'Divide': 0x0D, 'Modulo': 0x3F,
       'Less2': 0x48, 'Greater': 0x67, 'Equals2': 0x49, 'StrictEquals': 0x66, 'Not': 0x12,
       'BitAnd': 0x60, 'BitOr': 0x61, 'BitXor': 0x62, 'BitLShift': 0x63, 'BitRShift': 0x64,
       'BitURShift': 0x65, 'And': 0x10, 'Or': 0x11, 'StringAdd': 0x21, 'StringEquals': 0x13,
       'StringLess': 0x29, 'StringGreater': 0x68, 'InstanceOf': 0x54, 'GetVariable': 0x1C,
       'SetVariable': 0x1D, 'GetMember': 0x4E, 'SetMember': 0x4F, 'CallFunction': 0x3D,
       'CallMethod': 0x52, 'NewObject': 0x40, 'NewMethod': 0x53, 'InitArray': 0x42,
       'InitObject': 0x43, 'Pop': 0x17, 'Return': 0x3E, 'PushDuplicate': 0x4C, 'TypeOf': 0x44,
       'Increment': 0x50, 'Decrement': 0x51, 'ToInteger': 0x18, 'ToNumber': 0x4A, 'ToString': 0x4B,
       'StringLength': 0x14, 'StringExtract': 0x15, 'CharToAscii': 0x32, 'AsciiToChar': 0x33,
       'RandomNumber': 0x30, 'GetTime': 0x34, 'TargetPath': 0x45, 'CastOp': 0x2B,
       'DefineLocal': 0x3C, 'DefineLocal2': 0x41, 'Delete': 0x3A, 'Delete2': 0x3B,
       'Trace': 0x26, 'GetProperty': 0x22, 'SetProperty': 0x23, 'CloneSprite': 0x24,
       'RemoveSprite': 0x25, 'StartDrag': 0x27, 'EndDrag': 0x28, 'Play': 0x06, 'Stop': 0x07,
       'NextFrame': 0x04, 'PrevFrame': 0x05, 'StopSounds': 0x09, 'ToggleQuality': 0x08,
       'Call': 0x9E, 'SetTarget2': 0x20, 'Extends': 0x69, 'ImplementsOp': 0x2C, 'Throw': 0x2A,
       'Enumerate2': 0x55, 'End': 0x00}
BINOP = {'+': ['Add2'], '-': ['Subtract'], '*': ['Multiply'], '/': ['Divide'], '%': ['Modulo'],
         '<': ['Less2'], '>': ['Greater'], '<=': ['Greater', 'Not'], '>=': ['Less2', 'Not'],
         '==': ['Equals2'], '!=': ['Equals2', 'Not'], '===': ['StrictEquals'],
         '!==': ['StrictEquals', 'Not'], '&': ['BitAnd'], '|': ['BitOr'], '^': ['BitXor'],
         '<<': ['BitLShift'], '>>': ['BitRShift'], '>>>': ['BitURShift'], 'and': ['And'],
         'or': ['Or'], 'add': ['StringAdd'], 'eq': ['StringEquals'], 'ne': ['StringEquals', 'Not'],
         'lt': ['StringLess'], 'gt': ['StringGreater'], 'le': ['StringGreater', 'Not'],
         'ge': ['StringLess', 'Not'], 'instanceof': ['InstanceOf']}
COMPOUND = {'+=': '+', '-=': '-', '*=': '*', '/=': '/', '%=': '%', '&=': '&', '|=': '|',
            '^=': '^', '<<=': '<<', '>>=': '>>', '>>>=': '>>>'}

# funciones globales que son instrucciones propias de AVM1
EXPR_BUILTINS = {'getTimer': (0, 'GetTime'), 'random': (1, 'RandomNumber'), 'int': (1, 'ToInteger'),
                 'Number': (1, 'ToNumber'), 'String': (1, 'ToString'), 'length': (1, 'StringLength'),
                 'substring': (3, 'StringExtract'), 'ord': (1, 'CharToAscii'), 'chr': (1, 'AsciiToChar'),
                 'targetPath': (1, 'TargetPath')}
STMT_BUILTINS = {'trace': (1, 'Trace'), 'play': (0, 'Play'), 'stop': (0, 'Stop'),
                 'nextFrame': (0, 'NextFrame'), 'prevFrame': (0, 'PrevFrame'),
                 'stopAllSounds': (0, 'StopSounds'), 'toggleHighQuality': (0, 'ToggleQuality'),
                 'stopDrag': (0, 'EndDrag'), 'removeMovieClip': (1, 'RemoveSprite'),
                 'call': (1, 'Call'), 'setTarget': (1, None)}


def walk_names(stmts, acc_spec, acc_regs):
    """Recorre sentencias SIN entrar en funciones anidadas y junta los especiales
    (this, super...) y los registros _locN_ usados."""
    def ex(e):
        if not isinstance(e, tuple) or not e: return
        k = e[0]
        if k == 'func': return
        if k == 'object':
            for key, v in e[1]: ex(v)
            return
        if k == 'name':
            if e[1] in SPECIALS: acc_spec.add(e[1])
            m = LOCRE.match(e[1])
            if m: acc_regs.add(int(m.group(1)))
            return
        for y in e[1:]:
            if isinstance(y, tuple): ex(y)
            elif isinstance(y, list):
                for z in y:
                    if isinstance(z, tuple): ex(z)
                    elif isinstance(z, (list,)):
                        for w in z:
                            if isinstance(w, tuple): ex(w)

    def st(s):
        if not isinstance(s, tuple): return
        k = s[0]
        if k == 'fundecl':
            return
        if k == 'var':
            for nm, v in s[1]:
                m = LOCRE.match(nm)
                if m: acc_regs.add(int(m.group(1)))
                if v is not None: ex(v)
            return
        if k == 'forin':
            ex(s[2]); ex(s[3]); [st(x) for x in s[4]]; return
        if k == 'switch':
            ex(s[1])
            for lab, body in s[2]:
                if lab[0] == 'case': ex(lab[1])
                for x in body: st(x)
            return
        if k == 'try':
            [st(x) for x in s[1]]
            if s[2]:
                m = LOCRE.match(s[2])
                if m: acc_regs.add(int(m.group(1)))
            for b in (s[3], s[4]):
                if b: [st(x) for x in b]
            return
        for y in s[1:]:
            if isinstance(y, tuple):
                if y and y[0] in STMT_KINDS: st(y)
                else: ex(y)
            elif isinstance(y, list):
                for z in y:
                    if isinstance(z, tuple) and len(z) and isinstance(z[0], str) and z[0] in STMT_KINDS:
                        st(z)
                    elif isinstance(z, tuple):
                        ex(z)
    for s in stmts: st(s)


STMT_KINDS = {'block', 'empty', 'label', 'var', 'if', 'while', 'dowhile', 'for', 'forin', 'switch',
              'break', 'continue', 'return', 'goto', 'throw', 'with', 'try', 'fundecl', 'extends',
              'implements', 'expr'}


class Scope:
    """Contexto de una funcion (o del script principal)."""
    def __init__(self, is_func, preload=None, locregs=()):
        self.is_func = is_func
        self.preload = preload or {}        # nombre especial -> registro
        self.labels = {}
        self.loops = []                      # pila de (break_label, continue_label|None, es_forin)
        self.forin_depth = 0
        self.locregs = set(locregs)
        self.nlab = 0


class Gen:
    def __init__(self):
        self.lab_counter = 0

    def newlab(self):
        self.lab_counter += 1
        return '@%d' % self.lab_counter

    # ------------------------------------------------------------ helpers
    @staticmethod
    def op(name):
        return ('op', OPS[name])

    def reg_of(self, sc, name):
        m = LOCRE.match(name)
        if m:
            n = int(m.group(1))
            if not sc.is_func and n > 3:
                raise CompileError('%s: fuera de una funcion solo existen los registros 0 a 3' % name)
            if n > 254: raise CompileError('%s: registro fuera de rango' % name)
            return n
        if name in sc.preload:
            return sc.preload[name]
        return None

    # ------------------------------------------------------------ expresiones
    def ce(self, e, sc, out):
        k = e[0]
        if k == 'num': out.append(('push', num_val(e[1]))); return
        if k == 'str': out.append(('push', ('s', e[1]))); return
        if k == 'bool': out.append(('push', ('b', e[1]))); return
        if k == 'null': out.append(('push', ('null',))); return
        if k == 'undef': out.append(('push', ('undef',))); return
        if k == 'name':
            nm = e[1]
            r = self.reg_of(sc, nm)
            if r is not None: out.append(('push', ('r', r))); return
            if nm in PROPIDX:
                out += [('push', ('s', '')), ('push', num_val(PROPIDX[nm])), self.op('GetProperty')]; return
            out += [('push', ('s', nm)), self.op('GetVariable')]; return
        if k == 'member':
            self.ce(e[1], sc, out); out += [('push', ('s', e[2])), self.op('GetMember')]; return
        if k == 'index':
            self.ce(e[1], sc, out); self.ce(e[2], sc, out); out.append(self.op('GetMember')); return
        if k == 'call':
            self.call(e, sc, out); return
        if k == 'new':
            tgt, args = e[1], e[2]
            self.push_args(args, sc, out)
            if tgt[0] == 'name' and self.reg_of(sc, tgt[1]) is None:
                out += [('push', ('s', tgt[1])), self.op('NewObject')]
            elif tgt[0] == 'evalname':
                self.ce(tgt[1], sc, out); out.append(self.op('NewObject'))
            elif tgt[0] == 'member':
                self.ce(tgt[1], sc, out); out += [('push', ('s', tgt[2])), self.op('NewMethod')]
            elif tgt[0] == 'index':
                self.ce(tgt[1], sc, out); self.ce(tgt[2], sc, out); out.append(self.op('NewMethod'))
            else:
                self.ce(tgt, sc, out); out += [('push', ('undef',)), self.op('NewMethod')]
            return
        if k == 'array':
            for it in reversed(e[1]): self.ce(it, sc, out)
            out += [('push', num_val(len(e[1]))), self.op('InitArray')]; return
        if k == 'object':
            for key, v in e[1]:
                out.append(('push', ('s', key) if isinstance(key, str) else num_val(key)))
                self.ce(v, sc, out)
            out += [('push', num_val(len(e[1]))), self.op('InitObject')]; return
        if k == 'func':
            out.append(('func', self.function(e, sc))); return
        if k == 'not':
            self.ce(e[1], sc, out); out.append(self.op('Not')); return
        if k == 'neg':
            out.append(('push', num_val(0))); self.ce(e[1], sc, out); out.append(self.op('Subtract')); return
        if k == 'pos':
            self.ce(e[1], sc, out); out.append(self.op('ToNumber')); return
        if k == 'bnot':
            self.ce(e[1], sc, out); out += [('push', num_val(4294967295)), self.op('BitXor')]; return
        if k == 'typeof':
            self.ce(e[1], sc, out); out.append(self.op('TypeOf')); return
        if k == 'void':
            self.ce(e[1], sc, out); out += [self.op('Pop'), ('push', ('undef',))]; return
        if k == 'delete':
            t = e[1]
            if t[0] == 'member':
                self.ce(t[1], sc, out); out += [('push', ('s', t[2])), self.op('Delete')]
            elif t[0] == 'index':
                self.ce(t[1], sc, out); self.ce(t[2], sc, out); out.append(self.op('Delete'))
            elif t[0] == 'name':
                out += [('push', ('s', t[1])), self.op('Delete2')]
            else:
                self.ce(t, sc, out); out.append(self.op('Delete2'))
            return
        if k == 'bin':
            op, a, b = e[1], e[2], e[3]
            if op in ('&&', '||'):
                L = self.newlab()
                self.ce(a, sc, out); out.append(self.op('PushDuplicate'))
                if op == '&&': out.append(self.op('Not'))
                out += [('if', L), self.op('Pop')]
                self.ce(b, sc, out); out.append(('label', L)); return
            self.ce(a, sc, out); self.ce(b, sc, out)
            out += [self.op(o) for o in BINOP[op]]; return
        if k == 'cond':
            Lt = self.newlab(); Le = self.newlab()
            self.ce(e[1], sc, out); out.append(('if', Lt))
            self.ce(e[3], sc, out); out.append(('jump', Le))
            out.append(('label', Lt)); self.ce(e[2], sc, out); out.append(('label', Le)); return
        if k == 'assign':
            self.assign(e, sc, out, want=True); return
        if k in ('postinc', 'preinc'):
            self.incdec(e, sc, out, want=True); return
        raise CompileError('expresion no soportada: %s' % k)

    def push_args(self, args, sc, out):
        for a in reversed(args): self.ce(a, sc, out)
        out.append(('push', num_val(len(args))))

    def call(self, e, sc, out):
        f, args = e[1], e[2]
        if f[0] == 'name' and f[1] not in SPECIALS and self.reg_of(sc, f[1]) is None:
            nm = f[1]
            if nm in EXPR_BUILTINS and EXPR_BUILTINS[nm][0] == len(args):
                for a in args: self.ce(a, sc, out)
                out.append(self.op(EXPR_BUILTINS[nm][1])); return
            if nm == 'eval' and len(args) == 1:
                self.ce(args[0], sc, out); out.append(self.op('GetVariable')); return
            if nm == 'getProperty' and len(args) == 2:
                self.ce(args[0], sc, out); self.prop_index(args[1], sc, out)
                out.append(self.op('GetProperty')); return
            if nm == '__cast' and len(args) == 2:
                self.ce(args[0], sc, out); self.ce(args[1], sc, out); out.append(self.op('CastOp')); return
            self.push_args(args, sc, out)
            out += [('push', ('s', nm)), self.op('CallFunction')]; return
        # eval(X)(args) -> CallFunction con nombre calculado
        if f[0] == 'call' and f[1][0] == 'name' and f[1][1] == 'eval' and len(f[2]) == 1 \
                and self.reg_of(sc, 'eval') is None:
            self.push_args(args, sc, out); self.ce(f[2][0], sc, out)
            out.append(self.op('CallFunction')); return
        self.push_args(args, sc, out)
        if f[0] == 'member':
            self.ce(f[1], sc, out); out += [('push', ('s', f[2])), self.op('CallMethod')]
        elif f[0] == 'index':
            self.ce(f[1], sc, out); self.ce(f[2], sc, out); out.append(self.op('CallMethod'))
        else:
            self.ce(f, sc, out); out += [('push', ('undef',)), self.op('CallMethod')]

    def prop_index(self, a, sc, out):
        if a[0] == 'name' and a[1] in PROPIDX:
            out.append(('push', num_val(PROPIDX[a[1]])))
        else:
            self.ce(a, sc, out)

    # asignaciones --------------------------------------------------------
    def assign(self, e, sc, out, want):
        op, lhs, rhs = e[1], e[2], e[3]
        if op != '=':
            rhs = ('bin', COMPOUND[op], lhs, rhs)
        self.store(lhs, rhs, sc, out, want)

    def store(self, lhs, rhs, sc, out, want, value_code=None):
        """Guarda rhs (expresion) en lhs. Si want, deja el valor en la pila."""
        def val():
            if value_code is not None: out.extend(value_code)
            else: self.ce(rhs, sc, out)
        if lhs[0] == 'name':
            nm = lhs[1]
            r = self.reg_of(sc, nm)
            if r is not None:
                val(); out.append(('store', r))
                if not want: out.append(self.op('Pop'))
                return
            if nm in PROPIDX:
                out += [('push', ('s', '')), ('push', num_val(PROPIDX[nm]))]
                val()
                if want: out += [('store', 0)]
                out.append(self.op('SetProperty'))
                if want: out.append(('push', ('r', 0)))
                return
            out.append(('push', ('s', nm))); val()
            if want: out.append(('store', 0))
            out.append(self.op('SetVariable'))
            if want: out.append(('push', ('r', 0)))
            return
        if lhs[0] in ('member', 'index'):
            self.ce(lhs[1], sc, out)
            if lhs[0] == 'member': out.append(('push', ('s', lhs[2])))
            else: self.ce(lhs[2], sc, out)
            val()
            if want: out.append(('store', 0))
            out.append(self.op('SetMember'))
            if want: out.append(('push', ('r', 0)))
            return
        raise CompileError('destino de asignacion invalido')

    def incdec(self, e, sc, out, want):
        kind, d, t = e
        opn = 'Increment' if d > 0 else 'Decrement'
        code = []
        self.ce(t, sc, code); code.append(self.op(opn))
        if want and kind == 'postinc':
            self.ce(t, sc, out)          # valor anterior
            self.store(t, None, sc, out, False, value_code=code)
            return
        self.store(t, None, sc, out, want, value_code=code)

    # ------------------------------------------------------------ sentencias
    def cs_list(self, stmts, sc, out):
        for s in stmts: self.cs(s, sc, out)

    def cleanup_forin(self, out):
        L = self.newlab()
        out += [('label', L), ('push', ('null',)), self.op('Equals2'), self.op('Not'), ('if', L)]

    def cs(self, s, sc, out):
        k = s[0]
        try:
            self._cs(s, sc, out)
        except CompileError as ex:
            if not str(ex).startswith('linea'):
                raise CompileError('linea %s: %s' % (s[-1], ex))
            raise

    def _cs(self, s, sc, out):
        k = s[0]
        if k == 'empty': return
        if k == 'block': self.cs_list(s[1], sc, out); return
        if k == 'label':
            out.append(('label', sc.labels.setdefault(s[1], self.newlab()))); return
        if k == 'goto':
            out.append(('jump', sc.labels.setdefault(s[1], self.newlab()))); return
        if k == 'var':
            for nm, v in s[1]:
                r = self.reg_of(sc, nm)
                if r is not None and LOCRE.match(nm):
                    if v is not None:
                        self.ce(v, sc, out); out += [('store', r), self.op('Pop')]
                    continue
                out.append(('push', ('s', nm)))
                if v is None: out.append(self.op('DefineLocal2'))
                else: self.ce(v, sc, out); out.append(self.op('DefineLocal'))
            return
        if k == 'expr':
            self.expr_stmt(s[1], sc, out); return
        if k == 'if':
            c, then, els = s[1], s[2], s[3]
            # if(c) goto L;  ->  c If L
            if els is None and len(then) == 1 and then[0][0] == 'goto':
                self.ce(c, sc, out)
                out.append(('if', sc.labels.setdefault(then[0][1], self.newlab()))); return
            Lelse = self.newlab()
            self.ce(c, sc, out); out += [self.op('Not'), ('if', Lelse)]
            self.cs_list(then, sc, out)
            if els:
                Lend = self.newlab()
                out += [('jump', Lend), ('label', Lelse)]
                self.cs_list(els, sc, out); out.append(('label', Lend))
            else:
                out.append(('label', Lelse))
            return
        if k == 'while':
            H = self.newlab(); E = self.newlab()
            out.append(('label', H)); self.ce(s[1], sc, out); out += [self.op('Not'), ('if', E)]
            sc.loops.append((E, H, False)); self.cs_list(s[2], sc, out); sc.loops.pop()
            out += [('jump', H), ('label', E)]; return
        if k == 'dowhile':
            H = self.newlab(); C = self.newlab(); E = self.newlab()
            out.append(('label', H))
            sc.loops.append((E, C, False)); self.cs_list(s[1], sc, out); sc.loops.pop()
            out.append(('label', C)); self.ce(s[2], sc, out); out += [('if', H), ('label', E)]; return
        if k == 'for':
            init, cond, step, body = s[1], s[2], s[3], s[4]
            if init is not None:
                if init[0] == 'var': self.cs(init + (s[-1],) if len(init) == 2 else init, sc, out)
                else: self.expr_stmt(init[1], sc, out)
            H = self.newlab(); C = self.newlab(); E = self.newlab()
            out.append(('label', H))
            if cond is not None:
                self.ce(cond, sc, out); out += [self.op('Not'), ('if', E)]
            sc.loops.append((E, C, False)); self.cs_list(body, sc, out); sc.loops.pop()
            out.append(('label', C))
            if step is not None: self.expr_stmt(step, sc, out)
            out += [('jump', H), ('label', E)]; return
        if k == 'forin':
            isvar, lhs, o, body = s[1], s[2], s[3], s[4]
            H = self.newlab(); E = self.newlab()
            self.ce(o, sc, out); out.append(self.op('Enumerate2'))
            out += [('label', H), ('store', 0), ('push', ('null',)), self.op('Equals2'), ('if', E)]
            # variable del bucle <- registro 0
            if lhs[0] == 'name' and self.reg_of(sc, lhs[1]) is not None:
                out += [('push', ('r', 0)), ('store', self.reg_of(sc, lhs[1])), self.op('Pop')]
            elif lhs[0] == 'name' and isvar:
                out += [('push', ('s', lhs[1])), ('push', ('r', 0)), self.op('DefineLocal')]
            else:
                self.store(lhs, None, sc, out, False, value_code=[('push', ('r', 0))])
            sc.loops.append((E, H, True)); sc.forin_depth += 1
            self.cs_list(body, sc, out)
            sc.loops.pop(); sc.forin_depth -= 1
            out += [('jump', H), ('label', E)]; return
        if k == 'switch':
            subj, cases = s[1], s[2]
            E = self.newlab()
            labs = [self.newlab() for _ in cases]
            self.ce(subj, sc, out); out.append(('store', 0))
            first = True; dflt = E
            for (lab, body), L in zip(cases, labs):
                if lab[0] == 'default': dflt = L; continue
                if not first: out.append(('push', ('r', 0)))
                self.ce(lab[1], sc, out); out += [self.op('StrictEquals'), ('if', L)]
                first = False
            if first:   # sin ningun case: descartar el sujeto
                out.append(self.op('Pop'))
            out.append(('jump', dflt))
            cont = sc.loops[-1][1] if sc.loops else None
            sc.loops.append((E, cont, False))
            for (lab, body), L in zip(cases, labs):
                out.append(('label', L)); self.cs_list(body, sc, out)
            sc.loops.pop()
            out.append(('label', E)); return
        if k == 'break':
            if not sc.loops: raise CompileError('break fuera de un bucle')
            E, C, isfi = sc.loops[-1]
            if isfi: self.cleanup_forin(out)
            out.append(('jump', E)); return
        if k == 'continue':
            conts = [L for L in reversed(sc.loops) if L[1] is not None]
            if not conts: raise CompileError('continue fuera de un bucle')
            out.append(('jump', conts[0][1])); return
        if k == 'return':
            for _ in range(sc.forin_depth): self.cleanup_forin(out)
            if s[1] is None: out.append(('push', ('undef',)))
            else: self.ce(s[1], sc, out)
            out.append(self.op('Return')); return
        if k == 'throw':
            self.ce(s[1], sc, out); out.append(self.op('Throw')); return
        if k == 'with':
            self.ce(s[1], sc, out)
            body = []; self.cs_list(s[2], sc, body)
            out.append(('with', body)); return
        if k == 'try':
            tb, cn, cb, fb = s[1], s[2], s[3], s[4]
            t = []; self.cs_list(tb, sc, t)
            c = []
            if cb is not None: self.cs_list(cb, sc, c)
            f = []
            if fb is not None: self.cs_list(fb, sc, f)
            creg = self.reg_of(sc, cn) if cn else None
            out.append(('try', cn, creg, cb is not None, fb is not None, t, c, f)); return
        if k == 'fundecl':
            out.append(('func', self.function(s[1], sc))); return
        if k == 'extends':
            self.ce(s[1], sc, out); self.ce(s[2], sc, out); out.append(self.op('Extends')); return
        if k == 'implements':
            for i in reversed(s[2]): self.ce(i, sc, out)
            out.append(('push', num_val(len(s[2])))); self.ce(s[1], sc, out)
            out.append(self.op('ImplementsOp')); return
        raise CompileError('sentencia no soportada: %s' % k)

    def expr_stmt(self, e, sc, out):
        k = e[0]
        if k == 'assign':
            self.assign(e, sc, out, want=False); return
        if k in ('postinc', 'preinc'):
            self.incdec(e, sc, out, want=False); return
        if k == 'call' and e[1][0] == 'name' and e[1][1] not in SPECIALS and self.reg_of(sc, e[1][1]) is None:
            nm, args = e[1][1], e[2]
            if nm in STMT_BUILTINS and STMT_BUILTINS[nm][0] == len(args):
                for a in args: self.ce(a, sc, out)
                if nm == 'setTarget':
                    a = args[0]
                    if a[0] == 'str':
                        del out[-1]
                        out.append(('settarget', a[1]))
                    else:
                        out.append(self.op('SetTarget2'))
                else:
                    out.append(self.op(STMT_BUILTINS[nm][1]))
                return
            if nm == 'set' and len(args) == 2:
                self.ce(args[0], sc, out); self.ce(args[1], sc, out); out.append(self.op('SetVariable')); return
            if nm == 'setProperty' and len(args) == 3:
                self.ce(args[0], sc, out); self.prop_index(args[1], sc, out); self.ce(args[2], sc, out)
                out.append(self.op('SetProperty')); return
            if nm == 'duplicateMovieClip' and len(args) == 3:
                for a in args: self.ce(a, sc, out)
                out.append(self.op('CloneSprite')); return
            if nm == 'startDrag' and len(args) in (2, 6):
                if len(args) == 6:
                    for a in args[2:]: self.ce(a, sc, out)
                    out.append(('push', ('b', True)))
                else:
                    out.append(('push', num_val(0)))
                self.ce(args[1], sc, out); self.ce(args[0], sc, out)
                out.append(self.op('StartDrag')); return
            if nm in ('gotoAndStop', 'gotoAndPlay') and len(args) == 1:
                a = args[0]
                if nm == 'gotoAndStop' and a[0] == 'num' and isinstance(a[1], int) and a[1] >= 1:
                    out.append(('gotoframe', a[1] - 1)); return
                if nm == 'gotoAndStop' and a[0] == 'str':
                    out.append(('gotolabel', a[1])); return
                self.ce(a, sc, out); out.append(('gotoframe2', 1 if nm == 'gotoAndPlay' else 0)); return
            if nm in ('getURL', 'loadMovie', 'loadVariables') and 1 <= len(args) <= 3:
                meth = 0
                if len(args) == 3:
                    m = args[2]
                    if m[0] != 'str' or m[1].upper() not in ('GET', 'POST'):
                        raise CompileError('%s: el metodo debe ser "GET" o "POST"' % nm)
                    meth = 1 if m[1].upper() == 'GET' else 2
                tgt = args[1] if len(args) >= 2 else ('str', '')
                if nm == 'getURL' and meth == 0 and args[0][0] == 'str' and tgt[0] == 'str':
                    out.append(('geturl', args[0][1], tgt[1])); return
                self.ce(args[0], sc, out); self.ce(tgt, sc, out)
                fl = meth | {'getURL': 0, 'loadMovie': 0x40, 'loadVariables': 0x80}[nm]
                out.append(('geturl2', fl)); return
        self.ce(e, sc, out); out.append(self.op('Pop'))

    # ------------------------------------------------------------ funciones
    def function(self, f, parent):
        _, nm, params, body = f
        spec = set(); regs = set()
        walk_names(body, spec, regs)
        # registro 0: temporal de for-in / switch / asignaciones con valor
        preload = {}
        r = 1
        for s in SPECIALS:
            if s in spec:
                preload[s] = r; r += 1
        if any(v in regs for v in preload.values()):
            preload = {}          # choque con un _locN_: todo por nombre
        flags = 0
        for s in SPECIALS:
            pre, sup = SPFLAG[s]
            if s in preload: flags |= pre
            elif not preload and s in spec: pass
            elif s not in spec: flags |= sup
        sc = Scope(True, preload, regs)
        code = []
        self.cs_list(body, sc, code)
        nregs = max([0] + list(regs) + list(preload.values())) + 1
        return dict(name=nm, params=params, flags=flags, nregs=nregs, code=code)


def num_val(v):
    if isinstance(v, bool): return ('b', v)
    if isinstance(v, int) and -2 ** 31 <= v < 2 ** 31:
        return ('i', v)
    if isinstance(v, float) and v == v and v not in (float('inf'), float('-inf')) and v == int(v) \
            and -2 ** 31 <= v < 2 ** 31 and not (v == 0 and str(v).startswith('-')):
        return ('i', int(v))
    return ('d', float(v))


# ====================================================================== ensamblador
def cstr(s):
    return s.encode('utf-8') + b'\0'


class Assembler:
    def __init__(self, pool):
        self.pool = pool
        self.pidx = {s: i for i, s in enumerate(pool)}

    def pushval(self, v):
        k = v[0]
        if k == 's':
            i = self.pidx.get(v[1])
            if i is not None:
                return (b'\x08' + bytes([i])) if i < 256 else (b'\x09' + struct.pack('<H', i))
            return b'\x00' + cstr(v[1])
        if k == 'i': return b'\x07' + struct.pack('<i', v[1])
        if k == 'd':
            d = struct.pack('<d', v[1]); return b'\x06' + d[4:] + d[:4]
        if k == 'b': return b'\x05' + bytes([1 if v[1] else 0])
        if k == 'null': return b'\x02'
        if k == 'undef': return b'\x03'
        if k == 'r': return b'\x04' + bytes([v[1]])
        raise CompileError('valor de push desconocido %r' % (v,))

    def assemble(self, items):
        """items -> bytes (sin End). Resuelve etiquetas y agrupa los Push."""
        # 1) convertir a piezas con tamano fijo
        pieces = []          # (tipo, datos)
        pend = []
        def flush():
            if pend:
                data = b''.join(pend)
                if len(data) > 65535:
                    raise CompileError('Push demasiado largo')
                pieces.append(('raw', b'\x96' + struct.pack('<H', len(data)) + data))
                pend.clear()
        for it in items:
            k = it[0]
            if k == 'push':
                pv = self.pushval(it[1])
                if sum(len(x) for x in pend) + len(pv) > 65000: flush()
                pend.append(pv); continue
            flush()
            if k == 'op':
                pieces.append(('raw', bytes([it[1]])))
            elif k == 'store':
                pieces.append(('raw', b'\x87\x01\x00' + bytes([it[1]])))
            elif k in ('jump', 'if'):
                pieces.append((k, it[1]))
            elif k == 'label':
                pieces.append(('label', it[1]))
            elif k == 'func':
                pieces.append(('raw', self.func(it[1])))
            elif k == 'with':
                body = self.assemble(it[1])
                if len(body) > 65535: raise CompileError('with demasiado largo')
                pieces.append(('raw', b'\x94\x02\x00' + struct.pack('<H', len(body)) + body))
            elif k == 'try':
                _, cn, creg, hasc, hasf, t, c, f = it
                tb = self.assemble(t); cb = self.assemble(c) if hasc else b''; fb = self.assemble(f) if hasf else b''
                fl = (1 if hasc else 0) | (2 if hasf else 0) | (4 if creg is not None else 0)
                name = bytes([creg]) if creg is not None else cstr(cn or '')
                body = bytes([fl]) + struct.pack('<HHH', len(tb), len(cb), len(fb)) + name
                pieces.append(('raw', b'\x8f' + struct.pack('<H', len(body)) + body + tb + cb + fb))
            elif k == 'settarget':
                d = cstr(it[1]); pieces.append(('raw', b'\x8b' + struct.pack('<H', len(d)) + d))
            elif k == 'gotoframe':
                pieces.append(('raw', b'\x81\x02\x00' + struct.pack('<H', it[1])))
            elif k == 'gotolabel':
                d = cstr(it[1]); pieces.append(('raw', b'\x8c' + struct.pack('<H', len(d)) + d))
            elif k == 'gotoframe2':
                pieces.append(('raw', b'\x9f\x01\x00' + bytes([it[1]])))
            elif k == 'geturl':
                d = cstr(it[1]) + cstr(it[2]); pieces.append(('raw', b'\x83' + struct.pack('<H', len(d)) + d))
            elif k == 'geturl2':
                pieces.append(('raw', b'\x9a\x01\x00' + bytes([it[1]])))
            else:
                raise CompileError('pieza desconocida %r' % (k,))
        flush()
        # 2) posiciones
        pos = {}; p = 0
        for k, d in pieces:
            if k == 'label': pos[d] = p
            elif k in ('jump', 'if'): p += 5
            else: p += len(d)
        # 3) emitir
        out = bytearray(); p = 0
        for k, d in pieces:
            if k == 'label': continue
            if k in ('jump', 'if'):
                if d not in pos: raise CompileError('etiqueta sin definir: %s' % d)
                off = pos[d] - (p + 5)
                if not -32768 <= off <= 32767:
                    raise CompileError('salto demasiado largo (%d bytes); divide la funcion' % off)
                out += (b'\x99' if k == 'jump' else b'\x9d') + b'\x02\x00' + struct.pack('<h', off)
                p += 5
            else:
                out += d; p += len(d)
        return bytes(out)

    def func(self, f):
        body = self.assemble(f['code'])
        if len(body) > 65535:
            raise CompileError('funcion %r demasiado grande (%d bytes)' % (f['name'], len(body)))
        hdr = cstr(f['name']) + struct.pack('<H', len(f['params'])) + bytes([min(255, f['nregs'])])
        hdr += struct.pack('<H', f['flags'])
        for p in f['params']:
            hdr += b'\x00' + cstr(p)
        hdr += struct.pack('<H', len(body))
        return b'\x8e' + struct.pack('<H', len(hdr)) + hdr + body


def collect_strings(items, acc):
    for it in items:
        k = it[0]
        if k == 'push' and it[1][0] == 's':
            acc[it[1][1]] = acc.get(it[1][1], 0) + 1
        elif k == 'func':
            collect_strings(it[1]['code'], acc)
        elif k == 'with':
            collect_strings(it[1], acc)
        elif k == 'try':
            for b in it[5:8]: collect_strings(b, acc)


def build_pool(items):
    acc = {}
    collect_strings(items, acc)
    # ahorro por entrada: (largo+2 inline) - (2 o 3 por referencia)
    cand = sorted(acc.items(), key=lambda kv: -(kv[1] * (len(kv[0].encode('utf-8')) + 2)))
    pool = []; size = 2
    for s, n in cand:
        b = len(s.encode('utf-8')) + 1
        if n < 2 and b < 3: continue
        if size + b > 65535 or len(pool) >= 65535: continue
        pool.append(s); size += b
    # los mas usados primero para que usen indice de 1 byte
    pool.sort(key=lambda s: -acc[s])
    return pool


def compile_script(src, end=True):
    """Texto AS2 -> bytecode AVM1 (con ConstantPool y End)."""
    toks = lex(src)
    ast = Parser(toks).program()
    g = Gen()
    sc = Scope(False)
    items = []
    g.cs_list(ast, sc, items)
    pool = build_pool(items)
    asm = Assembler(pool)
    code = asm.assemble(items)
    head = b''
    if pool:
        d = struct.pack('<H', len(pool)) + b''.join(cstr(s) for s in pool)
        head = b'\x88' + struct.pack('<H', len(d)) + d
    return head + code + (b'\x00' if end else b'')


if __name__ == '__main__':
    import sys
    src = open(sys.argv[1], encoding='utf-8').read()
    b = compile_script(src)
    out = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].rsplit('.', 1)[0] + '.bin'
    open(out, 'wb').write(b)
    print('%s: %d bytes' % (out, len(b)))
