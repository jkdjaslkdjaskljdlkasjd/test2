# Sonny 2 a 16:9: I27 (árbol del lobo con la forma del árbol de clase)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I27) | `c78db85f44df641777cc4740ad59531f69d7fec6375e15a35dc063d4da416112` |
| Base: `SONNY2.swf` de I26 | `a2d139e7790607d93f4e80276db4df51173772309d203676507cae044d9eea22` |

Para instalar, reemplaza solo `SONNY2.swf`; el lanzador sigue siendo el mismo. Las partidas de I25 e I26 siguen sirviendo.

## Cambios respecto de I26

- **Forma del árbol de clase:**
  - misma grilla de 4x7 y en las mismas posiciones que el árbol de clase;
  - el ícono queda oscuro hasta que tiene un punto;
  - entre cada nodo y su requisito hay un caño negro con una línea dorada, que se enciende cuando el requisito ya tiene un punto.
- **Sin números de rango en los nodos:** el rango se ve en el tooltip, por ejemplo «(1/3) Rake».
- **Las conexiones ahora son requisitos reales**, como en el árbol de clase: para aprender un nodo hace falta al menos 1 punto en el nodo conectado de arriba. El árbol ya no es una columna entera por rama: tiene cortes, nodos sueltos y diagonales entre ramas vecinas, así que no hay que pasar por todos los nodos (ver la tabla).
- **Pasivas clave** (Scent of Blood, Deep Wounds, Shardfall): un anillo dorado fino pegado al ícono, en lugar del círculo grande.
- **Quitado:**
  - «Página 1: Habilidades»;
  - «Reiniciar lobo» (el Respec del juego sigue funcionando);
  - los nombres de rama arriba de las columnas (el árbol de clase no los tiene; la rama sale en el tooltip);
  - el texto «Otro clic en Mokoshotar: Instintos (pasivas)».
- **Cambio de página:** un selector «Abilities · Instincts» al pie del árbol. La página activa queda en claro y subrayada. El segundo clic en la pestaña Mokoshotar sigue funcionando.
- **Avisos:** los del árbol (por ejemplo, «Requires Level 8.») salen con el cartel del juego, como en el árbol de clase.
- **Tooltip de un nodo sin aprender:** ya no repite la descripción. Abajo dice los requisitos, el nivel y el costo, por ejemplo «Requires Feeding Frenzy. Learn: Lvl. 7, 1 Ability Point.».
- **Bono de Ancestral Wolf:** el bono de estadísticas ahora usa la llave que ya tiene la base, `_root.__i1AncBonus`:
  - 0,1 = +10 %; 0 = apagado;
  - tu capa night la deja en 0, así que hoy no suma;
  - los puntos extra siguen dependiendo de Scent of Blood;
  - el emblema muestra la estrella dorada solo si el bono suma, y el tooltip dice el porcentaje real.
- **Arreglo:** en algunos nodos se borraban el título y el texto del tooltip. El ícono que el tooltip trae adentro los pisaba con su propio texto vacío.

### Conexiones

Se leen «requisito → nodo»; ↘ y ↙ son diagonales entre ramas vecinas.

| Rama | Página 1 · Abilities | Página 2 · Instincts |
|---|---|---|
| Hunt | Rake → Pounce · Iron Jaws → Hamstring → Rupture · Cull the Weak → Killer Instinct | Scent of Blood → Predator's Patience · Deep Wounds → Bloodhound → Relentless Hunt |
| Winter | Wicked Claws → Shatter Guard · Hamstring ↘ Frost Fang · Cold Trail → Black Ice · Howl suelta | Shardfall → Winter's Grip → Cold Snap · Deep Wounds ↘ Frozen Blood |
| Pack | Canine Instincts → Rallying Cry · Second Wind ↙ Primal Breath · Feeding Frenzy → Frostbound Pack → Echo Ward · Guardian's Call suelta | Pack Tactics → Cold Comfort · Blood Drinker ↙ Shared Hunger |
| Endurance | Werezombie → Second Wind → Taste of Blood · Last Stand → Rime Coat · Ice Tomb suelta | Thick Hide → Blood Drinker · Unyielding → Winter Heart → Undying Will |

- Las 6 habilidades gratis (Rake, Iron Jaws, Wicked Claws, Howl, Canine Instincts, Werezombie) no tienen requisito. Lo que cuelga de ellas solo pide nivel.
- Siguen los requisitos de la otra página: Deep Wounds para Rupture, Frost Fang y Taste of Blood, y Shardfall para Black Ice y Rime Coat.
- Cada conexión es un dato en `fuente/src/rw_10_data.as` (`__rwPlace`), fácil de mover si prefieres otra forma.

## Sin cambios

Todo lo demás de I26: las habilidades y sus números, los estados, los Aspectos y las definitivas de la NULL ZONE, el combate, el 16:9 y tus capas.

## Probado

- **Banco fiel:** `fuente/tests/test_rework.py` hace 280 comprobaciones y pasan todas. Suma a I26:
  - la forma del árbol: cada conexión va a la fila de arriba, en la misma columna o la vecina; no hay dos nodos en una casilla y las gratis no tienen requisito;
  - los requisitos por conexión;
  - el bono de Ancestral con la llave de la base en 0 y en 0,1.
- **Ruffle** (1280x720, el mismo SWF más el gancho de depuración): las dos páginas, el cambio de página con el selector y con la pestaña, y los tooltips (con conexión, bloqueado, pasiva clave y emblema).
  - En este arnés la pantalla se estira en horizontal (x ×1,6 contra y ×1,24), por eso los íconos y los anillos se ven un poco ovalados en las capturas.
  - En tu app se ven redondos, como en tu captura de I26.

## Fuente (`fuente/`)

La misma estructura que en I26:
- `build.py`;
- `src/rw_*.as`;
- `debug_hook.as`;
- `tests/`;
- `ruffle/`, con `s_final27.json`, el guion de estas capturas.

## Capturas (`capturas/`)

| Captura | Qué muestra |
|---|---|
| `01_arbol_abilities.png` | Página Abilities con algunas aprendidas: caños dorados, diagonales y nodos oscuros sin aprender |
| `02_tooltip_conexion.png` | Frost Fang: «Requires Hamstring, Deep Wounds (Instincts)» y el rango siguiente |
| `03_tooltip_bloqueado.png` | Frostbound Pack sin aprender: requisito, nivel y costo, sin repetir la descripción |
| `04_arbol_instincts.png` | Página Instincts con los anillos finos de las pasivas clave |
| `05_tooltip_pasiva_clave.png` | Tooltip de Scent of Blood |
| `06_tooltip_ancestral.png` | Emblema de Ancestral Wolf con el bono de la base en 0 |
