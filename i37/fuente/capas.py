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
    # JAIL (I37): como en el juego original, los edificios de los costados van con el SUELO (siguen la camara) y
    # solo el cielo y la ciudad lejana quedan quietos. El borde es el contorno de los techos y las paredes
    # interiores (x 750 y 1809), y en el centro el pie de la ciudad (610). ('poligono', puntos, margen, fundido,
    # relleno): margen -3 = incluye la linea del techo; fundido 4 px; relleno = en la capa quieta, detras de los
    # edificios se prolonga el cielo de cada fila (si no, el zoom deja ver un "fantasma" del edificio).
    # contorno medido cada 50 px (primer borde fuerte desde arriba); el techo es levemente curvo
    'JAIL': ('poligono', [(0, 186), (50, 188), (100, 190), (150, 192), (200, 217), (250, 242), (300, 267), (350, 292), (400, 317), (450, 342), (500, 369), (550, 397), (600, 425), (650, 454), (700, 483), (725, 497), (751, 512),
                          (752, 612), (1807, 612),
                          (1808, 510), (1850, 487), (1900, 460), (1950, 432), (2000, 404), (2050, 377), (2100, 351), (2150, 326), (2200, 301), (2250, 276), (2300, 251), (2350, 227), (2400, 202), (2450, 197), (2500, 195), (2560, 192)], -3, 4, True),
    'CHURCH': ('linea', 605),
    'ROME': ('linea', 605),
    'STREETS2': ('linea', 600),
    'SEA': ('linea', 455),
    'TRAIN': ('linea', 470),
    'TUNNEL': ('linea', 480),
}

# I36: fondos que entran al SWF (el resto queda clasico por ahora)
ACTIVOS = ('JAIL', 'SNOW')

def borde(im, spec=('oscuro', 70, 330, 640)):
    from scipy.ndimage import median_filter, uniform_filter1d, percentile_filter
    W = im.size[0]
    if spec[0] in ('puntos', 'poligono'):
        xs, ys = zip(*spec[1])
        return np.interp(np.arange(W), xs, ys) + spec[2]
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

def fundido(spec):
    return spec[3] if spec[0] == 'poligono' else FUNDIDO

def alfa(b, H=1440, f=FUNDIDO):
    y = np.arange(H)[:, None].astype(float)
    a = np.clip((y - (b[None, :] - f / 2)) / f, 0, 1)
    return (a * 255).round().astype(np.uint8)

def relleno_cielo(im, b, desenfoque=6, adentro=14):
    """Capa quieta sin las estructuras que van con el suelo: en cada fila, los pixeles que quedan bajo el borde
    (de los costados hacia adentro) toman el color del primer pixel de cielo de esa fila, del lado del centro;
    despues se suaviza solo la parte rellenada. Las filas que son suelo de punta a punta quedan como estan."""
    from scipy.ndimage import gaussian_filter
    A = np.asarray(im.convert('RGB')).astype(float)
    H, W = A.shape[:2]
    y = np.arange(H)[:, None]
    tapado = y >= (b[None, :] - 1)
    out = A.copy(); hecho = np.zeros((H, W), bool)
    mitad = W // 2
    for r in range(H):
        fila = tapado[r]
        if fila.all() or not fila.any():
            continue
        libres = np.where(~fila)[0]
        izq = np.where(fila[:mitad])[0]
        if len(izq):
            fuente = libres[libres > izq.min()]
            if len(fuente):
                x0 = fuente.min(); xs = izq[izq < x0]
                out[r, xs] = A[r, min(x0 + adentro, W - 1)]; hecho[r, xs] = True
        der = np.where(fila[mitad:])[0] + mitad
        if len(der):
            fuente = libres[libres < der.max()]
            if len(fuente):
                x1 = fuente.max(); xs = der[der > x1]
                out[r, xs] = A[r, max(x1 - adentro, 0)]; hecho[r, xs] = True
    suave = np.stack([gaussian_filter(out[..., c], desenfoque) for c in range(3)], -1)
    out[hecho] = suave[hecho]
    return Image.fromarray(out.round().clip(0, 255).astype(np.uint8))

def jpeg3(cid, im, a, calidad=95):
    """DefineBitsJPEG3: id, desplazamiento del alfa, JPEG y alfa (zlib, 1 byte por pixel).
    El reproductor toma el color del JPEG como premultiplicado por el alfa (igual que Lossless2): si no se
    premultiplica, el borde difuminado sale con un contorno claro."""
    import struct
    rgb = np.asarray(im.convert('RGB')).astype(np.uint16)
    pm = ((rgb * a[:, :, None].astype(np.uint16) + 127) // 255).astype(np.uint8)
    buf = io.BytesIO(); Image.fromarray(pm).save(buf, 'JPEG', quality=calidad, subsampling=0, optimize=True)
    jb = buf.getvalue()
    return struct.pack('<HI', cid, len(jb)) + jb + zlib.compress(a.tobytes(), 9)

if __name__ == '__main__':
    import sys, glob
    vistas = []
    for k in ACTIVOS:
        spec = BORDES[k]
        im = Image.open(os.path.join(D, 'build/combate_%s_2560x1440.jpg' % k)).convert('RGB')
        b = borde(im, spec); a = alfa(b, f=fundido(spec))
        if spec[0] == 'poligono' and spec[4]:
            relleno_cielo(im, b).save(os.path.join(D, 'build/combate_%s_cielo.png' % k))
        prev = im.copy(); prev.putalpha(Image.fromarray(a))
        fondo = Image.new('RGBA', im.size, (255, 0, 255, 255)); fondo.alpha_composite(prev)
        v = fondo.convert('RGB').resize((640, 360)); vistas.append(v)
        print(k, 'borde y:', int(b.min()), '-', int(b.max()))
    hoja = Image.new('RGB', (1280, 360 * ((len(vistas) + 1) // 2)))
    for i, v in enumerate(vistas): hoja.paste(v, ((i % 2) * 640, (i // 2) * 360))
    hoja.save(os.path.join(D, 'build/capas_vista.png'))
