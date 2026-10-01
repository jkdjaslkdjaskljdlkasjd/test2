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

# Borde entre cielo (quieto) y suelo (sigue la camara) de cada fondo, en y de 2560x1440:
#   ('oscuro', umbral, y0, y1): ultima fila oscura del fondo (montanas) en cada columna  -> SNOW
#   ('claro',  umbral, y0, y1): primera fila clara del suelo en cada columna              -> STREETS, STREETS3
#   ('linea',  y):              borde recto (habitaciones, cubierta, cueva)
BORDES = {
    'SNOW': ('oscuro', 70, 330, 640),
    'STREETS': ('claro', 60, 380, 700),
    'STREETS3': ('claro', 60, 380, 700),
    'JAIL': ('linea', 620),
    'CHURCH': ('linea', 605),
    'ROME': ('linea', 605),
    'STREETS2': ('linea', 600),
    'SEA': ('linea', 455),
    'TRAIN': ('linea', 470),
    'TUNNEL': ('linea', 480),
}

def borde(im, spec=('oscuro', 70, 330, 640)):
    from scipy.ndimage import median_filter, uniform_filter1d, percentile_filter
    W = im.size[0]
    if spec[0] == 'linea':
        return np.full(W, float(spec[1]))
    tipo, umbral, y0, y1 = spec
    L = np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(3))).astype(float)
    b = np.full(W, np.nan)
    for x in range(W):
        col = L[y0:y1, x]
        if tipo == 'oscuro':
            idx = np.where(col < umbral)[0]
            if len(idx): b[x] = y0 + idx.max()
        else:
            ok = col > umbral
            # primera fila clara seguida de al menos 40 filas claras
            run = np.convolve(ok.astype(int), np.ones(40, int), 'valid')
            idx = np.where(run == 40)[0]
            if len(idx): b[x] = y0 + idx[0]
    xs = np.arange(W); ok = ~np.isnan(b)
    b = np.interp(xs, xs[ok], b[ok])
    # las piedritas o grietas oscuras dan picos hacia abajo: se toma un percentil bajo movil
    b = percentile_filter(b, 20, size=121)
    return uniform_filter1d(median_filter(b, size=41), size=61) - SUBIR

def alfa(b, H=1440):
    y = np.arange(H)[:, None].astype(float)
    a = np.clip((y - (b[None, :] - FUNDIDO / 2)) / FUNDIDO, 0, 1)
    return (a * 255).round().astype(np.uint8)

def jpeg3(cid, im, a, calidad=88):
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
    import sys, glob
    vistas = []
    for k, spec in sorted(BORDES.items()):
        im = Image.open(os.path.join(D, 'build/combate_%s_2560x1440.jpg' % k)).convert('RGB')
        b = borde(im, spec); a = alfa(b)
        prev = im.copy(); prev.putalpha(Image.fromarray(a))
        fondo = Image.new('RGBA', im.size, (255, 0, 255, 255)); fondo.alpha_composite(prev)
        v = fondo.convert('RGB').resize((640, 360)); vistas.append(v)
        print(k, 'borde y:', int(b.min()), '-', int(b.max()))
    hoja = Image.new('RGB', (1280, 360 * ((len(vistas) + 1) // 2)))
    for i, v in enumerate(vistas): hoja.paste(v, ((i % 2) * 640, (i // 2) * 360))
    hoja.save(os.path.join(D, 'build/capas_vista.png'))
