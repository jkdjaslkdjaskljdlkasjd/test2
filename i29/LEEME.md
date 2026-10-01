# Sonny 2 a 16:9: I29 (escudo del juego, estados con cantidad y turnos, y cada habilidad por Wounds o por Scent)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I29) | `b440bf336021bf4747df5d8647a392a76503e924acd0250c60022d77863cbf21` |
| Base: `SONNY2.swf` de I28 | `58fb99cad99c10cd15e9504fec6ac6e912b6ea827b0f3cd3fa8e5ef36e2df909` |

Para instalar, reemplaza solo `SONNY2.swf`; el lanzador sigue siendo el mismo. Las partidas de I25 a I28 siguen sirviendo.

## Cambios respecto de I28

### Árbol

- El selector de páginas vuelve a ser el de I27: el texto «Abilities · Instincts» con la página activa subrayada en dorado.
- Deep Wounds y Shardfall ya no dicen «Required by…». Es lo mismo que pediste para los tooltips: el árbol impide aprender y avisa con el cartel del juego.

### Escudos con el efecto del juego

Cuando el lobo crea un escudo aparece lo mismo que muestra el juego:
- la burbuja alrededor del personaje;
- el sonido `sfx_shield`;
- el cartel «SHIELDED».

Esto pasa con Guardian's Call, Echo Ward, Winter Heart, las maestrías de Blood Drinker y Shared Hunger, y Undying Will.

- **Al absorber:** pasa lo mismo cuando un escudo para un golpe del lobo (Wounds, estallidos, esquirlas) y cuando el escudo de Guardian's Call absorbe daño del aliado.
- **Guardian's Call** se lanza con el efecto de escudo del juego (`BOOM_SHIELD`).
- **Tooltip:** el del estado sigue diciendo cuánto escudo queda, por ejemplo «Shield: absorbs 220 damage.».

### Estados que se acumulan: cantidad y turnos

Wounds, Frostbite, Scent of Blood e Ice Shards:
- el contador del juego, abajo en el ícono, vuelve a mostrar los **turnos**, como en todos los demás estados;
- la **cantidad** aparece en dorado arriba a la derecha del ícono;
- el tooltip dice las dos cosas: «Scent of Blood (1/3)» y «Duration: 3 turns.».

### Cada habilidad sube por Wounds o por Scent, no por las dos

Rake y Hamstring ponen Wounds y Scent a la vez, así que una habilidad que sube por las dos cantidades se llena muy fácil. Apliqué tu regla a seis habilidades:

| Habilidad | Antes | Ahora |
|---|---|---|
| Canine Instincts | +1 turno por cada 2 Wounds o Scent del enemigo más marcado | +1 turno por cada 2 Wounds del enemigo con más Wounds |
| Pack Tactics | Aliados: +6 % de daño por Scent (hasta 18 %) y +3 % por Wound (hasta 15 %) | +3 % por Wound (hasta 15 %). Contra un enemigo Hunted sigue curando 15 % |
| Rallying Cry | +10 % de cura por Scent, Wound y Frostbite del equipo enemigo (hasta +80 %) | +10 % por Wound y Frostbite (hasta +80 %) |
| Relentless Hunt | Focus por Scent, Wound o Frostbite que consumes | Focus por Scent o Frostbite que consumes |
| Winter Heart | Escudo por Scent, Wound o Frostbite que consumes | Escudo por Wound o Frostbite que consumes |
| Unyielding | Consumir Scent o Wounds quita un daño en el tiempo (★ con 3 o más) | Solo Wounds |

- **Sin tocar, como pediste:** Cull the Weak, Second Wind, Shared Hunger y «Frostbite al que golpea».
- **Los números que quedan no cambiaron:** Pack Tactics y Relentless Hunt quedan más flojas que antes. Si quieres, las subo.

## Menú de habilidades en 2K

Queda para I30, como elegiste.
- **La idea:** el panel rojo cubre todo el 16:9, sin el recuadro con los costados borrosos, y los tres recuadros quedan más anchos. En el árbol, los íconos y las separaciones son más grandes.
- **Qué tiene de delicado:**
  - el Ability Pool y la Combat Action Bar son del juego y hay que mover sus piezas sin romper el arrastrar y soltar;
  - las otras páginas del menú (inventario, tienda, opciones) comparten el mismo panel.
- **Hay que probarlo en tu app:** el arnés de Ruffle estira la pantalla.

## Probado

- **Banco fiel:** `fuente/tests/test_rework.py` hace 298 comprobaciones y pasan todas. Suma a I28:
  - las seis habilidades con la regla nueva;
  - que consumir Scent ya no activa Unyielding ni Winter Heart;
  - que Rupture no da Focus de Relentless Hunt y que Iron Jaws sí.
- **Ruffle** (1280x720, el mismo SWF más el gancho de depuración):
  - el árbol con el selector de I27;
  - los tooltips de Canine Instincts y de Winter Heart;
  - una pelea de prueba con Echo Ward (escudo del juego en el lobo y el aliado), los íconos con cantidad y turnos, y Guardian's Call.
- **No se corrió ninguna simulación Heroic.**

## Fuente (`fuente/`)

- `build.py`: `python3 build.py i29.swf` arma el SWF desde I25 (herramientas del paso 5); con `--debug` suma el gancho de depuración.
- `src/rw_*.as`: la capa del rework. En esta versión cambiaron:
  - `rw_00_base.as`: `__rwShieldFx`, el escudo del juego;
  - `rw_20_status.as`: el escudo al crearse;
  - `rw_30_core.as` y `rw_40_casts.as`: el escudo al absorber y la regla de Wounds o Scent;
  - `rw_50_hooks.as`: Pack Tactics y el escudo de Guardian's Call;
  - `rw_60_texts.as`: los textos;
  - `rw_70_ui.as`: el selector y la cantidad en los íconos.
- `tests/`: el banco. Espera `i29.swf` al lado de `build.py`.
- `ruffle/`: los guiones de estas capturas (`s_final29.json`, y `s_final29_fx.json` para las ráfagas del escudo).

## Capturas (`capturas/`)

| Captura | Qué muestra |
|---|---|
| `01_arbol_selector.png` | El árbol con el selector «Abilities · Instincts» de I27 |
| `02_tooltip_canine.png` | Canine Instincts: la duración cuenta solo Wounds |
| `03_instincts.png` | La página Instincts |
| `04_tooltip_winter_heart.png` | Winter Heart: el escudo cuenta Wounds y Frostbite |
| `05_escudo_nativo.png` | Echo Ward: la burbuja y el cartel «SHIELDED» del juego sobre el lobo y el aliado |
| `06_estados_cantidad_y_turnos.png` | Íconos de estado: la cantidad en dorado y los turnos abajo |
| `07_tooltip_estado.png` | Tooltip de un estado que se acumula: «Wounds (4/5)» y «Duration: 3 turns.» |
| `08_guardians_call.png` | Guardian's Call con el efecto de escudo del juego |
