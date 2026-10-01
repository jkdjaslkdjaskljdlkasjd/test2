# Fondos de combate HD (desde I32; capas y diálogo desde I34)

## 1. Cómo es la pantalla de combate (fotograma 217, `KRINBATTLESCENE`)

| Profundidad | Pieza | Qué es |
|---|---|---|
| **58** | `__hdBattleBG` (4327, nuevo) | Fondo HD a pantalla completa, solo si el escenario tiene uno. Por dentro: el cielo (forma 4326, quieta) y `__hdGround` (sprite 4334 con la forma 4333 y el bitmap JPEG3 4332, que sigue a la cámara) |
| 59 | 3303 | Panel gris de arriba (se oculta con HD) |
| 60 | `UI_BAR` (2801) | Panel de abajo |
| 65 | 3308 | Parte del panel de abajo |
| 70 | 3309 | Ventana de combate con las bandas oscuras (se oculta con HD) |
| 72 | `__hdMask` (4328, antes la forma 213) | Máscara de la escena (`clipDepth` 340). Con HD pasa a cubrir toda la pantalla |
| 73 | 3328 | **Cielo** (`Krin.SkyBG`: SEA, JAIL, SNOW…). Se oculta con HD |
| 89 | `BATTLESCREEN` (3343) | **Suelo** (`Krin.ZoneBG`) y personajes. El zoom de cámara (`GridZoomer`) y el temblor (`GridShaker`) mueven y escalan este clip |
| 341 | `__hdMarco` (4330, antes la forma 3349) | Línea negra del borde de la ventana (se oculta con HD) |
| 342–432 | `p1BAR`…`p6BAR` | Barras de vida (quedan) |
| 480 | `battleClocker` | Panel de abajo: reloj y aliado |
| 484 | `krinToMove` | Panel de abajo: barra de habilidades |
| 498 | `krinToMove2` | Botón «!» |
| 628 | `moveSelectBoomer` | Efecto al elegir una habilidad |
| 634 | `combatScript` | Diálogo. El juego lo pone en (21,8 \| 473,3; 460,7); con HD, `__hdDialogo` lo pasa al 62 % |
| 644 / 646 | `__hdSkipX` / `__hdSkipXbg` (4329) | La X roja y su fondo |

El escenario se elige por **`Krin.ZoneBG`**, porque la imagen HD trae cielo y suelo juntos.

**Escenarios y cuántos combates tienen:**

| Escenario | Combates |
|---|---|
| JAIL | 18 |
| SNOW | 17 (`KBR51`–`53`, `200`–`205`, `211`, `212`…) |
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
   - el panel de abajo (60, 65, 480, 484, 498, 628, 644 y 646) se escala con `__hdBattleLayout = {s: 0.62, ax: 400, ay: 575, dy: -12}`: `x' = 400 + (x − 400)·0,62` e `y' = 575 − 12 + (y − 575)·0,62`. Es la misma medida que la barra de navegación de I22;
   - en cada fotograma corren `__hdCamSync` (cámara) y `__hdDialogo` (diálogo).
4. **No hace falta restaurar nada** al terminar: el fotograma 218 quita todas esas piezas, y el próximo combate las coloca de nuevo.
5. **El suelo original:** su envoltorio se oculta solo si `_root.__hdHideSuelo` es verdadero. Por eso funciona sin importar si su script corre antes o después de `__hdBattleSetup`.

**Interruptor:** `_root.__hdBattleEnabled = false` deja todos los combates clásicos.

## 3. Cámara: dos capas, como el original (I34)

**En el juego original:**
- el zoom de cada ataque (`GridZoomer` 3345: hasta ×1,193, hacia el objetivo, con `zoomRatioNEW = 0,4`) y el temblor (`GridShaker` 3344) mueven solo `BATTLESCREEN`, es decir, personajes y suelo;
- el cielo (3328), el marco y los paneles quedan quietos.

**En HD (`capas.py`) la imagen se separa en dos capas:**
- **cielo:** la imagen entera (bitmap 4325 y forma 4326). Queda quieta;
- **suelo** (`__hdGround`): la misma imagen, en JPEG3 con alfa 0 por encima del pie de las montañas. El borde se busca en cada columna: es la última fila con luminancia < 70 entre y 330 y 640 (a 2560x1440). Después:
  - se toma el percentil 20 móvil, con ventana 121, para quitar los picos de las piedritas;
  - se suaviza;
  - se sube 4 px;
  - se difumina 14 px.

  **El JPEG de la capa de suelo va premultiplicado por el alfa.** Si no, el reproductor dibuja un contorno claro en el difuminado.

**`__hdCamSync`** le copia al suelo la transformación de `BATTLESCREEN`: `x = B._x − B.saverX·k`, `y = B._y − B.saverY·k` y escala `100·k`. La llaman:
- el fotograma 4 de `GridZoomer`;
- los fotogramas 2, 4 y 5 de `GridShaker` (los cuatro con `p.script` en `build.py`);
- el `onEnterFrame` del contenedor.

En reposo las dos capas coinciden pixel por pixel.

Si un fondo no tiene capa de suelo, se mueve el contenedor entero con `R = 1,03`, como en I33. **No se recomienda.**

**Por qué el suelo no va dentro de `BATTLESCREEN`:** ahí taparía el panel de abajo (profundidades 60 y 65).

## 4. Agregar el siguiente fondo (ejemplo: JAIL)

1. **La imagen:** 2560x1440 (o 16:9 más chica; se amplía). Sin personajes, sin texto y sin nada importante abajo, donde va el panel. El suelo tiene que quedar donde se paran los personajes:

   | En el escenario | En 2560x1440 |
   |---|---|
   | Enemigos de atrás, y ≈ 230 | ≈ 575 px |
   | Los de adelante, y ≈ 420 | ≈ 1050 px |

   Conviene que el pie del fondo (paredes o montañas) se distinga bien del suelo.
2. **En `imagenes.py`:** agregar la imagen a `FONDOS`.
3. **En `capas.py`:** revisar el borde. Hay que correrlo y mirar `build/combate_X_suelo_vista.png`. Si el fondo no es oscuro, cambiar `UMBRAL`, `Y0` e `Y1`, o dibujar el borde a mano.
4. **En `batalla.py`:**
   - **`FONDOS`:** agregar `('JAIL', bitmap, forma, jpg, bitmap_suelo, forma_suelo, sprite_suelo)`, con ids nuevos. Hoy el último es 4334.
   - **`SUELOS`:** las colocaciones del suelo de ese escenario en BATTLESCREEN (3343). JAIL tiene tres (3331, 3333 y 3334), así que hay que pasar `SUELOS` a una lista de personajes por escenario.
5. **Compilar** con `python3 build.py SONNY2.swf`.
6. **Probar en Ruffle** con un combate de ese escenario (guion `banco/s_i34.json`, cambiando `BattlePick`).

## 5. Cosas a tener en cuenta

- **`blacker5` (686):** el fundido negro de las transiciones sigue con el ancho de I19-WS.
- **El texto «FPS»** de arriba a la izquierda es del juego (profundidades 632 y 633). No se tocó.
- **Las barras de los enemigos que mueren** hacen su fundido original. Ahora se ve sobre el cielo, por menos de un segundo.
