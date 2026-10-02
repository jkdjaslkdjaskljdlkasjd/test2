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
