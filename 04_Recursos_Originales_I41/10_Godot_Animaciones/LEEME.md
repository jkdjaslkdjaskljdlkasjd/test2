# Animaciones convertidas a Godot 4 (sin integrar en el proyecto)

Escenas independientes generadas a partir de los datos exactos del SWF I41. **No se ha tocado el proyecto Godot existente.**

- `sonny_i41/`: los **145 personajes** (`personajes/APxxx_<nombre>/APxxx_<nombre>.tscn`) con texturas compartidas en `texturas/`. Para usarlos, copia la carpeta `sonny_i41/` a la raíz de un proyecto Godot 4 (las rutas son `res://sonny_i41/...`) y abre cualquier `.tscn`.
- `Veradux_AP129/`: Veradux (miembro del equipo) como escena autónoma, con sus texturas y `datos_animacion.json` (todos los datos en JSON). Va en la raíz del proyecto (`res://Veradux_AP129/...`).
- `verificacion/`: comprobación de cada animación (ver abajo).

## Estructura de cada escena
- **Nodos.** `Node2D <personaje>` → `Modelo` → un `Node2D` por profundidad del `MODEL`, en el **orden de dibujo SWF**:
  - huesos (`head`, `chest`, `arm1`…);
  - sombra (`shadower`);
  - capas sin nombre (`capa_<prof>`), como el cuerpo de los modelos sin huesos (Orb, The Bomb);
  - efectos (`capa_33`: barridos de ataque, aturdimiento, lanzamiento).
- **Piezas de los huesos.** Un `Sprite2D` por pieza que adjunta `attachMovie`, en orden piel (−1) → equipo (0) → pelo (2). Usan textura PNG ×8 con `centered=false`, `offset = −anclaje` y `scale = 1/8`, así que **1 unidad Godot = 1 px SWF**. Escala el nodo `Modelo` para HD.
- **Sprites con animación propia** (efectos, cuerpo de Orb…). Son `AnimatedSprite2D` con sus fotogramas PNG ×4, más una pista `frame` que reproduce su avance como en Flash.
- **Cambio de carácter.** Si una profundidad cambia de carácter, cada carácter tiene su propio nodo con pista `visible`.
- **`AnimationPlayer`.** Una animación por etiqueta del `MODEL` (`stand`, `run`, `Attack_Upper`, `Attack_Stab`, `Attack`, `attack2`, `runback`, `cast`, `stun`, `stun2`, `outofstun`, `hit`, `dead`; varía por modelo), a 30 fps con interpolación **NEAREST**. Pistas:
  - `transform`: `Transform2D` exacto de la matriz SWF, sin descomponer;
  - `visible`;
  - `modulate`: multiplicadores de color SWF, incluidas las transparencias del código;
  - `frame`;
  - `metadata/desenfoque_swf`: `BlurFilter` en px. Godot no lo aplica solo; hace falta un shader.
- **Bucles y encadenado, según el código de cada `MODEL`.**
  - `stand` repite.
  - Los ataques pasan a `runback`, y `runback`, `cast` y `hit` vuelven a `stand`.
  - `dead` termina con `removeMovieClip`.
  - Las etiquetas sin acción final (`siguiente: null`) siguen en Flash con la etiqueta siguiente.
  - Varias etiquetas que comparten fotograma (`Attack_Stab`/`Attack_Upper`/`Attack` en `MODEL4`/`MODEL5`) son alias de la misma animación.

## Verificación (sin ejecutable de Godot en el entorno)
Se recompuso el **primer fotograma de las 1.863 animaciones** de los 145 personajes con la misma semántica que Godot (`Transform2D` × `Sprite2D` con offset/escala, `modulate`, `frame`) y se comparó con el render JPEXS del personaje reconstruido. Resultados en `verificacion/verificacion_145_personajes.csv`:
- **Coinciden:** 1.683 de 1.851 animaciones con contenido tienen IoU de alfa ≥ 0,90 (mediana 0,946). La diferencia restante es antialiasing y grosor de contorno: las texturas ×8 reducidas a ×2 dejan contornos más finos.
- **Desenfoque:** 162 quedan entre 0,75 y 0,90 y 6 por debajo de 0,75 (carreras y ataques de monstruos: Magical Monkey, Tunnel Beast, Bunny, Gregor). Coinciden con los fotogramas donde el SWF aplica `BlurFilter`, que la escena no aplica.
- **Transparentes:** 12 animaciones son transparentes en ambos lados (alfa 0 en el SWF, p. ej. el `runback` de los perros).
- **Sin probar en Godot:** las escenas no se han abierto en Godot real. Se comprobó la sintaxis de las 145: llaves balanceadas, referencias definidas, pistas que apuntan a nodos existentes, `load_steps` correcto y texturas presentes.

`verificacion/lamina_godot_vs_jpexs.png`: Veradux, primer fotograma de cada animación, JPEXS frente a Godot.

## Pendiente
- Shader de desenfoque.
- Términos aditivos de color (anotados en `datos_animacion.json`, no aplicados).
- Código de los efectos en tiempo de ejecución (p. ej. `setRGB(colortobe)` del efecto de lanzamiento, que el juego colorea según el movimiento).
- Prueba en el editor de Godot.
