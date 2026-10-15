# Escenarios — capas, posiciones, profundidad y movimiento

Fuente: líneas de tiempo del SWF I41 y código AS2. Coordenadas en píxeles del escenario (800×575); matriz en convención Flash (`x'=a·x+c·y+tx`).

- `escenarios.json`:
  - `pantallas_escenario`: las capas de cada una de las 34 etiquetas del escenario principal (mainMenu, Navigation, KRINBATTLESCENE, overMap…). Cada capa trae profundidad, instancia, CharacterID, linkage, posición, escala/rotación, color, filtros, máscara, si tiene código y `origen`.
  - `fondos_combate`: cielo (sprite 3328, profundidad 73, `gotoAndStop(_root.Krin.SkyBG)`) y suelo (sprite 3343 = `BATTLESCREEN`, profundidad 89, `gotoAndStop(_root.Krin.ZoneBG)`). Para cada etiqueta (SEA, JAIL, SNOW, CHURCH, TRAIN, TUNNEL, ROME, STREETS…) incluye su rango de fotogramas, sus capas, qué capas cambian dentro del rango y las acciones de fotograma.
  - `combates`: los 99 combates `KBR<n>` con su `ZoneBG`, `SkyBG` y `players`.
  - `movimiento_codigo`: referencias de código de cámara, zoom y temblor (`GridZoomer`, `GridShaker`, `BATTLEBLUR`, `KrinZoom*`, `KrinShake*`, `__hdBattle*`).
- `capas_pantallas.csv` y `combates.csv`: lo mismo en tabla.
- `render_fondos/` y `lamina_fondos_combate.png`: primer fotograma de cada etiqueta de cielo y suelo (render JPEXS).

## Cómo se arma un combate (evidencia)
1. `frame_201/DoAction.as` l.240-241: `Krin.ZoneBG/SkyBG = KBR[BattlePick].ZoneBG/SkyBG`.
2. En el fotograma 217 (`KRINBATTLESCENE`):
   - el cielo (3328) en la profundidad 73;
   - el suelo `BATTLESCREEN` (3343) en la 89, que contiene los huecos `player1..6` donde `__nzRawDress` adjunta a los personajes;
   - la UI va por encima (barras `p1BAR..p6BAR`, `selector`, `battleClocker`…).
3. Movimiento: el zoom y el temblor los hacen los sprites de código `GridZoomer` (3345) y `GridShaker` (3344) sobre `BATTLESCREEN`. Su código está en `03_Codigo` y en el proyecto Godot existente (`01_Codigo_Referencia_TXT`).

## Precauciones
- **Capas del mod.** `origen = MOD_HD` marca capas añadidas por el mod HD: instancias `__hd*` y, de forma heurística, CharacterID ≥ 4317 (por encima de los 4.316 símbolos del SWF base de PASO1). No son del juego original.
- **Huecos de jugador.** Los `player1..6` del suelo son marcadores (sprite 2503) que el código rellena; en el render estático no representan a ningún personaje.
- **Animación interna.** Ninguna etiqueta de cielo o suelo cambia sus capas dentro de su rango de fotogramas. Si hay animación (luces del tren, parpadeos), está dentro de los subsprites: ver `fotogramas_propios` de cada capa y `02_Datos/animaciones_json`.
- **Pantallas montadas por código.** Mapa, menús de personaje y combate se completan en tiempo de ejecución, así que las capas listadas son solo la parte estática.
