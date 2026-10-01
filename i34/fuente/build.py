# I34 - fondos de combate HD (Oberursel / SNOW) sobre I31: cielo quieto y suelo que sigue la camara, como el
#       original; dialogo al 62 % sobre su cuadro.
#
#   python3 build.py SALIDA.swf [--debug]
#
# Parte del mismo origen que I31 (SONNY2.swf del usuario del 29/09 separado en act1/act3), aplica I31
# (i31/build.py) y suma:
#   - batalla.py: imagen HD, contenedor __hdBattleBG, mascara de la escena como sprite y la X nombrada;
#   - hd_batalla.as: la capa que arma el combate HD (se agrega al final de DoAction_2).
import sys, os, hashlib
D = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(D)
sys.path.insert(0, os.path.join(W, 'paso5/tools')); sys.path.insert(0, D); sys.path.insert(0, os.path.join(W, 'i31'))
from swfpatch import Patcher
import batalla
import importlib.util
_s = importlib.util.spec_from_file_location('i31build', os.path.join(W, 'i31', 'build.py'))
i31 = importlib.util.module_from_spec(_s); _s.loader.exec_module(i31)

def main(out, debug=False):
    p = Patcher(i31.P1, i31.P3)
    i31.aplicar(p)
    batalla.aplicar(p, i31.P1)
    src = open(os.path.join(i31.P3, 'scripts/escenario/frame_0042/DoAction_2.as'), encoding='utf-8').read()
    src += '\n' + open(os.path.join(D, 'hd_batalla.as'), encoding='utf-8').read()
    if debug:
        src += '\n' + open(os.path.join(W, 'i31', 'debug_hook.as'), encoding='utf-8').read()
    p.script('escenario/frame_0042/DoAction_2.as', src)
    # camara: el zoom (GridZoomer, 3345) y el temblor (GridShaker, 3344) avisan a la imagen HD en el mismo fotograma
    for ref in ('DefineSprite_3345/frame_0004/DoAction.as', 'DefineSprite_3344/frame_0002/DoAction.as',
                'DefineSprite_3344/frame_0004/DoAction.as', 'DefineSprite_3344/frame_0005/DoAction.as'):
        s0 = open(os.path.join(i31.P3, 'scripts', ref), encoding='utf-8').read()
        p.script(ref, s0 + '\nif(_root.__hdCamSync)\n{\n   _root.__hdCamSync();\n}\n')
    p.build(out)
    h = hashlib.sha256(open(out, 'rb').read()).hexdigest()
    print('\n'.join(p.log)); print(out, os.path.getsize(out), h)
    return h

if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    main(args[0], '--debug' in sys.argv)
