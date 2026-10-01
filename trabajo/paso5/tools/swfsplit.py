# Paso 1 — divide un SWF en piezas reensamblables.
#
# Uso:  python3 swfsplit.py ENTRADA.swf CARPETA_SALIDA
#
# Produce:
#   CARPETA/header.bin          cabecera tras la firma (rect, fps, fotogramas)
#   CARPETA/manifest.json       orden exacto de las etiquetas y metadatos
#   CARPETA/tags/NNNNN_Nombre[_id].bin   cuerpo crudo de cada etiqueta
#   CARPETA/symbols.json        tabla de simbolos: id -> tipo, nombres exportados
#   CARPETA/frames.json         fotogramas y etiquetas de fotograma del escenario
#   CARPETA/sprites.json        arbol de cada DefineSprite (etiquetas internas)
#
# La regla de oro: swfjoin.py debe reconstruir el SWF identico byte a byte.
import sys, os, json, struct, zlib, hashlib

TAGN = {0:'End',1:'ShowFrame',2:'DefineShape',4:'PlaceObject',5:'RemoveObject',
 6:'DefineBits',7:'DefineButton',8:'JPEGTables',9:'SetBackgroundColor',10:'DefineFont',
 11:'DefineText',12:'DoAction',13:'DefineFontInfo',14:'DefineSound',15:'StartSound',
 17:'DefineButtonSound',18:'SoundStreamHead',19:'SoundStreamBlock',20:'DefineBitsLossless',
 21:'DefineBitsJPEG2',22:'DefineShape2',23:'DefineButtonCxform',24:'Protect',
 26:'PlaceObject2',28:'RemoveObject2',32:'DefineShape3',33:'DefineText2',
 34:'DefineButton2',35:'DefineBitsJPEG3',36:'DefineBitsLossless2',37:'DefineEditText',
 39:'DefineSprite',43:'FrameLabel',45:'SoundStreamHead2',46:'DefineMorphShape',
 48:'DefineFont2',56:'ExportAssets',57:'ImportAssets',58:'EnableDebugger',
 59:'DoInitAction',60:'DefineVideoStream',61:'VideoFrame',62:'DefineFontInfo2',
 64:'EnableDebugger2',65:'ScriptLimits',66:'SetTabIndex',69:'FileAttributes',
 70:'PlaceObject3',71:'ImportAssets2',73:'DefineFontAlignZones',74:'CSMTextSettings',
 75:'DefineFont3',76:'SymbolClass',77:'Metadata',78:'DefineScalingGrid',82:'DoABC',
 83:'DefineShape4',84:'DefineMorphShape2',86:'DefineSceneAndFrameLabelData',
 87:'DefineBinaryData',88:'DefineFontName',89:'StartSound2',90:'DefineBitsJPEG4',
 91:'DefineFont4'}

# etiquetas cuyo cuerpo empieza con el id de caracter (UI16)
DEFINES = {2,6,7,10,11,14,20,21,22,32,33,34,35,36,37,39,46,48,60,75,83,84,87,90,91}


def read_tags(d, s, e):
    """Lista de (codigo, cabecera_larga, cuerpo_offset, largo) en [s, e)."""
    out = []
    i = s
    while i < e:
        h = struct.unpack_from('<H', d, i)[0]
        code, ln = h >> 6, h & 63
        long_hdr = (ln == 63)
        hl = 2
        if long_hdr:
            ln = struct.unpack_from('<I', d, i + 2)[0]
            hl = 6
        out.append((code, long_hdr, i + hl, ln))
        i += hl + ln
        if code == 0:
            break
    return out


def cstr(b, i):
    j = b.index(b'\0', i)
    return b[i:j].decode('latin1'), j + 1


def main(src, outdir):
    raw = open(src, 'rb').read()
    sig = raw[:3]
    ver = raw[3]
    if sig == b'CWS':
        body = zlib.decompress(raw[8:])
    elif sig == b'FWS':
        body = raw[8:]
    else:
        raise SystemExit('firma no soportada: %r' % sig)
    d = b'FWS' + raw[3:8] + body
    nb = d[8] >> 3
    hdr_end = 8 + (5 + 4 * nb + 7) // 8 + 4
    rect_len = (5 + 4 * nb + 7) // 8
    fps = struct.unpack_from('<H', d, 8 + rect_len)[0] / 256.0
    nframes = struct.unpack_from('<H', d, 8 + rect_len + 2)[0]

    os.makedirs(os.path.join(outdir, 'tags'), exist_ok=True)
    open(os.path.join(outdir, 'header.bin'), 'wb').write(d[8:hdr_end])

    T = read_tags(d, hdr_end, len(d))
    manifest = dict(source=os.path.basename(src), signature=sig.decode(),
                    version=ver, file_length=struct.unpack_from('<I', raw, 4)[0],
                    sha256_file=hashlib.sha256(raw).hexdigest(),
                    sha256_uncompressed=hashlib.sha256(d).hexdigest(),
                    fps=fps, frames=nframes, tags=[])
    symbols = {}
    frames = []
    cur_frame = {'n': 1, 'labels': [], 'tags': 0}
    sprites = {}

    for k, (code, lh, off, ln) in enumerate(T):
        name = TAGN.get(code, 'Tag%d' % code)
        cid = None
        if code in DEFINES and ln >= 2:
            cid = struct.unpack_from('<H', d, off)[0]
        fn = '%05d_%s%s.bin' % (k, name, '_%d' % cid if cid is not None else '')
        open(os.path.join(outdir, 'tags', fn), 'wb').write(d[off:off + ln])
        manifest['tags'].append(dict(i=k, code=code, name=name, long=lh,
                                     len=ln, id=cid, file=fn))
        # tabla de simbolos
        if cid is not None:
            symbols.setdefault(str(cid), {'type': name, 'exports': []})
        if code == 56:            # ExportAssets
            n = struct.unpack_from('<H', d, off)[0]
            p = off + 2
            for _ in range(n):
                t = struct.unpack_from('<H', d, p)[0]
                nm, p = cstr(d, p + 2)
                symbols.setdefault(str(t), {'type': '?', 'exports': []})
                symbols[str(t)]['exports'].append(nm)
        # fotogramas del escenario
        if code == 43:
            lbl, _ = cstr(d, off)
            cur_frame['labels'].append(lbl)
        cur_frame['tags'] += 1
        if code == 1:
            frames.append(cur_frame)
            cur_frame = {'n': cur_frame['n'] + 1, 'labels': [], 'tags': 0}
        # arbol de sprites
        if code == 39:
            nf = struct.unpack_from('<H', d, off + 2)[0]
            inner = read_tags(d, off + 4, off + ln)
            fl = []
            f = 1
            for c2, _, o2, l2 in inner:
                if c2 == 43:
                    lb, _ = cstr(d, o2)
                    fl.append([f, lb])
                if c2 == 1:
                    f += 1
            cnt = {}
            for c2, _, _, _ in inner:
                nm2 = TAGN.get(c2, 'Tag%d' % c2)
                cnt[nm2] = cnt.get(nm2, 0) + 1
            sprites[str(cid)] = dict(frames=nf, labels=fl, tags=cnt,
                                     scripts=cnt.get('DoAction', 0))

    json.dump(manifest, open(os.path.join(outdir, 'manifest.json'), 'w'), indent=1)
    json.dump(symbols, open(os.path.join(outdir, 'symbols.json'), 'w'), indent=1)
    json.dump(frames, open(os.path.join(outdir, 'frames.json'), 'w'), indent=1)
    json.dump(sprites, open(os.path.join(outdir, 'sprites.json'), 'w'), indent=1)
    return manifest, symbols, frames, sprites


if __name__ == '__main__':
    m, sy, fr, sp = main(sys.argv[1], sys.argv[2])
    print('etiquetas de nivel superior:', len(m['tags']))
    print('simbolos:', len(sy), '| con nombre exportado:',
          sum(1 for v in sy.values() if v['exports']))
    print('fotogramas del escenario:', len(fr), '| sprites:', len(sp))
