# Mokoshotar — animaciones y sonidos nuevos (sobre el rig original MODEL5 de I41)

Contenido **nuevo**, creado a partir del rig extraído de I41 (`04_Recursos_Originales_I41`). No modifica el SWF ni el proyecto Godot existente.

## Qué hay
| | Nombre | Detalle |
|---|---|---|
| Animación de ataque | `Attack_Moko` — **Mordisco Glacial** | 28 fotogramas a 30 fps (0,93 s): se agacha, salta, muerde con un golpe de cabeza, deja una estela de tres zarpazos de hielo y vuelve. **Impacto en el fotograma 13.** |
| Animación de hechizo | `cast_Moko` — **Aullido de Escarcha** | 42 fotogramas (1,4 s): se sienta sobre las patas traseras, alza el hocico y aúlla con tiritera mientras brillan las runas. Sale un cono de aliento helado y se expande un anillo rúnico de escarcha en el suelo. **Liberación en el fotograma 16.** |
| Sonidos de ataque (2) | `moko_ataque_mordisco_1/2` | 1: salto + mordisco + crujido de hielo. 2: gruñido + zarpazo + esquirlas. Se disparan en el fotograma 7 y el impacto suena a +0,200 s, que coincide con el fotograma 13. |
| Sonidos de hechizo (2) | `moko_hechizo_escarcha_1/2` | 1: viento helado + cristales + estallido. 2: retumbe + aire invertido + campanas graves + viento. Se disparan en el fotograma 9 y la liberación suena a +0,233 s, que coincide con el fotograma 16. |
| Golpe crítico | `moko_critico_aullido` | Aullido de lobo de 2,6 s: tono que sube, sostiene con vibrato y cae, con formantes «u»→«a»→«u» y reverberación. |

**Aleatorio.** Cada habilidad elige uno de sus dos sonidos al azar (`AudioStreamRandomizer`, modo aleatorio, con una variación ligera de tono de ±4 % y ±3 %).

**Sonidos originales.** Todos están **sintetizados desde cero** (numpy/scipy), sin muestras de terceros. Van en `.ogg` para Godot y en `.wav` 44,1 kHz/16 bit para el mod de Flash u otros usos. `sonidos/espectrogramas.png` permite revisarlos de un vistazo.

## Cómo probarlo en Godot 4
1. Copia la carpeta `Mokoshotar/` a la **raíz** de un proyecto Godot 4. Las rutas son `res://Mokoshotar/...`.
2. Abre `Mokoshotar/Mokoshotar.tscn` y ejecuta la escena (F6).
3. Teclas: **1** ataque, **2** ataque crítico (suena el aullido en el impacto), **3** hechizo, **4** hechizo crítico.

Desde código: `$Mokoshotar.atacar(critico)` y `$Mokoshotar.lanzar_hechizo(critico)`. Al terminar vuelve a `stand`. La señal `impacto(critico)` se emite en el fotograma de contacto, para aplicar daño o efectos de golpe.

La escena conserva las 13 animaciones originales del lobo, más `Attack_Moko` y `cast_Moko`.

## Cómo está hecho
- **Mismo rig.** Usa las mismas piezas, texturas y huesos de `MODEL5` (piel `MOKO`). Las poses se calculan desde la pose `stand` original con rotaciones en las articulaciones. Como el rig del SWF es plano, cada muslo arrastra su pata para que no se separen. A eso se suman el movimiento del cuerpo completo y un `modulate` de brillo helado.
- **Efectos.** Son imágenes nuevas (`Mokoshotar/efectos/`), animadas con pistas `visible`/`transform`/`modulate`. Las animaciones originales los ocultan.
- **Sonido en la animación.** Va en una pista de método que llama a `play()` en el reproductor aleatorio correspondiente.

## Vista previa
- `vista_previa/mokoshotar_demo.mp4`: vídeo con sonido (11,7 s). Secuencia: reposo → ataque con sonido 1 → ataque con sonido 2 → hechizo con sonido 1 → hechizo con sonido 2 → ataque crítico con aullido. Está renderizado con la misma semántica que la escena Godot.
- `vista_previa/lamina_animaciones.png`, `fotogramas_*`: fotogramas sueltos.
- `vista_previa/rig_pivotes_stand.png`: pivotes de los huesos.

## Limitaciones
- **No probado en Godot real.** Aquí no hay ejecutable de Godot. Se comprobó la sintaxis de la escena: referencias, rutas de nodos, `load_steps` y archivos presentes.
- **Sonidos no escuchados.** Se generaron y revisaron por espectrograma, duración y nivel (pico −1 dBFS), pero no se han escuchado. Ajustar al gusto en `herramientas/sfx_moko.py`; cada sonido es una función.
- **Solo Godot.** Para el mod de Flash habría que llevar las animaciones al timeline de `MODEL5`; los WAV ya sirven tal cual.
