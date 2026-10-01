# Paso 5 — Validación del juego recompilado

El juego recompilado desde el AS2 **se comporta igual que el original** en todo el código que se pudo ejecutar: 94 % de las funciones y 83 % de las instrucciones.

## Juego recompilado vigente

`SONNY2_recompilado.swf`, SHA-256 `f6a98433a4591e755e97576f73f240f4e9c9422e84cc04a12d45db012d829e0d`.

**Reemplaza al del paso 4** (`be9e0774…`). Esta validación encontró un error real del descompilador que el paso 4 no había detectado: en `mx.managers.DepthManager`, el `x++` que estaba dentro de una expresión se escribía como una sentencia aparte, antes de la expresión. Por eso el contador de clips (`depthChild…`) se corría en uno. Quedó corregido, junto con las asignaciones encadenadas (`a = b = 30`), que tenían el mismo problema de orden. Los scripts del paso 3 que vienen acá ya incluyen el arreglo.

## Cómo se validó

No hay un reproductor de Flash disponible en este entorno: la red no permite bajar Ruffle. Por eso se usó una **ejecución diferencial**:

1. `tools/avmdiff.py` es una máquina AVM1 con grabadora. Ejecuta el bytecode real y anota cada efecto observable: escrituras en objetos y en el timeline, llamadas a clips (`gotoAndPlay`, `attachMovie`…), `trace` y valores devueltos. Implementa prototipos, `super`, `extends`, `instanceof`, registros globales y locales, `with` y cadenas UTF-8.
2. `tools/diffrun.py` corre el original y el recompilado con **el mismo guion**, sin trampas de por medio:
   - las clases `mx` (DoInitAction);
   - los 121 scripts del escenario, en orden de fotograma;
   - los scripts de sprites, clips y botones;
   - un estado de partida típico: jugador, 6 unidades con buffs y árbol de habilidades;
   - 3 fotogramas de combate: `enterFrame` y botones con `InBattle = true`;
   - un **barrido de todas las funciones que existan**, incluidas las closures y los handlers creados al vuelo, con 10 juegos de argumentos (vacío, ceros, unos, clips, texto, unidades, números, arreglos, mixto y una jugada de combate).
3. Todo se hace dos veces: con clips vacíos, y con clips que crean hijos al vuelo para entrar en más ramas.

| | Clips vacíos | Clips que crean hijos |
|---|---|---|
| Pasos comparados | 18.475 | 18.475 |
| Idénticos | **18.475** | **18.473** (+2 cortados por tiempo, iguales hasta el corte) |
| Distintos | **0** | **0** |
| Efectos comparados | 570.304 | 626.512 |
| Funciones ejecutadas | 1.598 de 1.692 | 1.598 de 1.692 |
| Instrucciones ejecutadas (original) | 83,1 % | 83,4 % |

## ¿La prueba detecta errores de verdad? (prueba de sensibilidad)

Metí 7 errores **a propósito** en la versión recompilada, en distintas partes del juego, y la prueba **encontró los 7**:

| Error introducido | Detectado |
|---|---|
| Clase `mx` DepthManager: `x++` cambiado por `++x` (el mismo error real que se corrigió) | Sí, 10 pasos |
| Motor: fórmula de `getStat`, un 10 cambiado por 11 | Sí, 41 pasos |
| Capa del mod `__v10Life`: el daño recibido sube un 1 % | Sí, 3 pasos |
| Datos: un espacio de más en el nombre de un logro | Sí, 1 paso |
| Clase `mx` UIObject: `!=` cambiado por `==` | Sí, 3.248 pasos |
| Árbol de habilidades: pide 4 puntos en vez de 1 | Sí, 3.957 pasos |
| Bucle que ordena las habilidades: una vuelta de más | Sí, 187 pasos |

El límite es que el barrido usa datos genéricos. Un error que solo aparece en una situación puntual (por ejemplo, un `<` cambiado por `<=` justo en un valor que el barrido no probó) puede pasar sin verse. De hecho, con los primeros datos de prueba, 3 de mis errores no se veían por eso; hubo que ajustar los datos para que aparecieran. Para cubrir el combate real existe además el banco del mod.

## Banco del mod (combate real del lobo)

Las 87 pruebas (57 del lobo y 30 de maestrías) dan **exactamente la misma salida**, número por número, en el original y en el recompilado vigente.

## Lo que falta: probarlo en el juego

Ninguna de estas pruebas reemplaza abrir el juego. Para probarlo, reemplazá `SONNY2.swf` en `SonnyLegacy.app/Contents/Resources` (con copia de respaldo), jugá un rato (menú, carga de partida, un combate, el árbol del lobo, una tienda) y contame si algo se ve o se comporta distinto.

## Archivos

- `tools/` — todas las herramientas de los pasos 1 a 5.
- `paso3/` — scripts regenerados con el descompilador corregido. Usar esta versión.
- `diferencial.json` — resultado completo, con la cobertura por script.
- `mutantes_resultado.json` — la prueba de sensibilidad.
- `roundtrip.json`, `opcheck.json` — las pruebas del paso 4, repetidas con el descompilador corregido: 981/981 y 978/981 (las mismas 3 diferencias equivalentes de antes).

Para repetir la validación: `python3 tools/diffrun.py paso1 paso3 p1_nuevo p3_nuevo salida.json` y `python3 tools/mutantes.py paso1 paso3 salida.json`.
