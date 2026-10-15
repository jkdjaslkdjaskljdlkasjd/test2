# Traspaso — Sonny 2 HD en Godot 4.7.2 (SNOW) — 15-10-2026

## Objetivo y reparto
- **Objetivo:** llevar Sonny 2 a Godot 4 en HD manteniendo la fidelidad al SWF original (I41).
- **Gemini:** desarrolla el código.
- **ChatGPT:** convierte las entregas en archivos, los guarda en Drive y los valida en carpetas aisladas.
- **Claude:** extrajo y catalogó los recursos originales del SWF y midió los modelos. Su trabajo está en GitHub `jkdjaslkdjaskljdlkasjd/test2`, rama `recursos-originales-i41`.

## Enlaces
- Drive general: https://drive.google.com/drive/folders/1kvwWUET7C5QYGSRgQf7u9JtbF4S0Faff
- Revisión 4 (proyecto completo e informe): https://drive.google.com/drive/folders/1HdN0Ixj3_gv5HBzgA0ZGUk088vMNtVKr
- Revisión 3 (extractor y JSON): https://drive.google.com/drive/folders/1LiG16emUQqicw9YgxeROqH28hHA6FhLA
- GitHub, rama `recursos-originales-i41`:
  - `04_Recursos_Originales_I41/`: recursos, catálogos, 145 personajes y escenas Godot;
  - `godot_snow/SNOW-002_REVISION_4_AISLADA_respaldo/`: copia sin cambios de la revisión 4 con sus hashes;
  - `godot_snow/SNOW-002_REVISION_5_AISLADA/`: la revisión 5.

## Comprobado
- **SNOW-001** funciona.
- **Revisión 4 (aislada).**
  - Godot importó y ejecutó correctamente: 72 casos sin fallos.
  - El render confirmó que la ayuda no tapa las barras.
  - El usuario la probó en Windows y funciona bien.
- **Colocación de personajes en el juego (código I41).**
  - `BATTLESCREEN["player"+id].attachMovie(model,"inner",0)` pone el origen del MODEL en el origen del slot, con matriz identidad. Los slots enemigos usan matriz espejo (a = −1).
- **La caja F1 no es el personaje.** Es el `MODEL1` crudo `inner2` del marcador 2503 colocado en (−9, −4), y se autodescarga en el juego (`unloadMovie`).
- **Medidas en reposo** (unidades SWF del slot, `stand` completo; medidas con el rig extraído de I41 y contrastadas con JPEXS, ±0,3 u):

  | Modelo | Caja del cuerpo | Apoyo (pies) |
  |---|---|---|
  | Veradux/Sonny (MODEL1) | x −16,88…16,25 / y −43,12…39,88 | **y = +39,88**, constante en los 45 fotogramas |
  | Felicity (MODEL4) | — | +42,6 |
  | Mokoshotar (MODEL5) | — | +45,9 (el juego lo escala 0,8 y lo baja 10) |

  La línea F1 (+45,75) queda **5,87 u (14,7 px a 1440p) por debajo** de los pies reales.

## Estado de integración
- La revisión 4 sigue aislada; **no se ha confirmado** que esté integrada en el proyecto principal.
- **Revisión 5: preparada, sin ejecutar en Godot.** Parte de la revisión 4 y añade:
  - Veradux AP129 reproduciendo `stand` en `player1`, en una capa nueva `GroundLayer/UnitsLayer`;
  - la línea de apoyo real;
  - el test `tests/test_snow005.gd` (anclaje y escala en cada tick de zoom y temblor).
- Faltan:
  - ejecutar `test_snow002.gd`, que debe seguir en 72/0;
  - ejecutar `test_snow005.gd`;
  - la prueba visual en Windows.

## Pendientes
- Validar la revisión 5 en Godot y en Windows.
- Decidir si el apoyo real (+39,88) sustituye a la línea F1 como referencia de pies.
- El borde duplicado sutil de SNOW sigue sin resolver.
- La copia de seguridad en Drive está pendiente: no hubo conector de Drive en la sesión de Claude.

## Reglas
- Conservar lo validado.
- No inventar valores originales.
- No implementar combate ni pasar a otro fondo.
- Distinguir siempre lo comprobado de lo propuesto.

---

## Mensaje para pegar en el nuevo chat de **ChatGPT**
```
Continúa como orquestador de Sonny 2 HD en Godot 4.7.2. Gemini desarrolla el código; tú conviertes sus entregas en archivos, los guardas en Drive y los validas en carpetas aisladas. No inventes archivos ni implementes funcionalidades por tu cuenta.

Estado comprobado: SNOW-001 funciona. SNOW-002 revisión 4 (aislada): 72 casos sin fallos, render correcto, probada en Windows por el usuario. No supongas que está integrada; verifica el proyecto principal y respáldalo antes de integrar.

Nuevo (de Claude, en GitHub jkdjaslkdjaskljdlkasjd/test2, rama recursos-originales-i41, carpeta godot_snow/): respaldo sin cambios de la revisión 4 y una revisión 5 aislada, PREPARADA PERO NO EJECUTADA. Pone a Veradux AP129 (modelo original en reposo) en player1, en GroundLayer/UnitsLayer, con la línea de apoyo real y un test nuevo (tests/test_snow005.gd).
Datos comprobados del código I41: el personaje va en el origen del slot (attachMovie "inner", identidad); la caja F1 es un marcador que se autodescarga; los pies de MODEL1 están en y=+39,88 u SWF (la línea F1 en +45,75 queda 5,87 u por debajo).

Tarea: sube la revisión 5 a Drive en carpeta aislada, ejecuta test_snow002.gd (debe seguir 72/0) y test_snow005.gd en Godot 4.7.2, haz capturas en reposo, con zoom y con temblor, e informa. No integres en el proyecto principal sin confirmación. Pendiente aparte: borde duplicado sutil de SNOW.
Lee LEEME.txt de la revisión 5 antes de actuar. Respuestas breves, sin subagentes.
```

## Mensaje para pegar en el nuevo chat de **Gemini**
```
Proyecto: Sonny 2 HD en Godot 4.7.2 (fondo SNOW). Desarrollas el código; ChatGPT lo guarda y valida. Conserva lo validado, no inventes valores originales, no implementes combate ni pases a otro fondo.

Comprobado: SNOW-002 revisión 4 aprobada (72/0, prueba visual en Windows correcta), aún aislada.
Datos del SWF I41 (medidos por Claude, en GitHub test2, rama recursos-originales-i41):
- El juego coloca al personaje con attachMovie(model,"inner",0) en el origen del slot, sin desplazamiento; los enemigos usan el espejo del slot.
- La caja F1 es un marcador (MODEL1 crudo en (-9,-4)) que el juego descarga; no es el personaje.
- MODEL1 en reposo: cuerpo x -16,88..16,25, y -43,12..39,88; pies en y=+39,88 u SWF. Escala: 1 u = 1440/575 px.
- Hay escenas Godot de los 145 personajes originales (1 unidad = 1 px SWF), con todas sus animaciones.

Revisión 5 (preparada por Claude, pendiente de validar por ChatGPT): Veradux real en player1 en GroundLayer/UnitsLayer, con línea de apoyo real y test de anclaje en zoom/temblor.
Siguiente, solo cuando la revisión 5 esté validada: proponer cómo extender a los 6 slots usando el apoyo medido de cada modelo, sin combate. No generes código hasta que se confirme la validación.
```
