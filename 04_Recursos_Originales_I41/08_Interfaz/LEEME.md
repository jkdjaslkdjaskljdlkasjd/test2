# Interfaz — pantallas, botones, estados y comportamiento

Fuente: líneas de tiempo del SWF I41 y código de cada botón (`03_Codigo/scripts_as/scripts/DefineButton2_<id>/`).

- `botones.csv`: los 138 botones. Cada fila incluye:
  - `pantallas`: etiquetas del escenario principal donde aparece el botón, por ejemplo `mainMenu`, `Navigation` o `KRINBATTLESCENE`;
  - `instancias` y `contenedores`: nombre de instancia y sprite padre;
  - `estado_up/over/down/hit`: CharacterID dibujado en cada estado;
  - `estados_visibles` y `tipo_boton`;
  - `eventos`: `on(press)`, `on(release)`…;
  - `acciones_resumen`: `gotoAndStop("…")`, funciones `_root.*` llamadas, variables asignadas;
  - rutas a los PNG/SVG de los estados y al código.
- `textos.csv`: los 226 textos. Cada fila incluye la variable vinculada (`variableName`), el texto inicial, la pantalla y la instancia.
- `interfaz.json`: todo lo anterior, más el código completo de cada evento y el índice `por_pantalla`.
- `laminas/`: una lámina por pantalla con el estado `up` de sus botones.

**Botones invisibles.** 95 de los 138 botones son **zonas invisibles**: solo tienen área de clic (estado hit), y lo que se ve es el texto o el gráfico de debajo. Por eso salen vacíos en las láminas. Los otros 43 cambian al pasar el ratón. Para Godot, los invisibles equivalen a un `Button` plano o `TextureButton` sin textura sobre el gráfico.

**Pantallas que monta el código.** Muchas (combate, mapa, menú de personaje) se completan en tiempo de ejecución con `attachMovie`. La pantalla indicada es aquella desde la que el botón es alcanzable en el escenario.
