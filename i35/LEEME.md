# Sonny 2 a 16:9: I35 (los 10 fondos de combate en HD)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I35) | `5d5a9bebb5f39843f0fd69d92cddb579aee3eb32a0b72dd078388eb9288e576e` |
| Base: I34 | `410c3be60574e40591825f3bf20a86118cdcd308eb3ab3c5b8f5eca511460021` |

Para instalar, abre `INSTALAR.bat` con doble clic. Guarda un respaldo y copia `SONNY2.swf` en la carpeta del juego. `RESTAURAR.bat` vuelve a la versión anterior.

La entrega pesa más de 30 MB, así que va en dos zips:
- **parte 1:** `SONNY2.swf`, el instalador y este LEEME;
- **parte 2:** este LEEME, `documentacion/`, `fuente/` y `capturas/`.

## Qué cambia

### Todos los combates del juego en HD

Entraron las 10 imágenes de `SONNY2_COMBATE_2K_FINAL.zip` (las versiones `completos/`, de 2560x1440). Cada combate usa la que corresponde a su suelo y su cielo:

| Imagen | Combates del juego (suelo \| cielo) | Cuántos |
|---|---|---|
| JAIL | JAIL \| JAIL | 18 |
| SNOW | SNOW \| SNOW | 17 |
| TUNNEL | TUNNEL \| TUNNEL | 15 |
| STREETS | STREETS \| STREETS y STREETS \| TUNNEL | 13 + 4 |
| TRAIN | TRAIN \| TRAIN | 13 |
| CHURCH | CHURCH \| CHURCH y CHURCH2 \| CHURCH | 6 + 1 |
| ROME | CHURCH \| ROME (la iglesia con el cielo rojo) | 5 |
| STREETS2 | STREETS2 \| STREETS | 5 |
| STREETS3 | STREETS3 \| STREETS3 | 1 |
| SEA | WHITE NOVEMBER \| SEA (la cubierta del barco) | 1 |

Así quedan cubiertos los 99 combates. Hay dos casos sin imagen propia:
- **STREETS \| TUNNEL** (4 combates en la calle con el cielo de túnel): usan la de STREETS.
- **CHURCH2** (1 combate): usa la de CHURCH. Conserva sus objetos en el suelo.

Capturas de cada uno en `capturas/` (`JAIL_JAIL.jpg`, `SEA` es `WHITENOVEMBER_SEA.jpg`, etc.).

### Cámara: cielo quieto, suelo con la cámara, y menos zoom

- **Dos capas, como el original:** igual que en I34 con la nieve, cada imagen va en dos capas. El cielo y el fondo lejano quedan quietos; el suelo se mueve con los personajes. `00_capas_cielo_y_suelo.png` muestra dónde corta cada una; el magenta es la parte quieta.
  - **Nieve, calles y la grieta (STREETS3):** el borde se detecta solo.
  - **Habitaciones, cárcel, tren, cubierta y cueva:** el borde es una línea recta al pie del fondo.
- **Menos zoom (mareo):** en los combates HD, el zoom de cada ataque ahora es la **mitad** que en el original (hasta un ~10 % en lugar de ~19 %). El temblor de los golpes no cambia. Se puede ajustar con `_root.__hdZoomF` (1 = como el original, 0 = sin zoom; está en 0,5).

### Lo demás sigue igual que en I34

- arriba, solo las barras de vida;
- el panel de abajo al 62 %, centrado;
- el diálogo en su cuadro;
- los fondos de zona de I31.

## Probado (Ruffle, 16:9)

- **Las 12 combinaciones de suelo y cielo del juego:** cada una con un combate, un disparo de Sonny (con zoom) y el turno enemigo.
- **Comprobado en todas:**
  - la imagen correcta;
  - los personajes sobre el suelo;
  - el suelo original oculto;
  - el cielo quieto en el zoom.

Falta probarlo en tu app (AIR).

## Notas

- **Calidad de imagen:** las imágenes van en JPEG de calidad 88 para que el SWF entre en 29,4 MB. Como son de colores planos, no se nota.
- **Dónde está el detalle:** la documentación de cómo funciona está en `documentacion/COMBATE_HD.md`.

## Fuente (`fuente/`)

- **`build.py`:** `python3 build.py SONNY2_I35.swf` da siempre el mismo SHA.
- **`capas.py`:** la tabla `BORDES` dice dónde corta el cielo del suelo en cada imagen.
- **`batalla.py`:** las piezas del SWF.
- **`hd_batalla.as`:** la capa del juego, con la tabla `__hdBattleMap` (suelo|cielo → imagen) y `__hdZoomF`.
- **`imagenes.py`:** prepara las imágenes.
- **`imagenes_preparadas/`:** las 10 imágenes tal como entran al juego. Las originales son las de tu zip.
- **`i31/`:** lo de I31.
- **`banco/`:** los guiones de Ruffle. `s_i35.json` recorre los 12 combates.
