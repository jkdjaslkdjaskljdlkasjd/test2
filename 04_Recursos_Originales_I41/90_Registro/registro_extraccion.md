# Registro de extracción — 15-10-2026

1. **Comprobación de la fuente.**
   - `SONNY2.swf` (adjunto): 42.221.005 bytes, SHA-256 `6b26ee6d…8812`, coincide con el esperado.
   - Se copió a una ruta de solo lectura. El hash se volvió a comprobar al final y no había cambiado.
2. **Entorno.**
   - Disponibles: Java 21, Python 3.13, ffmpeg y Chromium (Playwright). Versiones en `versiones_herramientas.txt`.
   - JPEXS: las descargas de binarios estaban bloqueadas. Se clonó `jindrapetrik/jpexs-decompiler` (commit `de7efbf`), se
     generaron los lexers con JFlex 1.6.0 y se compiló con `javac` (`ffdec_lib` + aplicación). Se ejecuta en modo
     headless con `herramientas/ffdec.sh`.
   - Ruffle/Flash Player: no disponibles (red bloqueada).
3. **Inventario estructural.**
   - `-swf2xml` y después `inventario.py`, que produce `02_Datos/inventario_swf.json`.
   - Contenido: 4.397 caracteres y 1.110 linkages.
4. **Código.**
   - `-export script` en formatos AS y P-code: 1.024 scripts.
5. **Análisis del ensamblaje.**
   - Funciones: `__nzRawDress`, `dressChar`, `createNewUnitKrin`, `skinSetter`, `createNewItemKrin` y `Krin.*Set`.
   - Herramientas: `items.py` y `personajes.py`.
6. **Muestra de Veradux.**
   - Exportación de piezas y SWF de reconstrucción (`build_assembly.py`).
   - Verificación con `compose_check.py` (SVG en Chromium) y `png_compose_check.py` (PNG en PIL).
   - Se identificó la variante A gracias a la captura del usuario.
7. **Extracción completa.**
   - `run_export.sh` y `run_export2.sh`; resultados en `logs_jpexs/_resumen.txt`.
   - Audio en flujo: `extract_streams.py`.
   - Animaciones: `export_timeline.py`.
8. **Personajes.**
   - `gen_specs.py` (145 apariencias únicas).
   - `render_chars.sh` (SWF de reconstrucción + poses por etiqueta con JPEXS).
   - `catalogo_personajes.py`.
9. **Catálogo y láminas.**
   - `catalogo.py` y `laminas_categorias.py`.

## Verificaciones registradas
- Lectura/escritura de etiquetas SWF: reconstrucción idéntica byte a byte del SWF descomprimido.
- MP3 exportado igual a `DefineSound.soundData[2:]`: comprobado en los sonidos 104 y 77.
- Audio en flujo: los 7 se decodifican sin errores y su duración coincide con fotogramas / 30.
- Recuentos de exportación frente al inventario:
  - formas 2.098/2.098; morphs 26 SVG (24 PNG, 2 vacías); bitmaps 113/113;
  - `DefineSound` 147/147; textos 226/226; botones 138/138;
  - sprites visibles 1.609/1.609 (+31 vacíos de clases).
- Personajes: 145/145 renderizados, con el número de poses esperado (1.817 PNG en total).
- Ensamblaje (Veradux A y B): composición independiente frente a JPEXS, IoU 0,98–0,99.
