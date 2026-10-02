# Sonny 2 a 16:9: I38 (New Alcatraz HD de prueba, calidad máxima y selector de zona)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I38) | `4cd1eac3f563e9ad809e49bd6fb2ccdcadaac9f811d8eef73709a5850e4e3a8f` |
| Base: I37 | `50c1a33a3014f49be6a85c40154fb2a415d98b82b1358d6a9012076f3d98640b` |

Se descarga **desde la repo** (`i38/SONNY2.swf`), no desde el chat. Pesa 49,6 MB porque las imágenes van sin pérdida. Para instalarlo, `instalador/INSTALAR.bat`.

## Qué cambia

### 1. Zona 1, New Alcatraz, con tu imagen (de prueba)

- **La imagen:** la que me pasaste (1672×941), ampliada ×4 con **Real-ESRGAN `realesr-animevideov3`** (los pesos oficiales) y bajada con Lanczos a 2560×1440.
- **Sin uniones:** la ampliación va por bloques solapados, y comprobé que da exactamente lo mismo que la imagen entera.
- **Dónde quedó guardada:** en `fondos_hd/world_map/`:
  - `PRISON_Z1.png`: la original;
  - `PRISON_Z1_2560x1440.png`: la ampliada.
- **El bug de Hew no vuelve:** la cárcel ocupa la misma capa que usa Hew, así que Hew ahora vacía esa capa y repone su marco antes de poner su fondo. Lo comprobé simulando cómo AIR recorre la pantalla de zonas, zona por zona: con I38 cada una muestra su fondo. Con tu SWF del 29/09, la misma simulación muestra el bug viejo (Hew con la cárcel).
- **Los tres anillos** quedan donde los pone el juego: puerta de celda izquierda, fondo del pasillo y pared derecha (`capturas/01_zona1_prision_hd.png`).

### 2. Calidad máxima en las imágenes

**Todas las imágenes HD que tienen fuente van ahora sin pérdida** (`DefineBitsLossless2`, sin JPEG):
- **combate:** JAIL y SNOW, las dos capas;
- **zonas:** New Alcatraz, Labyrinth e Il Sanctus. Labyrinth también se rehízo con Real-ESRGAN desde tu imagen de 1672×941.

Oberursel y NULL ZONE quedan como estaban, porque no tengo su imagen original sin comprimir. Si me la pasas, la cambio.

### 3. NULL ZONE: botón «ZONAS» para probar

- **Dónde está:** arriba a la izquierda de NULL ZONE hay un botón **ZONAS**, con el panel y los botones propios de NULL ZONE.
- **Qué hace:** abre la lista de las zonas 1 a 7; eliges una y el juego te lleva ahí, por el mismo camino que el mapa del mundo. La barra de abajo y los anillos se arman como siempre.
- **Para volver a NULL ZONE:** por el mapa del mundo, como siempre.
- **Tu capa no se tocó:** el botón se agrega envolviendo `__nzZoneReady`. Primero llama a la tuya y después agrega el botón.

## Lo que sigue igual que I37

- Combate HD en New Alcatraz (edificios con el suelo) y Oberursel.
- El arreglo de «siempre CHURCH».
- La calidad del zoom.
- El zoom al 50 %.

## Probado (Ruffle, 2560×1440)

- **NULL ZONE:**
  - el botón y el panel;
  - el clic en «Zona 1» lleva a New Alcatraz HD;
  - con `__zsIr` llegué a Labyrinth, Il Sanctus y Hew, con la barra de abajo correcta en cada una.
- **Zonas:** Zona 1 HD → Hew (original) → Oberursel → Japón, sin restos de la cárcel.
- **Combates JAIL y SNOW sin pérdida:** el borde de la capa del suelo sale limpio, y la calidad queda en HIGH durante el zoom con SFX3 apagado.

Falta probarlo en tu app.

## Fuente (`fuente/`)

- **`zona1.py`:** la Zona 1 HD y la regla de la capa 26 en Hew.
- **`calidad.py`:** las imágenes sin pérdida.
- **`nz_zonas.as`:** el botón ZONAS.
- **`batalla.py`:** los combates sin pérdida.
- **`build.py`:** arma todo y da siempre el mismo SHA.
- **La herramienta Real-ESRGAN:** está en `trabajo/herramientas/esrgan_np.py`, en numpy y sin torch, con los pesos oficiales al lado.

El plan para las cinco versiones con humo de New Alcatraz está en `planes/PLAN_NEW_ALCATRAZ_HUMO.md`.
