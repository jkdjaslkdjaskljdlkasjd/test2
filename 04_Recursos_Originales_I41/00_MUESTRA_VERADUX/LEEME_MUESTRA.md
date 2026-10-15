# Muestra de verificación — Veradux (SWF I41)

Fuente: `SONNY2.swf` I41, 42.221.005 bytes, SHA-256 `6b26ee6d5b1005a15824d10864941cee452072ef1942880aeb65fa6917738812`.
Se trabajó sobre una copia de solo lectura. Herramienta: JPEXS Free Flash Decompiler compilado desde el código fuente
(commit `de7efbf4754865f46c1c5bd36c9db9cc4ef2fa0b`, 19-09-2026). Más detalles en `../90_Registro/`.

## Qué Veradux es cuál

En el juego hay **dos definiciones distintas** con el nombre «Veradux». Ver `identificacion_veradux.json` (citas de línea del código).

| Variante | Qué es | Apariencia |
|---|---|---|
| **A** | **Veradux miembro del equipo** (tu captura) | `MODEL1` + piel `TWO` + pelo `HAIR_TWO` |
| **B** | A con su equipo inicial | + armadura `ZPCI3` (Medic Head/Chest/Hands/Legs/Feet) + arma `M4` (Gun) |
| **C** | Unidad NPC `KNU4` «Veradux» (y `__nzCatalog[4]` del mod) | `MODEL1` + piel `METABII` + `skinSetter="ZPCI3"` |
| **D** | Variante derivada, **no es Veradux** | `METABII` sin armadura |

`lamina_muestra_identificacion.png` compara tu captura con A, B, C y D, y con el `MODEL1` crudo. El `MODEL1` crudo muestra
marcadores NINJA que el juego descarga al cargar; **no es un personaje**.

## Contenido

- `piezas/<grupo>/<linkage>__chid<ID>/`
  - `pieza.svg`: vectorial, exportado por JPEXS.
  - `pieza_x4.png`: ráster ×4.
  - `pieza.json`: anclaje (punto de registro) en SVG y PNG, lista de visualización interna y filtros con todos sus parámetros.
  - `subelementos/`: formas y sub-sprites, cada uno con su CharacterID.
- `animacion/sprite_2462_MODEL1.json`: los 371 fotogramas de `MODEL1` con etiquetas (`stand` 1, `run` 46, `Attack_Upper` 78,
  `Attack_Stab` 108, `Attack` 138, `attack2` 153, `runback` 168, `cast` 189, `stun` 220, `stun2` 240, `outofstun` 280,
  `hit` 296, `dead` 313), y por fotograma: profundidad, instancia (hueso), CharacterID, matriz, color, ratio y filtros.
  Incluye las acciones de fotograma (bucles `gotoAndStop("stand")`, sonidos `sfx_swing`).
  `sprite_24xx.json`: los 8 huesos-marcador.
- `animacion/stand_f1-45/<variante>/png_x4/`: los 45 fotogramas de `stand` de cada variante. Para A hay además `svg_vectorial/`.
- `reconstruccion/`: SWF mínimos de cada variante.
  - Contienen las definiciones originales copiadas byte a byte, más sprites-hueso con lo que `attachMovie` colocaría.
  - `*.spec.json`: la entrada de cada variante.
  - `*.informe_ensamblaje.json`: cada `attachMovie`, si existe en la biblioteca y a qué profundidad va.
- `sonido/`: `hit_dux1` (CharacterID 104), voz de golpe de Veradux.
  - `.original.mp3`: idéntico byte a byte a los datos MP3 del `DefineSound`.
  - `.decodificado.wav`: decodificado para escuchar.
- `verificacion/`: comparaciones numéricas y láminas.

## Grado de certeza (sin mezclar categorías)

| Elemento | Categoría |
|---|---|
| Formas, sprites, sonido, nombres, CharacterID, matrices, profundidades, etiquetas y filtros | **Extracción correcta.** Datos leídos del SWF; MP3 comprobado byte a byte. |
| PNG/SVG de piezas | **Render de JPEXS** de datos correctos. Es un renderizador distinto de Flash Player. |
| Personaje ensamblado (A–D) | **Reconstrucción** que sigue literalmente la lógica `__nzRawDress`; todas las piezas y matrices son originales. |
| Concordancia de datos | **Comprobada**: el fotograma compuesto solo con los datos exportados coincide con el render de JPEXS. A: IoU de alfa 0,981–0,986 y diferencia media de color ≤ 2,3/255 en los 45 fotogramas; B (con filtros y M4): IoU 0,987–0,989. Las diferencias están en el antialiasing de bordes. |
| Fidelidad frente a Flash Player | **No comprobada píxel a píxel.** No hay Flash Player ni Ruffle en este entorno (npm/pip bloqueados). La única referencia real es tu captura: coincidencia visual clara con A, pero a otra escala y en el menú. |

## Notas técnicas para Godot (sin integrar todavía)

- **Contornos.** Los trazos tienen 0,05 px de ancho original. Flash los dibuja como línea de 1 px de pantalla, y JPEXS los
  marca `ffdec:has-small-stroke`. Si se importa el SVG tal cual y se escala, el contorno engorda. Se resolvió con
  `vector-effect: non-scaling-stroke`.
- **Escala.** Las piezas son pequeñas (la cabeza mide 7,9 × 11,35 px) y los huesos aplican escalas de 0,79 a 1,2. Para HD hay
  que exportar los PNG a más zoom o usar los SVG.
- **Efectos temporales.** El combate aplica en tiempo de ejecución filtros por estado (`KrinFilterHit/Heal/Frost/...`,
  `krinChangeColor`) y cambios de forma (`changeForm`). No forman parte de la apariencia base y no se han aplicado.
