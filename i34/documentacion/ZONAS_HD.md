# Pantallas de zona y fondos HD (vigente desde I31)

Este documento explica cómo están armadas las pantallas de zona de Sonny 2 y cómo agregar una imagen HD a pantalla completa sin romper otra zona.

## 1. Qué zona usa qué fotograma

La pantalla de navegación coloca `KrinScreen` (sprite **2908**) en el fotograma 181 (`Navigation`), en la profundidad 59. Al cargar, hace `gotoAndStop(_root.Krin.zoneName[_root.Krin.sectionIn])`. El arreglo `Krin.zoneName` está en el fotograma 41.

| Zona | Nombre en el juego | Etiqueta | Fotograma de 2908 | Fondo en I31 |
|---|---|---|---|---|
| 1 | New Alcatraz: The Iron Prison | `PRISON` | 1 | Original (bitmap 2803, 764x414) |
| 2 | Oberursel: The Frozen Village | `VILLAGE` | 31 | **HD** (4317/4318) |
| 3 | Ivory Line: The Train | `TRAIN` | 46 | Original (2838) |
| 4 | Labyrinth | `TUNNELS` | 60 | **HD** (4319/4320) |
| 5 | Hew: The Dystopia | `CITY` | 16 | Original (2816, el Pawn Shop) |
| 6 | Il Sanctus | `ROME` | 73 | **HD** (4323/4324) |
| 7 | (Japón) | `JAPAN` | 110 | Original (vectorial) |
| — | NULL ZONE | `NULLZONE` | 191 | **HD** (4321/4322) |

`CASINO` (86), `UTOPIA` (98), `EDEN` (123), `STORM` (136) y `BETA` (147) existen, pero el juego no las usa.

## 2. Profundidades dentro de 2908

| Profundidad | Qué hay |
|---|---|
| 1 a 22 | El dibujo original de la zona (bitmap o vectores) |
| **26** | **Fondo HD a pantalla completa** (también es el fondo original de CITY y de TRAIN) |
| 27, 31, 35, 52, 56 y 58 | Anillos y marcadores (2807 y similares) |
| **47** | **Marco 2812** alrededor del dibujo original |
| 48 a 66 | Botones invisibles y zonas de clic de cada lugar |

En `JAPAN` la profundidad 26 la usa un anillo (2807), así que ahí no se puede poner un fondo HD sin moverlo.

## 3. La trampa: el salto hacia adelante y las profundidades ocupadas

Cuando el juego hace `gotoAndStop(zona)` hacia adelante, Flash ejecuta las etiquetas de **todos** los fotogramas intermedios. `KrinScreen` siempre arranca en el fotograma 1, así que:

- todo lo que un fotograma pone y no quita llega a los fotogramas siguientes;
- si un fotograma coloca algo (sin «move») en una profundidad ocupada, Flash **ignora** la colocación nueva y se queda con lo viejo.

**El bug de Hew (entre I30 y el SWF del 29/09):**
1. La cárcel HD se puso en la profundidad 26 del fotograma 1.
2. CITY (fotograma 16) coloca su fondo 2818 en la 26 sin quitar nada antes.
3. Resultado: la colocación de CITY se ignoraba y Hew mostraba la cárcel.

**Reglas:**
1. El fotograma de una zona que pone algo en la 26 tiene que quitar la 26 antes (`RemoveObject2 26`), salvo que el fotograma anterior ya la deje libre.
2. El primer fotograma **sin HD** que viene después de una zona HD tiene que quitar la 26. Si esa zona usa el marco, también tiene que reponer el 47 (`PlaceObject2 47, 2812`).
3. Una zona HD quita el marco 47, porque si no se vería encima de la imagen.
4. Con un salto hacia atrás, Flash reconstruye desde el fotograma 1, así que alcanza con que la cadena hacia adelante esté bien.

**La cadena en I31:**

| Fotograma | Qué hace con la 26 y el 47 |
|---|---|
| 1 PRISON | Pone el marco 47; la 26 queda libre (original) |
| 16 CITY | Pone 2818 en la 26 (original) |
| 31 VILLAGE | Quita 26 y 47; pone 4318 en la 26 |
| 46 TRAIN | Quita 26; repone 47; pone 2848 en la 26 |
| 60 TUNNELS | Quita 26 (ya lo hacía) y 47; pone 4320 en la 26 |
| 73 ROME | Quita 26; pone 4324 en la 26 |
| 86 CASINO | Quita 26; repone 47 (para JAPAN y las demás) |
| 191 NULLZONE | Quita 1 a 100; pone 4322 en la 26 |

## 4. Coordenadas de una imagen HD a pantalla completa

- **Área visible del juego a 16:9:** x de −111,11 a 911,11, y de 0 a 575 (la pantalla de 2560x1440 es esto ×2,504).
- **En coordenadas de 2908** (la zona está colocada en 400; 222,9), eso es x de −511,1 a 511,1 e y de −222,9 a 352,1.
- **La forma** (DefineShape, relleno de bitmap recortado, tipo 0x41) tiene:
  - el rectángulo (−10222, −4458) – (10222, 7042) en twips;
  - la matriz del bitmap ×7,98593 en x y ×7,98611 en y;
  - una imagen de 2560x1440.

  Las formas 4320, 4322 y 4324 son idénticas, salvo el id del bitmap. Desde I31, 4318 también.
- **Colocación:** `PlaceObject2` en la profundidad 26, con matriz identidad.

## 5. Cómo agregar la próxima imagen HD

1. **La imagen:** 2560x1440 (16:9), PNG o JPG, sin los anillos dibujados (los pone el juego). Si viene más chica, `imagenes.py` la amplía con Lanczos.
2. **Ids:** agregar un `DefineBitsJPEG2` nuevo y su forma (copia de 4320 con el id del bitmap cambiado) **antes** de la etiqueta del sprite 2908, o reutilizar un par libre.
3. **En `zonas.py`:** en el fotograma de la zona, quitar la 26 (y la 47) y poner la forma en la 26. Después, revisar la regla 2 en el fotograma siguiente.
4. **Probar en Ruffle** entrando a la zona desde la cárcel y yendo a la zona siguiente:

   ```
   dbg call _root.KrinScreen.gotoAndStop PRISON
   dbg call _root.KrinScreen.gotoAndStop <ZONA>
   ```

**Casos especiales:**
- **Hew (CITY):** su fondo original ya está en la 26, así que la HD reemplaza 2818 en esa misma colocación.
- **Japón:** antes hay que mover el anillo de la profundidad 26.

## 6. Ids de imágenes agregadas (I31)

| Bitmap | Forma | Uso |
|---|---|---|
| 4317 | 4318 | Pueblo HD (Zona 2), desde I19-WS |
| 4319 | 4320 | **Labyrinth HD (Zona 4)**. Antes era el Pawn Shop HD de Hew, que se retiró |
| 4321 | 4322 | NULL ZONE HD, desde I23 |
| 4323 | 4324 | **Il Sanctus HD (Zona 6)**. Antes era la cárcel HD del 29/09, que se retiró |

## 7. Los reflejos de los costados

La capa `__wsFondo` (profundidad −16384) captura la pantalla cada vez que cambia la zona, el menú o el combate, y la muestra borrosa a los costados del área de 800. Las zonas sin HD la muestran, como el tren y ahora la cárcel. Las zonas HD la tapan, porque la imagen cubre toda la pantalla. `__rw2kApply` (I30) la oculta con el menú de habilidades abierto. No hace falta tocarla para agregar una zona HD.
