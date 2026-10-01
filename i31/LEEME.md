# Sonny 2 a 16:9: I31 (fondos HD de zona)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I31) | `0197c81640fc109a6d9d43ad2fe566f4c67af92263eedfc6552971ca63123c26` |
| Base: tu `SONNY2.swf` del 29/09 | `bca5eea5412e7111d0d90adf27989a03dfab39c87e75f0e19a52d539fe8beef6` |

Para instalar, reemplaza solo `SONNY2.swf` en `SonnyLegacy.app/Contents/Resources/` (guarda una copia del anterior). El lanzador es el mismo y las partidas siguen sirviendo.

La entrega pesa más de 30 MB, así que va en dos zips:
- **parte 1:** `SONNY2.swf` y este `LEEME.md`;
- **parte 2:** este `LEEME.md`, `documentacion/`, `fuente/` y `capturas/`.

## Cambios respecto de tu SWF del 29/09

| Zona | Nombre | Antes | Ahora |
|---|---|---|---|
| 1 | New Alcatraz: The Iron Prison | Imagen HD de la cárcel | **Arte original** (como el tren) |
| 2 | Oberursel | Pueblo HD | Pueblo HD, con una franja de 6 px a la derecha corregida |
| 3 | Ivory Line | Original | Sin cambios |
| 4 | Labyrinth | Original | **HD con tu imagen** |
| 5 | Hew: The Dystopia | **Mostraba la cárcel HD (bug)** | **Arte original** |
| 6 | Il Sanctus | Original | **HD con tu imagen** |
| 7 y NULL ZONE | | | Sin cambios |

### Zona 1: la cárcel vuelve al original

- Se quitó la imagen HD de la cárcel. La zona queda igual que en el juego, con el marco y los reflejos borrosos a los costados, como el tren (`01_zona1_prision_original.jpg`).
- La imagen retirada no se pierde: está en `fuente/imagenes/retiradas/`.

### Zona 5 (Hew): el bug de la imagen de la cárcel

**Qué pasaba:** al agregar la cárcel HD, se puso la imagen en la profundidad 26 del fotograma de la Zona 1. Hew usa esa misma profundidad para su fondo, pero no la vaciaba antes de poner el suyo. En Flash, si una profundidad está ocupada, la colocación nueva se ignora. Por eso Hew mostraba la cárcel (`00_antes_hew_con_la_carcel.jpg`).

**Arreglo:**
- los fotogramas de la Zona 1 y de Hew vuelven a ser exactamente los del juego base;
- Hew muestra su arte original, como pediste (`02_zona5_hew_original.jpg`). También se retiró la imagen HD del Pawn Shop que se había puesto en I23. Está en `fuente/imagenes/retiradas/` por si la quieres de vuelta.
- Se probó entrando a Hew justo después de la cárcel, que era el camino del bug (`07_hew_despues_de_prision.jpg`).

### Zonas 4 y 6: Labyrinth e Il Sanctus en HD

- Entran igual que el pueblo: la imagen cubre toda la pantalla de 2560x1440 y queda debajo de los anillos y de los botones del juego (`03_zona4_labyrinth_hd.jpg` y `04_zona6_il_sanctus_hd.jpg`).
- **Il Sanctus:** se usó tu imagen de 2560x1440 tal cual.
- **Labyrinth:** la imagen mide 1672x941, así que se amplió a 2560x1440 con Lanczos y un enfoque suave. Si tienes una versión más grande, la cambio directamente.
- Al salir de Il Sanctus hacia la Zona 7, la imagen se quita y vuelve el marco (`08_zona7_despues_de_il_sanctus.jpg`).
- **Los anillos los pone el juego en su lugar original.** Como tus imágenes tienen otro encuadre que el original, los anillos quedan donde estaban: en Labyrinth, sobre el agua, en el túnel y junto al cartel; en Il Sanctus, sobre las ruinas y el templo. Mira las capturas. Si quieres alguno en otro lugar, se puede mover.

### Pueblo HD: franja de 6 px

La forma del pueblo HD (4318, de I23) quedaba 2,5 unidades corta a la derecha y 1,15 abajo. A 2560x1440 se veía una franja oscura de 6 px en el borde derecho. Ahora usa la misma medida de pantalla completa que las demás. La imagen y su posición no cambian.

## Revisión del código que tocó ChatGPT

Comparé tu SWF del 29/09 con la fuente de I30 de la repo.

- **Código del juego, sin cambios.** El script principal (`DoAction_2`, el rework I26–I30) da **byte por byte** el mismo resultado que compilar la fuente de `i30/fuente/src/`. El reloj de combate y los demás scripts también coinciden con lo documentado en I19–I30. No hay código agregado por fuera de las versiones.
- **El único cambio sin documentar** era la cárcel HD:
  - la imagen 4323 y la forma 4324;
  - la colocación en la profundidad 26 del fotograma 1 de la pantalla de zona (sprite 2908), quitando el marco 2812.

  Ese cambio es el que causó el bug de Hew. I31 lo deshace.
- Todo lo demás que difiere del juego base corresponde a versiones documentadas:
  - los rectángulos a 1060 y la barra al 62 % (16:9);
  - el panel de combate;
  - los íconos de prueba de I26;
  - el menú 2K de I30.

Las habilidades no se tocaron.

## Probado (Ruffle, página 16:9, 2560x1440)

- se recorrieron todas las zonas: 1, 5, 4, 6, 2, 3 y 7;
- se entró a Hew después de la cárcel y a la Zona 7 después de Il Sanctus;
- el borde derecho del pueblo ya no tiene franja (la columna 2560 tiene el color de la imagen).

Falta probarlo en tu app (AIR).

## Fuente (`fuente/`)

- **`build.py`:** `python3 build.py SONNY2_I31.swf` arma el SWF desde tu SWF del 29/09 con las herramientas del paso 5. Da siempre el mismo SHA. Con `--debug` suma el gancho del banco de Ruffle.
- **`zonas.py`:** reescribe la pantalla de zona (sprite 2908) y la forma del pueblo.
- **`imagenes.py`:** prepara las imágenes HD a 2560x1440.
- **`imagenes/`:** tus dos imágenes originales y, en `retiradas/`, la cárcel HD y el Pawn Shop HD.
- **`banco/s_zonas2560.json`:** el guion de las capturas, para `drive.js` de la repo.

## Documentación (`documentacion/`)

- **`ZONAS_HD.md`:** cómo están armadas las pantallas de zona y cómo agregar una imagen HD sin repetir el bug. Esta documentación no existía.
- **`TRASPASO.md`:** el traspaso de la repo actualizado a I31.
- **`estado-mod-sonny.md`:** el estado del proyecto de la repo, actualizado con I31.

## Lo que sigue

- Probar I31 en tu app.
- **Faltan imágenes HD para:**
  - la Zona 1 (cuando tengas la cárcel definitiva);
  - Hew;
  - la Zona 3 (tren);
  - la Zona 7 (Japón);
  - los fondos de combate.

  Cada una entra igual que Labyrinth e Il Sanctus.
