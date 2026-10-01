from rwbench import RW
import time
t0 = time.time()
b = RW()
print('carga', round(time.time() - t0, 1), 's')
w = b.unit(1, 'Sonny', STR=100, MAG=60, SPD=70)
e = b.unit(2, 'Brute', STR=80, SPD=50)
e2 = b.unit(4, 'Grunt', STR=80, SPD=50)
al = b.unit(3, 'Veradux', STR=90, SPD=60)
for sid, r in [(811, 2), (814, 2), (861, 3), (810, 2), (812, 2), (831, 2), (865, 3), (815, 3), (816, 2)]:
    b.learn(sid, r)
b.start()
print('rangos', [(s, b.rank(s)) for s in (861, 811, 814, 831)])
print('Rake ->', b.cast(861, 2), b.st(2))
print('Rake ->', b.cast(861, 2), b.st(2))
print('tick enemigo ->', b.tick(2), b.st(2))
print('Rupture ->', b.cast(831, 2), b.st(2))
print('Wicked ->', b.cast(865, 2), b.st(2))
print('texto Rake 3:', b.text(861, 3))
