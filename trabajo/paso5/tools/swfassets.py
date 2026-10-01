# Paso 2 — extrae los recursos de la carpeta del Paso 1 a formatos abiertos.
#
# Uso:  python3 swfassets.py CARPETA_PASO1 CARPETA_SALIDA
#
#   images/  PNG (sin perdida y JPEG con alfa) y JPG (tal cual venian)
#   sounds/  MP3 de efectos y musica (DefineSound)
#   streams/ MP3 de sonido en flujo de cada sprite (SoundStreamBlock)
#   shapes/  SVG de cada DefineShape
#   morphs/  SVG del estado inicial y final de cada DefineMorphShape
#   fonts/   TTF reconstruido de cada DefineFont3 con glifos + JSON del mapa
#   texts/   textos.json con cada DefineEditText y DefineText
#   index.html  galeria navegable de todo lo anterior
#   report.json recuento, fallos y verificacion
import sys, os, json, struct, zlib, io, hashlib, re, html
sys.path.insert(0, os.path.dirname(__file__))
from swfsplit import read_tags
from swfshape import Bits, parse_shape, parse_morph, to_svg, read_records

try:
    from PIL import Image
except ImportError:
    Image = None


def safe(s):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', s)[:60]


def cstr(b, i):
    j = b.index(b'\0', i)
    return b[i:j].decode('latin1'), j + 1


class Extractor:
    def __init__(self, p1, out):
        self.p1 = p1; self.out = out
        self.m = json.load(open(os.path.join(p1, 'manifest.json')))
        self.sy = json.load(open(os.path.join(p1, 'symbols.json')))
        self.rep = {'images': [], 'sounds': [], 'streams': [], 'shapes': [],
                    'morphs': [], 'fonts': [], 'texts': 0, 'errors': []}
        self.bitmaps = {}      # id -> (ruta relativa desde shapes/, w, h)
        self.fonts = {}        # id -> dict(name, codes, ...)
        self.jpeg_tables = b''
        for d in ('images', 'sounds', 'streams', 'shapes', 'morphs', 'fonts', 'texts'):
            os.makedirs(os.path.join(out, d), exist_ok=True)

    def body(self, t):
        return open(os.path.join(self.p1, 'tags', t['file']), 'rb').read()

    def label(self, cid):
        e = self.sy.get(str(cid), {}).get('exports') or []
        return '%d%s' % (cid, ('_' + safe(e[0])) if e else '')

    def err(self, what, cid, e):
        self.rep['errors'].append('%s %s: %s' % (what, cid, e))

    # ------------------------------------------------------------ imagenes
    @staticmethod
    def _strip_jpeg(data):
        # algunos SWF antiguos anteponen FFD9FFD8 al JPEG
        if data[:4] == b'\xff\xd9\xff\xd8':
            data = data[4:]
        return data

    def image(self, t):
        b = self.body(t); code = t['code']; cid = t['id']
        name = self.label(cid)
        try:
            if code in (20, 36):
                fmt = b[2]; w, h = struct.unpack_from('<HH', b, 3)
                if fmt == 3:
                    ncol = b[7] + 1
                    raw = zlib.decompress(b[8:])
                    csz = 4 if code == 36 else 3
                    pal = raw[:ncol * csz]
                    stride = (w + 3) & ~3
                    px = raw[ncol * csz:]
                    img = Image.new('RGBA', (w, h))
                    data = []
                    for y in range(h):
                        for x in range(w):
                            k = px[y * stride + x]
                            c = pal[k * csz:(k + 1) * csz]
                            data.append((c[0], c[1], c[2], c[3] if csz == 4 else 255))
                    img.putdata(data)
                elif fmt == 5:
                    raw = zlib.decompress(b[7:])
                    import numpy as np
                    a = np.frombuffer(raw[:w * h * 4], dtype=np.uint8).reshape(-1, 4).astype(np.uint32)
                    A, R, G, B = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
                    if code == 36:
                        # color premultiplicado por alfa: se deshace
                        m = (A > 0) & (A < 255)
                        for ch in (R, G, B):
                            ch[m] = np.minimum(255, ch[m] * 255 // A[m])
                    else:
                        A = np.full_like(A, 255)
                    out = np.stack([R, G, B, A], axis=1).astype(np.uint8).tobytes()
                    img = Image.frombytes('RGBA', (w, h), bytes(out))
                else:
                    raise ValueError('formato sin perdida %d' % fmt)
                fn = name + '.png'
                img.save(os.path.join(self.out, 'images', fn))
            elif code in (21, 6):
                data = self._strip_jpeg(b[2:])
                if code == 6:
                    data = self._strip_jpeg(self.jpeg_tables)[:-2] + data[2:]
                if data[:8] == b'\x89PNG\r\n\x1a\n':
                    ext = '.png'
                elif data[:3] == b'GIF':
                    ext = '.gif'
                else:
                    ext = '.jpg'
                fn = name + ext
                open(os.path.join(self.out, 'images', fn), 'wb').write(data)
                img = Image.open(io.BytesIO(data)); img.load()
                w, h = img.size
            elif code in (35, 90):
                off = struct.unpack_from('<I', b, 2)[0]
                p = 6 if code == 35 else 8
                data = self._strip_jpeg(b[p:p + off])
                img = Image.open(io.BytesIO(data)).convert('RGBA'); img.load()
                w, h = img.size
                if data[:3] != b'\xff\xd8\xff' and data[:4] != b'\xff\xd8\xff\xe0':
                    pass
                alpha = zlib.decompress(b[p + off:]) if len(b) > p + off else b''
                if len(alpha) >= w * h:
                    img.putalpha(Image.frombytes('L', (w, h), alpha[:w * h]))
                fn = name + '.png'
                img.save(os.path.join(self.out, 'images', fn))
            else:
                return
            self.bitmaps[cid] = ('../images/' + fn, w, h)
            self.rep['images'].append(dict(id=cid, file='images/' + fn, w=w, h=h))
        except Exception as e:
            self.err('imagen', cid, e)

    # ------------------------------------------------------------ sonidos
    def sound(self, t):
        b = self.body(t); cid = t['id']
        try:
            f = b[2]
            fmt = f >> 4
            rate = [5512, 11025, 22050, 44100][(f >> 2) & 3]
            stereo = bool(f & 1)
            samples = struct.unpack_from('<I', b, 3)[0]
            name = self.label(cid)
            if fmt == 2:
                data = b[9:]          # 7 de cabecera + SeekSamples
                fn = name + '.mp3'
            elif fmt in (0, 3):
                pcm = b[7:]
                bits = 16 if f & 2 else 8
                ch = 2 if stereo else 1
                fn = name + '.wav'
                hdr = b'RIFF' + struct.pack('<I', 36 + len(pcm)) + b'WAVEfmt ' + struct.pack(
                    '<IHHIIHH', 16, 1, ch, rate, rate * ch * bits // 8, ch * bits // 8, bits) + b'data' + struct.pack('<I', len(pcm))
                data = hdr + pcm
            else:
                fn = name + '.fmt%d.bin' % fmt
                data = b[7:]
            open(os.path.join(self.out, 'sounds', fn), 'wb').write(data)
            self.rep['sounds'].append(dict(id=cid, file='sounds/' + fn, format=fmt, rate=rate,
                                           stereo=stereo, seconds=round(samples / float(rate), 2)))
        except Exception as e:
            self.err('sonido', cid, e)

    def streams_of(self, where, tags_iter, get):
        """Concatena el MP3 en flujo de una linea de tiempo."""
        fmt = None; chunks = []
        for c, lh, o, l in tags_iter:
            if c in (18, 45):
                fmt = get[o + 1] >> 4
            elif c == 19 and fmt == 2:
                chunks.append(get[o + 4:o + l])
        if chunks:
            fn = safe(where) + '.mp3'
            open(os.path.join(self.out, 'streams', fn), 'wb').write(b''.join(chunks))
            self.rep['streams'].append(dict(timeline=where, file='streams/' + fn,
                                            blocks=len(chunks)))

    # ------------------------------------------------------------ formas
    def shape(self, t):
        b = self.body(t); cid = t['id']
        try:
            bounds, groups, ver = parse_shape(b, t['code'])
            svg = to_svg(bounds, groups, self.bitmaps.get)
            fn = self.label(cid) + '.svg'
            open(os.path.join(self.out, 'shapes', fn), 'w').write(svg)
            self.rep['shapes'].append(dict(id=cid, file='shapes/' + fn, version=ver))
        except Exception as e:
            self.err('forma', cid, e)

    def morph(self, t):
        b = self.body(t); cid = t['id']
        try:
            b0, g0, b1, f1s, l1s = parse_morph(b, t['code'])
            # estado final: mismas aristas con los estilos finales
            g1 = [(f1s, l1s, g0[0][2])] + g0[1:]
            for tag, bounds, groups in (('inicio', b0, g0), ('fin', b1, g1)):
                fn = '%s_%s.svg' % (self.label(cid), tag)
                open(os.path.join(self.out, 'morphs', fn), 'w').write(
                    to_svg(bounds, groups, self.bitmaps.get))
            self.rep['morphs'].append(dict(id=cid, file='morphs/%s_inicio.svg' % self.label(cid)))
        except Exception as e:
            self.err('morph', cid, e)

    # ------------------------------------------------------------ fuentes
    def font(self, t):
        b = self.body(t); cid = t['id']
        try:
            flags = b[2]
            wide_off = bool(flags & 0x08); wide_codes = bool(flags & 0x04)
            has_layout = bool(flags & 0x80)
            nl = b[4]
            name = b[5:5 + nl].split(b'\0')[0].decode('latin1')
            p = 5 + nl
            ng = struct.unpack_from('<H', b, p)[0]; p += 2
            base = p
            osz = 4 if wide_off else 2
            offs = [struct.unpack_from('<I' if wide_off else '<H', b, p + i * osz)[0] for i in range(ng)]
            code_off = struct.unpack_from('<I' if wide_off else '<H', b, p + ng * osz)[0] if ng else 0
            glyphs = []
            for i in range(ng):
                s = base + offs[i]
                r = Bits(b, s)
                groups = read_records(r, 1, [{'type': 0, 'color': (0, 0, 0, 255)}], [])
                glyphs.append(groups[0][2])
            q = base + code_off
            codes = []
            for i in range(ng):
                if wide_codes:
                    codes.append(struct.unpack_from('<H', b, q)[0]); q += 2
                else:
                    codes.append(b[q]); q += 1
            adv = [1024 * 20] * ng
            ascent = descent = None
            if has_layout and ng:
                ascent, descent, leading = struct.unpack_from('<hhh', b, q); q += 6
                adv = list(struct.unpack_from('<%dh' % ng, b, q))
            self.fonts[cid] = dict(name=name, codes=codes, glyphs=glyphs, adv=adv)
            info = dict(id=cid, name=name, glyphs=ng,
                        chars=''.join(chr(c) for c in codes if 32 <= c < 0x10000))
            if ng:
                fn = '%d_%s.ttf' % (cid, safe(name))
                self._ttf(os.path.join(self.out, 'fonts', fn), name, codes, glyphs, adv,
                          ascent, descent)
                info['file'] = 'fonts/' + fn
            self.rep['fonts'].append(info)
        except Exception as e:
            self.err('fuente', cid, e)

    def _ttf(self, path, name, codes, glyphs, adv, ascent, descent):
        from fontTools.fontBuilder import FontBuilder
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        S = 20.0   # DefineFont3: 20480 unidades por EM -> 1024
        order = ['.notdef'] + ['g%d' % i for i in range(len(glyphs))]
        fb = FontBuilder(1024, isTTF=True)
        fb.setupGlyphOrder(order)
        cmap = {}
        for i, c in enumerate(codes):
            if c not in cmap: cmap[c] = 'g%d' % i
        fb.setupCharacterMap(cmap)
        gl = {}
        pen = TTGlyphPen(None); gl['.notdef'] = pen.glyph()
        metrics = {'.notdef': (512, 0)}
        for i, edges in enumerate(glyphs):
            pen = TTGlyphPen(None)
            # contornos: cadenas de aristas en orden de registro
            cur = None
            for x0, y0, cx, cy, x1, y1, f0, f1, ln in edges:
                if cur != (x0, y0):
                    if cur is not None: pen.closePath()
                    pen.moveTo((round(x0 / S), round(-y0 / S)))
                if cx is None:
                    pen.lineTo((round(x1 / S), round(-y1 / S)))
                else:
                    pen.qCurveTo((round(cx / S), round(-cy / S)), (round(x1 / S), round(-y1 / S)))
                cur = (x1, y1)
            if cur is not None: pen.closePath()
            try:
                g = pen.glyph()
            except Exception:
                g = TTGlyphPen(None).glyph()
            gl['g%d' % i] = g
            metrics['g%d' % i] = (max(0, round(adv[i] / S)), 0)
        fb.setupGlyf(gl)
        fb.setupHorizontalMetrics(metrics)
        # hay fuentes con metricas negativas o vacias: se normalizan
        asc = abs(round(ascent / S)) if ascent else 900
        dsc = abs(round(descent / S)) if descent else 250
        if asc == 0: asc = 900
        if dsc == 0: dsc = 250
        fb.setupHorizontalHeader(ascent=asc, descent=-dsc)
        fb.setupNameTable({'familyName': name or 'SonnyFont', 'styleName': 'Regular'})
        fb.setupOS2(sTypoAscender=asc, sTypoDescender=-dsc, usWinAscent=asc, usWinDescent=dsc)
        fb.setupPost()
        fb.save(path)

    # ------------------------------------------------------------ textos
    def edit_text(self, t, out):
        b = self.body(t); cid = t['id']
        try:
            r = Bits(b, 2)
            r.rect()
            f1 = r.u8(); f2 = r.u8()
            has_text = f1 & 0x80; has_col = f1 & 0x04; has_max = f1 & 0x02; has_font = f1 & 0x01
            has_fclass = f2 & 0x80; has_layout = f2 & 0x20; html_ = bool(f2 & 0x02)
            p = r.p
            e = {'id': cid, 'type': 'EditText', 'html': html_}
            if has_font:
                e['font'] = struct.unpack_from('<H', b, p)[0]; p += 2
            if has_fclass:
                e['fontClass'], p = cstr(b, p)
            if has_font:
                e['size'] = struct.unpack_from('<H', b, p)[0] / 20.0; p += 2
            if has_col:
                e['color'] = '#%02x%02x%02x' % tuple(b[p:p + 3]); p += 4
            if has_max:
                p += 2
            if has_layout:
                p += 9
            e['variable'], p = cstr(b, p)
            if has_text:
                e['text'], p = cstr(b, p)
            out.append(e)
        except Exception as ex:
            self.err('texto', cid, ex)

    def static_text(self, t, out):
        b = self.body(t); cid = t['id']; code = t['code']
        try:
            r = Bits(b, 2)
            r.rect(); r.matrix()
            gb = r.u8(); ab = r.u8()
            font = None; runs = []; cur = []
            while True:
                r.align()
                flags = r.u8()
                if flags == 0: break
                if flags & 0x80 == 0: break
                if flags & 0x08: font = r.u16()
                if flags & 0x04:
                    r.rgba() if code == 33 else r.rgb()
                if flags & 0x01: r.s16()
                if flags & 0x02: r.s16()
                if flags & 0x08: r.u16()
                n = r.u8()
                chars = []
                codes = self.fonts.get(font, {}).get('codes', [])
                for _ in range(n):
                    gi = r.ub(gb); r.sb(ab)
                    chars.append(chr(codes[gi]) if gi < len(codes) else '?')
                runs.append(''.join(chars))
            out.append({'id': cid, 'type': 'StaticText', 'font': font, 'text': '\n'.join(runs)})
        except Exception as ex:
            self.err('texto estatico', cid, ex)

    # ------------------------------------------------------------ recorrido
    def run(self):
        tags = self.m['tags']
        # 1) tablas JPEG y mapas de bits antes que las formas que los usan
        for t in tags:
            if t['code'] == 8:
                self.jpeg_tables = self.body(t)
        for t in tags:
            if t['code'] in (6, 20, 21, 35, 36, 90):
                self.image(t)
        for t in tags:
            if t['code'] in (10, 48, 75):
                if t['code'] == 75: self.font(t)
        texts = []
        for t in tags:
            c = t['code']
            if c == 14: self.sound(t)
            elif c in (2, 22, 32, 83): self.shape(t)
            elif c in (46, 84): self.morph(t)
            elif c == 37: self.edit_text(t, texts)
            elif c in (11, 33): self.static_text(t, texts)
        # 2) sonido en flujo: escenario principal y cada sprite
        top = [(t['code'], t['long'], None, t['len'], t) for t in tags]
        # escenario principal
        fmt = None; chunks = []
        for t in tags:
            if t['code'] in (18, 45): fmt = self.body(t)[1] >> 4
            elif t['code'] == 19 and fmt == 2: chunks.append(self.body(t)[4:])
        if chunks:
            open(os.path.join(self.out, 'streams', 'escenario.mp3'), 'wb').write(b''.join(chunks))
            self.rep['streams'].append(dict(timeline='escenario', file='streams/escenario.mp3', blocks=len(chunks)))
        for t in tags:
            if t['code'] == 39:
                b = self.body(t)
                self.streams_of('sprite_' + self.label(t['id']), read_tags(b, 4, len(b)), b)
        json.dump(texts, open(os.path.join(self.out, 'texts', 'textos.json'), 'w'), indent=1, ensure_ascii=False)
        self.rep['texts'] = len(texts)
        self.texts = texts
        return self.rep


def gallery(out, rep, texts):
    H = ['<!doctype html><meta charset="utf-8"><title>SONNY2 — recursos</title>',
         '<style>body{font:14px system-ui;margin:16px;background:#f4f4f4;color:#222}'
         'h2{margin-top:32px}.g{display:flex;flex-wrap:wrap;gap:8px}'
         '.c{background:#fff;border:1px solid #ddd;padding:6px;width:150px;text-align:center;font-size:11px;word-break:break-all}'
         '.c img{max-width:140px;max-height:110px;background:repeating-conic-gradient(#ddd 0 25%,#fff 0 50%) 0 0/12px 12px}'
         'audio{width:140px}table{border-collapse:collapse;background:#fff}td,th{border:1px solid #ddd;padding:4px 8px;vertical-align:top}</style>',
         '<h1>SONNY2.swf — recursos extraídos</h1>',
         '<p>Imágenes %d · Sonidos %d · Flujos %d · Formas %d · Morph %d · Fuentes %d · Textos %d</p>' % (
             len(rep['images']), len(rep['sounds']), len(rep['streams']), len(rep['shapes']),
             len(rep['morphs']), len(rep['fonts']), rep['texts'])]
    def card(src, cap, kind='img'):
        cap = html.escape(cap)
        if kind == 'img':
            return '<div class="c"><img loading="lazy" src="%s"><br>%s</div>' % (src, cap)
        return '<div class="c"><audio controls preload="none" src="%s"></audio><br>%s</div>' % (src, cap)
    H.append('<h2>Imágenes</h2><div class="g">')
    H += [card(i['file'], '%s (%dx%d)' % (os.path.basename(i['file']), i['w'], i['h'])) for i in rep['images']]
    H.append('</div><h2>Sonidos</h2><div class="g">')
    H += [card(s['file'], '%s · %ss' % (os.path.basename(s['file']), s['seconds']), 'a') for s in rep['sounds']]
    H.append('</div><h2>Sonido en flujo</h2><div class="g">')
    H += [card(s['file'], os.path.basename(s['file']), 'a') for s in rep['streams']]
    H.append('</div><h2>Formas</h2><div class="g">')
    H += [card(s['file'], os.path.basename(s['file'])) for s in rep['shapes']]
    H.append('</div><h2>Morph (estado inicial)</h2><div class="g">')
    H += [card(s['file'], os.path.basename(s['file'])) for s in rep['morphs']]
    H.append('</div><h2>Fuentes</h2><table><tr><th>Id</th><th>Nombre</th><th>Glifos</th><th>Caracteres</th></tr>')
    for f in rep['fonts']:
        H.append('<tr><td>%d</td><td>%s</td><td>%d</td><td>%s</td></tr>' % (
            f['id'], html.escape(f['name']), f['glyphs'], html.escape(f['chars'][:120])))
    H.append('</table><h2>Textos</h2><table><tr><th>Id</th><th>Variable</th><th>Texto</th></tr>')
    for t in texts:
        tx = re.sub('<[^>]+>', '', t.get('text', ''))
        H.append('<tr><td>%d</td><td>%s</td><td>%s</td></tr>' % (
            t['id'], html.escape(t.get('variable', '')), html.escape(tx[:200])))
    H.append('</table>')
    open(os.path.join(out, 'index.html'), 'w').write('\n'.join(H))


if __name__ == '__main__':
    ex = Extractor(sys.argv[1], sys.argv[2])
    rep = ex.run()
    gallery(sys.argv[2], rep, ex.texts)
    json.dump(rep, open(os.path.join(sys.argv[2], 'report.json'), 'w'), indent=1, ensure_ascii=False)
    for k in ('images', 'sounds', 'streams', 'shapes', 'morphs', 'fonts'):
        print('%-8s %d' % (k, len(rep[k])))
    print('texts   ', rep['texts'])
    print('errores ', len(rep['errors']))
    for e in rep['errors'][:15]: print('   ', e)
