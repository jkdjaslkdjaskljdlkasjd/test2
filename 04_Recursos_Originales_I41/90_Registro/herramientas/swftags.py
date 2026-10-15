#!/usr/bin/env python3
"""Lectura/escritura mínima de etiquetas SWF (sin interpretar su contenido salvo lo imprescindible).

read_swf(path) -> dict(version, header_rect_bytes, frame_rate_raw, frame_count, tags=[(code, body_bytes)])
write_swf(path, version, rect_bytes, rate_raw, frame_count, tags, compress=True)
char_id(code, body) -> id del carácter definido (o None)
"""
import struct, zlib

DEFINE_CODES = {
    2: 'DefineShape', 22: 'DefineShape2', 32: 'DefineShape3', 83: 'DefineShape4',
    39: 'DefineSprite', 14: 'DefineSound', 20: 'DefineBitsLossless', 36: 'DefineBitsLossless2',
    21: 'DefineBitsJPEG2', 35: 'DefineBitsJPEG3', 90: 'DefineBitsJPEG4', 6: 'DefineBits',
    34: 'DefineButton2', 7: 'DefineButton', 37: 'DefineEditText', 11: 'DefineText', 33: 'DefineText2',
    75: 'DefineFont3', 48: 'DefineFont2', 10: 'DefineFont', 46: 'DefineMorphShape', 84: 'DefineMorphShape2',
    60: 'DefineVideoStream',
}
TAG_NAMES = dict(DEFINE_CODES)
TAG_NAMES.update({0: 'End', 1: 'ShowFrame', 9: 'SetBackgroundColor', 12: 'DoAction', 26: 'PlaceObject2',
                  28: 'RemoveObject2', 43: 'FrameLabel', 56: 'ExportAssets', 59: 'DoInitAction',
                  69: 'FileAttributes', 70: 'PlaceObject3', 77: 'Metadata', 15: 'StartSound',
                  73: 'DefineFontAlignZones', 74: 'CSMTextSettings', 88: 'DefineFontName', 4: 'PlaceObject',
                  5: 'RemoveObject', 45: 'SoundStreamHead2', 18: 'SoundStreamHead', 19: 'SoundStreamBlock'})


def _rect_len(data, off):
    nbits = data[off] >> 3
    total_bits = 5 + 4 * nbits
    return (total_bits + 7) // 8


def parse_tags(data, off, end=None):
    tags = []
    end = len(data) if end is None else end
    while off < end:
        hdr = struct.unpack_from('<H', data, off)[0]
        off += 2
        code, ln = hdr >> 6, hdr & 0x3f
        long_form = False
        if ln == 0x3f:
            ln = struct.unpack_from('<I', data, off)[0]
            off += 4
            long_form = True
        body = data[off:off + ln]
        off += ln
        tags.append((code, body, long_form))
        if code == 0:
            break
    return tags, off


def read_swf(path):
    raw = open(path, 'rb').read()
    sig = raw[:3]
    version = raw[3]
    if sig == b'CWS':
        data = raw[:8] + zlib.decompress(raw[8:])
    elif sig == b'FWS':
        data = raw
    else:
        raise ValueError('firma SWF no soportada: %r' % sig)
    off = 8
    rl = _rect_len(data, off)
    rect = data[off:off + rl]
    off += rl
    rate_raw = data[off:off + 2]
    frame_count = struct.unpack_from('<H', data, off + 2)[0]
    off += 4
    tags, _ = parse_tags(data, off)
    return {'version': version, 'rect': rect, 'rate_raw': rate_raw, 'frame_count': frame_count,
            'tags': tags, 'sig': sig}


def tag_bytes(code, body, long_form=False):
    ln = len(body)
    if ln >= 0x3f or long_form:
        return struct.pack('<HI', (code << 6) | 0x3f, ln) + body
    return struct.pack('<H', (code << 6) | ln) + body


def write_swf(path, version, rect, rate_raw, frame_count, tags, compress=True):
    body = rect + rate_raw + struct.pack('<H', frame_count)
    body += b''.join(tag_bytes(*t) if len(t) == 3 else tag_bytes(t[0], t[1]) for t in tags)
    total = 8 + len(body)
    if compress:
        out = b'CWS' + bytes([version]) + struct.pack('<I', total) + zlib.compress(body, 9)
    else:
        out = b'FWS' + bytes([version]) + struct.pack('<I', total) + body
    open(path, 'wb').write(out)
    return total


def char_id(code, body):
    if code in DEFINE_CODES and len(body) >= 2:
        return struct.unpack_from('<H', body, 0)[0]
    return None


def sprite_subtags(body):
    """body de DefineSprite -> (id, frame_count, [(code, body, long)])"""
    sid, fc = struct.unpack_from('<HH', body, 0)
    tags, _ = parse_tags(body, 4)
    return sid, fc, tags


def make_sprite(sid, frame_count, subtags):
    return struct.pack('<HH', sid, frame_count) + b''.join(
        tag_bytes(*t) if len(t) == 3 else tag_bytes(t[0], t[1]) for t in subtags)


def string_z(s):
    return s.encode('latin-1') + b'\x00'


def export_assets(pairs):
    return struct.pack('<H', len(pairs)) + b''.join(struct.pack('<H', i) + string_z(n) for i, n in pairs)
