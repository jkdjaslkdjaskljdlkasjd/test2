# Sonny 2 a 16:9: I33 (cámara del combate HD)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I33) | `7798ab07613e2d44c893a6d88f7074889bc1a407e90c3c160bfd77e9667539fc` |
| Base: I32 | `33328f7fafebed4d27503857a144055e7785f2b8e3ddd97b6cb39a5e4921040a` |

Para instalar, abre `INSTALAR.bat` con doble clic. Guarda un respaldo y copia `SONNY2.swf` en la carpeta del juego. `RESTAURAR.bat` vuelve a la versión anterior.

## El problema de I32 (tu video)

**El juego original tiene dos capas de fondo:**
- **el cielo**, que queda quieto;
- **el suelo**, que va dentro del mismo clip que los personajes (`BATTLESCREEN`).

En cada ataque, la cámara del juego hace zoom (hasta un 19 %) hacia el objetivo y sacude la escena. Mueve **ese clip**, así que en el original el suelo se acerca junto con los personajes y ellos siguen pisándolo.

En I32 tu imagen trae cielo y suelo juntos, y quedaba quieta. Cuando la cámara se movía, solo se movían los personajes. Por eso se despegaban de la nieve, parecían flotar hacia las montañas y salir del mapa al pegar, y el zoom se veía raro.

## El arreglo

- **La imagen HD sigue a la cámara:** en cada fotograma copia el zoom y el desplazamiento de `BATTLESCREEN`, así que personajes y fondo se mueven juntos, como en el original (`ataque_con_camara.gif` y `01_zoom_fondo_acompana.jpg`).
- **Avisos en el mismo fotograma:** el zoom (`GridZoomer`) y el temblor (`GridShaker`) avisan a la imagen en el mismo fotograma en que mueven la escena. No hay ni un fotograma de retraso.
- **Margen para el temblor:** en reposo la imagen está un 3 % más grande, centrada. Así el temblor nunca deja bordes vacíos. Se pierde un 1,5 % de cada borde, que no se nota.
- **Comprobado:** con el zoom hacia objetivos de los dos lados no quedan bordes sin imagen. Al terminar el zoom, todo vuelve exactamente a su lugar.
- **Lo demás no cambia:** el panel de abajo, las barras, los combates clásicos y las habilidades.

## Probado (Ruffle, 16:9)

- Ataque del lobo con zoom y el contraataque enemigo, con capturas cada 120 ms.
- Revisé las cuatro esquinas y los costados de cada captura: ninguna tiene bordes negros.

Falta probarlo en tu app (AIR).

## Archivos

- **`SONNY2.swf`, `INSTALAR.bat` y `RESTAURAR.bat`.**
- **`documentacion/`:** `COMBATE_HD.md` (sección 4, actualizada), `ZONAS_HD.md`, `TRASPASO.md` y `estado-mod-sonny.md`.
- **`fuente/`:**
  - `build.py` arma I33 sobre I31;
  - `hd_batalla.as` lleva la función `__hdCamSync`;
  - `batalla.py`, `placeobj.py` e `imagenes.py`;
  - `i31/`, `imagenes/` y `banco/` (con el guion nuevo `s_camara.json`).
- **`capturas/`:** el GIF del ataque y tres capturas.
