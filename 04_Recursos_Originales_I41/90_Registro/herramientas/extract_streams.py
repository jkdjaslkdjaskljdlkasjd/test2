#!/usr/bin/env python3
"""Extrae el audio en flujo (SoundStreamHead/SoundStreamBlock) de cada sprite sin recodificar.
MP3: cada bloque = SampleCount(UI16) + SeekSamples(SI16) + tramas MP3 -> se concatenan las tramas.
Escribe <spriteId>_stream.mp3 y <spriteId>_stream_sync.json (fotograma de cada bloque, muestras, bytes).
uso: extract_streams.py I41.swf out_dir
"""
import sys, os, struct, json
sys.path.insert(0, os.path.dirname(__file__))
import swftags as S

s = S.read_swf(sys.argv[1])
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
summary = []
for code, body, lf in s['tags']:
    if code != 39:
        continue
    sid, fc, sub = S.sprite_subtags(body)
    head = None
    frame = 1
    data = bytearray()
    sync = []
    for c, b, _ in sub:
        if c in (18, 45) and head is None:
            head = b
        elif c == 19:
            if head is None:
                continue
            fmt = head[1] >> 4
            if fmt == 2:
                sc, seek = struct.unpack_from('<Hh', b, 0)
                sync.append({"fotograma": frame, "muestras": sc, "seek": seek, "offset_bytes": len(data), "bytes": len(b) - 4})
                data += b[4:]
            else:
                sync.append({"fotograma": frame, "bytes": len(b), "formato_no_mp3": fmt})
                data += b
        elif c == 1:
            frame += 1
    if not sync:
        continue
    fmt = head[1] >> 4
    ext = 'mp3' if fmt == 2 else 'raw'
    fn = '%d_stream.%s' % (sid, ext)
    open(os.path.join(out, fn), 'wb').write(bytes(data))
    info = {"spriteId": sid, "frames_sprite": fc, "bloques": len(sync), "archivo": fn,
            "formato": {2: "MP3"}.get(fmt, fmt), "rate_hz": [5512, 11025, 22050, 44100][(head[1] >> 2) & 3],
            "estereo": bool(head[1] & 1), "muestras_por_bloque_cabecera": struct.unpack_from('<H', head, 2)[0],
            "fps_swf": 30, "primer_fotograma_con_audio": sync[0]['fotograma'], "sync": sync}
    json.dump(info, open(os.path.join(out, '%d_stream_sync.json' % sid), 'w'), indent=0)
    summary.append({k: v for k, v in info.items() if k != 'sync'})
json.dump(summary, open(os.path.join(out, '_flujos.json'), 'w'), indent=1)
print(len(summary), 'flujos')
