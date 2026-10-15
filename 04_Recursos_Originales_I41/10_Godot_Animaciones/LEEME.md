# Animaciones convertidas a Godot 4 (sin integrar en el proyecto)

Escena independiente por personaje, generada a partir de los datos exactos del SWF I41. **No se ha tocado el proyecto Godot existente.** Para probarla, copia la carpeta del personaje (p. ej. `Veradux_AP129/`) a la raíz de un proyecto Godot 4 y abre su `.tscn`.

## Estructura de cada escena
- `Node2D <personaje>` → `Modelo` → un `Node2D` por instancia de `MODEL1`: los huesos `head`, `chest`, `arm1`… y la sombra `shadower`, en el **orden de profundidad SWF**, que es el orden de dibujo.
- Dentro de cada hueso, un `Sprite2D` por pieza que adjunta `attachMovie`:
  - en orden piel (−1) → equipo (0) → pelo (2);
  - textura PNG ×8 con `centered=false`, `offset = −anclaje` y `scale = 1/8`;
  - resultado: **1 unidad Godot = 1 px SWF**. Escala el nodo `Modelo` para HD.
- `AnimationPlayer` con una animación por etiqueta de `MODEL1`: `stand`, `run`, `Attack_Upper`, `Attack_Stab`, `Attack`, `attack2`, `runback`, `cast`, `stun`, `stun2`, `outofstun`, `hit` y `dead`. Funciona a 30 fps con interpolación **NEAREST** (fotograma a fotograma, como Flash). Pistas:
  - `transform`: `Transform2D` exacto de la matriz SWF, sin descomponer, así que conserva el sesgo;
  - `visible`: solo si un hueso desaparece;
  - `modulate`: multiplicadores de color SWF, p. ej. el oscurecimiento 154/256 de las extremidades traseras;
  - `metadata/desenfoque_swf` (Vector2, en px): el `BlurFilter` de los ataques. Godot no lo aplica solo; necesita un shader si se quiere reproducir.
- Bucles según el código de `MODEL1`:
  - `stand` y `stun2` repiten;
  - `Attack_Upper` y `Attack_Stab` pasan a `runback`; `runback`, `cast`, `outofstun` y `hit` pasan a `stand`;
  - `run` se detiene (`stop`); `dead` termina con `removeMovieClip`;
  - `Attack`, `attack2` y `stun` no tienen acción al final: en Flash siguen reproduciendo la etiqueta siguiente.

  Todo está en `datos_animacion.json` (`loop`, `siguiente`).
- `datos_animacion.json`: los mismos datos en JSON, más:
  - `sonidos_por_fotograma` (`sfx_swing`…);
  - `efectos_no_incluidos_en_escena`: los efectos de la profundidad 33 (barrido de ataque 2457/2461/2370, lanzamiento 2295, estrellas de aturdimiento 2298), con fotogramas y posición.

## Verificación (sin ejecutable de Godot en el entorno)
`verificacion/lamina_godot_vs_jpexs.png` muestra el primer fotograma de cada animación recompuesto con la misma semántica que Godot y comparado con el render JPEXS de la reconstrucción.
- **Coinciden:** 11 de 13 animaciones, con IoU de alfa entre 0,947 y 0,957. La diferencia restante es el grosor de contorno: las texturas ×8 reducidas a ×2 dejan los contornos más finos.
- **`attack2` (0,22) y `stun2` (0,84):** difieren solo porque faltan los efectos de la profundidad 33 y el desenfoque.
- **Sin probar en Godot:** la escena no se ha abierto en Godot real. Se comprobó la sintaxis: llaves balanceadas, referencias definidas y pistas que apuntan a nodos existentes.

## Pendiente
- Efectos de la profundidad 33 como escenas propias.
- Shader de desenfoque.
- Términos aditivos de color (anotados en el JSON, no aplicados).
- Prueba en el editor de Godot.
