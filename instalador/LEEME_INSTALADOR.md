# Instalador del mod (Windows)

- **`INSTALAR.bat`:** ponlo en la carpeta de la versión que descomprimiste, junto a `SONNY2.swf` (o en la carpeta de arriba), y ábrelo con doble clic.
  1. Pide permisos de administrador, porque el juego está en Program Files.
  2. Si el juego está abierto, espera a que lo cierres.
  3. Guarda el `SONNY2.swf` que había en `Resources\_respaldos_mod\` (deja los 5 más nuevos).
  4. Copia el nuevo y comprueba que quedó idéntico.
  5. Muestra el SHA-256, para compararlo con el del `LEEME.md` de la versión.
- **`RESTAURAR.bat`:** vuelve a poner el último respaldo, es decir, la versión que tenías antes de la última instalación.
- **Carpeta del juego:** por defecto es `C:\Program Files (x86)\Steam\steamapps\common\Sonny Legacy Collection\SonnyLegacy.app\Contents\Resources`.
  - Si no la encuentra, te pide la ruta; puedes arrastrar la carpeta a la ventana.
  - Si la cambias de lugar, edita la línea `DESTINO_DEFECTO` al principio de los dos `.bat`.
