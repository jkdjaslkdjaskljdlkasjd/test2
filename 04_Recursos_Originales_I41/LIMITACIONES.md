# Limitaciones y puntos no comprobados

## Entorno
- **No hay reproductor Flash.** No hay Flash Player ni Ruffle: npm, pip, Maven y SourceForge están bloqueados por la
  política de red (403).
  - Ningún resultado se ha comparado píxel a píxel con Flash Player.
  - Los PNG son renders de JPEXS (Java2D). JPEXS es otro renderizador: el antialiasing, los degradados y los filtros
    pueden diferir ligeramente de Flash.
- **JPEXS compilado desde fuente.** Su versión se identifica como `0.0.0` (commit `de7efbf`). Esta compilación tiene dos
  fallos, ambos sorteados:
  - el selector `-select all:N` falla junto con `-selectid`; se usó una selección explícita por ID;
  - una morph vacía (0×0) aborta la exportación PNG; se usó `-onerror ignore`.
- **Google Drive no se usó**, por indicación del usuario. Los archivos se recibieron como adjuntos y el SHA-256 coincide.

## Personajes
- **Lo que está comprobado del ensamblaje.** Componer cada fotograma solo con los datos exportados (matrices + SVG/PNG
  de las piezas) reproduce el render de JPEXS del SWF reconstruido:
  - IoU de alfa 0,98–0,99;
  - diferencia media de color ≤ 6/255;
  - comprobado en Veradux A (SVG y PNG) y B (con filtros).

  No está comprobado que la lógica `attachMovie` reproducida sea idéntica al motor real en todos los casos. Hay dos
  supuestos:
  - un `attachMovie` con un linkage inexistente no hace nada;
  - adjuntar en la misma profundidad sustituye lo anterior.
- **Huesos que faltan.** En 21 apariencias de monstruos (`MODEL2`, `MODEL5`–`MODEL9`) el modelo no tiene algunos huesos
  con nombre. Esos `attachMovie` no tienen efecto ni en el juego ni aquí. `MODEL2` (Orb) y `MODEL9` (The Bomb) no tienen
  ningún hueso con nombre: su aspecto es el del propio modelo.
- **Equipo de los miembros del equipo.** Es el **equipo inicial** de la partida (`Krin.equipArray<i>`). En el juego el
  jugador puede cambiarlo.
- **Formas de estado.** Cuando `dressChar(...)` no indica arma, se usa el equipo actual del jugador, que no se conoce de
  forma estática; se dejó vacío y se anotó en `informe_ensamblaje.json`.
- **`MODEL5`.** El juego reduce el contenedor al 80 % y lo baja 10 px. Está anotado pero no aplicado dentro del sprite.
- **Efectos en tiempo de ejecución no aplicados** (no son apariencia base):
  - filtros de estado `KrinFilterHit/Heal/Frost/Flame/...`;
  - `krinChangeColor`;
  - `setRGB` del efecto de lanzamiento (`colortobe`);
  - desenfoques de `BATTLESCREEN`.
- **Escala de pantalla.** No se ha reproducido la escala o zoom de cámara del combate (`GridZoomer`). Las piezas son
  pequeñas en unidades SWF y para HD conviene exportar a más zoom o usar los SVG.
- **Contornos finos.** Los contornos de 0,05 px deben dibujarse como línea de 1 px de pantalla (`non-scaling-stroke`). Si
  se escalan los SVG tal cual, salen gruesos.
- **Anomalías del catálogo del mod.**
  - «USA1 - base»: la piel USA1 solo tiene cabeza, así que el render es una cabeza suelta. Es fiel al código.
  - Varias entradas «- forma»/«- base» del mod duplican apariencias del juego.
- **Clasificación.** 126 piezas de personaje no tienen personaje en el código original y están marcadas `DESCONOCIDO`;
  102 de ellas solo aparecen en el catálogo del mod. 2.181 recursos genéricos (formas o sprites sin nombre exportado
  ni relación con piezas) quedan `sin_clasificar`. Su procedencia está en `padres` y `etiquetas_escenario_alcanzable`.

## Recursos
- **Escenario principal.** Sus fotogramas son estáticos: menús, combate y cinemáticas los rellena el código. Muchos
  salen negros o incompletos.
- **Animaciones largas** (más de 120 fotogramas, cinemáticas). Solo hay una muestra de ~25 fotogramas en PNG. La
  animación exacta está en `02_Datos/animaciones_json`.
- **Fotogramas crudos de `MODEL*`.** No se exportaron porque muestran marcadores NINJA. Sus datos están en JSON y los
  personajes vestidos en `04_Personajes`.
- **Sonidos.** Los WAV decodificados no se incluyen por tamaño; los MP3 son originales. Para regenerarlos:
  `ffmpeg -i X.mp3 X.wav`.
- **Fuentes.** 5 fuentes son de dispositivo (`_sans`, Tahoma, Hypatia Sans Pro, standard 07_55…) y no tienen glifos
  incrustados.
- **Sprites de clases AS2.** 31 sprites de 0 fotogramas (`__Packages.mx.*`) solo contienen clases AS2 y no tienen imagen.
