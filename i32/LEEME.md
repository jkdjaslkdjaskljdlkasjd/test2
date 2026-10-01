# Sonny 2 a 16:9: I32 (combate HD en Oberursel)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I32) | `33328f7fafebed4d27503857a144055e7785f2b8e3ddd97b6cb39a5e4921040a` |
| Base: I31 | `0197c81640fc109a6d9d43ad2fe566f4c67af92263eedfc6552971ca63123c26` |

Para instalar, abre `INSTALAR.bat` con doble clic: guarda un respaldo y copia `SONNY2.swf` en la carpeta del juego (ver `LEEME_INSTALADOR.md`). `RESTAURAR.bat` vuelve a la versión anterior. Incluye todo lo de I31.

## Qué cambia

Los combates de Oberursel (los 17 con escenario `SNOW`) usan tu imagen HD a pantalla completa (`01_oberursel_hd_2560x1440.jpg`; antes: `00_antes_combate_clasico.jpg`).

- **Fondo:** tu imagen cubre los 2560x1440. Ya no se ven el marco de la ventana de combate, las bandas oscuras de los costados ni las líneas negras de arriba y abajo de la escena.
- **Arriba:** se quitó el panel gris. Quedan solo las barras de vida (aliados a la izquierda y enemigos a la derecha), sobre el cielo.
- **Abajo:** el panel de los aliados se achica al 62 % y se centra abajo, igual que la barra del World Map. Tiene la misma medida y el mismo lugar que en la navegación: la habilidad elegida, la barra de habilidades, el botón «!» (saltar turno) con su tooltip y la X roja (`02_panel_y_tooltip.jpg`).
- **Personajes:** se paran en el mismo lugar que antes, ahora sobre la nieve de tu imagen. El zoom de cámara de los ataques sigue funcionando, y ya no corta a los personajes en el borde de la vieja ventana (`03_ataque.jpg` y `04_zoom_de_camara.jpg`).
- **Los demás combates** (cárcel, tren, túneles, iglesia y calles) siguen clásicos hasta que tengan su imagen (`06_carcel_sigue_clasico.jpg`).

## Tu imagen: ¿cumple?

**Sí.** Para este uso cumple bien:

- **Encuadre:** el cielo y las montañas quedan arriba, detrás de las barras de vida. La nieve, donde se paran los personajes, queda en el centro y abajo. La línea de las montañas cae justo detrás de la fila de enemigos de más atrás, como en el original.
- **Estilo:** es el mismo del fondo original de Oberursel (montañas violetas, nubes y piedras), pero limpio. Los personajes se leen bien encima.

**Lo que se podría mejorar** si la vuelves a generar (no es necesario):
1. **Resolución:** mide 1672x941 y la amplié a 2560x1440 con Lanczos y un enfoque suave. Como es un dibujo de colores planos casi no se nota, pero con una nativa de 2560x1440 quedaría más nítida.
2. **El brillo del centro abajo:** es fuerte. Ahí van los personajes de abajo, y los que tienen blanco (Sonny, el médico) pierden un poco de contraste. Un brillo algo más suave ayudaría.

Si la regeneras, pide 16:9 con el horizonte de las montañas a un 35-40 % de la altura, la parte de abajo sin objetos grandes (la tapa el panel) y sin personajes ni texto.

## Cómo está hecho

- **Contenedor nuevo:** `__hdBattleBG` (sprite 4327) va en la profundidad 58 del fotograma de combate, debajo de todos los paneles. Tiene un fotograma por cada escenario con HD, con la misma etiqueta que el juego (`SNOW`).
- **Al empezar el combate,** `__hdBattleSetup` (en `fuente/hd_batalla.as`) mira el escenario (`Krin.ZoneBG`). Si tiene HD:
  - muestra la imagen;
  - oculta el panel gris de arriba, la ventana, el cielo y el suelo originales y la línea negra del borde;
  - lleva la máscara de la escena a toda la pantalla;
  - achica y centra el panel de abajo.

  Si no tiene HD, no toca nada.
- **Piezas preparadas en el SWF** (`fuente/batalla.py`), porque algunas eran formas o botones sin nombre que el código no podía mover:
  - la máscara de la escena;
  - la X roja y su fondo;
  - la línea del borde;
  - el suelo de nieve de BATTLESCREEN.

  Se envolvieron en sprites o se les dio nombre. En los combates clásicos se ven igual que antes.
- **Para apagarlo:** `_root.__hdBattleEnabled = false` vuelve todo al combate clásico.
- **El código del juego y las habilidades no cambian.** Solo se agrega la capa `__hd*` al final del script principal.

## Probado (Ruffle, página 16:9)

- **Combate de Oberursel** a 2560x1440:
  - el panel y el tooltip de «!»;
  - una jugada del lobo con daño y zoom de cámara;
  - el turno de los enemigos y el turno siguiente.
- **Combate en la cárcel** después de uno de Oberursel: queda clásico, sin restos del modo HD.

Falta probarlo en tu app (AIR).

## Archivos

- **`SONNY2.swf`:** el juego.
- **`documentacion/COMBATE_HD.md`:** cómo funciona y cómo sumar el siguiente fondo de combate.
- **`fuente/`:**
  - `build.py` arma I32 sobre I31; `fuente/i31/` es lo de I31;
  - `batalla.py` y `placeobj.py` hacen las piezas del SWF;
  - `hd_batalla.as` es la capa;
  - `imagenes.py` prepara la imagen;
  - `imagenes/` tiene tu imagen original;
  - `banco/` tiene los guiones de Ruffle.
- **`capturas/`:** las capturas.

## Lo que sigue

- Probarlo en tu app.
- **Si te gusta, los otros escenarios entran igual,** uno por imagen. Hay 9 en total:
  - `JAIL` (18 combates), `STREETS` (17), `TUNNEL` (15), `TRAIN` (13) y `CHURCH` (11);
  - `STREETS2`, `STREETS3`, `CHURCH2` y `WHITE NOVEMBER`, con muy pocos combates.
- **Opcional:** el fondo es estático, como el original. Si quieres más vida, se puede agregar por código una nevada suave o nubes que se desplacen encima de tu imagen.
