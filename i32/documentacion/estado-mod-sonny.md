# Mod de Sonny 2: estado del proyecto

Última actualización: 01/10/2026 (I32: combate HD en Oberursel).

## Estado actual

- **I32 (vigente, 01/10):** es I31 con los combates de Oberursel (`ZoneBG` = SNOW) en HD a pantalla completa, con la imagen del usuario. Sin panel gris arriba (solo las barras de vida) y con el panel de abajo al 62 % y centrado, como la barra del World Map. Los demás combates siguen clásicos. Ver la sección I32 y `i32/documentacion/COMBATE_HD.md`.
- **I31 (01/10):** es el `SONNY2.swf` del usuario del 29/09 (I30 + una cárcel HD agregada por otra herramienta) con los fondos de zona corregidos: Zona 1 y Hew vuelven al original; Labyrinth e Il Sanctus en HD con las imágenes del usuario; el pueblo HD sin la franja de 6 px. El código del juego no cambia. Se entrega en `SONNY2_I31_parte1.zip` + `parte2.zip`. Ver la sección I31 y `i31/documentacion/ZONAS_HD.md`.
- **I30 (vigente):** es I29 con el menú de habilidades a lo ancho del 16:9 (sin las bandas borrosas): panel y recuadros más anchos, el árbol de clase y el del lobo en una grilla con los íconos al 140 %, la barra de combate y el Ability Pool más grandes, y el panel de Aspectos con las mismas medidas. Las demás páginas del menú siguen con el de 800. Se entrega en `SONNY2_I30.zip`. Ver la sección I30.
- **I29:** es I28 con el selector «Abilities · Instincts» de I27, el escudo del juego (burbuja, `sfx_shield` y «SHIELDED») en los escudos del lobo, los estados que se acumulan con la cantidad en dorado y los turnos en el contador, y la regla del usuario: cada habilidad sube por Wounds o por Scent, no por las dos. Se entregó en `SONNY2_I29.zip`. Ver la sección I29.
- **I28:** es I27 con el árbol del lobo ordenado por nivel (cada fila es un escalón), el tooltip y los avisos del árbol de clase, el +10 % de Ancestral Wolf restaurado y el panel de Aspectos rehecho con la forma del menú de personaje. El usuario lo probó y pidió los cambios de I29.
- **I27:** el árbol del lobo con la forma del árbol de clase y las conexiones como requisitos reales. El usuario lo probó y pidió los cambios de I28.
- **I26:** el rework del lobo (propuesta v4) implementado sobre I25. El usuario lo probó y pidió los cambios de I27.
- **I19_LOBO:** entregada; el usuario todavía no la probó en el juego.
- **Pantalla completa 16:9:** la versión vigente es **I22** (`SONNY2_16x9_I22.zip`). Suma a I20 (contraste, World Map y FPS) el HUD de navegación al 62 %, levantado 12 unidades. La prisión 2K de I21 quedó **apagada** hasta nuevo aviso: el usuario pidió volver al fondo original porque no se veía bien.
- **Maqueta del panel de batalla (25/09):** dos variantes mostradas como capturas, sin tocar el juego. Falta que el usuario elija.
- **Propuesta de rework de habilidades (25/09):** publicada como página («Mokoshotar: sangre y escarcha», https://claude.ai/artifact/LipbEoaCeY9mk7PqA1C3D4). La v4 quedó implementada en I26.
- **Imágenes HD de zona (I31):**
  - en HD: VILLAGE (Zona 2), TUNNELS/Labyrinth (Zona 4), ROME/Il Sanctus (Zona 6) y NULL ZONE;
  - en el original: PRISON (Zona 1, por pedido del usuario), CITY/Hew (Zona 5, por pedido del usuario), TRAIN (3) y JAPAN (7);
  - las imágenes retiradas (cárcel HD del 29/09 y Pawn Shop HD de I23) quedan en `i31/fuente/imagenes/retiradas/`.
- **Juego original:** el usuario mandó `sonnyoriginal.zip` con la app Sonny Legacy completa, en `SonnyLegacy.app/Contents/Resources/`:
  - `SONNY2.swf` = `114b566e…`, que es el original;
  - `SONNY.swf` = `bbf8f0d9…`, una variante del lanzador sin `loadSwf("SONNY2")` automático (muestra la selección de juego);
  - `application.xml` usa `renderMode` = **direct**.

Base de trabajo: la **versión modificada del SWF** que envió el usuario el 23/09. Incluye la capa I17 del mod y capas propias del usuario («night…», `__i18Version = "I18_UI_MASTERY_HANDOFF"`, y la puerta NULL ZONE `__nz*` del mapa). El usuario no quiere entrar en detalle sobre sus cambios. Hay que respetarlos siempre.

| | SHA-256 |
|---|---|
| SWF original | `114b566e30be41512399eff1aec919bbb1bfab980a54c10b8ad5281487a7d3a6` |
| SWF modificado del usuario (base) | `6541dd9a126f4218decd01d41bff7b9e7097e2cf717d4a5f5a170d9993aa0536` |
| Recompilado entero desde AS2 (paso 5) | `f6a98433a4591e755e97576f73f240f4e9c9422e84cc04a12d45db012d829e0d` |
| I19_LOBO | `5b80f4e0290a23c58054d1b7d74dd2bcb08e40d6813eb2570d21a2070ebb1236` |
| SONNY2 I19 + WS 16:9 (parte 1) | `f678e5065b93702572a2fcc7c629849cdcaa3a355756470244f4ec2c9b8e5783` |
| SONNY2 I20 | `b49e1bb720ed754b8164c36da6bd1b5e175405988516a1d201d7ce0665d4f2b6` |
| SONNY2 I21 (HUD 50 % + prisión IA) | `e4ea9692abc875f254e72629c61ba32a68d47a8253c1044007973256e9b95ff2` |
| SONNY2 I22 | `88ee7367a3f6138e60c6b3209d738737186125e9a0c1c814cf669590377939af` |
| SONNY2 I25 | `37a95f7138ee88e509dc5d5c0cdf4cd3b924ee26b0758d557cf804f31eba5469` |
| **SONNY2 I30 (menú de habilidades en 2K, vigente)** | `9a0f17755223035f6dc94763ac80ecfe51b160d1a2a6ad2d7299d348ddeb1444` |
| SONNY2 I29 (escudo del juego y regla Wounds o Scent) | `b440bf336021bf4747df5d8647a392a76503e924acd0250c60022d77863cbf21` |
| SONNY2 I28 (árbol por nivel y menús nativos) | `58fb99cad99c10cd15e9504fec6ac6e912b6ea827b0f3cd3fa8e5ef36e2df909` |
| SONNY2 I27 (árbol estilo clase) | `c78db85f44df641777cc4740ad59531f69d7fec6375e15a35dc063d4da416112` |
| SONNY2 I26 (rework del lobo) | `a2d139e7790607d93f4e80276db4df51173772309d203676507cae044d9eea22` |
| **Lanzador SONNY.swf 2K nativo** | `8d3fa0e19e670e381316fb5a52130767d0727d1774d7e2020d24a4dea7bfd3b2` |
| Lanzador modo rendimiento (1080p escalado, 16:9) | `bc8408378ce8c2f4d500944d1ded8ca79b52d8d2aee95f4d3f8766e966000870` |
| Lanzador original (Sonny Legacy, AS3/AIR) | `24308e9c80ee454f5a7ca41a23dc3672a74403b024d55d5c49373c82fd478a28` |

## Flujo de trabajo (desde I19)

Los cambios se hacen **editando el AS2 descompilado**, no agregando capas nuevas:

1. `i19/editar.py` + `textos.py` toman `paso3/.../frame_0042/DoAction_2.as`.
2. Aplican reemplazos de texto exacto: si no encuentran el texto, fallan.
3. El resultado queda en `cambios/`.
4. `swfpatch.py paso1 paso3 SALIDA.swf cambios` arma el SWF. Solo cambia esa etiqueta.

**Desde I20:** la base para 16:9 es el `SONNY2.swf` de la parte 1 (`f678e506…`), separado con `swfsplit.py` y descompilado con `swfcode.py`.

- `i20/build.py` reemplaza solo el bloque de la capa (de `_root.__wsL = -111.11;` a `__i19WsVersion`) por `i20/ws.as`.
- `i21/build.py` suma el HUD y la prisión.
- `i22/build.py` deja el HUD al 62 % con −12 en y, y la prisión solo con `--con-prision`.
- Con `--debug` se agrega `debug_hook.as` para el banco.
- Las utilidades de colocaciones están en `tools/swfutil.py`, extraídas de `ws_build.py`.

Para verificar el lobo se usa el banco fiel `bench2.Bench3`:

- `verificar_textos.py`: 185 comprobaciones;
- `test_lobo_fiel.py`: 57;
- `test_maestrias.py`: 30.

Las pantallas se verifican en Ruffle (ver más abajo).

## I19_LOBO (24/09)

- **Daño en % de Fuerza por rango:**

  | Habilidad | % de Fuerza |
  |---|---|
  | Rake | 170/200/235 |
  | Howl | 220/260/300 |
  | Iron Jaws | 280 |
  | Wicked Claws | 185/215/245 |
  | Pounce | 165/190 |
  | Hamstring | 175/205 |
  | Expose | 150/175 |
  | Frost Fang | 220/250/280 |
  | Shatter Guard | 115/145 por Frostbite |
  | Cold Trail | 140/160/180 |
  | Cull | 260/300/340 |

  En los ataques de hielo se usa Instinto ×1,4 si es mayor.
- **Focus:** Wicked Claws 8, Frost Fang 10, Cold Trail 15.
- **Arreglos:**
  - efectos que dependían del crítico (`perKSuccess`) y extras ocultos;
  - Expose sin daño;
  - Canine y Werezombie aplicaban dos veces;
  - sangrado de Rake;
  - Cull ×1,4 duplicado;
  - Last Stand rango 1;
  - Mastery de Rally;
  - duraciones;
  - Pounce +20 % oculto;
  - «★ Mastery»;
  - v14 `if(!im)`.
- **Thick Hide:** +18/28 % de Defensa Física y de Hielo (antes daba +15/25 %).
- **Textos:** números exactos en las 28 habilidades, y tooltips de combate con `__i19Texts()` (hacia el final de DoAction_2). Brittle hoy = +20 % de daño recibido del lobo.
- **Poder, en daño por turno:**

  | Clase | Daño por turno |
  |---|---|
  | Venenos | 1.751 |
  | **Lobo** | **1.154** (antes 610) |
  | Psíquica | 744 |
  | Hielo | 737 |

  Se ajusta con la tabla `NEW` de `editar.py`.

Notas técnicas: en DoAction_2 hay 3 definiciones de `__i1Post` y queda activa la última (línea ~31875).

## Decisiones del usuario sobre el rework (25/09, madrugada)

1. **Pestaña de pasivas:** sí, como pestaña temporal (Página 2: Instintos).
2. **Sangrado (Wounds):** tiene que ser una pieza clave del kit, al nivel de Scent of Blood.
3. **Expose Throat:** se elimina (es poco útil).
4. **Howl:** stun de 2 turnos también en jefes. Al lobo le falta control.
5. **Aspectos:** solo se ven y se eligen en la **NULL ZONE**; se preguntó qué significa "excluyentes" (respuesta: solo un Aspecto activo a la vez). Lista: Blood Moon, Long Winter, Pack Leader y uno **nuevo de transformación**, en el que los ancestros toman el cuerpo del lobo. Está ligado a la idea de Call of the Ancestors.
6. **Aliados que ponen Wounds:** NO.
7. **Puntos:** la pasiva de clase Ancestral Wolf (+10 % de estadísticas) además da **2 puntos de habilidad por nivel** y **3 en los niveles 5, 10, 15 y 20**.
8. **Antes de empezar el rework:** simular (con cálculos, sin jugar) una aventura Heroic completa con el árbol actual (I19).

## Propuesta v4 (25/09, mañana): cambios del usuario

Publicada en la misma página (https://claude.ai/artifact/LipbEoaCeY9mk7PqA1C3D4, versión 3 del artefacto). Fuente: `propuesta/datos.py` + `generar.py`; `editar_v3.py` aplica las decisiones y `editar_v4.py` estos cambios. Por error quedó una copia duplicada en https://claude.ai/artifact/WDYruEz5FGYGbKtNseQqBu; solo se borra si el usuario lo pide.

- **Al implementar:** íconos de prueba; no generar íconos ni imágenes.
- **Recursos (dos por elemento):**
  - sangre: Wounds (en el enemigo) y Scent of Blood (marcas);
  - hielo: Frostbite (en el enemigo) e **Ice Shards** (0–5, del lado del lobo): −3 % de daño recibido y +2 Focus por turno cada uno; duran 4 turnos. Se ganan al gastar Frostbite (Shatter Guard, 1 por cada 2) y al congelar (+2).
- **Pasivas clave:**
  - **Deep Wounds** (Hunt): tope de Wounds 3 → 5; R2 +35 %, 4 turnos, y los Wounds estallan al morir el enemigo (50 % del sangrado restante a los demás). Queda separada de Scent;
  - **Shardfall** (Winter, nueva): tope de Shards 2 → 3 (R1) / 5 (R2); con 3+ Shards, quien golpea al lobo gana 1 Frostbite; ★ con 5 Shards los ataques de hielo ignoran 20 % de Defensa de Hielo.
- **Máximo de Wounds:** 3 sin Deep Wounds, 5 con ella, 7 con Blood Moon. Puede haber 4. Wicked Claws «+1 por cada 2 Wounds» = +1 con 2–3 y +2 con 4–5.
- **Rupture:** gastar 3+ Wounds aplica **Hemorrhage** 2 turnos (−20 % Defensa Física y de Hielo, −15 % daño infligido); ★ con 5: 3 turnos + Torn.
- **Black Ice:** gasta los Shards (20 % [28 %] por Shard cada vez que un enemigo actúa); Cold Trail sobre el hielo pone el doble de Frostbite y lo alarga 1 turno; ★ congelado sobre el hielo estalla y devuelve 2 Shards.
- **Canine Instincts:** 2 turnos +1 por cada 2 Wounds o Scent del enemigo más marcado (máx. 5).
- **Killer Instinct (nueva, Hunt):** el lobo se muerde: −10 % vida actual, 2 Wounds sobre sí mismo, +15 % daño recibido; a cambio +40 % Strength e Instinct, +20 % Speed, no lo esquivan, +1 Wound por habilidad y +25 Focus (3 turnos).
- **Primal Breath (rework):** +20 Focus inmediato, 15 por turno, +20 % Speed, −10 % daño, quita 1 efecto; ★ nueva: al terminar cura 15 % y +15 % daño 2 turnos.
- **Second Wind:** 15 % + 20 % por Wound bebido (máx. 3 → 75 %).
- **Bloodhound ★:** Terrified (enemigo con < 20 Focus: −20 % daño; los ataques del lobo le sacan 5 Focus).
- **Más Focus:** Killer Instinct, Primal Breath, Ice Shards, Frozen Maw (+5, +10 contra Brittle), Terrified.
- **Definitivas (una por Aspecto, una vez por combate):** Blood Moon Rising (sangre), Endless Winter (hielo), Call of the Ancestors (Ancestros; números por cerrar). Pack Leader aún no tiene.
- **Aspectos:** a futuro también cambiarán la apariencia del lobo. El usuario responderá otras preguntas después.
- **Corrección técnica:** la Defensa sí baja el daño cuando supera el Piercing del atacante (el golpe se multiplica por Piercing ÷ Defensa, `executeMove`), además de afectar el crítico.

## I32 (01/10): combate HD en Oberursel

- **Pedido del usuario:**
  - el fondo de combate HD a pantalla completa, empezando por Oberursel;
  - arriba, quitar lo gris y dejar solo las barras de vida;
  - abajo, el panel de los aliados centrado como la barra del World Map.
- **SWF** (`i32/fuente/batalla.py`):
  - **piezas nuevas:**
    - bitmap 4325 y forma 4326 (la de 4320 con el bitmap cambiado y colocada en (400; 222,9));
    - contenedor 4327 `__hdBattleBG`, con un fotograma por escenario HD (etiqueta = ZoneBG), en la profundidad 58 del fotograma 217 y quitado en el 218;
  - **envoltorios con nombre**, para poder moverlos u ocultarlos por código:
    - la máscara 213 → 4328 `__hdMask`;
    - el fondo de la X 2919 → 4329 `__hdSkipXbg`;
    - la línea 3349 → 4330 `__hdMarco`;
    - el suelo SNOW 3335 de BATTLESCREEN → 4331 `__hdSuelo`;
  - **nombre nuevo** para el botón X 3408: `__hdSkipX`.
- **Capa `hd_batalla.as`** (al final de DoAction_2): `__hdBattleSetup`. Ver `COMBATE_HD.md`. La desactiva `_root.__hdBattleEnabled = false`.
- **Probado en Ruffle:**
  - combate SNOW a 2560x1440, con tooltip, ataque con zoom y el turno siguiente;
  - JAIL después de SNOW, que queda clásico.
- **La imagen del usuario** (1672x941) cumple. Se amplió a 2560x1440. Se le sugirió una nativa de 2560 y un brillo central más suave, opcional.
- **SHA-256:**

  | SWF | SHA-256 |
  |---|---|
  | I32 | `33328f7fafebed4d27503857a144055e7785f2b8e3ddd97b6cb39a5e4921040a` |

## I31 (01/10): fondos HD de zona y bug de Hew

**Base:** el `SONNY2.swf` del usuario del 29/09 (`bca5eea5…`). Es I30 más un cambio sin documentar, hecho con ChatGPT: la cárcel HD (bitmap 4323 y forma 4324) en la profundidad 26 del fotograma 1 de `KrinScreen` (2908), sin el marco 2812.

**Revisión de ese SWF:**
- `DoAction_2` es byte por byte lo que compila la fuente de `i30/fuente/src/`;
- los demás scripts coinciden con I19–I30;
- el único cambio sin documentar es la cárcel HD.

**Bug de Hew:**
1. CITY (fotograma 16) pone su fondo 2818 en la profundidad 26 sin vaciarla.
2. `KrinScreen` arranca en el fotograma 1 y salta hacia adelante.
3. La colocación de CITY se ignoraba y Hew mostraba la cárcel.

**Cambios** (`i31/fuente/build.py` + `zonas.py`):
- **Fotogramas 1 y 16 de 2908:** iguales al juego base. Zona 1 y Hew quedan con el arte original, por pedido del usuario: Hew sin el Pawn Shop HD.
- **Fotograma 60 (TUNNELS):** quita 47 y pone 4320 (Labyrinth HD) en la 26.
- **Fotograma 73 (ROME):** quita 26 y pone 4324 (Il Sanctus HD) en la 26.
- **Fotograma 86:** quita 26 y repone 47 para JAPAN.
- **Bitmaps 4319 y 4323:** se reutilizan para las imágenes nuevas, en JPEG 2560x1440 a calidad 92. Labyrinth se amplió desde 1672x941 con Lanczos y un enfoque suave.
- **Forma 4318 (pueblo HD):** pasa a la geometría de pantalla completa de 4320. Antes dejaba una franja de 6 px a la derecha a 2560x1440.

**Probado** en Ruffle (`page16.html`, 2560x1440): todas las zonas, Hew después de la cárcel y JAPAN después de ROME. Falta la prueba en AIR.

**SHA-256:**

| SWF | SHA-256 |
|---|---|
| I31 | `0197c81640fc109a6d9d43ad2fe566f4c67af92263eedfc6552971ca63123c26` |
| I31 con `--debug` | `b1ab5c84…` |

## I30 (26/09): menú de habilidades en 2K

Pedido del usuario: la página de habilidades del menú a lo ancho del 16:9, como la NULL ZONE, sin el recuadro de 800 con las bandas borrosas; íconos más grandes y el menú extendido.

- **Capa `src/rw_80_2k.as`:** trabaja por código sobre las piezas del juego del sprite 3239 (KRINMENU), fotograma 25, sin tocar dibujos.

  | Pieza | Profundidad | Cambio |
  |---|---|---|
  | Panel rojo (2951) | 2 | Se estira de −97 a 897 y de 15 a 470 (la barra de navegación empieza en 480) |
  | Recuadro del árbol (2955) | 7 | −68 a 294 |
  | Recuadro de la barra de combate (2955) | 5 | 506 a 868 |
  | Recuadro del centro, arriba (2957) | 23 | Llega hasta 320; el aviso de puntos (3205, profundidad 675) baja 15 |
  | Recuadro de atributos (2957) | 21 | Baja 30 con su contenido (643–650, 657, 659–668 y 671) |
  | Barra de combate (`selector`) | 25 | Al 118 % |
  | Ability Pool (`talentPool`) | 9 | Al 119 % |
  | Títulos | 672–674 | Centrados en su recuadro |
  | Cruz | 1431 y 1434 | +114 en x |

  Además:
  - las pestañas `__v9Tabs` se corren −113;
  - `__wsFondo.L` y `.R` (los reflejos) se ocultan con el menú o el panel de Aspectos abiertos.
- **Cuándo se aplica:**
  - al entrar a la página, por `__v8Sync` (lo llama `KrinCreateAbilityMatrix`);
  - en cada fotograma, por `__rwTick`;
  - al entrar a otra página, por `__v92Cleanup`, que llaman todas las páginas del menú. Ahí las piezas compartidas con otras páginas vuelven a su transformación original (profundidades 2, 5, 7, 21, 23, 1431 y 1434).

  Las piezas se buscan por profundidad recorriendo el menú con `for-in`, y los clips también con `getInstanceAtDepth`.
- **Grilla del árbol:**
  - `__rwG()` devuelve `__rw2kGrid` en la página de habilidades y `__rwGrid800` fuera de ella;
  - `__rw2kGrid`: columnas cada 70, centradas en el recuadro (x0 = 7,975), filas cada 45 desde y = 121, nodos al 140 %;
  - también fija los caños (8 y 3), el anillo (19,6), el emblema (28), los niveles y el selector de página;
  - el árbol de clase: `talenttreefull` al 140 % en (x0, y0), y sus nodos `st` en (50·col, 32,14·fila). Después se llama a `krinRemakeTree` para que el juego redibuje sus caños.
- **Panel de Aspectos:** `__rwAspGeo()` usa el panel y los recuadros de `__rw2kL`.
- **`build.py`:**
  - la línea del rectángulo de `lineMC` (forma 3145) pasa a ser transparente: coincidía con el borde del recuadro en el menú de 800 y en 2K quedaba suelto;
  - 119 colocaciones del tutorial del aviso de puntos (sprite 3205, profundidades 5, 7 y 9, fotogramas 12–150) se corren al lugar nuevo. Los números salen de `__rw2kL`.
- **Interruptor:** `_root.__rw2kEnabled = false` vuelve al menú de 800 de I29.
- **Arnés 16:9:** `ruffle/page16.html` (`scale: "showAll"`, `forceScale: true`, `letterbox: "off"`) muestra la pantalla como el lanzador 2K, sin estirar.
  - Coordenadas: pantalla = ((x + 111,11)·720/575, y·720/575) a 1280x720 (`ruffle/gen/mk.py`); a 2560x1440, el doble.
  - `drive.js` suma `down`/`up` y elige la página con `PAGE=`.
  - Asignar a la barra es clic en el Ability Pool y después clic en la casilla (no se arrastra).
  - Para el árbol de clase con datos en la partida rápida: `call _root.loadTalents 0`.
- **Pruebas:** 312 comprobaciones, todas bien (14 nuevas: `menu_2k`). En Ruffle: árbol, clase, tooltips, barra, tutorial, inventario, NULL ZONE y Aspectos.
- **Íconos:** los del lobo son de 128 px y se ven a unos 98 px a 2560x1440, así que siguen nítidos.

## I29 (26/09): escudo del juego, estados con cantidad y turnos, y regla Wounds o Scent

Pedido del usuario al probar I28 (en su app, nivel 14):
- volver al selector de páginas de I27;
- que todo escudo muestre el escudo del juego y diga «Shield» (o lo que use el juego), sin perder en el tooltip cuánto queda;
- ver en Scent y Frostbite la cantidad y también los turnos;
- revisar habilidades repetidas.

- **Escudo del juego:**
  - `__rwShieldFx(u, el)` hace lo mismo que el motor cuando un escudo para un golpe: `BATTLESCREEN["player"+id].shield.play()` (la burbuja), `addSound("Effects", "sfx_shield")` y `KrinNumberShow("shield", …)`, que muestra el cartel «SHIELDED»;
  - se llama al crear un escudo (`__rwShieldAdd`), al absorber en `__rwPure` y `__rwRawHit`, y cuando el escudo de Guardian's Call absorbe daño del aliado;
  - Guardian's Call se lanza con `BOOM_SHIELD` y `sfx_shield`.
- **Íconos de estado:**
  - el motor pone `buffCounter` = CD (turnos) al crear el ícono (`KrinBuffShower`); el rework ya no lo pisa con la cantidad;
  - la cantidad va en un campo `__rwStk` dorado con contorno negro, en el borde del dibujo (`buffIcon`), arriba a la derecha.
- **Repetidas:**
  - se le ofrecieron 4 cambios y no eligió ninguno;
  - pidió una regla: una habilidad no debe subir a la vez por la cantidad de Wounds y por la de Scent (Rake y Hamstring ponen los dos juntos);
  - se aplicó a Canine Instincts, Pack Tactics, Rallying Cry, Relentless Hunt, Winter Heart y Unyielding;
  - por pedido del usuario no se tocan Cull the Weak, Second Wind, Shared Hunger ni «Frostbite al que golpea»;
  - los números que quedan no cambiaron.
- **Textos:** Deep Wounds y Shardfall ya no dicen «Required by…».
- **Menú de habilidades en 2K:** el usuario preguntó si es factible. Lo es, y queda para I30:
  - el panel rojo cubre el 16:9 (`__wsL` = −111, `__wsR` = 911);
  - los recuadros son más anchos y los íconos del árbol más grandes;
  - hay que cuidar el arrastrar y soltar del Ability Pool.
- **Arnés:** el servidor HTTP local se cae entre comandos si no se lanza con `setsid`.
- **Pruebas:** 298 comprobaciones, todas bien.

## I28 (26/09): árbol ordenado por nivel y menús con aspecto nativo

Pedido del usuario al probar I27: una definitiva (Endless Winter) y el turno extra del aliado funcionan bien; los dos menús (árbol y Aspectos) no se veían nativos; al principio se abrían demasiadas habilidades y no quedaba claro qué subir primero. Durante el trabajo pidió además:
- que el tooltip no diga «Requires…», que use el formato del árbol de clase («You have no points in this ability yet.», «Next Tier (Lvl. X): …») y que el árbol impida aprender con el cartel del juego;
- restaurar el +10 % de estadísticas de Ancestral Wolf con Scent of Blood, como antes.

- **Orden por nivel:**
  - `__rwTiers = [1, 2, 3, 5, 6, 8, 10]`: cada fila es un escalón;
  - `__rwPlace` corre el primer rango al nivel de la fila y conserva la distancia de los rangos siguientes (las gratis no cambian);
  - las 6 gratis arriba son las únicas raíces de Abilities;
  - Hamstring (en la columna de Winter) abre Rupture, Frost Fang y Feeding Frenzy;
  - en Instincts, las pasivas clave van en cadena (Scent → Deep Wounds → Shardfall), y las raíces son Scent, Thick Hide y Pack Tactics (nivel 5);
  - a nivel 1 solo se abren Scent of Blood y Thick Hide.
- **Estados del nodo:**
  - aprendida;
  - se puede aprender ya: `GlowFilter` verde `0xB4FF45`, el del aviso de puntos del menú;
  - con requisitos, pero sin puntos: oscura;
  - bloqueada: alfa 38.

  Los niveles de fila van a la derecha de la grilla («Lvl. N», gris claro si ya se alcanzó).
- **Avisos del juego:**
  - `__rwErr(k)` lee `KrinLang[KLangChoosen].TALENTERROR1–4`;
  - `__rwCanLearn` sigue el orden del botón nativo (botón 3147): primero el requisito, después el nivel y al final los puntos;
  - los requisitos de la otra página también dan el aviso 4.
- **Tooltip:**
  - `SKILLTALENTTIP2`, `SKILLTALENTTIP` + nivel + «): » + rango siguiente y `SKILLTALENTTIP3`;
  - `SKILLAURA` para las pasivas (con «Key» delante en las clave);
  - el costo sin la rama.
- **Pestañas «Abilities» / «Instincts»:** con la forma de las pestañas del menú (`0x404040`, borde oscuro).
- **Emblema:** la marca `nightAncestralMark` del usuario, de 24 unidades, con brillo azul si está activa y alfa 45 si no.
- **Bono de Ancestral:**
  - `__rwAncBonus` devuelve 0,1 fijo (`__rwAncPct`) y se aplica con Scent of Blood;
  - `__i1AncBonus` queda en 0 por la capa night;
  - la capa I14 no suma dos veces: pregunta por `__v55Rank(811)`, que el rework deja en 0.
- **Panel de Aspectos** (`__rwAspectPanel`):
  - fondo `__nzNativePanel` del tamaño del menú de personaje;
  - título dorado con contorno, como «Achievements»;
  - lista de Aspectos en un recuadro `0x373737`, con el elegido en marco verde;
  - panel central `0x1A1A1A`, con el título en dos líneas, los puntos, el efecto y «Activar»;
  - a la derecha, la definitiva con ícono, costo, descripción, qué falta y «Aprender»;
  - `__rwFit` achica la letra si el texto no entra;
  - «Volver» abre el menú MOKOSHOTAR.

  Íconos de los Aspectos: los dibujos sin tinte de su definitiva (Scent of Blood, Cold Trail, Howl of the Ancestors) y Pack Tactics.
- **Colores:** muestreados del menú del juego (`__rwUi`).
- **Pruebas:** 294 comprobaciones, todas bien. Ruffle: árbol a nivel 3 y 12, tooltip, cartel, emblema y panel de Aspectos.

## I27 (26/09): árbol del lobo con la forma del árbol de clase

Pedido del usuario al ver I26: sin números de rango, sin «Reiniciar lobo», sin «Página 1: Habilidades» y sin el texto «Otro clic en Mokoshotar…»; anillos chicos en las pasivas clave; y la forma del árbol de clase, porque las líneas de I26 no servían (se podía aprender Shatter Guard sin Frost Fang aunque estuvieran conectadas).

- **Árbol de clase, como referencia:**
  - `talenttreefull` (sprite 3239, fotograma 25) pone los nodos `st0`–`st27` en una grilla con centros en x = 87 + 52·col, y ≈ 124 + 40,3·fila (coordenadas de `_root`), con los nodos al 100 %;
  - un nodo sin puntos muestra `thing2.bfilter` al 80 %;
  - entre cada nodo y su `PRESKILL` hay una línea negra de 6 y encima una de 2, `0xFFCC00` si el requisito tiene puntos y `0x2B2B2B` si no;
  - aprender pide al menos 1 punto en cada `PRESKILL`;
  - los rangos (`thingoShow`) solo se ven con Espacio apretado.
- **I27 copia eso:**
  - `pre` en cada habilidad es el requisito dibujado; `__rwPlace` en `rw_10_data.as` fija columna, fila y requisito;
  - hay cortes, raíces sueltas y 4 diagonales: Hamstring ↘ Frost Fang, Second Wind ↙ Primal Breath, Deep Wounds ↘ Frozen Blood y Blood Drinker ↙ Shared Hunger;
  - el cambio de página es un selector «Abilities · Instincts» al pie; el segundo clic en la pestaña sigue funcionando;
  - los avisos del árbol usan `KrinCombatText`.
- **Bono de Ancestral Wolf:** el usuario pidió un interruptor y después aclaró que ya existe en la base. Es `_root.__i1AncBonus`: 0,1 en I19 y 0 en la capa night. El rework ahora suma ese valor (`__rwAncBonus`) en lugar de un 0,1 fijo, así que hoy no suma. Los puntos extra siguen atados a Scent of Blood.
- **Tooltip:**
  - `KrinToolTipper.inner2` (un ícono dentro del tooltip) tiene el script nativo del ícono y, bajo el mouse, pisaba `tt` y `t` con textos vacíos. `__rwShowTip` le pone `zero` y `__uiTick` repone los textos guardados;
  - un nodo sin aprender ya no repite la descripción en «Next rank».
- **Arnés de Ruffle:** la pantalla se estira en horizontal (x ×1,6, y ×1,24; mouse ↔ `_root`). En la app del usuario la escala es pareja, así que los círculos van con el mismo radio en x y en y.
- **Pruebas:** 280 comprobaciones, todas bien.

## I26 (25/09, noche): rework del lobo implementado

- **Base:** I25 (`37a95f71…`), separado y descompilado con las herramientas del paso 5 (`DECOMPILACION_PASO5.zip`, que mandó el usuario). Recompilar sin cambios da el mismo hash.
- **Rutas de esta sesión:**
  - `/home/user/work/rework/` (`build.py`, `src/rw_*.as`, `debug_hook.as`, `tests/`);
  - banco: `/home/user/work/banco`;
  - Ruffle: `/home/user/work/ruffle`.
- **Arquitectura:** una capa `__rw` al final de DoAction_2.
  - Deja inertes las capas viejas del lobo: `__v55Rank`→0, `__v10Owned`→false, `__i1IsWolf`→false, etc.
  - `executeMove` manda las habilidades del lobo a `__rwCast`. El resto pasa por `__rwOther`, que suma los efectos del lobo sobre enemigos y aliados.
  - Los ataques 623–628 de otras unidades saltan las capas viejas y van a `__v55PrevExecute`: antes el NPC Mokoshotar quedaba mudo.
  - Las marcas son buffs nativos `RW*` (`__rwAdd` aplica `applyChangesKrin` al momento).
  - En el reloj (fotograma 217) hay dos parches: `__rwNoDodge` en la esquiva y `__rwExtraTurn` en el cambio de equipo (medio turno extra).
- **Ranuras de `talentMainArray`:**
  - rework: 100–152;
  - Aspecto: 160;
  - bonus de Ancestral: 161;
  - las viejas 38–64 se devuelven solas (`__rwMigrate`).
- **Ids de habilidades:**
  - nuevas: 831–846 y 854–857;
  - las libres usan 861–865 (Rake, Canine, Howl, Iron Jaws, Wicked), porque 623–628 son del NPC Mokoshotar;
  - la barra de I25 se mapea: 624→861 … 628→865 y 623→809.
- **Íconos de prueba:** fotogramas 1015–1034 del sprite 2186 (copias teñidas por rama). Los estados son etiquetas nuevas del sprite 1986 sobre fotogramas existentes.
- **Pruebas:**
  - `tests/test_rework.py` (banco AVM1 fiel), 265 comprobaciones;
  - Ruffle: árbol, tooltips, NULL ZONE, Aspectos y dos combates reales (batalla 103).
  - Por pedido del usuario **no se corrió la simulación Heroic**.
- **Hallazgos técnicos:**
  - un clip con `onUnload` se borra al final del fotograma; si se crea otro con el mismo nombre en el mismo fotograma, la ruta apunta al viejo (la página 2 salía en blanco);
  - los íconos del lobo (fotograma 987 en adelante de 2186) tienen su propio script en `bfilter`: suelta el tooltip propio cada fotograma y usa `__v55Desc`. Se protegió el tooltip (`__rwOwnTip`) y `__v55Desc` devuelve el texto nuevo;
  - `KrinToolTipper` hace `startDrag(true)` en cada fotograma. En Ruffle gana la posición del mouse sobre `__uiLayout`, así que el panel de Aspectos usa un recuadro propio;
  - la capa night cambia el título «Ancestral Wolf» por «Ancestral Mark (inactive)». El emblema usa «Ancestral Wolf (Class Passive)»;
  - la fuente de Ruffle no tiene «★».
- **Ayudas del banco en Ruffle** (`debug_hook.as`, solo con `--debug`):
  - `__dbgAwaitingPlayer`, `__dbgPlay(casilla, objetivo)`, `__dbgUnit(pid)`, `__dbgTough(pid, vida)` y `__dbgGlobal(ruta)`;
  - comandos `wrap`/`log` (traza de llamadas) y `callo` (argumentos que son objetos);
  - `drive.js` acepta `move` con `steps` (sin pasos, Ruffle no dispara el rollover).
- **Combate de prueba:**
  1. `set _root.Krin.BattlePick 103`;
  2. `bossFight` y `progressFight` en false;
  3. `go LOADBATTLESCENE`.

  Quedan Sonny y Veradux contra 3 Convicts. La batalla 1 es el tutorial contra Veradux: el enemigo es la unidad 4.

## I25 (25/09)

- Combate clásico por defecto; `--combate-b` pone el panel B.
- **Skin al iniciar:** el catálogo `__nzCatalog` solo se armaba en el fotograma 449 (mapa), y `dressChar` (fotograma 217) no encontraba `__nzGetLook(__nzChosen)`: Sonny salía sin modelo. Ahora el catálogo se arma al cargar y `__nzChosen` se guarda en el SharedObject `sonny2_mod_skin` con `_root.watch`.
- SHA-256: `37a95f71…`.

## I23–I24 (25/09)

- **Regla de entrega del usuario:** siempre un **zip con LEEME.md, fuente y capturas**, nunca el SWF suelto. Hay un límite de 30 MB por archivo: si no entra, se divide en varios zips.
- **I23:** imágenes HD del usuario en Hew (CITY, fotograma 16 de 2908, prof. 26 en lugar de 2818) y en la NULL ZONE (fotograma 191). En la NULL ZONE se oculta `this.plaza` (la plaza `__v8Plaza` que pone `__nzZoneReady`).
- **I24:**
  - **Panel de combate B (temporal, fotograma 217):**
    - arriba al 72 % (prof. 59 y vidas 342–432);
    - abajo al 66 % −4 (prof. 60, 65, 480, 484, 498, 628, 634);
    - escena ×1,2 (prof. 70, 73 y 89);
    - la máscara 213 (prof. 72) a todo el ancho, de y 99,1 a 476;
    - selectores parcheados con `_xscale/100`;
    - diálogo `combatScript` recolocado.
    - Los fondos de combate para B miden 2560x944 (de y 248 a 1192).
    - `--clasico` lo quita; el zip del revert va aparte.
  - **Traducción:** NAVTEXT (21) y BATTLESPEECH (145) de la tabla ENGLISH, en los fotogramas 1 y 41 (`i24/traduccion.py`). Los campos usan fuentes del sistema, así que las tildes se ven bien.
  - **Ventana de mensaje** (sprite 3251 prof. 2, 5 y 6, más navText/navTitle en la prof. 1650/1651 del fotograma 181): al 80 %.
  - **Hashes:**
    - B: `a4e617bc…`;
    - clásico: `77a18b23…`.
- **Nota del banco:** con el atajo de partida nueva, el modelo de Sonny (player1.inner) no aparece en combate, tampoco en I22. No es una regresión.

## Propuesta de rework de habilidades (25/09, sin implementar)

Página publicada: «Mokoshotar: sangre y escarcha». Fuente: `/home/claude/propuesta/datos.py` + `generar.py`.

- **Pedido del usuario:**
  - tooltips de combate en lenguaje Krin y siempre con matemática exacta («+15% damage received», «100% stunned»);
  - Endurance, hielo y físicas le parecen poco interesantes;
  - el sangrado y el Frostbite se sienten desperdiciados, sobre todo en Pack;
  - usar el segundo menú de Mokoshotar.
- **Segundo menú:** un segundo clic en la pestaña «Mokoshotar» (`__v9Tabs.moko` → `__v8OpenTree`, la última definición está en la línea ~23246) hoy muestra un panel vacío. La propuesta lo usa para una **Página 2: Instintos (pasivas) + 3 Aspectos excluyentes**. La Página 1 queda solo con activas.
- **Núcleo propuesto:**
  - **Wounds**: sangrado acumulable de 1 a 5, 15 % de Strength por turno cada uno, 3 turnos, se refresca;
  - ciclo **Frost Fang** (Wounds → Frostbite) y **Shatter Guard** (Frostbite → Wounds);
  - Hunted conserva «cannot dodge» y suma −25 % de curación recibida.
- **Corrección (25/09): la esquiva SÍ existe.** Está en `battleClocker` (fotograma 217, ~línea 373):
  - `r = SPEEDU objetivo / (SPEEDU atacante × acierto de la habilidad [mAry1[9]])`;
  - probabilidad = `r·(3r+3)` %, con un máximo de 75 % (si da menos de 1 queda en 0);
  - no aplica a los ataques de tipo «Shock» ni a objetivos aturdidos.
  - El «no hay fallos de ataque» de `MOTOR_QUE_SE_PUEDE.md` se refería a otra cosa: `perKSuccess` es el crítico, no el acierto.
- **Idea del usuario (25/09), sin diseñar todavía:** la definitiva **Call of the Ancestors** / **Ancestors' Blessing**. Es una transformación con aura celeste; da daño doble, turno extra, Focus y vida, y marca a un aliado que al morir es reemplazado por un lobo. Queda pendiente hasta que el usuario lo pida (tiene pocos créditos).
- **Números:** 25 activas (57 rangos), 16 pasivas (31 rangos) y 3 Aspectos. Hay 17 nuevas, 20 con rework y 7 que se mantienen. Se elimina Expose Throat (su drenaje de Focus pasa a Iron Jaws R2).
- **Nuevas activas:**
  - Rupture;
  - Black Ice;
  - Feeding Frenzy;
  - Frostbound Pack;
  - Taste of Blood;
  - Rime Coat;
  - Ice Tomb (probar el stun sobre un aliado en el banco).
- **Nuevas pasivas:**
  - Bloodhound;
  - Frozen Blood;
  - Winter's Grip;
  - Cold Snap;
  - Shared Hunger;
  - Cold Comfort;
  - Blood Drinker.
- **Aspectos:** Blood Moon, Long Winter y Pack Leader.
- **Balance:** la build Sangre (Rake → Hamstring → Rupture, con Deep Wounds R2) da unos 403 % de Strength por turno, dentro del rango aprobado de 380–440 %.
- **Preguntas abiertas al usuario:**
  1. ¿Separar el árbol en dos páginas?
  2. ¿Wounds acumulables?
  3. ¿Eliminar Expose Throat?
  4. Howl con stun de 2 turnos: ¿también en jefes?
  5. ¿Aspectos excluyentes?
  6. ¿Aliados que ponen Wounds?
  7. Puntos: 89 rangos contra 20–25 puntos de campaña.

## Maqueta del panel de batalla (25/09, sin implementar)

La maqueta se hizo moviendo las piezas reales en el banco de Ruffle (`/home/claude/ruffle/mock.py A|B|reset`); no se tocó el juego. Capturas en `maqueta_combate/`.

- **Variante A:**
  - la escena ×1,40 cubre todo el ancho, pegada arriba;
  - el panel superior (3303) está oculto y las vidas flotan sobre la escena con un fondo oscuro al 50 %;
  - la barra inferior queda al 85 %, por encima de la escena.
- **Variante B:** los paneles al 72 % (arriba anclado arriba, abajo anclado abajo) y la escena ×1,2 entre ellos.
- **Datos técnicos:**
  - el cuadro negro 213 en la profundidad 72 es una **máscara** (clipDepth 340) que recorta el fondo (prof. 73) y BATTLESCREEN (prof. 89);
  - las vidas p1–p6BAR están en las profundidades 342–432;
  - la cámara del combate (GridZoomer) hace zoom en los ataques: al implementarlo hay que ajustarla a la escala nueva.
- **Pendiente:** que el usuario elija A o B antes de implementar.

## Simulación de campaña Heroic (hecha el 25/09, árbol I19)

- **Entrega:** informe publicado en https://claude.ai/artifact/3zTchMrun3CK8nyGHrQYGu y `SONNY2_SIM_HEROIC.zip` (LEEME, datos, fuente y capturas).
- **Código:** `/home/claude/sim/campana/`:
  - `motor.py`: clase `Sim` sobre Bench3 (`applyChangesKrin` nativo portado; `krinAddMove` grabado);
  - `politicas.py`: builds, barra de 8 y reglas por prioridad;
  - `campana.py`: XP, farmeo y reintentos;
  - `informe.py` + `textos.py`.
  - Se parcheó el opcode Enumerate (0x46) de `avmvm.py` para que recorra los índices de los arrays; la IA lo necesita.
- **Resultados, campaña principal (Prisión a Ciudad):**

  | Clase | Victorias | Rondas para ganar | Niveles extra |
  |---|---|---|---|
  | Lobo I19 | 99 % | 15,2 | 0 |
  | Psycho | 92 % | 17,6 | 2 |
  | Bio | 90 % | 20,8 | 6 |
  | Hydro | 89 % | 23,0 | 2 |

  - **Lobo:**
    - el 36 % de sus acciones son Pounce: se queda sin Focus;
    - se traba en Clemons (2/4), City Council (3/4) y Nostalgia (2/4);
    - los sangrados son ~10 % del daño del equipo.
  - **Comparación:** Bio no pasa Baron Brixius ni al Police Colonel, ni con +3 niveles.
  - **Sin evaluar:** The Bomb y la Zona 7 las pierden todas las clases (mecánicas especiales).
  - **Órdenes de puntos:** Caza primero (A) es el mejor; Invierno primero (B), 95 %; Manada/Resistencia primero (C), 92 % y +39 % de rondas.
- **Supuestos:**
  - equipo al 85 % del mejor de su nivel;
  - puntos según los ratios de la clase;
  - el lobo usa la base de Bio;
  - Veradux en Phalanx y Roald en Relentless;
  - farmeo hasta el nivel del enemigo más fuerte;
  - 4 intentos por batalla.
- **Pendiente:** volver a correrla con el rework implementado (I26), cuando el usuario la pida. Medir sobre todo el stun de 2 turnos de Howl en jefes, Killer Instinct y las definitivas.

## Pantalla completa 16:9 a 2560x1440 (parte 1, 24/09)

Por qué no se veía en 2K: el lanzador AS3 (`SONNY.swf`, escenario de 1920x1080) hacía `fullScreenSourceRect = 1920x1080`. Además, la máscara `GAMEMASK` recortaba el juego a 800x575, escalado por la altura (1080/575).

**Lanzador.** Parches de bytes con `abcpatch2.py`, comprobados descompilando con JPEXS:

- `fullScreenSourceRect = null`;
- `GAMEMASK` a 1920x1080 en (0, 0);
- `stage.addChild(WRAPPERMENU)` anulado: la tuerca y pantalla completa quedan debajo del juego; ESC sigue abriendo el menú de salida.

A 16:9 se ve de x = -111,1 a 911,1.

**Juego.** `ws_build.py` sobre I19:

- **Capa `ws.as`:** relleno ambiental de las bandas (reemplazada en I20, ver abajo).
- **Barras y paneles:**
  - UI_BAR 2801 y el panel 3303 se estiran solo por los bordes (`shape_edit.py`);
  - los paneles izquierdo y derecho se abren ±55,6;
  - las barras de vida se pegan a los bordes (±111,1);
  - la barra inferior pasa a la profundidad 60.
- **Rectángulos:**
  - los fundidos y oscurecidos de pantalla completa (altura real ≥ 500) se ensanchan a 1060;
  - el fondo negro del combate (213 dentro de 3309, y la profundidad 72) no se ensancha.
- **Otros ajustes:**
  - el borde 3349 de la ventana de combate se lleva fuera de la pantalla;
  - pueblo HD: personaje nuevo 4317/4318, profundidad 26 de la zona VILLAGE.

## I20: arreglos de la versión 16:9 (24/09, noche)

Bugs que reportó el usuario al probar la parte 1 en su app: el contraste subía y bajaba, el World Map mostraba solo NULL ZONE y el juego iba con lag (combate a 14 FPS).

- **Causa común del contraste y del mapa:** I19-WS creaba `__wsFondo` en la profundidad AS `-16383`, que es la **profundidad 1 del SWF** en la línea de tiempo principal. Ahí el juego coloca:
  - `krinMapper` (4103, fotograma 449 `overMap`);
  - el fondo degradado del menú (2637, fotograma 46);
  - el cuadro negro 213 (fotogramas 45, 151, 201 y 218);
  - 2628, 3266 y 3410 (intro del cómic).

  La capa los pisaba. Además, el reflejo ×0,5 dejaba un escalón visible en x = 0 y x = 800.
- **Arreglo de profundidad:** un solo clip `__wsFondo` en **-16384** (profundidad 0 del SWF, que nunca se usa) con:
  - la base #0E1215;
  - el reflejo L/R sin oscurecer;
  - un degradado negro de 0 a 45 % hacia el borde de la pantalla.

  **Regla: nunca crear clips en profundidades AS de -16383 a -1 en `_root`.**
- **Rendimiento:**
  - antes el reflejo se redibujaba cada 2 fotogramas y además se ocultaba y mostraba la capa, lo que invalidaba la pantalla entera: un repintado completo a 1440p unas 15 veces por segundo;
  - ahora se captura solo al cambiar la clave `_root._currentframe | KrinScreen | KRINMENU | getInstanceAtDepth(-16311)`, a los 3, 12 y 36 fotogramas, sin ocultar la capa.
- **Verificación en Ruffle:**
  - el menú queda píxel por píxel igual al original en el área 800x575;
  - `krinMapper` presente y el mapa completo;
  - se recorrieron intro, navegación, pueblo, inventario, habilidades y combate.
- **Lanzador modo rendimiento (opcional):** es el 2K con `stage.fullScreenSourceRect = screenRect` restaurado (3 bytes: `20 02 02` → `d0 66 41`). Dibuja a 1080p y el GPU escala, manteniendo el 16:9 completo. 2560x1440 son un 78 % más de píxeles que 1080p.
- Falta la confirmación del usuario en AIR.

## I21 e I22: HUD de navegación y prisión 2K (24–25/09)

- **HUD:**
  - se escalan las 23 colocaciones del fotograma 181 del escenario (UI_BAR en la profundidad 60 y las profundidades 126 a 166), con el ancla en (400, 575);
  - I21 lo dejó al 50 %; I22 lo pasó al **62 %** y lo subió 12 unidades a pedido del usuario;
  - el combate (fotograma 217) no cambia;
  - clics de I22 en Ruffle: inventario (651, 1304), habilidades (728, 1304), World Map (1280, 1304);
  - en las zonas sin imagen HD queda oscuro el espacio que liberó la barra.
- **Prisión 2K (I21, apagada en I22):** el original 2803 mide 764x414; en el juego se veía sin suavizado (relleno 0x43). La forma 2804 está en (-383,5, -206,9) de la zona, que en pantalla es x 319,6–2232,9, y 40,1–1076,9.
  - **Modelos, en ONNX sobre onnxruntime (CPU):**
    - Real-ESRGAN x4: `github.com/facefusion/facefusion-assets/releases/download/models-3.0.0/real_esrgan_x4.onnx`;
    - LaMa: `github.com/CloudyTabzy/Gimp-lama-inpainting/releases/download/v1.1.0/lama_fp32.onnx`.
    - PyPI, npm, HuggingFace y raw.githubusercontent están bloqueados en el entorno; las descargas de releases de GitHub funcionan.
  - **Proceso:**
    1. el centro se amplía con ESRGAN ×4;
    2. el borde se extiende con LaMa en 3 pasos a 1280x720; los recortes tienen que ser múltiplos de 32;
    3. lo extendido se amplía y se une en una franja de 24 px;
    4. los artefactos se borran con Telea;
    5. se aplica el grano de papel.
  - **Integración:** bitmap + forma en la profundidad 26 del fotograma 1 (PRISON) de 2908. El borde 2812 de la profundidad 47 se omite en PRISON y se repone en el fotograma 16.
  - **Resultado:** al usuario no le gustó cómo se ven las extensiones (difusas). Se apagó hasta nuevo aviso.

**Banco en Ruffle** (en `/home/claude/ruffle`):

- Ruffle nightly se baja de las releases de GitHub (`github.com/ruffle-rs/ruffle/releases/download/nightly-AAAA-MM-DD/ruffle-nightly-AAAA_MM_DD-web-selfhosted.zip`). npm devuelve 403.
- Se sirve con `http.server` en el puerto 8765.
- `servidor.py SWF W H` + `cmd.py` manejan la sesión, con el gancho `debug_hook.as` (ExternalInterface `dbg`). Si el contenedor se reinicia, hay que volver a lanzar los dos.
- **Partida nueva sin guardado:**
  1. clic en «Click to play»;
  2. `dbg set _root.Krin.slotInUse 1`;
  3. `dbg go classMenu`;
  4. clic en la clase;
  5. clic en «Click here to START!»;
  6. `dbg go Navigation`.
- `tour_i20.py`, `tour_i21.py` y `tour_i22.py` sacan las capturas.
- **Combate:** zona VILLAGE, clic en `sc(498, 233)` (`entrar_combate.py`).
- El fondo de combate es la instancia en `getInstanceAtDepth(-16311)`.
- `getInstanceAtDepth` de una profundidad vacía o de una forma devuelve `_level0`: nunca usar ese resultado como ruta.
- Los FPS en Ruffle (swiftshader, 2 CPU) no sirven como medida de AIR.

## Parte 2: imágenes HD

En `SONNY2_HD_PARTE2.zip` van `NECESITO.md`, las plantillas con guías, los originales y `tabla_imagenes.csv` (86 imágenes).

- **Zonas, 2560x1440:**
  - VILLAGE está hecha con la imagen del usuario;
  - PRISON quedó apagada;
  - faltan CITY (2816), TRAIN (2838), TUNNELS (2855), ROME (vectorial) y JAPAN (vectorial);
  - el original va en x 319–2232, y 40–1077.
- **Combate, 2560x786** (9): son los fotogramas etiquetados de 3328, a saber SEA, JAIL, SNOW, CHURCH, TRAIN, TUNNEL, ROME, STREETS y STREETS3. La franja va en y 327–1113; el original en x 316–2244.
- **Sin uso:** CASINO, EDEN, STORM y UTOPIA están vacías; BETA es de prueba.
- **Integración:** cada imagen entra igual que el pueblo, como personaje nuevo a pantalla completa en su zona.

## Pendientes

- **Esperando al usuario:**
  - que elija la variante A o B del panel de batalla;
  - que responda las 7 preguntas del rework;
  - que pruebe I22 en AIR.
- **Rework:**
  - implementado en I26, árbol con forma de clase en I27, ordenado por nivel con menús nativos en I28, escudo del juego y regla Wounds o Scent en I29, y menú en 2K en I30;
  - el usuario probó Endless Winter y el turno extra del aliado (bien) e I28 a nivel 14; falta que pruebe I29 e I30;
  - la simulación Heroic con el árbol nuevo queda pendiente: el usuario pidió no correrla (25/09).
- **Idioma:** el usuario mencionó cambios «a nivel lenguaje». Hasta ahora pidió solo el formato nativo del tooltip (I28).
- **Menú de habilidades en 2K:** hecho en I30 (también el panel de Aspectos). Falta que el usuario lo pruebe en su app. Si lo pide, se pueden pasar a 2K las demás páginas del menú (inventario, tienda, datos, opciones y logros).
- **Orden acordado (26/09):**
  1. ~~el menú de habilidades en 2K~~ (I30);
  2. revisar las habilidades: el usuario siente que pocas explotan las marcas (Scent, Wounds, Frostbite), salvo unas cuantas. Lo van a conversar antes de tocar nada.
- **Menú principal en 2K:** el usuario va a pedirle a ChatGPT el fondo del título en 2560x1440 (con y sin el título «SONNY 2», sin textos ni botones) para integrarlo como los fondos HD.
- **Repositorio GitHub** `a7kp2mq9xx-cyber/test` (rama `claude/jru-33pp84`, pública): la fuente del rework se puede subir. El juego (SWF) y `DECOMPILACION_PASO5.zip` se suben solo cuando el usuario la haga privada.
- **2K:** imágenes de pantalla completa para las demás zonas (las da el usuario).
- **Mod:**
  - Frozen Maw;
  - Slot 5;
  - fases v9–v11 (Heroic).

## Auditoría del 24/09 (juego base, sin tocar)

- 3 comparaciones con `== NaN`.
- `Stage.showMenu = false()`.
- La etiqueta `ArenaNav` con distintas mayúsculas.
- Dux Leading Strike dice 100 % pero pega 200 %.
- Wound no dice el % del golpe directo.

## Traducción (pendiente, cuando el usuario la pida)

Solo los diálogos:

- `BATTLESPEECH`: 146 líneas;
- `CUTSUB`: 27 subtítulos.

Están en los fotogramas 1 y 41. Las voces quedan en inglés.

## Decisiones de diseño cerradas

- Escalado: Hunt usa solo Strength; Glacial, Pack y Endurance usan el mayor entre Strength e Instinct (Instinto = Fuerza × 1,4).
- Solo el lobo genera Scent.
- Frostbite se detiene en 5.
- Cuando el motor no permite el efecto descrito, se cambia el texto.
- No hay efectos ocultos.
- **Textos de combate siempre con números exactos, en lenguaje Krin.**
- **Árbol del lobo (26/09):**
  - tooltip con el formato del árbol de clase;
  - no se escriben los requisitos: el árbol los impide con el cartel del juego;
  - cada fila es un escalón de nivel.
- **Ancestral Wolf:** +10 % de estadísticas fijo con Scent of Blood (el usuario, 26/09).
- **Wounds o Scent:** una habilidad sube por la cantidad de Wounds o por la de Scent, nunca por las dos (el usuario, 26/09). Frostbite puede ir con cualquiera de las dos.
- **Escudos:** siempre con el efecto del juego (burbuja, sonido y «SHIELDED»), y el tooltip del estado dice cuánto queda.
- Duración Krin: «N turnos» = CD − 1.
- 16:9 sin deformar: se escala por la altura. Lo que se estira son solo los bordes de paneles y los rectángulos lisos; nunca el arte.
- HUD de navegación: dock al 62 %, abajo al centro y levantado 12 unidades (I22).
- Idioma de la conversación: español neutral.
