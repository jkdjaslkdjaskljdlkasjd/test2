# Paso 4 — recompilacion: cambia piezas sueltas del juego y arma un SWF nuevo.
#
# Todo lo que no se toca queda byte a byte igual que el original.
#
# Uso por carpeta de cambios (lo normal):
#   python3 swfpatch.py PASO1 PASO3 SALIDA.swf CARPETA_CAMBIOS
#     CARPETA_CAMBIOS/scripts/<misma ruta que en paso3>.as   -> reemplaza ese script
#     CARPETA_CAMBIOS/images/<id>.png|.jpg                   -> reemplaza la imagen <id>
#     CARPETA_CAMBIOS/sounds/<id>[_lo_que_sea].mp3           -> reemplaza el sonido <id>
#
# Recompilar el juego entero desde los .as de PASO3:
#   python3 swfpatch.py PASO1 PASO3 SALIDA.swf --todo
#
# Como libreria:
#   p = Patcher('paso1', 'paso3')
#   p.script('escenario/frame_0042/DoAction_2.as', texto_as2)   # o bytes ya compilados
#   p.image(2803, 'nueva.png'); p.sound(102, 'nuevo.mp3')
#   p.build('salida.swf')
import sys, os, io, re, json, struct, zlib, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from as2comp import compile_script, CompileError


class PatchError(Exception):
    pass


class Patcher:
    def __init__(self, p1, p3):
        self.p1 = p1; self.p3 = p3
        self.m = json.load(open(os.path.join(p1, 'manifest.json')))
        self.hdr = open(os.path.join(p1, 'header.bin'), 'rb').read()
        idx = json.load(open(os.path.join(p3, 'index.json')))
        self.index = {}
        for s in idx:
            k = s['file'][len('scripts/'):] if s['file'].startswith('scripts/') else s['file']
            self.index[k] = s
        self.bytag = {t['file']: t for t in self.m['tags']}
        self.byid = {}
        for t in self.m['tags']:
            if t['id'] is not None: self.byid.setdefault(t['id'], t)
        self.edits = {}        # archivo de etiqueta -> [(a0, a1, bytes_nuevos, fix)]
        self.replace = {}      # archivo de etiqueta -> (codigo_nuevo, cuerpo_nuevo)
        self.log = []

    # ------------------------------------------------------------ scripts
    def find(self, ref):
        r = ref.replace('\\', '/')
        if '/scripts/' in r: r = r.split('/scripts/', 1)[1]
        if r.startswith('scripts/'): r = r[len('scripts/'):]
        if r.endswith('.pcode'): r = r[:-6] + '.as'
        if r not in self.index:
            raise PatchError('no existe ese script en el indice del paso 3: %s' % ref)
        return r, self.index[r]

    def script(self, ref, source):
        """Reemplaza un script. source: texto AS2 (se compila) o bytes de AVM1."""
        r, s = self.find(ref)
        if isinstance(source, str):
            try:
                code = compile_script(source)
            except CompileError as ex:
                raise PatchError('%s: %s' % (r, ex))
        else:
            code = bytes(source)
        L = s['loc']
        self.edits.setdefault(L['tag'], []).append((L['a0'], L['a1'], code, L['fix'], r))
        self.log.append('script  %s  (%d -> %d bytes)' % (r, L['a1'] - L['a0'], len(code)))
        return code

    def script_file(self, ref, path):
        return self.script(ref, open(path, encoding='utf-8').read())

    # ------------------------------------------------------------ recursos
    def _tag_of_id(self, cid, kinds):
        t = self.byid.get(cid)
        if t is None or t['name'] not in kinds:
            raise PatchError('el id %d no es %s' % (cid, ' / '.join(kinds)))
        return t

    def image(self, cid, path):
        """Reemplaza la imagen cid por un PNG/JPG (se guarda como DefineBitsLossless2)."""
        from PIL import Image
        t = self._tag_of_id(cid, ('DefineBitsLossless', 'DefineBitsLossless2', 'DefineBitsJPEG2',
                                  'DefineBitsJPEG3', 'DefineBits'))
        im = Image.open(path).convert('RGBA')
        w, h = im.size
        old = self._image_size(t)
        if old and old != (w, h):
            self.log.append('AVISO   imagen %d: el original mide %dx%d y la nueva %dx%d; '
                            'se vera escalada distinto' % (cid, old[0], old[1], w, h))
        import numpy as np
        a = np.asarray(im, dtype=np.uint16)
        al = a[:, :, 3:4]
        rgb = (a[:, :, :3] * al + 127) // 255          # Lossless2 guarda color premultiplicado
        argb = np.concatenate([al, rgb], axis=2).astype(np.uint8)
        data = zlib.compress(argb.tobytes(), 9)
        body = struct.pack('<HBHH', cid, 5, w, h) + data
        self.replace[t['file']] = (36, body)
        self.log.append('imagen  %d  <- %s (%dx%d)' % (cid, os.path.basename(path), w, h))

    def _image_size(self, t):
        b = open(os.path.join(self.p1, 'tags', t['file']), 'rb').read()
        if t['name'].startswith('DefineBitsLossless'):
            return struct.unpack_from('<HH', b, 3)
        try:
            from PIL import Image
            d = b[2:] if t['name'] != 'DefineBitsJPEG3' else b[6:6 + struct.unpack_from('<I', b, 2)[0]]
            if d[:4] == b'\xff\xd9\xff\xd8': d = d[4:]
            return Image.open(io.BytesIO(d)).size
        except Exception:
            return None

    def sound(self, cid, path):
        """Reemplaza el sonido cid por un MP3 (44100, 22050 o 11025 Hz)."""
        t = self._tag_of_id(cid, ('DefineSound',))
        mp3 = open(path, 'rb').read()
        frames, rate, stereo, samples = mp3_scan(mp3)
        rc = {44100: 3, 22050: 2, 11025: 1}.get(rate)
        if rc is None:
            raise PatchError('%s: Flash solo acepta MP3 a 44100, 22050 o 11025 Hz (este es %d)' % (path, rate))
        flags = (2 << 4) | (rc << 2) | (1 << 1) | (1 if stereo else 0)
        body = struct.pack('<HBI', cid, flags, samples) + struct.pack('<h', 0) + frames
        self.replace[t['file']] = (14, body)
        self.log.append('sonido  %d  <- %s (%d Hz, %s, %.1f s)' % (
            cid, os.path.basename(path), rate, 'estereo' if stereo else 'mono', samples / rate))

    # ------------------------------------------------------------ armado
    def tag_body(self, t):
        f = t['file']
        if f in self.replace:
            return self.replace[f]
        body = open(os.path.join(self.p1, 'tags', f), 'rb').read()
        if f not in self.edits:
            return t['code'], body
        buf = bytearray(body)
        eds = sorted(self.edits[f], key=lambda e: -e[0])
        for i in range(len(eds) - 1):
            if eds[i + 1][1] > eds[i][0]:
                raise PatchError('dos cambios se solapan en %s' % f)
        for a0, a1, code, fix, r in eds:
            delta = len(code) - (a1 - a0)
            buf[a0:a1] = code
            for kind, off in sorted(fix, key=lambda x: -x[1]):
                if kind == 'u32':
                    v = struct.unpack_from('<I', buf, off)[0] + delta
                    struct.pack_into('<I', buf, off, v)
                elif kind == 'u16':
                    v = struct.unpack_from('<H', buf, off)[0] + delta
                    if not 0 < v <= 65535:
                        raise PatchError('%s: el evento del boton quedo demasiado grande' % r)
                    struct.pack_into('<H', buf, off, v)
                elif kind == 'taghdr':
                    h = struct.unpack_from('<H', buf, off)[0]
                    code_, ln = h >> 6, h & 63
                    if ln == 63:
                        v = struct.unpack_from('<I', buf, off + 2)[0] + delta
                        struct.pack_into('<I', buf, off + 2, v)
                    else:
                        v = ln + delta
                        if v >= 63:
                            buf[off:off + 2] = struct.pack('<HI', (code_ << 6) | 63, v)
                        else:
                            struct.pack_into('<H', buf, off, (code_ << 6) | v)
        return t['code'], bytes(buf)

    def build(self, out=None):
        parts = []
        changed = 0
        for t in self.m['tags']:
            code, body = self.tag_body(t)
            if t['file'] in self.edits or t['file'] in self.replace:
                changed += 1
            if t['long'] or len(body) >= 63:
                parts.append(struct.pack('<HI', (code << 6) | 63, len(body)))
            else:
                parts.append(struct.pack('<H', (code << 6) | len(body)))
            parts.append(body)
        tail = b''.join(parts)
        total = 8 + len(self.hdr) + len(tail)
        unc = b'FWS' + bytes([self.m['version']]) + struct.pack('<I', total) + self.hdr + tail
        data = b'CWS' + unc[3:8] + zlib.compress(unc[8:], 9)
        if out:
            open(out, 'wb').write(data)
        self.changed = changed
        return data, unc


# ---------------------------------------------------------------- MP3
BITRATES = {  # (version, layer) -> kbps
    (1, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
    (2, 3): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]}
RATES = {1: [44100, 48000, 32000], 2: [22050, 24000, 16000], 25: [11025, 12000, 8000]}


def mp3_scan(d):
    """Devuelve (frames_sin_etiquetas, frecuencia, estereo, muestras)."""
    p = 0
    if d[:3] == b'ID3':
        sz = (d[6] << 21) | (d[7] << 14) | (d[8] << 7) | d[9]
        p = 10 + sz
    end = len(d)
    if end >= 128 and d[end - 128:end - 125] == b'TAG':
        end -= 128
    out = bytearray(); rate = None; stereo = False; samples = 0
    while p + 4 <= end:
        h = struct.unpack('>I', d[p:p + 4])[0]
        if (h >> 21) & 0x7FF != 0x7FF:
            p += 1; continue
        vb = (h >> 19) & 3; lb = (h >> 17) & 3
        ver = {3: 1, 2: 2, 0: 25}.get(vb)
        if ver is None or lb != 1:
            p += 1; continue
        bi = (h >> 12) & 15; ri = (h >> 10) & 3; pad = (h >> 9) & 1; ch = (h >> 6) & 3
        if bi in (0, 15) or ri == 3:
            p += 1; continue
        br = BITRATES[(1 if ver == 1 else 2, 3)][bi] * 1000
        sr = RATES[ver][ri]
        spf = 1152 if ver == 1 else 576
        flen = (144 if ver == 1 else 72) * br // sr + pad
        if p + flen > end: break
        if rate is None: rate = sr; stereo = ch != 3
        elif sr != rate: raise PatchError('MP3 con frecuencia variable')
        out += d[p:p + flen]; samples += spf; p += flen
    if rate is None:
        raise PatchError('no se encontraron cuadros MP3 validos')
    return bytes(out), rate, stereo, samples


# ---------------------------------------------------------------- CLI
def apply_folder(p, folder):
    n = 0
    sd = os.path.join(folder, 'scripts')
    if os.path.isdir(sd):
        for root, _, files in os.walk(sd):
            for f in sorted(files):
                if f.endswith('.as'):
                    rel = os.path.relpath(os.path.join(root, f), sd)
                    p.script_file(rel, os.path.join(root, f)); n += 1
    for sub, fn in (('images', p.image), ('sounds', p.sound)):
        d = os.path.join(folder, sub)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                m = re.match(r'^(\d+)', f)
                if m: fn(int(m.group(1)), os.path.join(d, f)); n += 1
    return n


def main(argv):
    if len(argv) < 4:
        print(__doc__ if __doc__ else 'uso: swfpatch.py PASO1 PASO3 SALIDA.swf (CARPETA_CAMBIOS | --todo)')
        return 2
    p1, p3, out, what = argv[:4]
    p = Patcher(p1, p3)
    if what == '--todo':
        for r in p.index:
            p.script_file(r, os.path.join(p3, 'scripts', r))
        p.log = ['script  (los %d scripts recompilados desde AS2)' % len(p.index)]
    else:
        if not apply_folder(p, what):
            print('la carpeta de cambios esta vacia'); return 1
    data, unc = p.build(out)
    for l in p.log: print(l)
    print('etiquetas cambiadas: %d de %d' % (p.changed, len(p.m['tags'])))
    print('%s: %d bytes, sha256 %s' % (out, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
