# Simula como Flash/AIR recorre KrinScreen (sprite 2908) al entrar a cada zona desde el fotograma 1:
# un salto hacia adelante ejecuta las etiquetas de todos los fotogramas intermedios, y una colocacion (sin "move")
# en una profundidad ocupada SE IGNORA. Ruffle no lo reproduce: esta simulacion es la prueba de la regla de la 26.
#   python3 simular_2908.py CARPETA_SWFSPLIT [CARPETA_SWFSPLIT ...]
# Imprime, por zona, que queda en la profundidad 26 (fondo HD o fondo original) y en la 47 (marco 2812).
import sys, os, glob, struct
D = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(D)
sys.path.insert(0, os.path.join(W, 'paso5/tools')); sys.path.insert(0, os.path.join(W, 'i31'))
import zonas

def sim(path):
    b = open(glob.glob(path + '/tags/*_DefineSprite_2908.bin')[0], 'rb').read()
    F = zonas.frames_of(zonas.raw_tags(b))
    labels = {}
    for n, fr in enumerate(F):
        for t in fr:
            if t[0] == 43:
                labels[t[1].rstrip(b'\0').decode()] = n
    res = {}
    for lab in ('PRISON', 'CITY', 'VILLAGE', 'TRAIN', 'TUNNELS', 'ROME', 'JAPAN', 'NULLZONE'):
        dl = {}
        for n in range(labels[lab] + 1):
            for t in F[n]:
                code, bd = t[0], t[1]
                if code in (26, 70):
                    f = bd[0]; i = 1 + (1 if code == 70 else 0); d = struct.unpack_from('<H', bd, i)[0]; i += 2
                    c = struct.unpack_from('<H', bd, i)[0] if f & 2 else None
                    if f & 1:
                        if d in dl and c:
                            dl[d] = c
                    elif d not in dl:
                        dl[d] = c
                elif code == 28:
                    dl.pop(struct.unpack_from('<H', bd, 0)[0], None)
        res[lab] = (dl.get(26), dl.get(47))
    return res

if __name__ == '__main__':
    rs = [sim(p) for p in sys.argv[1:]]
    print('zona      ' + ''.join('%-22s' % os.path.basename(p.rstrip('/')) for p in sys.argv[1:]) + '  (prof. 26, prof. 47)')
    for k in rs[0]:
        print('%-9s ' % k + ''.join('%-22s' % (r[k],) for r in rs))
