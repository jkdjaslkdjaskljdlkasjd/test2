# Traspaso para la siguiente sesión (LLM): mod de Sonny 2, rework del lobo

Última actualización: 01/10/2026. Versión vigente: **I32** (combate HD en Oberursel).

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
  | **I32** | Combate HD en Oberursel: fondo a pantalla completa, solo las barras arriba y el panel de abajo al 62 % |

## 2. Reglas del usuario (vigentes, respetarlas siempre)

- **Idioma:** conversar en español neutro.
- **Entregas:**
  - siempre un **zip con `LEEME.md`, la fuente y las capturas**, nunca el SWF suelto;
  - máximo 30 MB por archivo: si no entra, se divide en partes.
- **No correr nunca una simulación Heroic.** Las peleas de prueba sueltas en Ruffle sí están permitidas.
- **Íconos:** solo íconos de prueba; nunca generar íconos ni imágenes.
- **Capas del usuario:** respetarlas y no modificarlas: NULL ZONE (`__nz*`), night e i18. Envolver una función suya llamando a la original está bien.
- **Repo:**
  - es `a7kp2mq9xx-cyber/test` y sigue **pública**;
  - se trabaja solo en la rama `claude/jru-33pp84`, y no se abre PR salvo que el usuario la pida;
  - mientras sea pública, solo se suben la fuente y los textos: **no** el SWF, ni las capturas, ni `DECOMPILACION_PASO5.zip`. Ese zip se sube cuando el usuario la haga privada (ya eligió hacerla privada primero).
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
| `/home/user/test/` | La repo: `README.md`, `estado-mod-sonny.md`, este archivo e `i26/` … `i30/` (`LEEME` y `fuente/`) |

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

## 5. Lo último que se hizo: I32, combate HD en Oberursel (01/10)

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
- Subir `DECOMPILACION_PASO5.zip`, los SWF y las capturas cuando la repo sea privada.

## 8. Trampas técnicas conocidas

- **Zonas:** `KrinScreen` (2908) arranca en el fotograma 1 y salta hacia adelante, así que una colocación en una profundidad ocupada se ignora. Toda zona que pone algo en la 26 tiene que vaciarla antes. Ver `ZONAS_HD.md`.

- Las profundidades AS en `_root` deben estar fuera del rango −16383..−1, porque pisan piezas del juego. `__wsFondo` usa −16384.
- `getInstanceAtDepth` de una forma o de una profundidad vacía devuelve `_level0` en Ruffle: no usar ese resultado como ruta.
- Un clip con `onUnload` se borra al final del fotograma. Si se recrea con el mismo nombre en ese fotograma, la ruta apunta al viejo.
- Una vez que un script toca la transformación de una pieza de la línea de tiempo, la línea de tiempo ya no la mueve. Por eso `rw_80_2k.as` guarda el original (`__rw2kO`) y lo restaura.
- La fuente de Ruffle no tiene «★».
- El tooltip `KrinToolTipper` hace `startDrag` en cada fotograma. Los tooltips propios usan `__rwShowTip`, que pone `inner2.zero`.
- En AS2 `var` es de la función entera: cuidado con nombres repetidos dentro de los bucles. En I30 una variable `A` pisaba la geometría.
