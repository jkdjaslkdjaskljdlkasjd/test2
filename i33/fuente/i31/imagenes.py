# I31 — prepara las imagenes HD de zona a 2560x1440 (JPEG para DefineBitsJPEG2)
from PIL import Image, ImageFilter
import io, os
D = os.path.dirname(os.path.abspath(__file__))
def preparar(src, dst):
    im = Image.open(src).convert('RGB')
    if im.size != (2560, 1440):
        im = im.resize((2560, 1440), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=2))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=92, optimize=True)
    open(dst, 'wb').write(buf.getvalue())
    return len(buf.getvalue())
if __name__ == '__main__':
    os.makedirs(os.path.join(D, 'build'), exist_ok=True)
    print('TUNNELS', preparar(os.path.join(D, 'fuente/imagenes/Labyrinth_TUNNELS_usuario_1672x941.png'), os.path.join(D, 'build/zona_TUNNELS_2560x1440.jpg')))
    print('ROME', preparar(os.path.join(D, 'fuente/imagenes/IlSanctus_ROME_usuario_2560x1440.png'), os.path.join(D, 'build/zona_ROME_2560x1440.jpg')))
