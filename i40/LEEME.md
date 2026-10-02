# Sonny 2 a 16:9: I40 (el tren en HD y el SWF más liviano)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I40) | `0142abdd7da0e1c424508e86da123a5820d553fb0b76026dd41608d3fc92ed64` |
| Base: I39 | `eb3402172a3d3369583d92300e2c7451455f5ae3a728c33ded895bb7bc76d64a` |

**Cómo instalarlo:**
- **Desde la repo:** descarga `i40/SONNY2.swf`. Pesa **42,3 MB**; I39 pesaba 77,5.
- **Instalador:** `instalador/INSTALAR.bat`, en la misma carpeta que el SWF. El SHA que muestra al final tiene que empezar con `0142abdd`.

## Qué cambia

### 1. Zona 3, Ivory Line (el tren), en HD

- **Tus dos imágenes:** la cálida y la azul, ampliadas con Real-ESRGAN `realesr-animevideov3` a 2560×1440. Guardadas en `fondos_hd/world_map/TRAIN_Z3_*.png`.
- **El parpadeo del original se mantiene:**
  - en el juego original, el vagón alterna entre luz cálida y luz azul con un filtro de color que cambia en cada uno de sus 56 fotogramas;
  - leí ese filtro fotograma por fotograma: 33 son azules y 23 cálidos, cada uno con su brillo;
  - armé la animación HD con la misma secuencia: tus dos imágenes se alternan igual, con el mismo ritmo y los mismos destellos de brillo (`capturas/tren_*.png`).
- **Las luces que pasan por las ventanas** (el «haz de luz» de los costados) quedan tapadas por ahora, como dijiste. En el original pasan por detrás del vagón y se ven por los huecos de las ventanas. Para recuperarlas en HD hay que recortar las ventanas de tu imagen o dibujar los haces encima. Lo vemos cuando decidas si se rehace.
- **Las otras zonas siguen bien:** la simulación de AIR, zona por zona, da bien todas (Hew, Labyrinth, Il Sanctus y Japón incluidas).

### 2. Imágenes más livianas, sin pérdida visible

**Todas las imágenes HD van ahora en JPEG de calidad 97 con color completo**, en vez de sin pérdida:
- **combate:** los 10 fondos;
- **zonas:** New Alcatraz, el tren, Labyrinth e Il Sanctus.

**Cuánto cambia:**
- cada imagen pesa más o menos un tercio;
- contra la versión sin pérdida, la diferencia en pantalla es de 5 sobre 255 como máximo y 0,3 en promedio. No se distingue (`capturas/comparacion_sin_perdida_vs_jpeg97.png`);
- la capa del suelo de los combates sigue con su transparencia exacta.

## Lo que sigue igual que I39

- Los 10 fondos de combate activos, con los mismos arreglos pendientes: pilares de CHURCH y ROME, paneles de TRAIN y columnas de STREETS2.
- La Zona 1 HD y el botón ZONAS de NULL ZONE.

## Probado (Ruffle)

- **Tren:** NULL ZONE → ZONAS → Zona 3, con 12 capturas seguidas: alterna cálido y azul, y los anillos quedan en su lugar.
- **Zonas 1, 4 y 5:** bien.
- **Combates JAIL y CHURCH:** en reposo y con zoom.

Falta probarlo en tu app.

## Fuente

- **`tren.py`:** lee el filtro del original, arma el sprite HD (ids 4402 a 4406) y cambia el fotograma 46 de la pantalla de zonas.
- **`calidad.py`:**
  - `CALIDAD_JPEG = 97`;
  - `jpeg2()` y `jpeg3()` (la segunda, con el alfa premultiplicado);
  - `lossless2()` sigue ahí, si alguna imagen tiene que volver a ir sin pérdida.
- **Compilar:** `python3 trabajo/i40/build.py SONNY2_I40.swf` da siempre el mismo SHA.
