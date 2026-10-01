# Paso 2 — lectura de formas SWF (DefineShape 1-4, DefineMorphShape 1-2,
# glifos de DefineFont3) y conversion a SVG.
import struct


class Bits:
    """Lector de bits y valores alineados, big-endian en bits como el SWF."""
    def __init__(self, b, pos=0):
        self.b = b; self.p = pos; self.bit = 0

    def align(self):
        if self.bit:
            self.bit = 0; self.p += 1

    def ub(self, n):
        v = 0
        for _ in range(n):
            v = (v << 1) | ((self.b[self.p] >> (7 - self.bit)) & 1)
            self.bit += 1
            if self.bit == 8:
                self.bit = 0; self.p += 1
        return v

    def sb(self, n):
        if n == 0: return 0
        v = self.ub(n)
        if v & (1 << (n - 1)): v -= 1 << n
        return v

    def fb(self, n):
        return self.sb(n) / 65536.0

    def u8(self):
        self.align(); v = self.b[self.p]; self.p += 1; return v

    def u16(self):
        self.align(); v = struct.unpack_from('<H', self.b, self.p)[0]; self.p += 2; return v

    def s16(self):
        self.align(); v = struct.unpack_from('<h', self.b, self.p)[0]; self.p += 2; return v

    def u32(self):
        self.align(); v = struct.unpack_from('<I', self.b, self.p)[0]; self.p += 4; return v

    def rect(self):
        self.align()
        n = self.ub(5)
        r = (self.sb(n), self.sb(n), self.sb(n), self.sb(n))
        self.align()
        return r   # xmin, xmax, ymin, ymax (twips)

    def matrix(self):
        self.align()
        a = d = 1.0; b = c = 0.0
        if self.ub(1):
            n = self.ub(5); a = self.fb(n); d = self.fb(n)
        if self.ub(1):
            n = self.ub(5); b = self.fb(n); c = self.fb(n)
        n = self.ub(5)
        tx = self.sb(n); ty = self.sb(n)
        self.align()
        return (a, b, c, d, tx, ty)

    def rgb(self):
        self.align(); r, g, bl = self.b[self.p:self.p + 3]; self.p += 3
        return (r, g, bl, 255)

    def rgba(self):
        self.align(); r, g, bl, a = self.b[self.p:self.p + 4]; self.p += 4
        return (r, g, bl, a)


# ------------------------------------------------------------------ estilos
def read_gradient(r, ver, focal=False):
    r.align()
    spread = r.ub(2); interp = r.ub(2); n = r.ub(4)
    stops = []
    for _ in range(n):
        ratio = r.u8()
        col = r.rgba() if ver >= 3 else r.rgb()
        stops.append((ratio, col))
    fp = 0.0
    if focal:
        fp = r.s16() / 256.0
    return dict(spread=spread, interp=interp, stops=stops, focal=fp)


def read_fill(r, ver):
    t = r.u8()
    f = {'type': t}
    if t == 0x00:
        f['color'] = r.rgba() if ver >= 3 else r.rgb()
    elif t in (0x10, 0x12, 0x13):
        f['matrix'] = r.matrix()
        f['grad'] = read_gradient(r, ver, focal=(t == 0x13))
    elif t in (0x40, 0x41, 0x42, 0x43):
        f['bitmap'] = r.u16()
        f['matrix'] = r.matrix()
    return f


def read_fills(r, ver):
    n = r.u8()
    if n == 0xFF and ver >= 2:
        n = r.u16()
    return [read_fill(r, ver) for _ in range(n)]


def read_lines(r, ver):
    n = r.u8()
    if n == 0xFF and ver >= 2:
        n = r.u16()
    out = []
    for _ in range(n):
        w = r.u16()
        if ver >= 4:
            start_cap = r.ub(2); join = r.ub(2); has_fill = r.ub(1)
            r.ub(1); r.ub(1); r.ub(1); r.ub(5); r.ub(1)
            end_cap = r.ub(2)
            r.align()
            if join == 2: r.u16()
            if has_fill:
                fill = read_fill(r, ver)
                col = fill.get('color', (0, 0, 0, 255))
            else:
                col = r.rgba()
            out.append(dict(width=w, color=col, cap=start_cap, join=join))
        else:
            col = r.rgba() if ver >= 3 else r.rgb()
            out.append(dict(width=w, color=col, cap=0, join=0))
    return out


# ------------------------------------------------------------------ bordes
def read_records(r, ver, fills, lines):
    """Devuelve una lista de grupos; cada grupo = (fills, lines, bordes).
    Un borde = (x0, y0, cx, cy, x1, y1, f0, f1, ln); cx None si es recto."""
    r.align()
    nfb = r.ub(4); nlb = r.ub(4)
    groups = []
    edges = []
    x = y = 0
    f0 = f1 = ln = 0
    while True:
        if r.ub(1) == 0:
            new_styles = r.ub(1); ls = r.ub(1); fs1 = r.ub(1); fs0 = r.ub(1); mv = r.ub(1)
            if not (new_styles or ls or fs1 or fs0 or mv):
                break
            if mv:
                n = r.ub(5); x = r.sb(n); y = r.sb(n)
            if fs0: f0 = r.ub(nfb)
            if fs1: f1 = r.ub(nfb)
            if ls: ln = r.ub(nlb)
            if new_styles:
                groups.append((fills, lines, edges))
                edges = []
                fills = read_fills(r, ver)
                lines = read_lines(r, ver)
                r.align()
                nfb = r.ub(4); nlb = r.ub(4)
                f0 = f1 = ln = 0
        else:
            if r.ub(1):          # recto
                n = r.ub(4) + 2
                if r.ub(1):
                    dx = r.sb(n); dy = r.sb(n)
                else:
                    if r.ub(1):
                        dx = 0; dy = r.sb(n)
                    else:
                        dx = r.sb(n); dy = 0
                edges.append((x, y, None, None, x + dx, y + dy, f0, f1, ln))
                x += dx; y += dy
            else:                # curva cuadratica
                n = r.ub(4) + 2
                cdx = r.sb(n); cdy = r.sb(n); adx = r.sb(n); ady = r.sb(n)
                cx, cy = x + cdx, y + cdy
                nx, ny = cx + adx, cy + ady
                edges.append((x, y, cx, cy, nx, ny, f0, f1, ln))
                x, y = nx, ny
    groups.append((fills, lines, edges))
    return groups


def parse_shape(body, code):
    ver = {2: 1, 22: 2, 32: 3, 83: 4}[code]
    r = Bits(body, 2)
    bounds = r.rect()
    if ver == 4:
        r.rect(); r.align(); r.u8()
    fills = read_fills(r, ver)
    lines = read_lines(r, ver)
    return bounds, read_records(r, ver, fills, lines), ver


def parse_morph(body, code):
    """Devuelve (bounds_inicio, grupos_inicio, bounds_fin, grupos_fin)."""
    r = Bits(body, 2)
    b0 = r.rect(); b1 = r.rect()
    if code == 84:
        r.rect(); r.rect(); r.align(); r.u8()
    r.u32()
    n = r.u8()
    if n == 0xFF: n = r.u16()
    f0s, f1s = [], []
    for _ in range(n):
        t = r.u8()
        a = {'type': t}; bb = {'type': t}
        if t == 0x00:
            a['color'] = r.rgba(); bb['color'] = r.rgba()
        elif t in (0x10, 0x12, 0x13):
            a['matrix'] = r.matrix(); bb['matrix'] = r.matrix()
            m = r.u8() & 15
            sa, sb2 = [], []
            for _ in range(m):
                sa.append((r.u8(), r.rgba())); sb2.append((r.u8(), r.rgba()))
            a['grad'] = dict(spread=0, interp=0, stops=sa, focal=0)
            bb['grad'] = dict(spread=0, interp=0, stops=sb2, focal=0)
            if t == 0x13:
                r.s16(); r.s16()
        elif t in (0x40, 0x41, 0x42, 0x43):
            bid = r.u16()
            a['bitmap'] = bid; bb['bitmap'] = bid
            a['matrix'] = r.matrix(); bb['matrix'] = r.matrix()
        f0s.append(a); f1s.append(bb)
    n = r.u8()
    if n == 0xFF: n = r.u16()
    l0s, l1s = [], []
    for _ in range(n):
        if code == 84:
            w0 = r.u16(); w1 = r.u16()
            r.ub(2); join = r.ub(2); hf = r.ub(1); r.ub(11)
            r.align()
            if join == 2: r.u16()
            if hf:
                t = r.u8()
                c0 = c1 = (0, 0, 0, 255)
                if t == 0:
                    c0 = r.rgba(); c1 = r.rgba()
            else:
                c0 = r.rgba(); c1 = r.rgba()
        else:
            w0 = r.u16(); w1 = r.u16(); c0 = r.rgba(); c1 = r.rgba()
        l0s.append(dict(width=w0, color=c0, cap=0, join=0))
        l1s.append(dict(width=w1, color=c1, cap=0, join=0))
    g0 = read_records(r, 3, f0s, l0s)
    return b0, g0, b1, f1s, l1s


# ------------------------------------------------------------------ SVG
def _col(c):
    return '#%02x%02x%02x' % c[:3], c[3] / 255.0


def _pt(v):
    s = ('%.2f' % (v / 20.0)).rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def _chain(segs):
    """Une segmentos (x0,y0,cx,cy,x1,y1) en subtrazados cerrados/abiertos."""
    by_start = {}
    for i, s in enumerate(segs):
        by_start.setdefault((s[0], s[1]), []).append(i)
    used = [False] * len(segs)
    paths = []
    for i in range(len(segs)):
        if used[i]: continue
        used[i] = True
        cur = [segs[i]]
        start = (segs[i][0], segs[i][1])
        end = (segs[i][4], segs[i][5])
        while end != start:
            nxt = None
            for j in by_start.get(end, ()):
                if not used[j]:
                    nxt = j; break
            if nxt is None: break
            used[nxt] = True
            cur.append(segs[nxt])
            end = (segs[nxt][4], segs[nxt][5])
        paths.append(cur)
    return paths


def _d(paths, close):
    out = []
    for p in paths:
        out.append('M%s %s' % (_pt(p[0][0]), _pt(p[0][1])))
        for s in p:
            if s[2] is None:
                out.append('L%s %s' % (_pt(s[4]), _pt(s[5])))
            else:
                out.append('Q%s %s %s %s' % (_pt(s[2]), _pt(s[3]), _pt(s[4]), _pt(s[5])))
        if close: out.append('Z')
    return ''.join(out)


class SvgCtx:
    def __init__(self, bitmap_href):
        self.defs = []
        self.n = 0
        self.bitmap_href = bitmap_href   # funcion id -> (href, w, h) o None

    def paint(self, f):
        t = f['type']
        if t == 0x00:
            c, a = _col(f['color'])
            return 'fill="%s"%s' % (c, '' if a >= 1 else ' fill-opacity="%.3f"' % a)
        if t in (0x10, 0x12, 0x13):
            self.n += 1
            gid = 'g%d' % self.n
            a, b, c, d, tx, ty = f['matrix']
            tr = 'matrix(%.5f %.5f %.5f %.5f %s %s)' % (a, b, c, d, _pt(tx), _pt(ty))
            spread = ['pad', 'reflect', 'repeat', 'pad'][f['grad']['spread']]
            stops = ''.join('<stop offset="%.4f" stop-color="%s"%s/>' % (
                r / 255.0, _col(col)[0],
                '' if col[3] == 255 else ' stop-opacity="%.3f"' % (col[3] / 255.0))
                for r, col in f['grad']['stops'])
            if t == 0x10:
                self.defs.append('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="-819.2" x2="819.2" y1="0" y2="0" spreadMethod="%s" gradientTransform="%s">%s</linearGradient>' % (gid, spread, tr, stops))
            else:
                fx = 819.2 * f['grad'].get('focal', 0)
                self.defs.append('<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="819.2" fx="%.2f" fy="0" spreadMethod="%s" gradientTransform="%s">%s</radialGradient>' % (gid, fx, spread, tr, stops))
            return 'fill="url(#%s)"' % gid
        if t in (0x40, 0x41, 0x42, 0x43):
            info = self.bitmap_href(f['bitmap']) if self.bitmap_href else None
            if not info:
                return 'fill="none"'
            href, w, h = info
            self.n += 1
            pid = 'p%d' % self.n
            a, b, c, d, tx, ty = f['matrix']
            tr = 'matrix(%.5f %.5f %.5f %.5f %s %s)' % (a / 20, b / 20, c / 20, d / 20, _pt(tx), _pt(ty))
            self.defs.append('<pattern id="%s" patternUnits="userSpaceOnUse" width="%d" height="%d" patternTransform="%s"><image href="%s" width="%d" height="%d"/></pattern>' % (pid, w, h, tr, href, w, h))
            return 'fill="url(#%s)"' % pid
        return 'fill="none"'


def groups_to_svg_body(groups, ctx):
    parts = []
    for fills, lines, edges in groups:
        per_fill = {}
        per_line = {}
        for e in edges:
            x0, y0, cx, cy, x1, y1, f0, f1, ln = e
            if f1:
                per_fill.setdefault(f1, []).append((x0, y0, cx, cy, x1, y1))
            if f0:
                per_fill.setdefault(f0, []).append((x1, y1, cx, cy, x0, y0))
            if ln:
                per_line.setdefault(ln, []).append((x0, y0, cx, cy, x1, y1))
        for fi in sorted(per_fill):
            if fi - 1 >= len(fills): continue
            paint = ctx.paint(fills[fi - 1])
            d = _d(_chain(per_fill[fi]), True)
            parts.append('<path %s fill-rule="evenodd" d="%s"/>' % (paint, d))
        for li in sorted(per_line):
            if li - 1 >= len(lines): continue
            L = lines[li - 1]
            c, a = _col(L['color'])
            w = max(L['width'] / 20.0, 0.05)
            cap = ['round', 'butt', 'square'][min(L.get('cap', 0), 2)]
            join = ['round', 'bevel', 'miter'][min(L.get('join', 0), 2)]
            d = _d(_chain(per_line[li]), False)
            parts.append('<path fill="none" stroke="%s"%s stroke-width="%.2f" stroke-linecap="%s" stroke-linejoin="%s" d="%s"/>' % (
                c, '' if a >= 1 else ' stroke-opacity="%.3f"' % a, w, cap, join, d))
    return ''.join(parts)


def to_svg(bounds, groups, bitmap_href=None):
    xmin, xmax, ymin, ymax = bounds
    w = max((xmax - xmin) / 20.0, 1); h = max((ymax - ymin) / 20.0, 1)
    ctx = SvgCtx(bitmap_href)
    body = groups_to_svg_body(groups, ctx)
    defs = '<defs>%s</defs>' % ''.join(ctx.defs) if ctx.defs else ''
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'viewBox="%s %s %.2f %.2f" width="%.2f" height="%.2f">%s%s</svg>'
            % (_pt(xmin), _pt(ymin), w, h, w, h, defs, body))
