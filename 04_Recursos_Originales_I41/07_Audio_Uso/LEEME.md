# Uso del audio — quién lo usa y cuándo suena

Fuente: código AS2 decompilado de I41 (`03_Codigo/scripts_as`) y líneas de tiempo del SWF. Solo se anota lo que el código o el SWF demuestran.

- `audio_uso.csv` / `.json`: los 147 `DefineSound` con:
  - `quien`: unidad, personaje o movimiento que lo usa;
  - `cuando`: momento en que suena;
  - `combates`: combates `KBR<n>` donde se dice la frase;
  - `frase`: texto en pantalla, de `BATTLESPEECH`;
  - `usos`: recuento por tipo;
  - todas las referencias (archivo:línea) en el JSON.
- `flujos_cinematicas` (JSON): las 7 pistas de audio en flujo y la etiqueta del escenario donde suenan (`CS_INTRO2`, `CS_CUT1`…`CS_CUT5`, `resetHere`).

## Sistema de reproducción (evidencia)
- **`addSound("Effects", nombre)`** (`frame_42/DoAction_2.as` l.1-90): 3 canales rotativos (`my_sound1..3`) al 80 % de volumen.
- **Música**:
  - `addSound("Music",1)` en menús y `addSound("Music",2)` en combate, con fundido entre `music1`/`music2`;
  - la pista sale de `soundPlayArray` (`frame_41/DoAction.as` l.4522, 12 entradas en rotación);
  - `_music_boss` suena si `Krin.bossFight`/`bossMusic` o en `progressLevelOn` 24, 30 y 36.
- **Voces de combate**: `voiceHit[random(3)]` al recibir un golpe y `voiceDie` al morir. Los miembros del equipo las toman de su clase `KNU[ClassStats]`.
- **Diálogos de combate**: `KBR<n>.speeches[].voiceOver`. `"v_"` = sin voz.
- **Movimientos**: el último argumento de `addNewMove(...)` es el sonido del golpe.

Todas las entradas tienen al menos una referencia en el código; ninguna quedó sin evidencia.
