# Sonny 2 a 16:9: I34 (cámara como el original y diálogo en su cuadro)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I34) | `410c3be60574e40591825f3bf20a86118cdcd308eb3ab3c5b8f5eca511460021` |
| Base: I33 | `7798ab07613e2d44c893a6d88f7074889bc1a407e90c3c160bfd77e9667539fc` |

Para instalar, abre `INSTALAR.bat` con doble clic. Guarda un respaldo y copia `SONNY2.swf` en la carpeta del juego. `RESTAURAR.bat` vuelve a la versión anterior.

## Por qué la cámara se veía rara (tus dos videos)

**Así es en el juego original:**
- en cada ataque la cámara hace un zoom de hasta un 19 % hacia el objetivo, y el temblor sacude la escena;
- ese zoom solo mueve `BATTLESCREEN`, es decir, los personajes y **el suelo**;
- **el cielo** (`3328`), el marco de la ventana y los paneles quedan quietos.

Por eso en el original casi no se nota: el objetivo queda en su lugar y el resto se acerca un poco dentro de la ventana chica.

**Qué pasaba en HD:** tu imagen trae cielo y suelo en una sola pieza.
- **I32:** la imagen quedaba quieta. Los personajes se acercaban y se alejaban sobre un suelo que no se movía, así que parecían flotar y salirse del mapa al pegar.
- **I33:** la imagen entera seguía al zoom. Así se movía toda la pantalla de 2560, montañas y cielo incluidos, y parecía que la cámara se iba con el ataque.

## El arreglo: dos capas, como el original

- **Cielo:** tu imagen entera. Queda **quieta**, como el cielo del juego.
- **Suelo:** la misma imagen, pero transparente por encima del pie de las montañas. **Sigue el zoom y el temblor** junto con los personajes, como el suelo original. Así los personajes siempre pisan la nieve.
- **El borde entre las dos capas** se detecta solo, columna por columna, en el pie de las montañas (`fuente/capas.py`). Tiene un difuminado de 14 px. En reposo las dos capas coinciden pixel por pixel, así que no se ve ninguna costura.
- **En el zoom,** la nieve se acerca y tapa un poco más el pie de las montañas, igual que el suelo del original sobre su cielo (`02_zoom_suelo_cielo_quieto.jpg`).

## El diálogo, en su cuadro

El cuadro de diálogo («Press SPACEBAR to Skip» y el texto) ahora se achica al 62 % y queda dentro de su cuadro del panel de abajo, igual que el resto del panel:
- **lo que dicen tus personajes** va en el cuadro de los compañeros (izquierda);
- **lo que dicen los enemigos** va en el cuadro de la derecha (`01_dialogo_en_su_cuadro.jpg`).

## Lo que viste en el video y no es un error

- **La barra del enemigo que muere se ve como un recuadro oscuro vacío por un momento:** es la animación original en la que la barra se apaga. Antes se apagaba sobre el panel gris y casi no se veía; ahora se apaga sobre el cielo. Dura menos de un segundo. Si quieres, se puede ocultar de golpe.
- **El final del video** (vuelve a la pantalla de Armor Games) es por el botón «Quit» de la X roja, no por un cierre del juego.

## Probado (Ruffle, 16:9)

- **Combate real de Oberursel** (`KBR200`, con diálogos):
  - el diálogo de Sonny en el cuadro de la izquierda y el del enemigo en el de la derecha;
  - una jugada del lobo y el contraataque, con capturas cada 120 ms.
- **Borde entre las capas:** en reposo no se ve, y en el zoom el suelo se mueve con los personajes.

Falta probarlo en tu app (AIR).

## Archivos

- **`SONNY2.swf`, `INSTALAR.bat` y `RESTAURAR.bat`.**
- **`documentacion/`:** `COMBATE_HD.md` (con las capas y el diálogo), `ZONAS_HD.md`, `TRASPASO.md` y `estado-mod-sonny.md`.
- **`fuente/`:**
  - `build.py` y `batalla.py`;
  - `capas.py`, que es nuevo;
  - `hd_batalla.as`, con `__hdCamSync` y `__hdDialogo`;
  - `placeobj.py` e `imagenes.py`;
  - `i31/`, `imagenes/` y `banco/`.
- **`capturas/`.**
