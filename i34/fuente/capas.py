# I34 - separa la imagen HD de combate en dos capas, como el juego original:
#   cielo  = la imagen entera (queda quieta, como el cielo 3328 del juego)
#   suelo  = la misma imagen con transparencia por encima del pie de las montanas (sigue el zoom y el
#            temblor de la camara, como el suelo de BATTLESCREEN)
# El borde se detecta solo: en cada columna, la ultima fila oscura de las montanas (luminancia < UMBRAL)
# entre y = 330 y 640 (en 2560x1440); despues se suaviza y se difumina FUNDIDO px.
from PIL import Image, ImageFilter
import numpy as np, zlib, io, os
D = os.path.dirname(os.path.abspath(__file__))
UMBRAL, Y0, Y1, FUNDIDO, SUBIR = 70, 330, 640, 14, 4

def borde(im):
    from scipy.ndimage import median_filter, uniform_filter1d
    L = np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(3))).astype(float)
    W = L.shape[1]; b = np.full(W, np.nan)
    for x in range(W):
        idx = np.where(L[Y0:Y1, x] < UMBRAL)[0]
        if len(idx): b[x] = Y0 + idx.max()
    xs = np.arange(W); ok = ~np.isnan(b)
    b = np.interp(xs, xs[ok], b[ok])
    # las piedritas oscuras justo debajo del borde dan picos hacia abajo: se toma un percentil bajo movil
    from scipy.ndimage import percentile_filter
    b = percentile_filter(b, 20, size=121)
    return uniform_filter1d(median_filter(b, size=41), size=61) - SUBIR

def alfa(b, H=1440):
    y = np.arange(H)[:, None].astype(float)
    a = np.clip((y - (b[None, :] - FUNDIDO / 2)) / FUNDIDO, 0, 1)
    return (a * 255).round().astype(np.uint8)

def jpeg3(cid, im, a, calidad=92):
    """DefineBitsJPEG3: id, desplazamiento del alfa, JPEG y alfa (zlib, 1 byte por pixel).
    El reproductor toma el color del JPEG como premultiplicado por el alfa (igual que Lossless2): si no se
    premultiplica, el borde difuminado sale con un contorno claro."""
    import struct
    rgb = np.asarray(im.convert('RGB')).astype(np.uint16)
    pm = ((rgb * a[:, :, None].astype(np.uint16) + 127) // 255).astype(np.uint8)
    buf = io.BytesIO(); Image.fromarray(pm).save(buf, 'JPEG', quality=calidad, optimize=True)
    jb = buf.getvalue()
    return struct.pack('<HI', cid, len(jb)) + jb + zlib.compress(a.tobytes(), 9)

if __name__ == '__main__':
    im = Image.open(os.path.join(D, 'build/combate_SNOW_2560x1440.jpg')).convert('RGB')
    b = borde(im); a = alfa(b)
    Image.fromarray(a).save(os.path.join(D, 'build/combate_SNOW_suelo_alfa.png'))
    prev = im.copy(); prev.putalpha(Image.fromarray(a))
    fondo = Image.new('RGBA', im.size, (255, 0, 255, 255)); fondo.alpha_composite(prev)
    fondo.convert('RGB').resize((1280, 720)).save(os.path.join(D, 'build/combate_SNOW_suelo_vista.png'))
    print('borde y:', int(b.min()), '-', int(b.max()))
