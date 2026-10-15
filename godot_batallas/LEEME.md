# godot_batallas — combates de Sonny 2 (I41) en Godot 4

Estado: **preparado, NO ejecutado en Godot**.

- `BATALLAS-001_AISLADO/` es un proyecto Godot aislado, un visor de los 99 combates. Lee su `LEEME.txt`.
  - Cada combate muestra:
    - el fondo HD de dos capas, según `__hdBattleMap`;
    - los personajes originales en sus 6 slots, en reposo;
    - las animaciones bajo demanda;
    - la cámara original (zoom y temblor).
  - No tiene lógica de combate.
  - `previews/` contiene vistas previas renderizadas en Python con la misma semántica. **No son capturas de Godot.**
- `combates_alineaciones.json` describe, para cada combate, cada slot: tipo (jugador, compañero, KNU o vacío), nombre, apariencia y modelo, con su procedencia en el código.
  - Lo generó un script en línea durante la sesión, a partir de `KBR<n>`/`KNU<n>` (frame_42).
- `capas_zonas.json` recoge la regla de borde y las estadísticas de las capas de cielo y suelo de las 10 zonas.
- `herramientas/`:
  - `generar_capas_zonas.py`: genera las capas con las funciones sin cambios de `i40/fuente/capas.py`;
  - `preview_batallas.py`: renderiza las vistas previas;
  - `rig.py`: el rig que usa `preview_batallas.py`.
