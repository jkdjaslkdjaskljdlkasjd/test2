# 04_Recursos_Originales_I41 — Extracción y catálogo de recursos de Sonny 2 (I41)

**Fuente.** Copia de solo lectura de `SONNY2.swf`, versión I41.
- Tamaño: 42.221.005 bytes.
- SHA-256: `6b26ee6d5b1005a15824d10864941cee452072ef1942880aeb65fa6917738812`. Se comprobó antes y después de la extracción.
- Formato: SWF 9, ActionScript 2 (AVM1), escenario de 800×575 a 30 fps y 449 fotogramas.

**Herramienta.** JPEXS Free Flash Decompiler, compilado desde el código fuente (commit `de7efbf`). Los scripts de apoyo
están en Python y quedan en `90_Registro/herramientas/`. **No se ha modificado ningún proyecto existente** ni se ha hecho
integración en Godot.

## Empieza por aquí

1. `00_MUESTRA_VERADUX/LEEME_MUESTRA.md`: método verificado con Veradux, identificación de sus variantes y comprobaciones.
2. `06_Laminas/`: vista rápida de todo (personajes, pieles, equipo, armas, pelos, efectos, bitmaps, escenario).
3. `05_Catalogo/catalogo_personajes.csv`: qué es cada personaje y con qué piezas se monta.
4. `05_Catalogo/catalogo_recursos.csv`: un registro por CharacterID (4.397) con sus archivos.

## Estructura

| Carpeta | Contenido |
|---|---|
| `00_MUESTRA_VERADUX/` | Muestra de verificación: piezas base y armadura de Veradux, animación `stand`, sonido y verificaciones numéricas |
| `01_Recursos/formas/` | 2.098 formas: `svg/` (vector) y `png_x2/` |
| `01_Recursos/morphs/` | 26 morphs: `svg/` y PNG inicio/fin ×2 (2 morphs vacías no tienen PNG) |
| `01_Recursos/imagenes/` | 113 bitmaps: `original/` (JPEG original y alfa aparte donde existe) y `png/` |
| `01_Recursos/sonidos/` | `original_mp3/`: 147 `DefineSound` idénticos byte a byte al SWF. `flujos_en_sprites/`: 7 pistas de audio en flujo de cinemáticas (MP3 original concatenado) con su sincronía por fotograma |
| `01_Recursos/fuentes/` | 4 TTF (las otras 5 fuentes son de dispositivo, sin glifos) |
| `01_Recursos/textos/` | 226 textos: `plano/` y `con_formato/` |
| `01_Recursos/botones/` | 138 botones × 4 estados, en PNG ×2 y SVG |
| `01_Recursos/sprites/` | `svg_fotograma1/` y `png_fotograma1_x2/` de los 1.609 sprites visibles. `png_todos_fotogramas_x2/` de las 168 animaciones de 2 a 120 fotogramas. `png_muestreo_animaciones_largas_x1/` con ~25 fotogramas de las 20 animaciones largas |
| `01_Recursos/escenario_principal/` | 449 fotogramas del escenario: render estático, sin el contenido que añade el código |
| `02_Datos/` | `inventario_swf.json` (estructura completa: CharacterID, linkage, líneas de tiempo, matrices, filtros, padres/hijos). `animaciones_json/` (1.640 sprites y el escenario, estado por fotograma). `items.json` (449 objetos KRINITEM con su `looks`). `personajes_codigo.json` (unidades, equipo, formas, catálogo del mod). `dumpSWF_jpexs.txt`. `symbolclass_jpexs.csv` |
| `03_Codigo/` | 1.024 scripts AS2 decompilados (`scripts_as/`) y en P-code (`scripts_pcode/`) |
| `04_Personajes/apariencias/` | 145 apariencias únicas. Cada una incluye: SWF de reconstrucción, informe de ensamblaje, poses (primer fotograma de cada animación) en PNG ×2, fotograma 1 en SVG y lámina |
| `05_Catalogo/` | `catalogo_recursos.csv/json` y `catalogo_personajes.csv/json` |
| `06_Laminas/` | Láminas visuales |
| `90_Registro/` | `registro_extraccion.md`, versiones de las herramientas, herramientas y registros de JPEXS |
| `LIMITACIONES.md` | Qué no se pudo hacer o no está comprobado |

## Cómo se monta un personaje (evidencia: `__nzRawDress`, `frame_217/DoAction.as`)

1. `attachMovie(model[0])`: `MODEL1` para hombre, `MODEL4` para mujer; los monstruos usan `MODEL5` a `MODEL9`.
2. En cada hueso (`head`, `chest`, `arm1`… `shoulder`) se adjuntan:
   - la piel `G_S<RANURA>_<piel>` a profundidad −1;
   - el equipo `G_<RANURA>_<set>` a profundidad 0;
   - el pelo `HAIR_<pelo>` a profundidad 2, solo sin casco o si es mujer.
3. Las armas van con `M_WEAPON_<looks>`.
4. Los marcadores visibles de `MODEL*` (piezas NINJA/KATANA) se autodescargan (`unloadMovie(this)`). Por eso **un render
   directo de `MODEL1` no es un personaje**.
5. Las piezas sueltas tampoco son personajes completos: los personajes completos están en `04_Personajes/`.

## Grados de certeza en el catálogo

- **Extracción correcta.** Todo lo leído del SWF: formas, bitmaps, sonidos, nombres, CharacterID, matrices,
  profundidades, etiquetas, filtros y código.
- **Reconstrucción.** Los personajes de `04_Personajes`: lógica de `attachMovie` aplicada sobre definiciones originales.
  - Columna `evidencia = codigo_original`: la apariencia sale de unidades `createNewUnitKrin`, miembros del equipo o
    formas `dressChar`.
  - `solo_catalogo_mod`: solo la define el catálogo `__nzCatalog` del mod.
- **Fidelidad visual comprobada.** Solo Veradux (equipo) frente a la captura del usuario, de forma visual. No hay
  comparación píxel a píxel con Flash Player (ver `LIMITACIONES.md`).
- **Personajes desconocidos.** `DESCONOCIDO` en `personajes_con_evidencia` = pieza sin personaje en el código original.
  Hay 126 piezas así; 102 solo aparecen en el catálogo del mod.
