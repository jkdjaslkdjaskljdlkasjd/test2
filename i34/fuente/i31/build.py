# I31 — arma SONNY2_I31.swf a partir del SONNY2.swf que mando el usuario el 29/09 (I30).
#
#   python3 build.py SALIDA.swf [--debug]
#
# Cambios (ver LEEME.md):
#   - KrinScreen (sprite 2908): Zona 1 y Zona 5 vuelven al original; HD en Zona 4 y Zona 6.
#   - Imagenes 4319 (Labyrinth) y 4323 (Il Sanctus) reemplazan a las HD que ya no se usan.
#   - Forma 4318 (pueblo HD) a pantalla completa.
#   El codigo del juego no cambia (con --debug se agrega el gancho del banco de Ruffle).
import sys, os, struct, glob, hashlib, json
D = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(D)
sys.path.insert(0, os.path.join(W, 'paso5/tools')); sys.path.insert(0, D)
from swfpatch import Patcher
import zonas

# Preparacion (herramientas del paso 5):
#   python3 paso5/tools/swfsplit.py SONNY2_29-09.swf act1      (bca5eea5...)
#   python3 paso5/tools/swfcode.py  act1 act3
#   python3 paso5/tools/swfsplit.py paso5/SONNY2_recompilado.swf base1
P1 = os.path.join(W, 'act1')      # SONNY2.swf del usuario (29/09) separado con swfsplit
P3 = os.path.join(W, 'act3')      # y descompilado con swfcode
BASE1 = os.path.join(W, 'base1')  # juego base (paso 5): de ahi salen los fotogramas originales 1 y 16

def aplicar(p):
    """Cambios de I31 sobre un Patcher de act1/act3 (tambien lo usa I32)."""
    # 1) KrinScreen
    t = p.byid[2908]
    a = open(os.path.join(P1, 'tags', t['file']), 'rb').read()
    b = open(glob.glob(os.path.join(BASE1, 'tags', '*_DefineSprite_2908.bin'))[0], 'rb').read()
    p.replace[t['file']] = (39, zonas.build_sprite(a, b))
    p.log.append('sprite  2908 KrinScreen: PRISON y CITY originales; HD en TUNNELS y ROME')
    # 1b) Pueblo HD: la forma 4318 cubre ahora toda la pantalla
    t4320 = p.byid[4320]; t4318 = p.byid[4318]
    p.replace[t4318['file']] = (2, zonas.village_shape(open(os.path.join(P1, 'tags', t4320['file']), 'rb').read()))
    p.log.append('forma   4318 (pueblo HD): pantalla completa, sin la franja de 6 px a la derecha')
    # 2) Imagenes HD (DefineBitsJPEG2: id + JPEG)
    for cid, f in ((zonas.HD_TUNNELS[0], 'build/zona_TUNNELS_2560x1440.jpg'),
                   (zonas.HD_ROME[0], 'build/zona_ROME_2560x1440.jpg')):
        tt = p.byid[cid]
        assert tt['name'] == 'DefineBitsJPEG2'
        p.replace[tt['file']] = (21, struct.pack('<H', cid) + open(os.path.join(D, f), 'rb').read())
        p.log.append('imagen  %d <- %s' % (cid, f))


def main(out, debug=False):
    p = Patcher(P1, P3)
    aplicar(p)
    # 3) Gancho de depuracion (opcional)
    src = open(os.path.join(P3, 'scripts/escenario/frame_0042/DoAction_2.as'), encoding='utf-8').read()
    if debug:   # solo para el banco; sin --debug el script queda byte a byte igual
        p.script('escenario/frame_0042/DoAction_2.as',
                 src + '\n' + open(os.path.join(D, 'debug_hook.as'), encoding='utf-8').read())
    p.build(out)
    h = hashlib.sha256(open(out, 'rb').read()).hexdigest()
    print('\n'.join(p.log)); print(out, os.path.getsize(out), h)
    return h

if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    main(args[0], '--debug' in sys.argv)
