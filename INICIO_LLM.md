# Empieza aquí: guía para cualquier LLM que trabaje en este proyecto

Este proyecto lo trabajan varias IA (Claude, ChatGPT y otras) por turnos, con el mismo usuario. Para no perder el contexto entre una y otra, **lee este archivo primero**. Al terminar tu sesión, actualiza la sección 9.

Conversa con el usuario en **español neutro**.

## 1. Qué es

Es un **mod de Sonny 2**: el juego Flash de Krin/Armor Games, en AS2/AVM1. El usuario lo juega en la **Sonny Legacy Collection de Steam**, que es una app Adobe AIR con un lanzador AS3 «2K nativo», en pantalla de **2560×1440 (16:9)**.

El mod hace dos cosas:
- **El juego a 16:9 y 2K, con fondos HD:** pantallas de zona y fondos de combate.
- **El rework del lobo Mokoshotar:** una clase nueva, con su árbol de habilidades y su tienda. Está en pausa.

**El archivo que se cambia:** `SONNY2.swf`, en `C:\Program Files (x86)\Steam\steamapps\common\Sonny Legacy Collection\SonnyLegacy.app\Contents\Resources`. `instalador/INSTALAR.bat` lo copia con respaldo, y `RESTAURAR.bat` vuelve atrás.

## 2. Dónde está todo (repo `jkdjaslkdjaskljdlkasjd/test2`, privada, rama `main`)

| Ruta | Qué es |
|---|---|
| `INICIO_LLM.md` | Este archivo: por dónde empezar |
| `TRASPASO.md` | El detalle técnico de lo último hecho: cómo compilar y probar, reglas y trampas. **Léelo después de este** |
| `estado-mod-sonny.md` | El historial completo, versión por versión |
| `README.md` | El índice de carpetas |
| `iNN/` | Cada versión entregada, con `LEEME.md`, `fuente/`, `documentacion/` y `capturas/`. La vigente tiene además `SONNY2.swf`. Hay versiones desde **I26** (las anteriores no se subieron) |
| `iNN/documentacion/ZONAS_HD.md` | Cómo funcionan las pantallas de zona y cómo agregar una imagen HD |
| `iNN/documentacion/COMBATE_HD.md` | Cómo funcionan los fondos HD de combate: las dos capas y la cámara |
| `trabajo/` | Base compilable: `bases/` (el SWF de partida), `paso5/` (herramientas y descompilación), `iNN/` (fuente de trabajo) y `herramientas/` (Real-ESRGAN en numpy) |
| `fondos_hd/` | **El arte HD del usuario**, por zona: `batallas/` (fondos de combate) y `world_map/` (pantallas de zona). Aquí se dejan las imágenes nuevas |
| `planes/` | Planes de arte para generar imágenes (por ejemplo, `PLAN_NEW_ALCATRAZ_HUMO.md`) |
| `instalador/` | `INSTALAR.bat` y `RESTAURAR.bat` |

## 3. Quién hace qué

- **ChatGPT u otra IA de imágenes:**
  - dirige el arte y **genera las imágenes**, siguiendo un plan de `planes/`;
  - trabaja en **modo plan**: primero pregunta, después genera;
  - deja los PNG en `fondos_hd/`, sin comprimir.
- **Claude, u otra IA que programe:**
  - **no genera imágenes**: compone, amplía (Real-ESRGAN) e integra;
  - compila el SWF;
  - lo prueba en Ruffle;
  - documenta y sube a la repo.
- **El usuario:** elige y lo prueba en su app (AIR). La prueba que vale es la suya: Ruffle no reproduce todos los comportamientos de AIR (ver la sección 7).

## 4. Reglas del usuario (vigentes)

1. **Español neutro.**
2. **Entregas solo por GitHub.** No subir archivos al chat de Claude: tiene un límite de 30 MB y comprime.
3. **Calidad máxima en imágenes:**
   - PNG o bitmaps sin pérdida (`DefineBitsLossless2` dentro del SWF);
   - nada de JPEG;
   - si hay que ampliar, se usa Real-ESRGAN `realesr-animevideov3` y después Lanczos.
4. **En la repo quedan solo los 5 SWF más nuevos**, cada uno en `iNN/SONNY2.swf`. Al subir uno nuevo, se borra el más viejo; los anteriores se recompilan desde `trabajo/`.
5. **El arte tiene que parecer del Sonny 2 original, limpio a 2K:** formas planas y bordes nítidos. Nada de pintura, anime ni fotorrealismo.
6. **De a poco:**
   - un cambio por vez;
   - probarlo;
   - preguntar antes de decisiones que no se pueden deshacer.
7. **Hoy no se tocan las habilidades.** Hay una revisión pendiente que se conversa antes.
8. **Respetar las capas propias del usuario** (`__nz*`, NULL ZONE, night, i18):
   - no se modifican;
   - envolver sus funciones (llamar a la original y agregar algo) sí se puede.
9. **Nunca correr una simulación Heroic.**
10. **Commits de Claude:** terminan con su trailer de sesión.

## 5. Estado actual (versión vigente: I39, 01/10/2026)

| Pantalla | Estado |
|---|---|
| **Zona 1 New Alcatraz** (pantalla de zona) | **HD de prueba** (`fondos_hd/world_map/PRISON_Z1*.png`). Hay un plan de 5 versiones con humo: `planes/PLAN_NEW_ALCATRAZ_HUMO.md` |
| Zona 2 Oberursel | HD (desde I19) |
| Zona 3 tren, Zona 5 Hew y Zona 7 Japón | Arte original |
| Zona 4 Labyrinth y Zona 6 Il Sanctus | HD (I31). Desde I38, sin pérdida; Labyrinth ampliada con Real-ESRGAN |
| NULL ZONE (zona del usuario) | HD. Desde I38 tiene el botón **ZONAS**, que lleva a cualquier zona para probar |
| **Combates HD** | **Los 10 fondos activos** (desde I39): las 12 combinaciones de suelo y cielo, es decir, los 99 combates. JAIL ya tiene el corte final entre capas; los demás todavía usan el de I35 |

**Pendientes, en orden:**
1. **El usuario prueba I39 en su app:**
   - todos los combates;
   - la Zona 1 HD;
   - el botón ZONAS;
   - que Hew siga bien después de la cárcel.
2. **Arreglar el corte entre capas, fondo por fondo**, con la regla de la sección 6:
   - **CHURCH y ROME:** los pilares se parten con el zoom. Hace falta una versión «sin pilares» de cada imagen, que la genera la IA de imágenes;
   - **TRAIN:** la base de los paneles;
   - **STREETS2:** el pie de las columnas;
   - el resto, según el video del usuario. La tabla está en `i39/LEEME.md`.
3. **Las 5 versiones con humo de New Alcatraz,** según el plan de `planes/`.
4. **`fondos_hd/world_map/VILLAGE_Z2.jpg` y `ROME_Z6.jpg`:** las subió el usuario, pero todavía no están en el juego. Preguntar si van y, si van, pedir el PNG sin pérdida.

## 6. Reglas para las imágenes HD

**Pantallas de zona:**
- PNG opaco de 2560×1440 (o 1673×941, que se amplía);
- sin HUD ni anillos pintados;
- los tres anillos del juego tienen que caer en lugares legibles: ver las coordenadas en el plan de New Alcatraz y en `ZONAS_HD.md`;
- abajo, la barra de navegación (al 62 %, centrada) tapa x 330–1345, y 800–910, sobre 1673×941.

**Fondos de combate:**
- PNG opaco de 2560×1440;
- **la cámara del juego hace zoom sobre el suelo y los personajes**, así que la imagen se separa en dos capas:
  - **capa quieta:** solo lo lejano: cielo, montañas y la ciudad del horizonte;
  - **capa que se mueve:** todo lo cercano: piso, paredes, edificios, pilares y rejas;
- si una estructura cercana tapa el fondo (pilares, edificios), hace falta lo que hay detrás: Claude lo estira desde el cielo o, si no alcanza, pide a la IA de imágenes una versión «solo fondo».

## 7. Trampas técnicas que ya costaron caro

- **Profundidad ocupada:**
  - un `gotoAndStop` hacia adelante recorre todos los fotogramas intermedios, y Flash/AIR **ignora una colocación en una profundidad ocupada**;
  - dos veces quedó una imagen pegada en otra zona: el bug de Hew en I31 y «siempre CHURCH» en I35;
  - **Ruffle no lo reproduce.** Hay que simular la línea de tiempo (ver `TRASPASO.md`) o probar en AIR.
- **Calidad en el zoom:** con la opción SFX3 apagada, el juego baja la calidad a `LOW` durante el zoom de los ataques. En HD se mantiene la calidad del jugador.
- **Bitmaps con alfa** (`Lossless2`, `JPEG3`): el color va **premultiplicado** por el alfa. Si no, aparece un contorno claro.
- **El tamaño del SWF:**
  - hoy pesa unos 50 MB, por las imágenes sin pérdida;
  - GitHub avisa desde los 50 MB y rechaza desde los 100 MB por archivo;
  - si se pasa de 100 MB, consultar al usuario.

## 8. Cómo compilar y probar (para una IA con terminal)

```
cd trabajo && sh preparar.sh            # arma act1/act3/base1 (una vez por contenedor)
python3 i39/build.py SONNY2_I39.swf     # mismo SHA que i39/SONNY2.swf
python3 i39/build.py X.swf --debug      # con el gancho para el banco de Ruffle
```

- **El banco de Ruffle:**
  - el reproductor se baja de las releases de GitHub (`ruffle-rs/ruffle`, nightly *web-selfhosted*);
  - los guiones van en `iNN/fuente/banco/*.json`, y el que los corre es `i30/fuente/ruffle/drive.js` (ver `TRASPASO.md`, sección 4).
- **En el juego:** NULL ZONE → botón **ZONAS** → la zona que se quiera probar.

## 9. Registro de sesiones (agregar una línea al terminar, la más nueva arriba)

- **01/10/2026, Claude:** I39, con los 10 fondos de combate activos, sin pérdida. Probados en Ruffle; quedan anotados los arreglos de cada mapa.

- **01/10/2026, Claude:**
  - I38: Zona 1 con la imagen HD del usuario (de prueba, ampliada con Real-ESRGAN), imágenes sin pérdida, botón ZONAS en NULL ZONE;
  - plan de las 5 versiones con humo;
  - este archivo.
- **01/10/2026, ChatGPT:** ordenó `fondos_hd/` (batallas y world_map) y subió `VILLAGE_Z2.jpg` y `ROME_Z6.jpg`.
- **01/10/2026, Claude:** I31 a I37 (fondos de zona y de combate HD, cámara en dos capas, arreglos para AIR) y mudanza a esta repo.
