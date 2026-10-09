# Traspaso para la siguiente sesión (LLM): mod de Sonny 2, rework del lobo

> **Si eres una IA que recién llega, lee primero `INICIO_LLM.md`** (por dónde empezar, quién hace qué, reglas y estado). Este archivo es el detalle técnico.

Última actualización: 01/10/2026. Versión vigente: **I41** (nueva New Alcatraz HD en la Zona 1; además, de I40: Zona 3, el tren, en HD con el parpadeo del original; imágenes en JPEG 97 4:4:4; los 10 fondos de combate; Zona 1 HD de prueba; botón ZONAS en NULL ZONE).

Este documento resume lo último que se hizo y cómo seguir. El historial completo está en `estado-mod-sonny.md`, y cada versión tiene su `LEEME.md` en `iNN/`.

## 1. Qué es el proyecto

- **El juego:** Sonny 2 (Flash, AS2/AVM1, `SONNY2.swf`). Corre en la app del usuario (AIR, lanzador AS3 «2K nativo», pantalla 2560x1440, 16:9).
- **El área visible en coordenadas del juego:** x de −111,11 a 911,11 e y de 0 a 575. El escenario original mide 800x575.
- **El trabajo actual** es el rework de las habilidades del lobo **Mokoshotar** (la propuesta v4, «Mokoshotar: sangre y escarcha»), hecho sobre la base I25.
- **Iteraciones:**

  | Versión | Qué hizo |
  |---|---|
  | I26 | El rework |
  | I27 | El árbol con la forma del árbol de clase |
  | I28 | El árbol ordenado por nivel y los menús con aspecto nativo |
  | I29 | El escudo del juego, los estados con cantidad y turnos, y la regla «Wounds o Scent» |
  | I30 | El menú de habilidades en 2K |
  | I31 | Fondos HD de zona: Zona 1 y Hew al original, Labyrinth e Il Sanctus en HD, bug de Hew |
  | I32 | Combate HD en Oberursel: fondo a pantalla completa, solo las barras arriba y el panel de abajo al 62 % |
  | I33 | La imagen HD del combate sigue la cámara (zoom y temblor) |
  | I34 | Combate HD en dos capas (cielo quieto y suelo con la cámara) y diálogo al 62 % |
  | I35 | Los 10 fondos de combate en HD (99 combates) y el zoom al 50 % en HD |
  | I36 | Combate HD solo en JAIL y SNOW; arreglo de «siempre CHURCH» en AIR; sin bajar a LOW en el zoom; JPEG 95 |
  | I37 | JAIL: los edificios van con el suelo (capa que sigue la cámara) y la capa quieta lleva el cielo prolongado detrás |
  | I38 | Zona 1 New Alcatraz HD (prueba, Real-ESRGAN); imágenes HD sin pérdida; botón ZONAS en NULL ZONE |
  | I39 | Los 10 fondos de combate HD activos (12 combinaciones, 99 combates), sin pérdida |
  | I40 | Zona 3 (tren) HD con el parpadeo cálido/azul; imágenes en JPEG 97 4:4:4 (SWF de 42 MB) |
  | **I41** | Zona 1: la imagen nueva de New Alcatraz del usuario (v2) |

## 2. Reglas del usuario (vigentes, respetarlas siempre)

- **Idioma:** conversar en español neutro.
- **Entregas:**
  - siempre un **zip con `LEEME.md`, la fuente y las capturas**, nunca el SWF suelto;
  - máximo 30 MB por archivo: si no entra, se divide en partes.
- **No correr nunca una simulación Heroic.** Las peleas de prueba sueltas en Ruffle sí están permitidas.
- **Íconos:** solo íconos de prueba; nunca generar íconos ni imágenes.
- **Capas del usuario:** respetarlas y no modificarlas: NULL ZONE (`__nz*`), night e i18. Envolver una función suya llamando a la original está bien.
- **Repo:**
  - desde el 01/10/2026 es **`jkdjaslkdjaskljdlkasjd/test2`**, **privada**, rama `main`. Ahí va todo: fuente, textos, el SWF vigente, las imágenes, las capturas y la base de trabajo (`trabajo/`);
  - las anteriores (`a7kp2mq9xx-cyber/test` y `jkdjaslkdjaskljdlkasjd/test`, públicas) quedan como historial y solo tienen fuente y textos;
  - no se abre PR salvo que el usuario lo pida;
  - **regla de oro del usuario:** en la repo quedan solo los **5 SWF más nuevos** (hoy I37 a I41, cada uno en `iNN/SONNY2.swf`). Al subir uno nuevo se borra el más viejo; los anteriores se recompilan desde su fuente.
- **Entregas (desde el 01/10):** solo por GitHub. No subir zips ni archivos al chat de Claude: tiene un límite de 30 MB y comprime.
- **Calidad de las imágenes:**
  - el 01/10 el usuario pidió calidad máxima: sin pérdida (I38–I39);
  - el 02/10 pidió **bajar un poco el peso sin perder calidad visible**. Desde I40, **JPEG 97 con color completo (4:4:4)**: ~51 dB contra la imagen sin pérdida y un tercio del peso;
  - las fuentes en la repo siguen en PNG;
  - para ampliar, Real-ESRGAN `realesr-animevideov3` ×4 (`trabajo/herramientas/esrgan_np.py`) y después Lanczos a 2560×1440.
- **Varias IA:** el usuario trabaja también con ChatGPT (imágenes y orden de `fondos_hd/`). Al terminar, actualizar el registro de `INICIO_LLM.md`.
- **Commits:** terminan con el trailer de la sesión.
- **Antes de cambiar habilidades:** conversar con el usuario. Ver la sección 6.

## 3. Dónde está todo (contenedor de trabajo)

| Ruta | Qué hay |
|---|---|
| `/home/user/work/rework/` | El proyecto: `build.py`, `src/rw_*.as`, `debug_hook.as`, `dl.py`, `tests/` |
| `/home/user/work/i25/` | La base I25 separada (`paso1/`, etiquetas) y descompilada (`paso3/scripts/`) |
| `/home/user/work/paso5/tools/` | Las herramientas (`swfpatch`, `as2comp`, `swfshape`, …) |
| `/home/user/work/ruffle/` | El arnés de Ruffle (`drive.js`, `page.html`, `page16.html`, `gen/mk.py`, guiones `s_*.json`) |
| `/home/user/work/entrega_i30/` y `SONNY2_I30.zip` | La última entrega |
| `test2/` | La repo: `README.md`, `estado-mod-sonny.md`, este archivo, `i26/` … `i35/` (`LEEME`, `fuente/`, desde I31 `documentacion/` y `capturas/`), `instalador/` y `trabajo/` (base compilable) |

Si el contenedor es nuevo, `/home/user/work` no existe. La fuente está en `i30/fuente/` de la repo, pero faltan la base I25 y las herramientas: vienen de `DECOMPILACION_PASO5.zip`, que tiene el usuario. Pedírsela.

## 4. Compilar, probar y ver

```
cd /home/user/work/rework
python3 build.py i30.swf            # reproducible: SHA 9a0f1775…1444
python3 build.py i30_dbg.swf --debug  # + gancho ExternalInterface "dbg" para Ruffle
cd tests && python3 test_rework.py  # banco AVM1 fiel: 312 comprobaciones, todas bien (rwbench.py apunta a ../i30.swf)
```

- **Cómo arma el SWF `build.py`:**
  - suma `src/rw_*.as`, en orden, al final de `DoAction_2` (fotograma 42);
  - parchea el reloj de combate (fotograma 217);
  - agrega los íconos de prueba (sprites 2186 y 1986);
  - en I30 hace dos arreglos más, descritos en la sección 5.

### Arnés de Ruffle

1. Levantar el servidor:
   ```
   cd /home/user/work && setsid nohup python3 -m http.server 8765 >log 2>&1 </dev/null &
   ```
   Sin `setsid`, el servidor se cae entre comandos.
2. Correr un guion:
   ```
   cd ruffle && PAGE=page16.html node drive.js /rework/i30_dbg.swf 1280 720 guion.json ../shots/carpeta
   ```
   - `page16.html` (`forceScale` y sin letterbox) muestra el 16:9 real, igual que la app del usuario.
   - La `page.html` vieja estira la pantalla.
3. Para pasar coordenadas del juego a pantalla, usar `gen/mk.py`: `sc(x, y)` = ((x + 111,11)·720/575, y·720/575). A 2560x1440 es el doble.
4. Pasos que acepta el guion: `wait`, `dbg`, `click`, `move`, `down`, `up`, `shot`, `until`, `waitdbg`.
5. Para crear una partida rápida, usar `inicio()` de `mk.py`. Para que el árbol de clase tenga datos: `{"dbg": "call _root.loadTalents 0"}`.
6. Asignar una habilidad a la barra de combate son dos clics: uno en el Ability Pool y otro en la casilla. No se arrastra.

## 5. Lo último que se hizo: I41, nueva New Alcatraz (02/10)

- La Zona 1 usa la imagen v2 del usuario: en `zona1.py`, `SRC = fuente/zonas/PRISON_Z1_v2_2560x1440_esrgan.png` (Real-ESRGAN + Lanczos).
- La v1 queda en `fondos_hd/world_map/PRISON_Z1_v1*.png`.
- **Compilar:** `python3 i41/build.py SONNY2_I41.swf` da `6b26ee6d…8812`.
- **Pendiente:** el usuario tiene el prompt para que ChatGPT haga la máscara de las ventanas del tren y el haz de luz (`planes/PROMPT_TREN_LUCES.md`). Con esas dos imágenes se rearman las luces que pasan por las ventanas.

## 5u. I40, el tren en HD y el SWF más liviano (02/10)

- **Pedido del usuario:**
  - bajar un poco el peso de las imágenes sin perder mucha calidad;
  - agregar el HD del tren con sus dos imágenes, la cálida y la azul;
  - sobre el haz de luz de los costados: «no sé si reworkearlo; por ahora solo agrega el HD».
- **`tren.py`:**
  - lee el `ColorMatrixFilter` de cada uno de los 56 fotogramas de 2846 y lo aplica a un naranja del vagón para saber si ese fotograma es azul o cálido, y con qué brillo (33 azules y 23 cálidos);
  - arma el sprite 4406 con las dos HD (4402/4403 cálida, 4404/4405 azul encima) y transformaciones de color: el alfa de la azul y el brillo (60 % del cambio original, de ×1,00 a ×1,21);
  - en 2908, fotograma 46: 4406 en la 26 (en lugar de 2848) y sin marco 47. Verificado con `simular_2908.py`.
- **Las luces de las ventanas** (2837) quedan tapadas: ver `ZONAS_HD.md`, sección 6c.
- **`calidad.py`:** `jpeg2()` y `jpeg3()` a calidad 97 4:4:4. El suelo va en JPEG3 premultiplicado. Contra I39 (sin pérdida): diferencia máxima 5/255 en pantalla.
- **Compilar:** `python3 i40/build.py SONNY2_I40.swf` da `0142abdd…ed64`. Pesa 42,3 MB.
- **Ruffle:** `s_i40_tren.json` (tren: 12 capturas seguidas, más las zonas 1, 4 y 5) y `s_i40_bat.json` (JAIL y CHURCH).

## 5v. I39, todos los fondos de combate (01/10)

- **Pedido del usuario:** «implementa todas las etapas de batallas; luego vemos los arreglos correspondientes».
- **Cambios:**
  - `capas.ACTIVOS` tiene los 10 fondos: JAIL, SNOW, TRAIN, TUNNEL, STREETS, STREETS2, STREETS3, CHURCH, ROME y SEA;
  - `__hdBattleMap` tiene las 12 combinaciones;
  - los ids van de 4341 a 4390, cinco por imagen, y no chocan con 4400/4401 (Zona 1).
- **Tamaño:** el SWF pesa 77,5 MB, por los bitmaps sin pérdida. El límite de GitHub es 100 MB por archivo.
  - Si hace falta espacio, recortar el bitmap del suelo a la parte con alfa > 0: hoy es la imagen entera, con alfa 0 arriba.
- **Pendiente:** el corte entre capas de cada fondo nuevo es el de I35. La tabla de arreglos está en `i39/LEEME.md`:
  - CHURCH/ROME: pilares, que necesitan una imagen «sin pilares»;
  - TRAIN: paneles;
  - STREETS2: columnas.
- **Compilar:** `python3 i39/build.py SONNY2_I39.swf` da `eb340217…d64a`.
- **Ruffle:** `s_i39_1.json`, `s_i39_2.json` y `s_i39_3.json`, cuatro combinaciones cada uno; juntos pasan de los 10 minutos que dura un comando.

## 5w. I38 (01/10)

- **Pedido:**
  - probar en la Zona 1 la imagen de New Alcatraz que mandó el usuario y guardarla en `fondos_hd/world_map/`;
  - calidad máxima en las imágenes;
  - un selector de zona en NULL ZONE;
  - ajustar el plan de 5 versiones con humo: `planes/PLAN_NEW_ALCATRAZ_HUMO.md`;
  - un `.md` de inicio para cualquier LLM: `INICIO_LLM.md`.
- **`zona1.py`:**
  - bitmap 4400 (`Lossless2`) y forma 4401 (copia de 4320), insertados antes de 2908;
  - fotograma 1: quita el 47 y pone 4401 en la 26;
  - fotograma 16 (CITY): al empezar, quita la 26 y repone el 47.
  - Verificado con `herramientas/simular_2908.py`: todas las zonas, bien.
- **Real-ESRGAN sin torch:** `herramientas/esrgan_np.py` carga el `.pth` oficial con un unpickler propio y corre SRVGGNetCompact en numpy (float32), por bloques de 128 con 24 px de solapamiento. Da diferencia 0 contra la imagen entera. Tarda unos 75 s por imagen de 1672×941 en 2 núcleos.
- **`calidad.lossless2()`:** cielo y suelo de combate, y Zona 1. Además, `p.image()` para 4319 (Labyrinth, desde Real-ESRGAN) y 4323 (Il Sanctus). El SWF pasa a 49,6 MB.
- **`nz_zonas.as`:** envuelve `__nzZoneReady` y agrega el botón ZONAS. `__zsIr(n)`: `sectionIn = n`, `overMap` y en el fotograma siguiente `Navigation`.
- **Compilar:** `python3 i38/build.py SONNY2_I38.swf` da `4cd1eac3…3a8f`.
- **Ruffle:** guiones `s_i38_zonas.json`, `s_i38_nz.json` y `s_i38_batalla.json`.

## 5x. I37, New Alcatraz como el original (01/10)

- **Pedido del usuario (video de I36):** «pareciera que las estructuras fueran solo una imagen y por eso el zoom las corre; pasa con todas las estructuras, pero vamos de a poco». Se arregló solo JAIL.
- **Cómo es el original** (Ruffle, `BATTLESCREEN` oculto): el cielo 3328 de JAIL es solo cielo + ciudad lejana; los edificios de los costados están en el suelo (`BATTLESCREEN`) y se mueven con el zoom.
- **I37:** `capas.BORDES['JAIL'] = ('poligono', puntos, -3, 4, True)`:
  - el borde es el contorno de los techos (medido cada 50 px: primer borde con gradiente > 45 desde arriba; el techo es curvo) y las paredes interiores (x 751/752 y 1807/1808); en el centro, 612 (pie de la ciudad);
  - margen −3 (incluye la línea del techo) y fundido de 4 px;
  - `relleno=True`: la capa quieta se arma con `capas.relleno_cielo()`. En cada fila, lo que queda bajo el borde toma el color del cielo 14 px hacia adentro, y se suaviza (σ 6). Sin esto, el zoom deja ver el edificio viejo detrás del que se mueve.
- **Regla para los próximos fondos:** lo lejano (cielo, montañas, horizonte) queda quieto; lo cercano (piso, paredes, pilares, rejas) va con el suelo. Si una estructura grande deja un hueco que el relleno no cubre bien, pedirle al usuario una versión «solo fondo» de la imagen (no generarla).
- **Compilar:** `python3 build.py SONNY2_I37.swf` da `50c1a33a…640b`. Fuente: `trabajo/i37/` o `i37/fuente/`.
- **Ruffle:** `banco/s_i37.json` (JAIL en reposo y un ataque, con capturas cada 120 ms).

## 5y. I36, arreglo del combate HD en AIR (01/10)

- **El bug (video del usuario, I35):** en su app todos los combates mostraban la imagen de CHURCH. El contenedor `__hdBattleBG` tiene un fotograma por imagen y todas van en las profundidades 1 y 2. `gotoAndStop(etiqueta)` hacia adelante recorre los fotogramas intermedios y Flash/AIR **ignora una colocación en una profundidad ocupada**, así que quedaba la del primer fotograma (CHURCH). Ruffle no lo reproduce. Arreglo: cada fotograma del contenedor quita las profundidades 1 y 2 antes de colocar (`batalla.py`). Es la misma trampa que el bug de Hew (I31).
- **Calidad en el zoom:** con la opción SFX3 apagada, `GridZoomer` (3345, fotogramas 2 y 6) baja `_quality` a `LOW` mientras dura el zoom, y la imagen HD se dibuja sin suavizado (pilares pixelados). En HD se vuelve a `KrinSettings.QUALITY` al final de esos dos scripts (`CALIDAD` en `build.py`).
- **Pedido del usuario:** HD solo en New Alcatraz (JAIL, Zona 1) y Oberursel (SNOW, Zona 2). `capas.ACTIVOS = ('JAIL', 'SNOW')` decide qué imágenes entran al SWF, y `__hdBattleMap` tiene solo esas dos combinaciones. El resto queda clásico. Para volver a activar otra imagen, agregarla a `ACTIVOS` y a `__hdBattleMap` (la lista está comentada en `hd_batalla.as`).
- **JAIL:** el borde entre capas ya no es la línea recta en 620 (cortaba la base de los edificios de los costados con el zoom). Ahora es `('puntos', …)`: sigue la base de los edificios, 8 px hacia el suelo.
- **Pilares de CHURCH y ROME:** cualquier corte entre capas parte los pilares en el zoom. Antes de reactivarlos: o una sola capa que siga la cámara, o sin zoom en esos fondos.
- **Imágenes:** JPEG 95 con color completo (4:4:4). El suelo se codifica desde el PNG original (antes se recomprimía el JPEG). El SWF pesa 28,5 MB.
- **Fuente:** `trabajo/i36/` (en la repo) o `i36/fuente/`. `python3 build.py SONNY2_I36.swf` da `49a3537f…2cfd`.
- **Ruffle:** `banco/s_i36.json` (JAIL con SFX3 apagado, SNOW, TRAIN y CHURCH), en menos de 10 minutos.

## 5z. I35, los 10 fondos de combate (01/10)

- **Fuente:** `i35/fuente/`.
  - `capas.BORDES`: el borde entre cielo y suelo de cada imagen;
  - `batalla.py`: los ids desde 4325, con los fondos desde 4341;
  - `hd_batalla.as`: `__hdBattleMap` y `__hdZoomF`.
- **Compilar:** `python3 build.py SONNY2_I35.swf` da `5d5a9beb…576e`.
- **Ruffle:** `s_i35.json` recorre los 12 combates. Pasa de los 10 minutos que dura un comando: hay que correrlo por partes.
- **Límite de tamaño:** el SWF pesa 29,4 MB. Si se agregan más imágenes, bajar la calidad JPEG o recortar los bitmaps del suelo a su parte visible.

## 5a. I34, cámara como el original (01/10)

- **Fuente:** `i34/fuente/`. `capas.py` separa la imagen en cielo y suelo; `__hdCamSync` mueve solo `__hdGround`; `__hdDialogo` acomoda `combatScript`.
- **Compilar:** `python3 build.py SONNY2_I34.swf` da `410c3be6…0021`.
- **Detalle:** el JPEG3 tiene que ir premultiplicado por el alfa.

## 5a. I33, cámara del combate HD (01/10)

- **Fuente:** `i33/fuente/`, que es I32 más `__hdCamSync` y los avisos en `GridZoomer` y `GridShaker`.
- **Compilar:** `python3 build.py SONNY2_I33.swf` da `7798ab07…39fc`.
- **Sugerencias que quedaron abiertas:**
  - escena ×1,15;
  - velo y viñeta;
  - nevada;
  - ocultar el texto «FPS».

## 5b. I32, combate HD en Oberursel (01/10)

- **Fuente:** `i32/fuente/`. `build.py` aplica I31 (`i31/build.py`, función `aplicar`) y después `batalla.py` y `hd_batalla.as`.
- **Compilar:** `python3 build.py SONNY2_I32.swf` da `33328f7f…040a`.
- **Cómo funciona y cómo sumar otro escenario:** `i32/documentacion/COMBATE_HD.md`.
- **Guiones de Ruffle:** `banco/s_batalla2560.json` y `banco/s_batalla_lobo.json`. Para forzar el escenario: `set _root.KBR103.ZoneBG SNOW` y `set _root.KBR103.SkyBG SNOW`.
- **Pendiente:** que el usuario lo pruebe en AIR y mande las imágenes de los demás escenarios de combate.

## 5a. I31, fondos HD de zona (01/10)

**El foco actual del usuario es el mod HD, no las habilidades.**

- **Base:** el `SONNY2.swf` del usuario del 29/09 (`bca5eea5…`), que es I30 más una cárcel HD hecha con ChatGPT. Esa cárcel causó el bug: Hew mostraba la imagen de la cárcel.
- **Cambios:** Zona 1 y Hew vuelven al original; Labyrinth (4319/4320) e Il Sanctus (4323/4324) van en HD; la forma del pueblo 4318 pasa a pantalla completa.
- **Fuente y guía:** la fuente está en `i31/fuente/` (`build.py`, `zonas.py`, `imagenes.py`). Todo lo de las zonas está en **`i31/documentacion/ZONAS_HD.md`**: el mapa de fotogramas, las profundidades, la trampa de la profundidad 26 y cómo agregar la próxima imagen.
- **Preparar el build:** `swfsplit` del SWF del 29/09 a `act1`, `swfcode` a `act3`, y `swfsplit` de `paso5/SONNY2_recompilado.swf` a `base1`.
- **Compilar:** `python3 build.py SONNY2_I31.swf` da `0197c816…3c26`.
- **Probar en Ruffle:** con el mismo `drive.js` y `page16.html`, y el guion `i31/fuente/banco/s_zonas2560.json`. Para cambiar de zona: `dbg call _root.KrinScreen.gotoAndStop ETIQUETA`.

## 5b. I30, menú de habilidades en 2K (26/09)

**Pedido:** que la página de habilidades del menú ocupe todo el 16:9, como la NULL ZONE, sin el recuadro de 800 con las bandas borrosas, y con íconos más grandes.

### `src/rw_80_2k.as` (archivo nuevo)

Trabaja por código sobre las piezas del menú (`KRINMENU`, sprite 3239, fotograma 25), sin tocar dibujos.

- **Dónde se aplica:** `__rw2kApply()`. La llaman tres envoltorios:
  - `__v8Sync`, al entrar a la página;
  - `__rwTick`, en cada fotograma;
  - `__v92Cleanup`, que llaman todas las demás páginas al entrar. Ahí se **restauran** las piezas compartidas con otras páginas (profundidades 2, 5, 7, 21, 23, 1431 y 1434).
- **Geometría:** está en `_root.__rw2kL`.

  | Pieza | Medida |
  |---|---|
  | Panel | x de −97 a 897, y de 15 a 470 (la barra de navegación empieza en 480) |
  | Recuadro del árbol | x de −68 a 294 |
  | Recuadro de la barra de combate | x de 506 a 868 |
  | Bajos de los recuadros | 449,5 |
  | Recuadro de atributos y su contenido | Bajan 29,9 |
  | Aviso de puntos | Baja 14,95 |
  | Barra de combate | ×1,18 |
  | Ability Pool | ×1,19 |
  | Cruz | +114 en x |
  | Pestañas `__v9Tabs` | −112,9 en x |

- **Grilla del árbol** (`__rw2kGrid`):
  - columnas cada 70, desde x0 = 7,975; filas cada 45, desde y = 121;
  - nodos al 140 %;
  - caños de 8 y 3;
  - anillo de radio 19,6.
- **Elegir la grilla:** en `rw_70_ui.as`, `__rwG()` elige `__rw2kGrid` o `__rwGrid800`. El árbol de clase (`talenttreefull`) se escala al 140 %, sus nodos se reubican y se llama a `krinRemakeTree()` para que el juego redibuje sus caños.
- **Reflejos de los costados:** `__wsFondo.L` y `.R` se ocultan con el menú o el panel de Aspectos abiertos.
- **Panel de Aspectos** (NULL ZONE): también pasó a 2K. Sus medidas salen de `__rwAspGeo()` en `rw_70_ui.as`.
- **Interruptor:** `_root.__rw2kEnabled = false` vuelve al menú de 800 de I29.

### Arreglos en `build.py`

- **Forma 3145:** la línea del rectángulo de `lineMC` del árbol de clase pasa a ser transparente. En 2K quedaba suelta.
- **Sprite 3205** (el tutorial del aviso «Click Here»): se corren 119 colocaciones de los fotogramas 12 a 150, con los números de `__rw2kL`.

### Lo que no cambió

- las demás páginas del menú (inventario, tienda, datos, opciones y logros) siguen con el menú de 800;
- las habilidades, sus números y sus textos.

### Pruebas y entrega

- **Pruebas:** 312 comprobaciones (la nueva es `menu_2k`) y Ruffle en 16:9, incluida una captura a 2560x1440.
- **Entregado:** `SONNY2_I30.zip` (29,9 MB). La fuente está en la repo (commit `c92900b`).
- **Hashes:**

  | SWF | SHA-256 |
  |---|---|
  | I30 | `9a0f17755223035f6dc94763ac80ecfe51b160d1a2a6ad2d7299d348ddeb1444` |
  | I29 | `b440bf33…` |

- **Falta:** que el usuario lo pruebe en su app (AIR).

## 6. Pendiente principal: revisión de habilidades (sin tocar nada todavía)

El usuario siente que pocas habilidades aprovechan las marcas (Scent of Blood, Wounds y Frostbite), salvo unas cuantas. Se acordó **conversar antes de cambiar**. Se le mandó este análisis y quedó esperando su respuesta.

### Las 26 activas del árbol y Frozen Maw

| Grupo | Habilidades |
|---|---|
| Aprovechan fuerte | Rupture, Cull the Weak, Pounce, Frost Fang, Shatter Guard, Second Wind |
| Aprovechan algo | Canine Instincts, Rallying Cry, Feeding Frenzy, Frostbound Pack, Taste of Blood, Last Stand |
| Gastan Scent para algo chico | Iron Jaws, Howl, Primal Breath, Guardian's Call, Echo Ward. Echo Ward, en rango 1, gasta la Scent y no da nada |
| Solo ponen marcas o no las usan | Rake, Hamstring, Killer Instinct, Wicked Claws, Cold Trail, Black Ice, Werezombie, Rime Coat, Ice Tomb, Frozen Maw |

Las pasivas están mejor: 11 de 17 crecen con las marcas.

### Lo que se encontró

- **Wounds:** está bien servido.
- **Scent:**
  - es escaso: máximo 3, y con 3 el enemigo queda Hunted;
  - lo gastan 7 habilidades, y 5 de ellas para algo chico, lo que además le baja el Hunted al enemigo.
- **Frostbite:** lo ponen unas 10 habilidades, pero solo Shatter Guard lo gasta para hacer daño.

### Propuestas que se le hicieron

- **A.** Las 5 que gastan Scent para algo chico: que solo lean la Scent, sin gastarla, o que la gasten para algo grande.
- **B.** Más cobros de Frostbite:
  - Howl: más daño por cada Frostbite;
  - Black Ice: daño por cada Frostbite en lugar de por cada Shard;
  - Cold Trail: gasta 1 Frostbite de cada enemigo para un extra.
- **C.** Las que solo ponen marcas reciben un extra chico por la marca que ya hay: Rake por Wound, Hamstring por Scent, Wicked Claws por Frostbite.
- **D.** Ice Tomb y Rime Coat crecen con el Frostbite de los enemigos.

### Preguntas abiertas al usuario

1. ¿Cuáles son las «unas cuantas» que sí le gustan? Sirven de modelo.
2. ¿Qué enfoques acepta: A, B, C o D?

Después: armar los números, mostrárselos y recién ahí implementar (I31). Al implementar, agregar pruebas en `tests/test_rework.py`.

### Reglas de diseño del usuario para esta revisión

- Una habilidad no puede subir a la vez por la cantidad de Wounds y por la de Scent (I29).
- No tocar: Cull the Weak, Second Wind, Shared Hunger ni «Frostbite al que golpea».
- Aliados que ponen Wounds: **no**.
- Pack Tactics y Relentless Hunt quedaron más flojas en I29. Se ofreció subirlas, pero el usuario no lo pidió.

Las descripciones completas, al rango máximo, se obtienen con el banco: `b.call('__rwFullDesc', id, max)` sobre `__rwList`.

## 7. Otros pendientes (menores)

- Si el usuario lo pide, pasar a 2K las demás páginas del menú, con el mismo enfoque que `rw_80_2k.as`.
- La maqueta del panel de batalla (variante A o B): sin elegir.
- Las imágenes HD de las demás zonas (cárcel definitiva, Hew, tren, Japón y fondos de combate): las da el usuario. Agregarlas siguiendo `i31/documentacion/ZONAS_HD.md`.
- El fondo del menú principal en 2K: el usuario lo pide a otra herramienta.
- Traducir los diálogos, cuando el usuario lo pida.
- **Compilar desde la repo (contenedor nuevo):** `cd trabajo && sh preparar.sh` (arma `act1`, `act3` y `base1` con las herramientas de `paso5/tools`) y después `python3 i41/build.py SONNY2_I41.swf` (sale `6b26ee6d…8812`), `python3 i40/build.py SONNY2_I40.swf` (sale `0142abdd…ed64`), `python3 i39/build.py SONNY2_I39.swf` (sale `eb340217…d64a`), `python3 i38/build.py SONNY2_I38.swf` (sale `4cd1eac3…3a8f`), `python3 i37/build.py SONNY2_I37.swf` (sale `50c1a33a…640b`), `python3 i36/build.py SONNY2_I36.swf` (sale `49a3537f…2cfd`) o `python3 i35/build.py SONNY2_I35.swf` (sale `5d5a9beb…576e`). `trabajo/paso5/` es el contenido de `DECOMPILACION_PASO5.zip`; `trabajo/bases/SONNY2_29-09.swf` es el SWF del usuario del 29/09 (I30).
- **Resuelto en I36:** «solo se muestra la primera imagen» (era la profundidad ocupada en el `gotoAndStop`). Falta que el usuario lo confirme en su app.

## 8. Trampas técnicas conocidas

- **Zonas:** `KrinScreen` (2908) arranca en el fotograma 1 y salta hacia adelante, así que una colocación en una profundidad ocupada se ignora. Toda zona que pone algo en la 26 tiene que vaciarla antes. Ver `ZONAS_HD.md`. **Ruffle no lo reproduce:** comprobarlo con `trabajo/herramientas/simular_2908.py`.

- Las profundidades AS en `_root` deben estar fuera del rango −16383..−1, porque pisan piezas del juego. `__wsFondo` usa −16384.
- `getInstanceAtDepth` de una forma o de una profundidad vacía devuelve `_level0` en Ruffle: no usar ese resultado como ruta.
- Un clip con `onUnload` se borra al final del fotograma. Si se recrea con el mismo nombre en ese fotograma, la ruta apunta al viejo.
- Una vez que un script toca la transformación de una pieza de la línea de tiempo, la línea de tiempo ya no la mueve. Por eso `rw_80_2k.as` guarda el original (`__rw2kO`) y lo restaura.
- La fuente de Ruffle no tiene «★».
- El tooltip `KrinToolTipper` hace `startDrag` en cada fotograma. Los tooltips propios usan `__rwShowTip`, que pone `inner2.zero`.
- En AS2 `var` es de la función entera: cuidado con nombres repetidos dentro de los bucles. En I30 una variable `A` pisaba la geometría.
