# Sonny 2 a 16:9: I30 (menú de habilidades en 2K)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I30) | `9a0f17755223035f6dc94763ac80ecfe51b160d1a2a6ad2d7299d348ddeb1444` |
| Base: `SONNY2.swf` de I29 | `b440bf336021bf4747df5d8647a392a76503e924acd0250c60022d77863cbf21` |

Para instalar, reemplaza solo `SONNY2.swf`; el lanzador sigue siendo el mismo. Las partidas de I25 a I29 siguen sirviendo.

## Cambios respecto de I29

### El menú de habilidades ocupa todo el 16:9

Ya no se ve el recuadro de 800 con las bandas borrosas a los costados (`09_antes_despues.png`).

- **Panel:** el panel rojo llega hasta 14 unidades del borde de la pantalla y baja hasta justo arriba de la barra de navegación.

  | | Ancho (x) | Alto (y) |
  |---|---|---|
  | Antes | de 14 a 783 | de 15 a 440 |
  | Ahora | de −97 a 897 | de 15 a 470 |

- **Recuadros:**
  - el del árbol y el de la barra de combate pasan de 249 a 362 de ancho;
  - los tres miden 30 unidades más de alto;
  - el del centro conserva su ancho. El recuadro de Sonny es más alto, con el aviso de puntos centrado, y el de atributos baja con todo su contenido.
- **Árbol:** el de clase y el del lobo usan la misma grilla.

  | | Íconos | Columnas | Filas |
  |---|---|---|---|
  | Antes | 24 unidades | cada 52 | cada 40 |
  | Ahora | 34 unidades (140 %) | cada 70 | cada 45 |

  Crecen en proporción:
  - los caños;
  - el anillo de las pasivas clave;
  - el emblema;
  - los niveles de cada fila;
  - el selector «Abilities · Instincts».
- **Barra de combate y Ability Pool:** la barra está al 118 % y el Ability Pool al 119 %, los dos centrados en su recuadro.
- **Pestañas, títulos y cruz:** las pestañas «Class» y «Mokoshotar», los títulos de los recuadros y la cruz de cerrar se mueven con su recuadro.
- **Tutorial «< Click Here >»:** el marco verde y las flechas apuntan al nuevo lugar de cada cosa:
  - «Ability Points» y el árbol;
  - «Attribute Points» y los atributos;
  - el Ability Pool y la barra de combate.
- **Nitidez:** los íconos del lobo son imágenes de 128 px. En 2560x1440, al 140 %, se ven a unos 98 px, así que no pierden definición (`10_2560x1440.png`).

### El panel de Aspectos también está en 2K

NULL ZONE → MOKOSHOTAR → «Aspectos y definitivas» usa el mismo panel y los mismos recuadros que el menú de habilidades:
- la lista de Aspectos y la definitiva van en los recuadros anchos;
- las descripciones tienen más lugar;
- «Volver» está arriba a la derecha.

### Lo que no cambia

- **Las otras páginas del menú** (inventario, tienda, datos, opciones y logros) siguen con el menú de 800. El panel y los recuadros son las mismas piezas del juego para todas las páginas: al salir de habilidades vuelven a su lugar, sin parpadeo (`07_inventario_sin_cambios.png`). Si quieres, en otra versión las paso a 2K también.
- **Las habilidades** no cambian: sus números, sus textos y los íconos son los mismos.
- **Tus capas** no cambian: el hub MOKOSHOTAR de la NULL ZONE y las capas night e i18.

## Cómo está hecho

- **Por código:** todo el cambio está en `src/rw_80_2k.as` y trabaja sobre las piezas del juego, sin tocar dibujos ni íconos.
  - El panel y los recuadros se estiran; los textos y los botones se mueven.
  - El árbol de clase se reubica en la grilla nueva, y el juego redibuja sus caños solo.
  - Mientras el menú está abierto se ocultan los reflejos borrosos de los costados, y cuando se cierra vuelven.
- **Cuándo se aplica:** al entrar a la página de habilidades. Al entrar a cualquier otra página (todas llaman a `__v92Cleanup`), las piezas compartidas vuelven a su lugar antes de dibujarse.
- **Dos arreglos en el SWF** (`build.py`):
  - **Rectángulo del árbol de clase:** el árbol trae un rectángulo negro (forma 3145) que coincidía con el borde de su recuadro. En 2K quedaba suelto, así que ahora es transparente; en el menú de 800 no cambia nada.
  - **Tutorial del aviso de puntos:** las 119 colocaciones de la animación del sprite 3205 se corren al nuevo lugar. Los números salen de `__rw2kL`, así que si cambia el diseño se acomodan solas.
- **Volver al menú de 800:** con `_root.__rw2kEnabled = false` vuelve el menú de I29.

## Probado

- **Banco fiel:** `fuente/tests/test_rework.py` hace 312 comprobaciones y pasan todas. Son las 298 de I29 más 14 del menú 2K:
  - la grilla está centrada en el recuadro del árbol, y los íconos, los niveles y el selector entran en él;
  - el panel está dentro del 16:9 y no llega a la barra de navegación;
  - fuera de la página de habilidades (o con `__rw2kEnabled = false`) vuelve la grilla de 800.
- **Ruffle en 16:9:** ahora el arnés muestra la pantalla como tu lanzador 2K, sin estirarla (x de −111 a 911). Lo hace con la página `page16.html`, con escala fija y sin bandas negras. Las capturas son a 1280x720 y una a 2560x1440, y se probó esto:
  - el árbol del lobo en sus dos páginas, con tooltips y emblema;
  - el árbol de clase con datos: al aprender, los caños se redibujan en su lugar;
  - asignar habilidades a la barra: clic en el Ability Pool y clic en la casilla;
  - las tres partes del tutorial;
  - pasar a inventario y volver, y cerrar el menú;
  - abrir el árbol desde la NULL ZONE;
  - el panel de Aspectos: elegir, activar, aprender y «Volver».
- **Falta:** probarlo en tu app (AIR).
- **No se corrió ninguna simulación Heroic.**

## Fuente (`fuente/`)

- **`build.py`:** `python3 build.py i30.swf` arma el SWF desde I25 con las herramientas del paso 5; con `--debug` suma el gancho de depuración. Da siempre el mismo SHA.
- **`src/rw_*.as`:** la capa del rework. En esta versión:
  - `rw_80_2k.as` es nuevo: el menú de habilidades en 2K;
  - `rw_70_ui.as` cambió: la grilla del árbol (`__rwG`, 800 o 2K) y las medidas del panel de Aspectos (`__rwAspGeo`).
- **`dl.py`:** lista las piezas de un sprite en un fotograma. Con esto se midió el menú.
- **`tests/`:** el banco. Espera `i30.swf` al lado de `build.py`.
- **`ruffle/`:**
  - `page16.html`: la página 16:9;
  - `drive.js`: ahora acepta `down` y `up` del mouse, y la página se elige con `PAGE`;
  - `gen/mk.py`: pasa coordenadas del juego a coordenadas de pantalla;
  - `s_final30.json` y `s_final30_2560.json`: los guiones de estas capturas.

## Capturas (`capturas/`)

| Captura | Qué muestra |
|---|---|
| `01_habilidades_2k.png` | El árbol del lobo (Abilities) en el menú 2K |
| `02_instincts_2k.png` | La página Instincts, con los anillos de las pasivas clave |
| `03_clase_2k.png` | La pestaña Class: el árbol de clase en la misma grilla, con sus caños |
| `04_tooltip_2k.png` | Tooltip de Primal Breath |
| `05_barra_y_pool.png` | Dos habilidades asignadas a la barra desde el Ability Pool |
| `06_tutorial_2k.png` | La parte 3 del tutorial: el marco verde rodea el Ability Pool y la flecha sube a la barra |
| `07_inventario_sin_cambios.png` | Inventario: las otras páginas siguen como antes |
| `08_aspectos_2k.png` | El panel de Aspectos en 2K |
| `09_antes_despues.png` | I29 contra I30, en la misma vista 16:9 |
| `10_2560x1440.png` | El árbol del lobo a 2560x1440, la resolución de tu pantalla |

## Lo que sigue

Revisar las habilidades: dijiste que pocas aprovechan las marcas (Scent, Wounds y Frostbite), salvo unas cuantas. Antes de cambiar nada lo conversamos.
