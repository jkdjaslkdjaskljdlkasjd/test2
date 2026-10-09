# Prompt: luces de las ventanas del tren (Zona 3) para ChatGPT

**Para qué sirve:** en el juego original, unas luces de afuera pasan por las ventanas del vagón. En I40 quedaron tapadas por la imagen HD. Con estas dos piezas, Claude abre las ventanas en la imagen y anima los haces por detrás, como en el original. El parpadeo cálido/azul ya funciona y no hace falta tocarlo.

**Cómo se usa:** pega el prompt en ChatGPT y adjunta `fondos_hd/world_map/TRAIN_Z3_calido.png` y `TRAIN_Z3_azul.png`.

**Qué hacer después:** sube los resultados a `fondos_hd/world_map/` como `TRAIN_Z3_mascara.png` y `TRAIN_Z3_luz.png`, en PNG y sin comprimir.

```
ROLE: Art assets for the 2D Flash RPG "Sonny 2", zone 3 "Ivory Line: The Train". Ask me first.

CONTEXT: Image 1 (warm) and image 2 (blue) are the final train backgrounds (1673x941). In the game, lights from the outside pass across the windows from right to left, seen through the window glass. I need two assets to rebuild that effect. Do NOT redraw the train.

HOW WE WORK
1. Do NOT generate anything yet. Ask me the QUESTIONS in Spanish, numbered, in one message, with 2-3 options each and one marked "(recomendado)".
2. Make ASSET 1, wait for my ok, then make ASSET 2.

ASSET 1 - WINDOW MASK (1673x941, PNG, exact same framing as image 1)
- Copy image 1 exactly, and fill ONLY the glass area of every window (the dark panes between the curtains, on both sides of the car, near and far) with flat pure magenta #FF00FF.
- Curtains, frames, wall lamps, seats and everything else stay pixel-identical to image 1.
- No soft edges, no glow, no antialias halo in magenta. The same mask is used for the blue version.

ASSET 2 - PASSING LIGHT (PNG, 1024x256, pure black background)
- One soft horizontal streak of light, as seen from inside a moving train at night: a bright warm-white core, fading to the left and right, slightly blurred, in Sonny 2 style (simple, clean, no lens flare, no texture).
- Centered, nothing else in the image. The game moves and tints it.

QUESTIONS
1. Color de la luz que pasa: (a) blanco cálido (recomendado); (b) amarillo de faroles; (c) blanco azulado.
2. Forma: (a) una franja alargada suave (recomendado); (b) un punto de luz con estela; (c) dos franjas paralelas.
3. ¿Marco también las ventanas del fondo, las más lejanas? (a) sí, todas (recomendado); (b) solo las más grandes.
```
