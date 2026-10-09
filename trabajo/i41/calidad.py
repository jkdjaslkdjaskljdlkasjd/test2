# I38 - calidad maxima: las imagenes HD van como DefineBitsLossless2 (sin perdida; ARGB premultiplicado, zlib),
# en lugar de JPEG. El SWF pesa mas (GitHub admite hasta 100 MB por archivo) pero no pierde nada de la imagen.
import struct, zlib
import numpy as np

def lossless2(cid, im, alfa=None):
    """im: imagen PIL RGB; alfa: arreglo HxW uint8 o None (opaca). Devuelve el cuerpo del tag 36."""
    a = np.asarray(im.convert('RGB'), dtype=np.uint16)
    h, w = a.shape[:2]
    al = np.full((h, w, 1), 255, np.uint16) if alfa is None else alfa.astype(np.uint16)[:, :, None]
    rgb = (a * al + 127) // 255                      # Lossless2 guarda el color premultiplicado por el alfa
    argb = np.concatenate([al, rgb], axis=2).astype(np.uint8)
    return struct.pack('<HBHH', cid, 5, w, h) + zlib.compress(argb.tobytes(), 9)

# I40 - el usuario pidio bajar un poco el peso sin perder calidad visible: JPEG calidad 97 con color completo
# (4:4:4). Contra la imagen sin perdida da ~51 dB de PSNR (no se distingue) y pesa ~1/3.
CALIDAD_JPEG = 97

def _jpeg(im):
    import io
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=CALIDAD_JPEG, subsampling=0, optimize=True)
    return buf.getvalue()

def jpeg2(cid, im):
    """DefineBitsJPEG2 (tag 21), opaca."""
    return struct.pack('<H', cid) + _jpeg(im)

def jpeg3(cid, im, alfa):
    """DefineBitsJPEG3 (tag 35) con alfa: el color va premultiplicado por el alfa (si no, contorno claro)."""
    from PIL import Image
    a = np.asarray(im.convert('RGB'), dtype=np.uint16)
    pm = ((a * alfa.astype(np.uint16)[:, :, None] + 127) // 255).astype(np.uint8)
    jb = _jpeg(Image.fromarray(pm))
    return struct.pack('<HI', cid, len(jb)) + jb + zlib.compress(alfa.astype(np.uint8).tobytes(), 9)
