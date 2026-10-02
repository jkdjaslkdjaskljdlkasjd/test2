# Fondos de combate HD (desde I32; capas y diálogo desde I34; zoom suave desde I35; arreglo para AIR desde I36; estructuras con el suelo desde I37; sin pérdida desde I38)

**Desde I36 solo están activos JAIL y SNOW** (`capas.ACTIVOS` y `__hdBattleMap`). El resto de los combates es clásico.

## 1. Cómo es la pantalla de combate (fotograma 217, `KRINBATTLESCENE`)

| Profundidad | Pieza | Qué es |
|---|---|---|
| **58** | `__hdBattleBG` (4325) | Fondo HD a pantalla completa. Tiene un fotograma por imagen activa (JAIL y SNOW). Cada uno quita primero las profundidades 1 y 2 y después coloca: el cielo (forma quieta) y `__hdGround` (sprite con la forma del suelo y su bitmap JPEG3, que sigue a la cámara). Los ids van desde 4341, cinco por imagen |
| 59 | 3303 | Panel gris de arriba (se oculta con HD) |
| 60 | `UI_BAR` (2801) | Panel de abajo |
| 65 | 3308 | Parte del panel de abajo |
| 70 | 3309 | Ventana de combate con las bandas oscuras (se oculta con HD) |
| 72 | `__hdMask` (4326, antes la forma 213) | Máscara de la escena (`clipDepth` 340). Con HD pasa a cubrir toda la pantalla |
| 73 | 3328 | **Cielo** (`Krin.SkyBG`: SEA, JAIL, SNOW…). Se oculta con HD |
| 89 | `BATTLESCREEN` (3343) | **Suelo** (`Krin.ZoneBG`) y personajes. El zoom de cámara (`GridZoomer`) y el temblor (`GridShaker`) mueven y escalan este clip |
| 341 | `__hdMarco` (4328, antes la forma 3349) | Línea negra del borde de la ventana (se oculta con HD) |
| 342–432 | `p1BAR`…`p6BAR` | Barras de vida (quedan) |
| 480 | `battleClocker` | Panel de abajo: reloj y aliado |
| 484 | `krinToMove` | Panel de abajo: barra de habilidades |
| 498 | `krinToMove2` | Botón «!» |
| 628 | `moveSelectBoomer` | Efecto al elegir una habilidad |
| 634 | `combatScript` | Diálogo. El juego lo pone en (21,8 \| 473,3; 460,7); con HD, `__hdDialogo` lo pasa al 62 % |
| 644 / 646 | `__hdSkipX` / `__hdSkipXbg` (4327) | La X roja y su fondo |

**Cómo se elige la imagen:** cada combate la elige por su suelo y su cielo, con `_root.__hdBattleMap[Krin.ZoneBG + "|" + Krin.SkyBG]`. Si no está en la tabla, el combate es clásico. Hay 12 combinaciones en el juego; hoy están activas solo `JAIL|JAIL` y `SNOW|SNOW`:

| Suelo \| cielo | Imagen |
|---|---|
| CHURCH \| CHURCH | CHURCH |
| CHURCH \| ROME | ROME |
| CHURCH2 \| CHURCH | CHURCH |
| **JAIL \| JAIL** | **JAIL** |
| **SNOW \| SNOW** | **SNOW** |
| STREETS \| STREETS | STREETS |
| STREETS \| TUNNEL | STREETS |
| STREETS2 \| STREETS | STREETS2 |
| STREETS3 \| STREETS3 | STREETS3 |
| TRAIN \| TRAIN | TRAIN |
| TUNNEL \| TUNNEL | TUNNEL |
| WHITE NOVEMBER \| SEA | SEA |

**Suelos originales ocultos con HD:** los personajes 3330, 3331, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341 y 3342 de BATTLESCREEN.
- Cada uno va en su envoltorio (4329–4340), con el nombre `__hdSuelo<personaje>`. La lista está en `_root.__hdSueloNames`.
- En STREETS3, el «move» que cambiaba de personaje pasa a quitar y volver a poner.
- Los objetos de CHURCH2 (1788, 1792…1806) se dejan visibles.

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
2. Busca la imagen en `__hdBattleMap[Krin.ZoneBG + "|" + Krin.SkyBG]`:
   - si no hay, queda en el fotograma 1, se oculta y el combate es **clásico**;
   - si hay, hace `gotoAndStop(imagen)` y el combate es **HD**.

   **Trampa (I36):** `gotoAndStop` hacia adelante recorre todos los fotogramas intermedios, y Flash/AIR **ignora una colocación en una profundidad ocupada**. Por eso cada fotograma de imagen empieza con `RemoveObject2` de las profundidades 1 y 2. Sin eso, en AIR siempre quedaba la imagen del primer fotograma (CHURCH en I35). Ruffle no reproduce este comportamiento, así que no sirve para probarlo.
3. **Con HD:**
   - oculta 59, 70 y 73, `__hdMarco` y los `BATTLESCREEN.__hdSuelo*` (el suelo original);
   - la máscara pasa a x −111,11, y 0, 1022,22 × 575;
   - el panel de abajo (60, 65, 480, 484, 498, 628, 644 y 646) se escala con `__hdBattleLayout = {s: 0.62, ax: 400, ay: 575, dy: -12}`: `x' = 400 + (x − 400)·0,62` e `y' = 575 − 12 + (y − 575)·0,62`. Es la misma medida que la barra de navegación de I22;
   - en cada fotograma corren `__hdCamSync` (cámara) y `__hdDialogo` (diálogo).
4. **No hace falta restaurar nada** al terminar: el fotograma 218 quita todas esas piezas, y el próximo combate las coloca de nuevo.
5. **El suelo original:** su envoltorio se oculta solo si `_root.__hdHideSuelo` es verdadero. Por eso funciona sin importar si su script corre antes o después de `__hdBattleSetup`.

**Interruptor:** `_root.__hdBattleEnabled = false` deja todos los combates clásicos.

## 3. Cámara: dos capas, como el original (I34, corregido en I37)

**En el juego original:**
- el zoom de cada ataque (`GridZoomer` 3345: hasta ×1,193, hacia el objetivo, con `zoomRatioNEW = 0,4`) y el temblor (`GridShaker` 3344) mueven solo `BATTLESCREEN`: personajes, suelo **y las estructuras cercanas** (en JAIL, los edificios de los costados);
- el cielo (3328) es solo **lo lejano**: cielo y horizonte (en JAIL, la ciudad del fondo). Queda quieto, igual que el marco y los paneles.

**La regla para cada imagen HD:** lo lejano (cielo, montañas, ciudad del horizonte) va en la capa quieta; lo cercano (piso, paredes, edificios, pilares, rejas) va en la capa del suelo. Si una estructura cercana queda en la capa quieta, el piso se desliza sobre ella en el zoom y parece pegada a una imagen (video del usuario, I36).

**En HD (`capas.py`) la imagen se separa en dos capas:**
- **cielo** (forma quieta): la imagen entera o, si el borde lo pide, la imagen con lo cercano reemplazado por cielo (`relleno_cielo`, ver abajo);
- **suelo** (`__hdGround`): la misma imagen, en JPEG3 con alfa 0 por encima del borde. **Desde I38 las dos capas van sin pérdida** (`DefineBitsLossless2`, `calidad.py`), y no en JPEG2/JPEG3. **El color de la capa de suelo va premultiplicado por el alfa.** Si no, el reproductor dibuja un contorno claro en el difuminado.

**Tipos de borde (`capas.BORDES`):**
- `('oscuro', umbral, y0, y1)` (SNOW): en cada columna, la última fila con luminancia < umbral entre y0 e y1 (el pie de las montañas). Después: percentil 20 móvil con ventana 121 (quita los picos de las piedritas), suavizado, 4 px hacia arriba y fundido de 14 px;
- `('claro', umbral, y0, y1)`: la primera fila clara del suelo;
- `('linea', y)`: un borde recto;
- `('puntos', [(x, y), …], margen)`: un borde a mano;
- `('poligono', [(x, y), …], margen, fundido, relleno)` (JAIL, I37): el contorno de lo cercano, a mano. Admite saltos verticales (dos puntos con x seguidos, como `(751, 512), (752, 612)` para la pared de adentro de un edificio). Con `relleno = True`, la capa quieta se arma con `relleno_cielo()`.

**JAIL (I37):** el contorno se midió cada 50 px como el primer borde fuerte desde arriba (gradiente vertical > 45). El techo es levemente curvo: con una recta quedaba hasta 8 px corrido.
- **Techo izquierdo:** de (0, 186) a (700, 483).
- **Pared de adentro:** x = 751.
- **Centro:** 612, el pie de la ciudad.
- **Pared derecha:** x = 1808.
- **Techo derecho:** hasta (2560, 192).
- **Margen y fundido:** margen −3, para incluir la línea negra del techo, y fundido de 4 px.

**`relleno_cielo(im, b)`:**
- **Qué rellena:** en cada fila, los píxeles bajo el borde, desde los costados hacia adentro. Toman el color del cielo de esa misma fila, 14 px hacia el centro desde el borde, para no tomar la línea del techo.
- **Suavizado:** después, solo la parte rellenada se suaviza (gaussiana σ 6).
- **Lo que no se toca:** las filas que son suelo de punta a punta quedan como estaban.
- **Por qué hace falta:** si la capa quieta conserva el edificio, el zoom lo mueve en la capa del suelo y deja ver el viejo detrás, como un «fantasma».
- **Qué no es:** no es una imagen generada; son los colores del cielo de la misma imagen, estirados. Solo se ve en franjas finas durante el zoom.
- **Cuándo no alcanza:** para estructuras grandes que dejan huecos grandes (pilares hasta el piso), pedirle al usuario una versión «solo fondo» de la imagen.

**`__hdCamSync`** le copia al suelo la transformación de `BATTLESCREEN`: `x = B._x − B.saverX·k`, `y = B._y − B.saverY·k` y escala `100·k`. La llaman:
- el fotograma 4 de `GridZoomer`;
- los fotogramas 2, 4 y 5 de `GridShaker` (los cuatro con `p.script` en `build.py`);
- el `onEnterFrame` del contenedor.

En reposo las dos capas coinciden pixel por pixel.

**Por qué el suelo no va dentro de `BATTLESCREEN`:** ahí taparía el panel de abajo (profundidades 60 y 65).

## 3b. Zoom más suave en HD (I35)

Al final del fotograma 2 de `GridZoomer` (3345), cuando `__hdBattleOn` es verdadero, `zoomPointX/Y` y `zoomScaleX/Y` se multiplican por `_root.__hdZoomF`, que vale 0,5. Así el zoom máximo baja de ×1,193 a ×~1,097, y la traslación también se reduce a la mitad. El objetivo sigue quedando casi fijo. El temblor no cambia.

## 3c. Calidad en el zoom (I36)

Si la opción SFX3 está apagada, `GridZoomer` (3345) pone `_root._quality = "LOW"` en sus fotogramas 2 y 6 mientras dura el zoom, y la vuelve a `KrinSettings.QUALITY` al terminar. En LOW, Flash dibuja los bitmaps sin suavizado: la imagen HD se pixela. En los combates HD, al final de esos dos scripts se vuelve a `KrinSettings.QUALITY` (`CALIDAD` en `build.py`).

**Imágenes:** JPEG 95 con color completo (`subsampling=0`). Las dos capas se codifican desde el PNG original.

**CHURCH y ROME:** los pilares llegan hasta el piso, así que van enteros en la capa del suelo, y detrás de ellos hace falta fondo. Probablemente haga falta una versión «sin pilares» de la imagen.

## 4. Cambiar o agregar un fondo

1. **La imagen:** `fuente/imagenes/combate_<ETIQUETA>.png`, de 2560x1440 (o 16:9 más chica; se amplía). Sin personajes, sin texto y sin nada importante abajo, donde va el panel. El suelo tiene que quedar donde se paran los personajes:

   | En el escenario | En 2560x1440 |
   |---|---|
   | Enemigos de atrás, y ≈ 230 | ≈ 575 px |
   | Los de adelante, y ≈ 420 | ≈ 1050 px |

2. **`imagenes.py`:** toma todas las imágenes solas.
3. **En `capas.py`:** agregar o ajustar la entrada en `BORDES`, separando lo lejano de lo cercano (ver 3), y agregar la etiqueta a `ACTIVOS`. Después, `python3 capas.py` dibuja `build/capas_vista.png` (el magenta es lo que queda quieto) y, con relleno, `build/combate_<X>_cielo.png` (la capa quieta).
4. **En `batalla.py`:** los ids se reparten solos, cinco por imagen desde 4341.
5. **En `hd_batalla.as`:** agregar o descomentar la combinación en `__hdBattleMap`.
6. **Compilar** con `python3 build.py SONNY2.swf`.
7. **Probar en Ruffle:**
   - `set _root.KBR103.ZoneBG X`, `set _root.KBR103.SkyBG Y` y `go LOADBATTLESCENE` (guion `banco/s_i37.json`, con capturas cada 120 ms durante un ataque);
   - para ver las capas del original: `banco/s_orig_jail.json` (HD apagado y `BATTLESCREEN` oculto);
   - Ruffle **no** muestra el bug de profundidades de AIR.

## 5. Cosas a tener en cuenta

- **`blacker5` (686):** el fundido negro de las transiciones sigue con el ancho de I19-WS.
- **El texto «FPS»** de arriba a la izquierda es del juego (profundidades 632 y 633). No se tocó.
- **Las barras de los enemigos que mueren** hacen su fundido original. Ahora se ve sobre el cielo, por menos de un segundo.
