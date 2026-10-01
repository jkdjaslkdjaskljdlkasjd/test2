# Sonny 2 a 16:9: I28 (árbol del lobo ordenado por nivel y menús con aspecto nativo)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I28) | `58fb99cad99c10cd15e9504fec6ac6e912b6ea827b0f3cd3fa8e5ef36e2df909` |
| Base: `SONNY2.swf` de I27 | `c78db85f44df641777cc4740ad59531f69d7fec6375e15a35dc063d4da416112` |

Para instalar, reemplaza solo `SONNY2.swf`; el lanzador sigue siendo el mismo. Las partidas de I25 a I27 siguen sirviendo. Los puntos que ya tenías gastados se quedan donde están, aunque el árbol nuevo pida otro camino. Si quieres repartirlos de nuevo, usa el Respec del juego.

## Cambios respecto de I27

### Árbol ordenado por nivel

- **Cada fila es un escalón de nivel:** 1, 2, 3, 5, 6, 8 y 10, de arriba hacia abajo.
  - A la derecha de la grilla dice el nivel de cada fila («Lvl. 1», «Lvl. 2»…).
  - Las filas que ya alcanzaste se ven más claras.
  - El primer rango de cada habilidad pide el nivel de su fila, y los rangos siguientes conservan su distancia (ver la tabla de niveles).
- **Al principio se abren pocas.**
  - Las 6 gratis están arriba y son las únicas raíces de Abilities.
  - Todo lo demás cuelga de un requisito, como en el árbol de clase.
  - Esto es lo que se abre (sin contar las gratis):

    | Nivel | Qué se puede aprender |
    |---|---|
    | 1 | Scent of Blood y Thick Hide (Instincts) |
    | 2 | Además, Rallying Cry y Second Wind |
    | 3 | Pounce, Hamstring y Deep Wounds (esta última con Scent) |

- **Hamstring es el nudo del árbol:** de ella salen Rupture, Frost Fang y Feeding Frenzy. Es la fuente de Wounds que usan la sangre, el hielo y la manada.
- **Las pasivas clave van en cadena:** Scent of Blood → Deep Wounds → Shardfall.
- **Cómo se ve cada nodo:**

  | Estado | Cómo se ve |
  |---|---|
  | Aprendida | Ícono claro |
  | Se puede aprender ahora | Brillo verde (el mismo del aviso «You have upgrade points available!») |
  | Con requisitos cumplidos, pero sin puntos | Oscura |
  | Bloqueada por nivel o por requisito | Oscura y atenuada |

### Tooltip y avisos como en el árbol de clase

- **El tooltip usa el formato nativo:**
  - el título, por ejemplo «(0/2)  Hamstring»;
  - el costo, por ejemplo «Costs 10 Focus. (CD: 2)»;
  - en el cuerpo, «You have no points in this ability yet.» o el rango que tienes;
  - abajo, «Next Tier (Lvl. 3): …» con el rango siguiente, o «This ability is at its maximum tier.».
- **Las pasivas** dicen «Passive Combat Effect», y las pasivas clave «Key Passive Combat Effect».
- **Los requisitos ya no se escriben.** Si haces clic en algo que no puedes aprender, sale el cartel del juego: «You don't have the required abilites to access this one.», «Your Level is not high enough.», «You do not have enough Ability Points.» o «This Ability cannot be developed further.».
  - Los textos salen de los del juego (`KrinLang`), así que siguen el idioma del juego.
  - Hay requisitos de la otra página:
    - Rupture, Frost Fang y Taste of Blood piden Deep Wounds;
    - Black Ice y Rime Coat piden Shardfall.

    Esas habilidades se ven atenuadas hasta que tengas la pasiva.

### Aspecto nativo

- **Pestañas «Abilities» e «Instincts»** al pie del árbol, con la forma de las pestañas Class / Mokoshotar. El segundo clic en la pestaña Mokoshotar sigue cambiando de página.
- **El emblema de Ancestral Wolf** es tu marca ancestral de la capa night (las runas azules, `nightAncestralMark`). Tiene un brillo azul cuando está activa y se ve atenuada si no lo está.
- **Los íconos de las habilidades no cambiaron.**

### +10 % de Ancestral Wolf restaurado

Con el primer punto en Scent of Blood suma 10 % de Health, Strength, Instinct y Speed, como en I26. Ya no depende de `_root.__i1AncBonus` (la capa night lo deja en 0 para la marca vieja, que sigue inerte), y no se suma dos veces. Los puntos extra siguen igual.

### Panel de Aspectos (NULL ZONE → MOKOSHOTAR → «Aspectos y definitivas»)

Tiene la forma del menú de personaje, con los mismos colores, recuadros y botones:

- **Izquierda:** los 4 Aspectos con su ícono.
  - El Aspecto que estás mirando tiene el marco verde.
  - El activo aparece en dorado y dice «Activo».
  - Si ya aprendiste su definitiva, también dice «definitiva aprendida».
- **Centro:**
  - el Aspecto que estás mirando, con el título en dos líneas («Aspect of the» / «Long Winter»);
  - si está activo o no;
  - tus puntos de habilidad y su efecto;
  - el botón «Activar», con el marco verde.
- **Derecha:** su definitiva, con ícono, costo y descripción, y el botón «Aprender (1 punto)».
  - Si todavía no puedes aprenderla, dice por qué: «Requiere Nivel 12.», «Primero activa este Aspecto.» o «No tienes puntos de habilidad.».
  - Pack Leader sigue sin definitiva.
- **Aviso dorado:** al activar un Aspecto o aprender una definitiva, aparece arriba del botón.
- **«Volver»** te lleva al menú MOKOSHOTAR.

## El árbol nuevo

Se lee «requisito → habilidad». ↘ y ↙ son diagonales a la columna vecina. «(DW)» quiere decir que además pide Deep Wounds, y «(SF)» que además pide Shardfall. Hamstring es de Hunt, pero está en la columna de Winter porque es el puente entre la sangre y el hielo.

### Página 1 · Abilities

| Nivel | Hunt | Winter | Pack | Endurance |
|---|---|---|---|---|
| 1 | Rake (gratis) | Wicked Claws (gratis) | Canine Instincts (gratis) | Werezombie (gratis) |
| 2 | Rake → Iron Jaws (gratis) | Wicked Claws → Howl of the Ancestors (gratis) | Canine Instincts → Rallying Cry | Werezombie → Second Wind |
| 3 | Iron Jaws → Pounce | Iron Jaws ↘ Hamstring | Rallying Cry → Primal Breath | |
| 5 | Hamstring ↙ Rupture (DW) | Hamstring → Frost Fang (DW) | Hamstring ↘ Feeding Frenzy | Second Wind → Taste of Blood (DW) |
| 6 | | Frost Fang → Shatter Guard | Feeding Frenzy → Guardian's Call | Taste of Blood → Last Stand |
| 8 | Rupture → Cull the Weak | Shatter Guard → Cold Trail | Guardian's Call → Frostbound Pack | Last Stand → Rime Coat (SF) |
| 10 | Cull the Weak → Killer Instinct | Cold Trail → Black Ice (SF) | Frostbound Pack → Echo Ward | Rime Coat → Ice Tomb |

### Página 2 · Instincts

| Nivel | Hunt | Winter | Pack | Endurance |
|---|---|---|---|---|
| 1 | Scent of Blood (clave) | | | Thick Hide |
| 3 | Scent of Blood → Deep Wounds (clave) | | | Thick Hide → Unyielding |
| 5 | Deep Wounds → Predator's Patience | Deep Wounds ↘ Shardfall (clave) | Pack Tactics | Unyielding → Blood Drinker |
| 6 | Predator's Patience → Relentless Hunt | Shardfall → Frozen Blood | Pack Tactics → Cold Comfort | Blood Drinker → Winter Heart |
| 8 | Relentless Hunt → Bloodhound | Frozen Blood → Winter's Grip | Cold Comfort → Shared Hunger | |
| 10 | | Winter's Grip → Cold Snap | | Winter Heart → Undying Will |

- Pack Tactics es la entrada de la manada en Instincts: no tiene requisito, pero pide nivel 5.
- Cada conexión es un dato en `fuente/src/rw_10_data.as` (`__rwPlace`), y los niveles de fila están en `__rwTiers`. Es fácil de mover si prefieres otra forma.

### Niveles que cambiaron

Los niveles de las demás habilidades y de las definitivas no cambiaron.

| Habilidad | I27 (por rango) | I28 (por rango) |
|---|---|---|
| Pounce | 1, 3 | 3, 5 |
| Rallying Cry | 3, 4, 5 | 2, 3, 4 |
| Second Wind | 3, 4 | 2, 3 |
| Feeding Frenzy | 6, 7 | 5, 6 |
| Guardian's Call | 5, 6 | 6, 7 |
| Frostbound Pack | 7, 8 | 8, 9 |
| Rime Coat | 6, 7 | 8, 9 |
| Killer Instinct | 8, 10 | 10, 12 |
| Black Ice | 8, 9 | 10, 11 |
| Echo Ward | 8, 9, 10 | 10, 11, 12 |
| Deep Wounds | 4, 5 | 3, 4 |
| Unyielding | 5, 6 | 3, 4 |
| Predator's Patience | 6, 7 | 5, 6 |
| Bloodhound | 7, 8 | 8, 9 |
| Shared Hunger | 7, 8 | 8, 9 |
| Cold Snap | 9, 10 | 10, 11 |
| Undying Will | 12 | 10 |

## Probado

- **Banco fiel:** `fuente/tests/test_rework.py` hace 294 comprobaciones y pasan todas. Suma a I27:
  - la forma del árbol: cada fila es su nivel, las conexiones suben de fila, no hay diagonales cruzadas ni raíces sueltas en Abilities, y las gratis están arriba;
  - lo que se abre a nivel 1, 2 y 3;
  - los avisos del juego, en su orden: requisito, nivel, puntos y rango máximo;
  - el +10 % de Ancestral Wolf con Scent of Blood, sin sumarse dos veces y sin bono sin Scent.
- **Ruffle** (1280x720, el mismo SWF más el gancho de depuración):
  - el árbol a nivel 3 y a nivel 12, en las dos páginas;
  - el tooltip con el formato nativo;
  - el cartel del juego al hacer clic en algo bloqueado;
  - el emblema;
  - el panel de Aspectos: elegir, activar, aprender la definitiva y «Volver».

  En este arnés la pantalla se estira en horizontal (x ×1,6 contra y ×1,24), por eso los íconos y los anillos se ven un poco ovalados en las capturas. En tu app se ven redondos.
- **No se corrió ninguna simulación Heroic.**

## Fuente (`fuente/`)

- `build.py`: `python3 build.py i28.swf` arma el SWF desde I25 (herramientas del paso 5); con `--debug` suma el gancho de depuración.
- `src/rw_*.as`: la capa del rework. En esta versión cambiaron:
  - `rw_10_data.as`: el orden del árbol, los avisos y el bono;
  - `rw_70_ui.as`: el árbol y el panel de Aspectos.
- `tests/`: el banco. Espera `i28.swf` al lado de `build.py`.
- `ruffle/`: el guion de estas capturas (`s_final28.json`).

## Capturas (`capturas/`)

| Captura | Qué muestra |
|---|---|
| `01_arbol_nivel3.png` | Abilities a nivel 3: brillan solo Pounce, Hamstring, Rallying Cry y Second Wind |
| `02_tooltip_nativo.png` | Hamstring con el tooltip del árbol de clase: «You have no points in this ability yet.» y «Next Tier (Lvl. 3): …» |
| `03_aviso_requisito.png` | Clic en Rupture sin Hamstring: el cartel del juego |
| `04_instincts_nivel3.png` | Instincts a nivel 3 con Scent of Blood |
| `05_emblema.png` | El emblema (tu marca ancestral) y su tooltip |
| `06_arbol_nivel12.png` | Abilities a nivel 12 con varias aprendidas |
| `07_instincts_nivel12.png` | Instincts a nivel 12 |
| `08_aspectos.png` | Panel de Aspectos al abrirlo |
| `09_aspecto_activado.png` | Aspect of the Long Winter activado |
| `10_definitiva_aprendida.png` | Endless Winter aprendida |
| `11_aspecto_ancestros.png` | Aspect of the Ancestors sin activar: la definitiva dice qué falta |
