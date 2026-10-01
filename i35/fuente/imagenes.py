# I32 - prepara los fondos de combate HD a 2560x1440 (JPEG para DefineBitsJPEG2)
from PIL import Image, ImageFilter
import io, os
D = os.path.dirname(os.path.abspath(__file__))
import glob
FONDOS = dict((os.path.basename(f)[8:-4], f) for f in sorted(glob.glob(os.path.join(D, 'fuente/imagenes/combate_*.png'))))
def preparar(src, dst):
    im = Image.open(src).convert('RGB')
    if im.size != (2560, 1440):
        im = im.resize((2560, 1440), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=2))
    im.save(dst, 'JPEG', quality=88, optimize=True)
    return os.path.getsize(dst)
if __name__ == '__main__':
    os.makedirs(os.path.join(D, 'build'), exist_ok=True)
    for k, f in FONDOS.items():
        print(k, preparar(os.path.join(D, f), os.path.join(D, 'build/combate_%s_2560x1440.jpg' % k)))
