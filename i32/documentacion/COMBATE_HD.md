# Fondos de combate HD (desde I32)

## 1. Cómo es la pantalla de combate (fotograma 217, `KRINBATTLESCENE`)

| Profundidad | Pieza | Qué es |
|---|---|---|
| **58** | `__hdBattleBG` (4327, nuevo) | Fondo HD a pantalla completa, solo si el escenario tiene uno |
| 59 | 3303 | Panel gris de arriba (se oculta con HD) |
| 60 | `UI_BAR` (2801) | Panel de abajo |
| 65 | 3308 | Parte del panel de abajo |
| 70 | 3309 | Ventana de combate con las bandas oscuras (se oculta con HD) |
| 72 | `__hdMask` (4328, antes la forma 213) | Máscara de la escena (`clipDepth` 340). Con HD pasa a cubrir toda la pantalla |
| 73 | 3328 | **Cielo** (`Krin.SkyBG`: SEA, JAIL, SNOW…). Se oculta con HD |
| 89 | `BATTLESCREEN` (3343) | **Suelo** (`Krin.ZoneBG`) y personajes. El zoom de cámara (`GridZoomer`) mueve y escala este clip |
| 341 | `__hdMarco` (4330, antes la forma 3349) | Línea negra del borde de la ventana (se oculta con HD) |
| 342–432 | `p1BAR`…`p6BAR` | Barras de vida (quedan) |
| 480 | `battleClocker` | Panel de abajo: reloj y aliado |
| 484 | `krinToMove` | Panel de abajo: barra de habilidades |
| 498 | `krinToMove2` | Botón «!» |
| 628 | `moveSelectBoomer` | Efecto al elegir una habilidad |
| 634 | `combatScript` | Diálogo (el juego lo ubica a y = 460,7; no se mueve) |
| 644 / 646 | `__hdSkipX` / `__hdSkipXbg` (4329) | La X roja y su fondo |

El escenario se elige por **`Krin.ZoneBG`**, porque la imagen HD trae cielo y suelo juntos.

**Escenarios y cuántos combates tienen:**

| Escenario | Combates |
|---|---|
| JAIL | 18 |
| SNOW | 17 |
| STREETS | 17 |
| TUNNEL | 15 |
| TRAIN | 13 |
| CHURCH | 11 |
| STREETS2 | 5 |
| CHURCH2, STREETS3 y WHITE NOVEMBER | 1 cada uno |

## 2. Qué hace `__hdBattleSetup` (`hd_batalla.as`)

1. Lo llama el fotograma 1 de `__hdBattleBG` cuando se coloca, en cada combate. Para entonces todas las piezas del fotograma 217 ya existen.
2. Hace `gotoAndStop(Krin.ZoneBG)`:
   - si no existe esa etiqueta, queda en el fotograma 1, se oculta y el combate es **clásico**;
   - si existe, el combate es **HD**.
3. **Con HD:**
   - oculta 59, 70 y 73, `__hdMarco` y `BATTLESCREEN.__hdSuelo` (el suelo original);
   - la máscara pasa a x −111,11, y 0, 1022,22 × 575;
   - el panel de abajo (60, 65, 480, 484, 498, 628, 644 y 646) se escala con `__hdBattleLayout = {s: 0.62, ax: 400, ay: 575, dy: -12}`: `x' = 400 + (x − 400)·0,62` e `y' = 575 − 12 + (y − 575)·0,62`. Es la misma medida que la barra de navegación de I22.
4. **No hace falta restaurar nada** al terminar: el fotograma 218 quita todas esas piezas, y el próximo combate las coloca de nuevo.
5. **El suelo:** su envoltorio se oculta solo si `_root.__hdHideSuelo` es verdadero. Por eso funciona sin importar si su script corre antes o después de `__hdBattleSetup`.

**Interruptor:** `_root.__hdBattleEnabled = false` deja todos los combates clásicos.

## 3. Agregar el siguiente fondo (ejemplo: JAIL)

1. **La imagen:** 2560x1440 (o 16:9 más chica; se amplía). Sin personajes, sin texto y sin nada importante abajo, donde va el panel. El suelo tiene que quedar donde se paran los personajes:

   | En el escenario | En 2560x1440 |
   |---|---|
   | Enemigos de atrás, y ≈ 230 | ≈ 575 px |
   | Los de adelante, y ≈ 420 | ≈ 1050 px |

2. **En `imagenes.py`:** agregar la imagen a `FONDOS`.
3. **En `batalla.py`:**
   - **`FONDOS`:** agregar `('JAIL', id_bitmap, id_forma, 'build/combate_JAIL_2560x1440.jpg')`, con ids nuevos y libres. Hoy el último es 4331.
   - **`SUELOS`:** las colocaciones del suelo de ese escenario en BATTLESCREEN (3343). JAIL tiene tres (3331, 3333 y 3334), así que hay que envolver las tres: cambiar `SUELOS` por una lista de personajes por escenario. SNOW tiene una sola (3335).
4. **Compilar** con `python3 build.py SONNY2.swf`.
5. **Probar en Ruffle:** `set _root.KBR103.ZoneBG JAIL` y `go LOADBATTLESCENE` (guion `banco/s_batalla2560.json`).

## 4. Cosas a tener en cuenta

- **El fondo HD no hace zoom:** el zoom de cámara escala solo `BATTLESCREEN` (personajes y suelo). El cielo original tampoco hacía zoom. Si se quiere que la imagen siga al zoom, hay que meterla dentro de `BATTLESCREEN`, pero entonces tapa el panel de abajo (profundidades 60 y 65).
- **`blacker5` (686):** el fundido negro de las transiciones sigue con el ancho de I19-WS.
- **El texto «FPS»** de arriba a la izquierda es del juego (profundidades 632 y 633). No se tocó.
