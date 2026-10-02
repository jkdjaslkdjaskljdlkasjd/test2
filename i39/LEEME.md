# Sonny 2 a 16:9: I39 (todos los fondos de combate en HD)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I39) | `eb3402172a3d3369583d92300e2c7451455f5ae3a728c33ded895bb7bc76d64a` |
| Base: I38 | `4cd1eac3f563e9ad809e49bd6fb2ccdcadaac9f811d8eef73709a5850e4e3a8f` |

**Cómo instalarlo:**
- **Desde la repo:** descarga `i39/SONNY2.swf`. Pesa 77,5 MB, porque las imágenes van sin pérdida. GitHub muestra un aviso para archivos de más de 50 MB, pero lo acepta (el límite es 100 MB).
- **Instalador:** `instalador/INSTALAR.bat`, en la misma carpeta que el SWF. El SHA que muestra al final tiene que empezar con `eb340217`.

## Qué cambia

Están activos **los 10 fondos de combate** de `SONNY2_COMBATE_2K_FINAL.zip`, en las 12 combinaciones de suelo y cielo del juego, así que **los 99 combates** tienen fondo HD:

| Imagen | Zona | Combinaciones del juego (suelo \| cielo) |
|---|---|---|
| JAIL | New Alcatraz, Zona 1 | JAIL \| JAIL |
| SNOW | Oberursel, Zona 2 | SNOW \| SNOW |
| CHURCH | Oberursel, la catedral, Zona 2 | CHURCH \| CHURCH y CHURCH2 \| CHURCH |
| TRAIN | Ivory Line, Zona 3 | TRAIN \| TRAIN |
| TUNNEL | Labyrinth, Zona 4 | TUNNEL \| TUNNEL |
| STREETS, STREETS2 y STREETS3 | Hew, Zona 5 | STREETS \| STREETS, STREETS \| TUNNEL, STREETS2 \| STREETS y STREETS3 \| STREETS3 |
| ROME | Il Sanctus, Zona 6 | CHURCH \| ROME |
| SEA | White November (el barco) | WHITE NOVEMBER \| SEA |

**Lo que ya tenían JAIL y SNOW y ahora tienen todos:**
- van sin pérdida y en dos capas (cielo quieto y suelo con la cámara);
- tienen el arreglo de «siempre CHURCH» y la calidad del zoom;
- el zoom está al 50 %;
- el panel de abajo está al 62 %.

**En JAIL**, los edificios siguen yendo con el suelo, como en I37.

## Lo que falta arreglar (lo vemos mapa por mapa)

En los fondos nuevos, el corte entre la capa quieta y la que se mueve todavía es el de I35: una línea recta o un borde automático. Cuando ese corte pasa por algo vertical cercano, el zoom lo parte, como pasaba con los edificios de JAIL antes de I37.

| Fondo | Qué se parte con el zoom | Arreglo probable |
|---|---|---|
| CHURCH y ROME | Los pilares, que llegan al piso | Pilares con el suelo y, detrás, una versión «sin pilares» de la imagen (la genera la IA de imágenes) |
| TRAIN | La base de los paneles de la pared | Corte por el contorno de la pared, como en JAIL |
| STREETS2 | El pie de las columnas de la ventana | Columnas con el suelo y el cielo estirado detrás |
| STREETS y STREETS3 | Las paredes de los costados, si se ve | Revisar con tu video |
| TUNNEL y SEA | Seguramente nada grave | Revisar con tu video |

Lo más útil para ordenar los arreglos es un video tuyo pasando por cada zona. Ahora es fácil: NULL ZONE → **ZONAS**.

## Probado (Ruffle, 16:9)

- **Combinaciones:** las 12, cada una con el fondo correcto, en reposo y con el zoom de un disparo de Sonny.
- **Capturas:** están en `capturas/`.

Falta probarlo en tu app.

## Fuente

- **Igual que I38:** `capas.ACTIVOS` ahora tiene los 10 fondos, y `__hdBattleMap`, las 12 combinaciones.
- **Compilar:** `python3 trabajo/i39/build.py SONNY2_I39.swf` da siempre el mismo SHA.
