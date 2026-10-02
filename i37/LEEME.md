# Sonny 2 a 16:9: I37 (New Alcatraz: los edificios se mueven con el suelo, como el original)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I37) | `50c1a33a3014f49be6a85c40154fb2a415d98b82b1358d6a9012076f3d98640b` |
| Base: I36 | `49a3537f2a68d05b564ab6b3260c768e78c201f2badbdbdc1299bbb140792cfd` |

Para instalar, abre `INSTALAR.bat` con doble clic. Guarda un respaldo y copia `SONNY2.swf` en la carpeta del juego. `RESTAURAR.bat` vuelve a la versión anterior.

La entrega pesa más de 30 MB, así que va en dos zips:
- **parte 1:** `SONNY2.swf`, el instalador y este LEEME;
- **parte 2:** este LEEME, `documentacion/`, `fuente/` y `capturas/`.

## El bug de tu video: «pareciera que las estructuras fueran solo una imagen»

Tenías razón. Comparé con el juego original en New Alcatraz (`capturas/original_JAIL_*.png`):

- **En el original:** el fondo quieto es solo **el cielo y la ciudad lejana**. Los edificios de los costados van **junto con el suelo**, así que en el zoom se acercan con el piso y con los personajes.
- **En I36:** los edificios estaban en la capa quieta, con el cielo, y en el zoom solo se movía el piso. Por eso el piso «se deslizaba» sobre la base de los edificios y se veían pegados a una imagen.

## El arreglo (solo New Alcatraz, como pediste: de a poco)

- **Capa del suelo** (sigue la cámara): el piso **y los dos edificios**. El corte sigue el contorno de los techos (medido cada 50 px, porque el techo es levemente curvo) y las paredes de adentro.
- **Capa quieta:** el cielo y la ciudad lejana. Detrás de los edificios, en esa capa, prolongué el cielo de cada fila. Así, cuando el zoom mueve un edificio, lo que aparece detrás es cielo y no un «fantasma» del edificio. No es una imagen nueva: son los mismos colores de tu cielo, estirados.
- `capturas/00_JAIL_capas.jpg`: arriba, la capa quieta; abajo, la capa del suelo (el magenta es lo que queda quieto).
- `capturas/JAIL_reposo.png` y `capturas/JAIL_zoom.png`: el mismo combate en reposo y en pleno zoom.

**No hace falta que generes ninguna imagen para JAIL.** Si en algún fondo el relleno no alcanza (por ejemplo, si una estructura grande se mueve mucho), ahí sí te pediría una versión «solo cielo» de esa imagen.

## Lo que sigue igual que I36

- HD solo en New Alcatraz y Oberursel (SNOW). En SNOW las montañas son fondo lejano, igual que en el original, así que quedan quietas.
- El arreglo de «siempre CHURCH», la calidad en el zoom, JPEG 95, el zoom al 50 %, el panel de abajo al 62 % y el diálogo en su cuadro.

## Probado (Ruffle, 16:9)

- **JAIL:** reposo y un ataque de Sonny, con capturas cada 120 ms. Los edificios se acercan con el suelo y no se ven cortes ni fantasmas.
- **Original sin HD:** cielo solo (sin `BATTLESCREEN`) y zoom, para comparar.

Falta probarlo en tu app.

## Para los próximos fondos (cuando sigamos)

Cada imagen necesita su corte entre «lejano» (quieto) y «cercano» (con la cámara), igual que el original:
- **Lo lejano:** cielo, montañas, ciudad del horizonte.
- **Lo cercano:** piso, paredes, pilares, edificios, rejas.

Con pilares que llegan al piso (CHURCH, ROME), los pilares tienen que ir enteros con el suelo, y detrás de ellos hace falta fondo. Ahí puede que te pida una versión «sin pilares» de la imagen.

## Fuente (`fuente/`)

- **`capas.py`:**
  - el tipo de borde `('poligono', puntos, margen, fundido, relleno)`, con el contorno de JAIL;
  - `relleno_cielo()`, que arma la capa quieta.
- **`batalla.py`:** usa la capa quieta rellenada cuando el borde lo pide.
- **`build.py`, `hd_batalla.as`, `imagenes.py`:** como en I36.
- **`banco/s_i37.json`:** el guion de Ruffle.
