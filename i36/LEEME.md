# Sonny 2 a 16:9: I36 (combate HD arreglado: New Alcatraz y Oberursel)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I36) | `49a3537f2a68d05b564ab6b3260c768e78c201f2badbdbdc1299bbb140792cfd` |
| Base: I35 | `5d5a9bebb5f39843f0fd69d92cddb579aee3eb32a0b72dd078388eb9288e576e` |

Para instalar, abre `INSTALAR.bat` con doble clic. Guarda un respaldo y copia `SONNY2.swf` en la carpeta del juego. `RESTAURAR.bat` vuelve a la versión anterior.

La entrega pesa más de 30 MB, así que va en dos zips:
- **parte 1:** `SONNY2.swf`, el instalador y este LEEME;
- **parte 2:** este LEEME, `documentacion/`, `fuente/` y `capturas/`.

## Qué arregla (tu video de I35)

### «Solo se muestra la primera imagen»: siempre salía CHURCH

**Qué pasaba:**
- todas las imágenes de combate van en un mismo clip, una por fotograma, y todas en las mismas capas (profundidades 1 y 2);
- para elegir la imagen, el juego salta hacia adelante hasta el fotograma de esa imagen, y en el camino pasa por todos los anteriores;
- tu app (AIR, igual que Flash) **ignora** poner algo en una capa que ya está ocupada, así que quedaba la del primer fotograma: CHURCH, en todos los combates (`capturas/tu_video_I35_siempre_CHURCH.jpg`);
- es la misma trampa que el bug de Hew de I31. Ruffle no se comporta así, y por eso en mis pruebas se veían bien las 10.

**El arreglo:** cada fotograma vacía las dos capas antes de poner su imagen. Así, al llegar a la imagen buscada, la que queda es esa.

### La imagen pixelada en el zoom (los pilares)

- **Calidad baja durante el zoom:** el juego tiene una opción de efectos (SFX3). Si está apagada, durante el zoom de cada ataque baja la calidad a «LOW». En esa calidad Flash dibuja las imágenes sin suavizado, y la imagen HD se pixela: los pilares y todos los bordes. **En los combates HD ya no la baja:** queda la calidad que tengas elegida.
- **Las capas cortaban lo vertical:** el corte entre cielo (quieto) y suelo (con la cámara) era una línea recta. Al hacer zoom, la parte de abajo de los pilares se movía y la de arriba no. En JAIL pasaba lo mismo con la base de los edificios de los costados. Ahora el corte de JAIL sigue la base de los edificios, así que quedan enteros (`capturas/JAIL_zoom_edificios_enteros.png`). En la catedral (CHURCH) los pilares llegan hasta el piso y cualquier corte los parte; por eso queda apagada hasta resolverlo.

### Mejor calidad de imagen

Las imágenes van en JPEG de calidad 95 (antes 88) y con el color completo (antes reducido a la mitad, que es lo que deja bordes sucios en el rojo y el morado). El suelo se toma directo de tu PNG, sin comprimir dos veces. Como ahora entran solo dos imágenes, el SWF pesa menos que antes: 28,5 MB.

## Qué combates tienen HD (lo que elegiste)

| Imagen | Zona | Combates | En I36 |
|---|---|---|---|
| JAIL | New Alcatraz, Zona 1 | 18 | **HD** |
| SNOW | Oberursel, Zona 2 | 17 | **HD** |
| Todas las demás | | | Fondo original |

Las otras 8 imágenes quedan listas en la fuente para activarlas cuando quieras: hay que agregarlas a `ACTIVOS` en `capas.py` y descomentar su línea en `hd_batalla.as`.

Lo demás sigue igual que en I35:
- arriba, solo las barras de vida;
- el panel de abajo al 62 %;
- el diálogo en su cuadro;
- el zoom al 50 %;
- los fondos de zona de I31.

## Probado (Ruffle, 16:9)

- **JAIL:** HD, con la opción SFX3 apagada; la calidad queda en HIGH durante el zoom.
- **SNOW:** HD.
- **TRAIN y CHURCH:** clásicos.

Capturas en `capturas/`. Ruffle no reproduce el bug de las capas de AIR, así que **la prueba que vale es la de tu app**.

## Fuente (`fuente/`)

- **`build.py`:** `python3 build.py SONNY2_I36.swf` da siempre el mismo SHA.
- **`batalla.py`:** las capas se vacían en cada fotograma.
- **`capas.py`:** `ACTIVOS` y el borde por puntos de JAIL.
- **`hd_batalla.as`:** `__hdBattleMap`, ahora solo con JAIL y SNOW.
- **`imagenes/`:** tus dos PNG.
- **`banco/s_i36.json`:** el guion de Ruffle.

La guía completa está en `documentacion/COMBATE_HD.md`.
