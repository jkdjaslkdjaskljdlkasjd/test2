# Paso 1 — reensambla un SWF a partir de la carpeta que genera swfsplit.py.
#
# Uso:  python3 swfjoin.py CARPETA SALIDA.swf [--fws]
#
# Respeta el orden del manifiesto y el tipo de cabecera de cada etiqueta
# (corta o larga), porque el reproductor Flash distingue ambas en algunos casos
# y porque es lo que permite la reconstruccion byte a byte.
#
# Si el cuerpo de una etiqueta cambia de tamano y ya no cabe en cabecera corta
# (>= 63 bytes), se promueve automaticamente a cabecera larga.
import sys, os, json, struct, zlib, hashlib


def build(folder):
    m = json.load(open(os.path.join(folder, 'manifest.json')))
    hdr = open(os.path.join(folder, 'header.bin'), 'rb').read()
    parts = []
    for t in m['tags']:
        body = open(os.path.join(folder, 'tags', t['file']), 'rb').read()
        code = t['code']
        if t['long'] or len(body) >= 63:
            parts.append(struct.pack('<HI', (code << 6) | 63, len(body)))
        else:
            parts.append(struct.pack('<H', (code << 6) | len(body)))
        parts.append(body)
    tail = b''.join(parts)
    total = 8 + len(hdr) + len(tail)
    unc = b'FWS' + bytes([m['version']]) + struct.pack('<I', total) + hdr + tail
    return m, unc


def main(folder, out, fws=False):
    m, unc = build(folder)
    if fws or m['signature'] == 'FWS':
        data = unc
    else:
        data = b'CWS' + unc[3:8] + zlib.compress(unc[8:], 9)
    open(out, 'wb').write(data)
    return m, unc, data


if __name__ == '__main__':
    fws = '--fws' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    m, unc, data = main(args[0], args[1], fws)
    ok = hashlib.sha256(unc).hexdigest() == m['sha256_uncompressed']
    print('contenido descomprimido identico al original:', ok)
    print('sha256 del archivo generado:', hashlib.sha256(data).hexdigest())
    sys.exit(0 if ok else 1)
