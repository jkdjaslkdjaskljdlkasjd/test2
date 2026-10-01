# Sonny 2 a 16:9: I26 (rework del lobo, propuesta v4)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I26) | `a2d139e7790607d93f4e80276db4df51173772309d203676507cae044d9eea22` |
| Base: `SONNY2.swf` de I25 | `37a95f7138ee88e509dc5d5c0cdf4cd3b924ee26b0758d557cf804f31eba5469` |

Para instalar, reemplaza solo `SONNY2.swf`; el lanzador sigue siendo el mismo. Las partidas guardadas siguen sirviendo (ver «Partidas de I25»).

La entrega va en dos zips por el límite de 30 MB, y los dos traen este LEEME:

- **parte 1:** `SONNY2.swf` y `fuente/`;
- **parte 2:** `capturas/`.

Es la propuesta v4 «Mokoshotar: sangre y escarcha» implementada sobre I25, con las decisiones del 25/09. Todo lo demás de I25 (16:9, HUD, traducción, NULL ZONE, skins, capas propias) queda igual.

## Qué trae

- **Árbol en dos páginas** (pestaña Mokoshotar):
  - primer clic: **Página 1: Habilidades**, las 26 activas en 4 ramas (Hunt, Winter, Pack, Endurance);
  - otro clic: **Página 2: Instintos**, las 17 pasivas. Las pasivas clave (Scent of Blood, Deep Wounds, Shardfall) llevan un anillo dorado;
  - arriba: el emblema de Ancestral Wolf y el botón «Reiniciar lobo», que devuelve todos los puntos del lobo (gratis).
  - Nodo aprendido al 100 %, que se puede aprender al 60 % y bloqueado al 30 %. El rango se ve abajo de cada nodo y en dorado cuando está al máximo (maestría).
- **Ancestral Wolf** (pasiva de clase): con 1 punto en Scent of Blood da +10 % de Health, Strength, Instinct y Speed, y 2 puntos por nivel en lugar de 1 (3 en los niveles 5, 10, 15 y 20). Si se quita Scent of Blood, los puntos extra se retiran (sin dejar puntos negativos).
- **Aspectos y definitivas, solo en la NULL ZONE:** en el panel MOKOSHOTAR hay un botón nuevo, «Aspectos y definitivas»:
  - 4 Aspectos: Blood Moon, Long Winter, Pack Leader y Ancestros (el nuevo, de transformación). Hay uno activo a la vez, y elegirlo o cambiarlo es gratis;
  - 3 definitivas: Blood Moon Rising, Endless Winter y Call of the Ancestors. Cuestan 1 punto, piden nivel 12, se usan una vez por combate y solo aparecen con su Aspecto activo. Pack Leader todavía no tiene;
  - al pasar el mouse por una definitiva, su texto sale en el recuadro de abajo del panel.
- **Recursos del lobo:**
  - **Wounds:** tope de 3, 5 con Deep Wounds y 7 con Blood Moon;
  - **Scent of Blood:** hasta 3; con 3 el enemigo queda Hunted;
  - **Frostbite:** tope de 5 (7 con Long Winter). Desde 3 el enemigo está Brittle, y uno más sobre el tope lo congela;
  - **Ice Shards:** 2, o 3/5 con Shardfall.
- **Frozen Maw:** el ataque básico del lobo, siempre disponible en la lista.
- **Textos:** en inglés Krin, con los números exactos del rango actual y del siguiente. La maestría se muestra al llegar al rango máximo. En combate, cada ícono de estado muestra la cantidad de marcas; el tope y la duración salen en su tooltip.
- **Íconos de prueba:** las 20 habilidades nuevas usan una copia del ícono más parecido, teñida con el color de su rama (Hunt rojo, Winter celeste, Pack dorado, Endurance verde, definitivas violeta). Los estados nuevos usan íconos que ya existían. No se generó ninguna imagen.

### Habilidades (id, rangos, nivel por rango, Focus y recarga)

| Rama | Activas |
|---|---|
| Hunt | Rake 861 (3, gratis, Nv 1/2/3, 10 F) · Pounce 810 (2, Nv 1/3, 0 F) · Hamstring 812 (2, Nv 3/4, 10 F, CD 2) · Iron Jaws 864 (2, gratis, Nv 1/6, 12 F, CD 3) · Rupture 831 (2, Nv 5/6, 15 F, CD 3, pide Deep Wounds) · Cull the Weak 819 (3, Nv 8/9/10, 25/20/20 F, CD 4) · Killer Instinct 832 (2, Nv 8/10, 10 % de la vida actual, CD 6) |
| Winter | Wicked Claws 865 (3, gratis, Nv 1/3/5, 10 F, CD 1) · Howl of the Ancestors 863 (3, gratis, Nv 1/4/7, 10 F, CD 4) · Frost Fang 815 (3, Nv 5/6/7, 12 F, CD 2, pide Deep Wounds) · Shatter Guard 816 (2, Nv 6/7, 0 F, CD 1) · Cold Trail 818 (3, Nv 8/9/10, 20 F, CD 5) · Black Ice 833 (2, Nv 8/9, 18 F, CD 6, pide Shardfall) |
| Pack | Canine Instincts 862 (2, gratis, Nv 1/4, 15 F, CD 5/4) · Rallying Cry 821 (3, Nv 3/4/5, 15/12/12 F, CD 4/3/3) · Primal Breath 808 (2, Nv 3/5, 0 F, CD 6) · Guardian's Call 822 (2, Nv 5/6, 20 F, CD 5) · Feeding Frenzy 834 (2, Nv 6/7, 20 F, CD 5) · Frostbound Pack 835 (2, Nv 7/8, 20 F, CD 5) · Echo Ward 824 (3, Nv 8/9/10, 30/28/28 F, CD 6/5/5) |
| Endurance | Werezombie 809 (2, gratis, Nv 1/6, 25 F, CD 7/5) · Second Wind 826 (2, Nv 3/4, 0 F, CD 6) · Taste of Blood 836 (2, Nv 5/6, 12 F, CD 3, pide Deep Wounds) · Last Stand 827 (2, Nv 6/7, 15 F, CD 6) · Rime Coat 837 (2, Nv 6/7, 15 F, CD 5, pide Shardfall) · Ice Tomb 838 (1, Nv 10, 20 F, CD 7) |

| Rama | Pasivas |
|---|---|
| Hunt | **Scent of Blood** 811 (clave, Nv 1/4) · **Deep Wounds** 814 (clave, Nv 4/5) · Predator's Patience 817 (Nv 6/7) · Bloodhound 839 (Nv 7/8) · Relentless Hunt 820 (Nv 6/7) |
| Winter | **Shardfall** 840 (clave, Nv 5/6) · Frozen Blood 841 (Nv 6/7) · Winter's Grip 842 (Nv 8/9) · Cold Snap 843 (Nv 9/10) |
| Pack | Pack Tactics 823 (Nv 5/6) · Shared Hunger 844 (Nv 7/8) · Cold Comfort 845 (Nv 6/7) |
| Endurance | Thick Hide 825 (Nv 1/2) · Blood Drinker 846 (Nv 5/6) · Unyielding 828 (Nv 5/6) · Winter Heart 829 (Nv 6/7) · Undying Will 830 (1 rango, Nv 12) |

Definitivas: Blood Moon Rising 854 (30 F), Endless Winter 855 (30 F), Call of the Ancestors 856 (0 F). Ataque básico: Frozen Maw 857.

## Decisiones e interpretaciones para revisar

Donde la propuesta no fijaba un detalle, se eligió esto:

- **Niveles:** los niveles de las habilidades nuevas los elegí yo. Las definitivas piden nivel 12.
- **Ancestral Wolf:** pide Scent of Blood, así que los puntos extra también.
- **Wounds:**
  - sangran al final del turno de quien los tiene, con la fórmula nativa de daño en el tiempo y la Strength actual del lobo;
  - «for N turns» son N tics: un Wound nuevo sangra al final de cada uno de los N turnos siguientes del enemigo, y el tooltip del estado muestra cuántos quedan.
- **Brittle** solo sube el daño de los ataques directos del lobo.
- **Reducciones de daño:** se combinan multiplicando (Thick Hide, Ice Shards, Rime Coat, Last Stand, Ancestral Form…).
- **Rake:** su regla de Scent (1, o 2 si ya estaba herido) vale en todos los rangos.
- **Cull the Weak:** los bonos se suman (1 + 0,8 por Scent + 0,25 por Wound). Hace ×1,4 por debajo del 35 % de vida, y en R3 hace crítico seguro contra Brittle.
- **Shatter Guard** pega al menos una vez aunque no haya Frostbite.
- **Cold Trail:** Frostbite = 1 + 1 si es sobre Black Ice + 1 con la maestría si ya tenía Frostbite.
- **Rallying Cry:** quita 1/1/2 efectos negativos y da Courage de +15/20/25 % de daño por 3 turnos.
- **Call of the Ancestors:**
  - hace ×2 todo el daño (directo y en el tiempo) durante 3 turnos;
  - el turno extra es medio turno más del equipo del lobo: el lobo vuelve a actuar antes que los enemigos y los aliados pasan;
  - el aliado bendecido que cae vuelve como **Ancestral Wolf**, con números provisorios: 50 % de su vida máxima, la Strength e Instinct del lobo, forma de lobo (HOUND) y los ataques nativos Rake, Wicked Claws y Canine Instincts.
- **Ancestral Wolf y la capa night:** tu capa «night» cambia el título «Ancestral Wolf» por «Ancestral Mark (inactive)». Como en la v4 la pasiva está activa, el emblema usa el título «Ancestral Wolf (Class Passive)». No se tocó la capa night.

## Arreglos que aparecieron al probar

- **Mokoshotar como NPC o aliado:** las capas viejas del lobo descartaban los ataques 623–628 de cualquier unidad cuando el jugador no tenía esas habilidades. Afectaba al Mokoshotar de la NULL ZONE y ahora al Ancestral Wolf. Ahora esos ataques funcionan con el efecto nativo del juego.
- **Tooltips de la reserva y la barra:** las habilidades que conservan su id viejo (Pounce, Hamstring, Frost Fang y otras) mostraban el texto de I25. Ahora muestran el del rework.
- **Tooltips del árbol:** los íconos del lobo traen un script viejo que soltaba el tooltip en cada fotograma. Ahora el árbol y el panel de Aspectos lo mantienen mientras el mouse está encima.

## Partidas de I25

- Los puntos gastados en el árbol viejo se devuelven solos. Al abrir el árbol aparece el aviso «Árbol nuevo: se devolvieron N puntos del árbol anterior».
- La barra de combate conserva las habilidades con su id nuevo: 623→809, 624→861, 625→862, 626→863, 627→864 y 628→865. Expose Throat (813) ya no existe y sale de la barra.
- El botón nativo de reinicio de puntos (Respec) sigue funcionando: devuelve todos los puntos según el nivel. El Aspecto elegido vuelve a «ninguno», y elegirlo otra vez es gratis.

## Probado

- **Banco AVM1 fiel** (el mismo intérprete del juego, sin simulación Heroic, como pediste): `fuente/tests/test_rework.py` hace 265 comprobaciones y pasan todas. Cubre puntos y migración, fichas y barra, cada activa y pasiva con su maestría, los 4 Aspectos, las 3 definitivas, Frozen Maw, el NPC Mokoshotar y los textos. Las cuentas esperadas salen de la propuesta v4.
- **Ruffle** (1280x720), con el mismo SWF más el gancho de depuración:
  - las dos páginas del árbol con sus tooltips, el emblema, el panel MOKOSHOTAR y el de Aspectos (elegir un Aspecto y aprender una definitiva);
  - un combate real de la campaña (batalla 103, tres Convicts; se les subió la vida para que dure) con Rake, Howl, Wicked Claws, Rupture, Killer Instinct, Cold Trail, Frozen Maw y Blood Moon Rising. Se vio:
    - Wounds hasta el tope de 7 con Blood Moon;
    - Hunted a los 3 Scent, con los 2 Wounds de la maestría;
    - Wounds que no se disipan con el Adrenaline enemigo;
    - stun, Dread, Frostbite, Hemorrhage y Torn;
    - la herida de Blood Moon Rising al empezar el turno enemigo;
  - otro combate con Ancestros: Call of the Ancestors (curación, Focus, aura y un solo turno extra), la bendición en Veradux y el Ancestral Wolf que toma su lugar.

## Limitaciones conocidas

- La estrella «★» de las maestrías no existe en la fuente que usa Ruffle y no se ve (en Flash con fuentes del sistema sí). Por eso el rango al máximo también se pinta en dorado.
- En Ruffle, el tooltip nativo de los estados sigue al mouse y en los enemigos se corta por el borde derecho. Es comportamiento de I25, no del rework.
- Los números del Ancestral Wolf son provisorios (la propuesta decía «números por cerrar»).
- **Pendiente:** correr la simulación Heroic con el árbol nuevo, cuando la pidas.

## Fuente (`fuente/`)

- `build.py`: arma el SWF sobre I25 separado (`paso1`) y descompilado (`paso3`) con las herramientas del paso 5 (`swfpatch.py`, `as2comp.py`). Uso: `python3 build.py SALIDA.swf [--debug] [--sin-rework]`. Espera esta estructura de carpetas: `../paso5/tools` (de `DECOMPILACION_PASO5.zip`) y `../i25/paso1` y `../i25/paso3` (I25 pasado por `swfsplit.py` y `swfcode.py`).
  - Suma los 20 fotogramas de íconos de prueba al sprite 2186 y las etiquetas de estado al sprite 1986.
  - Agrega `src/rw_*.as` al final de DoAction_2 (fotograma 42).
  - Parchea el reloj de combate (fotograma 217) en dos puntos: la esquiva (Hunted y Killer Instinct no se esquivan) y el turno extra.
- `src/`: la capa del rework en orden de carga:
  - `rw_00_base`: utilidades; deja inertes las capas viejas del lobo;
  - `rw_10_data`: tabla de habilidades, puntos y migración;
  - `rw_15_records`: fichas KRINABILITY y barra;
  - `rw_20_status`: estados y marcas;
  - `rw_30_core`: daño, curación y marcas;
  - `rw_40_casts`: cada habilidad;
  - `rw_50_hooks`: ganchos del motor, Aspectos y definitivas;
  - `rw_60_texts`: textos;
  - `rw_70_ui`: árbol, NULL ZONE e íconos de estado.
- `debug_hook.as`: gancho `dbg` para el banco, solo con `--debug`.
- `tests/`:
  - `rwbench.py`: banco que arma un combate a mano. Usa `motor.py` y `avmvm.py` del banco de `SONNY2_SIM_HEROIC.zip` (en `../../banco`) y el SWF en `../i26.swf`;
  - `test_rework.py`: las pruebas;
  - `smoke.py`: prueba rápida.
- `ruffle/`: `drive.js` y los guiones de las capturas (`s_final_A/B/C.json`).

## Capturas (`capturas/`, parte 2)

Ruffle 1280x720, build con el gancho de depuración (el mismo código de juego que `SONNY2.swf`).

| Captura | Qué muestra |
|---|---|
| `01_arbol_pagina1.png` | Página 1: Habilidades, con algunas aprendidas (Rake y Wicked Claws al máximo en dorado) |
| `02_tooltip_habilidad.png` | Tooltip de Rake: rango, costo, texto exacto y maestría |
| `03_arbol_pagina2.png` | Página 2: Instintos, con los anillos de las pasivas clave |
| `04_tooltip_pasiva.png` | Tooltip de Scent of Blood |
| `05_tooltip_ancestral.png` | Emblema de Ancestral Wolf: activo y 23 puntos extra a nivel 20 |
| `06_null_zone.png` | Panel MOKOSHOTAR de la NULL ZONE con el botón nuevo |
| `07_aspectos.png` | Panel de Aspectos y definitivas |
| `08_aspectos_definitiva.png` | Blood Moon elegido, Blood Moon Rising aprendida y el texto de Call of the Ancestors en el recuadro |
| `10_combate_marcas.png` | Combate: 7 Wounds, Scent, Frostbite, stun y Dread en los Convicts (cantidad en cada ícono) |
| `11_tooltip_estado.png` | Tooltip de un estado: «Frostbite (2/5)», duración y efecto |
| `12_rupture.png` | Rupture: consume los Wounds y pone Hemorrhage y Torn |
| `13_blood_moon_rising.png` | Blood Moon Rising: un Wound por turno enemigo, y el sangrado cura al lobo |
| `15_call_of_the_ancestors.png` | Call of the Ancestors: aura, bendición en Veradux y «Mokoshotar acts again!» |
| `16_lobo_ancestral.png` | Veradux cae y el Ancestral Wolf toma su lugar |
| `17_turno_siguiente.png` | El combate sigue con el lobo ancestral |
