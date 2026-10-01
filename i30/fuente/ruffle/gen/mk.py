# Genera guiones para drive.js con la pagina 16:9 (page16.html, 1280x720).
# Coordenadas de _root -> pantalla: escala 720/575, x desde -111.11.
import json, sys
S = 720 / 575.0
def sc(x, y):
    return [round((x + 111.11) * S), round(y * S)]
def inicio(nivel=20, puntos=40):
    return [{"wait": 55000}, {"click": sc(765, 17.6)}, {"wait": 1500}, {"click": sc(400, 541.5)}, {"wait": 1500},
            {"click": sc(400, 541.5)}, {"waitdbg": 60000}, {"wait": 3000},
            {"dbg": "set _root.Krin.slotInUse 1"}, {"dbg": "go classMenu"}, {"wait": 3000},
            {"click": sc(400, 473.6)}, {"wait": 4000}, {"dbg": "go Navigation"}, {"wait": 6000},
            {"dbg": "set _root.Krin.Level %d" % nivel}, {"dbg": "set _root.Krin.skillPoints %d" % puntos}]
def aprender(ids):
    return [{"dbg": "call _root.__rwLearn %d" % i} for i in ids]
def guardar(pasos, nombre):
    json.dump(pasos, open(nombre, 'w'))
