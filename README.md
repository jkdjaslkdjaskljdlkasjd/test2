# test2

Repositorio del mod de Sonny 2.

- `TRASPASO.md`: resumen para retomar el trabajo (lo último hecho, cómo compilar y probar, pendientes).
- `estado-mod-sonny.md`: estado del proyecto.
- `i26/`: rework del lobo (propuesta v4 «Mokoshotar: sangre y escarcha»), con su `LEEME.md` y `fuente/` (código propio del mod: capa `rw_*.as`, `build.py`, pruebas y guiones de Ruffle).
- `i27/`: el árbol del lobo con la forma del árbol de clase (conexiones como requisitos), con su `LEEME.md` y `fuente/`.
- `i28/`: el árbol del lobo ordenado por nivel, el tooltip y los avisos del árbol de clase, el +10 % de Ancestral Wolf restaurado y el panel de Aspectos con la forma del menú de personaje, con su `LEEME.md` y `fuente/`.
- `i29/`: el escudo del juego en los escudos del lobo, los estados que se acumulan con cantidad y turnos, y la regla «cada habilidad sube por Wounds o por Scent», con su `LEEME.md` y `fuente/`.
- `i30/`: el menú de habilidades a lo ancho del 16:9 (2K), con el árbol y la barra más grandes, y el panel de Aspectos con las mismas medidas, con su `LEEME.md` y `fuente/`.

- `i31/`: fondos HD de zona (Labyrinth e Il Sanctus en HD, Zona 1 y Hew al original, arreglo del bug de Hew), con `LEEME.md`, `documentacion/` (`ZONAS_HD.md`) y `fuente/`.
- `i32/`: combate HD en Oberursel (fondo a pantalla completa, solo las barras arriba, panel de abajo al 62 %).
- `i33/`: la imagen HD del combate sigue la cámara.
- `i34/`: combate HD en dos capas (cielo quieto, suelo con la cámara) y el diálogo en su cuadro.
- `i35/`: los 10 fondos de combate en HD (los 99 combates) y el zoom al 50 % en HD.
- `i36/`: combate HD solo en New Alcatraz y Oberursel, con el arreglo de «siempre CHURCH» en AIR y sin pixelado en el zoom. **Versión vigente.** La guía está en `i36/documentacion/COMBATE_HD.md`.
- `fondos_hd/`: fondos de referencia organizados en `batallas/` y `world_map/`. Los mapas limpios son `world_map/VILLAGE_Z2.jpg` (Oberursel) y `world_map/ROME_Z6.jpg` (Il Sanctus), ambos de 2560x1440.
- `instalador/`: `INSTALAR.bat` y `RESTAURAR.bat` (copian `SONNY2.swf` a la carpeta del juego de Steam con respaldo).

- `trabajo/`: la base para compilar. `sh trabajo/preparar.sh` y después `python3 trabajo/i35/build.py SONNY2_I35.swf` dan el mismo SWF que I35 (SHA `5d5a9beb…576e`); con `trabajo/i36/build.py` sale I36 (`49a3537f…2cfd`).
  - `bases/SONNY2_29-09.swf`: el SWF de I30 del que parten I31 a I35;
  - `paso5/`: el contenido de `DECOMPILACION_PASO5.zip` (herramientas, juego base recompilado y su descompilación);
  - `i31/`, `i35/` e `i36/`: la fuente de trabajo, con las imágenes ya preparadas en `build/`.
- **SWF:** se guardan solo los 5 más nuevos (regla del usuario), cada uno en `iNN/SONNY2.swf`: hoy I32 a I36. El vigente es `i36/SONNY2.swf`, para instalar con `instalador/INSTALAR.bat`. Los anteriores se recompilan desde su fuente.

La repo es privada, así que lleva también el SWF, las imágenes y las capturas.
