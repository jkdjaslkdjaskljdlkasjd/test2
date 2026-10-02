# Plan: cinco versiones de New Alcatraz centradas en el humo

Pantalla de zona de la **Zona 1, New Alcatraz: The Iron Prison** (la etiqueta `PRISON` de `KrinScreen`). No es un fondo de combate.

**Reparto:**
- **ChatGPT:** genera las imágenes.
- **Claude:** las compone, las amplía, las mete en el juego y las prueba.
- **Usuario:** elige.

## 1. Lo que quiere el usuario (decidido en las conversaciones)

- **Que parezca del Sonny 2 original, solo que limpio a 2K.** El usuario dijo que lo HD «se ve raro comparado con el juego original». Por eso: formas planas, bordes nítidos y bandas de humo planas y translúcidas. Nada de óleo, acuarela, anime, fotorrealismo, borroso ni pixelado.
- **Se cambia poco y por zonas.** Las paredes, las celdas, el piso, los focos y la perspectiva ya están aprobados. En esta tanda solo cambian el cielo, el humo, la bruma y la luz del fondo.
- **Calidad máxima:**
  - PNG sin pérdida en todo el camino;
  - nada de JPEG ni de capturas;
  - nada de archivos subidos al chat de Claude, que comprime y tiene un límite de 30 MB. Todo va por GitHub.
- **Modo plan:** antes de generar, ChatGPT hace las preguntas de la sección 6 y espera las respuestas.
- **Se trabaja de a poco:** una versión por vez; después de cada una, el usuario opina.

## 2. Base y referencias

**La base** es la imagen que el usuario eligió el 01/10 y que ya está en el juego como prueba (I38):

| Archivo | Uso |
|---|---|
| `fondos_hd/world_map/PRISON_Z1.png` | La imagen tal como vino, de 1672×941. **Es la base para generar** |
| `fondos_hd/world_map/PRISON_Z1_2560x1440.png` | La misma, ampliada como la usa el juego. **Es la base para componer** |

En esta base la luna es naranja y el farol redondo de la fortaleza ya es amarillo.

**Referencias:**
- **El arte original del juego** (bitmap 2803, de 764×414) es el ADN del estilo:
  - siluetas de bloques simples;
  - cielo negro con estrellas;
  - bandas de humo planas;
  - dos columnas de humo verde-amarillo a la derecha;
  - el disco detrás de la fortaleza.
- **La captura de referencia del humo** (la del juego con la HUD): se usa solo para el **humo orgánico y la atmósfera**. No se copia nada de su HUD, ni anillos, ni texto.

## 3. Qué no se toca (zonas protegidas)

Las coordenadas son sobre el lienzo de 1672×941.

**Se queda igual que en la base, píxel por píxel después de componer:**
- las dos paredes de celdas, con su dibujo;
- las puertas y los barrotes;
- las cajas de luz fluorescente;
- las torres de los focos y sus lámparas;
- los **conos de luz amarilla** y los **charcos de luz** del piso;
- el piso y sus reflejos;
- la sangre, el alambre de púas y el farol de la derecha;
- la perspectiva y el punto de fuga;
- **la fortaleza.**

**Zonas del juego, que deben quedar libres y legibles:**
- **Los tres anillos** que dibuja el juego:
  - cian en la puerta de celda izquierda, cerca de (381, 516);
  - rojo al fondo del pasillo, cerca de (979, 411);
  - amarillo en la pared derecha, cerca de (1217, 453).
  - No hay que pintarlos ni poner nada fuerte en esos lugares.
- **La barra de navegación de abajo** (al 62 %, centrada): cubre aproximadamente x 330–1345, y 800–910. Se pinta, pero ahí no va nada importante.

## 4. Los cinco colores y las cinco versiones

**En las cinco versiones:**
- la **luna pasa a roja**. Se recolorea con una máscara local que mantiene su forma, su borde y su textura;
- el **farol redondo de la fortaleza queda amarillo** (ya lo es en la base);
- la **ciudad conserva su altura** y queda en parte velada por la bruma, sin perder la silueta de bloques.

| # | Versión | Qué cambia | Cuánto |
|---|---|---|---|
| 1 | **Mínima** | Los dos colores, el humo actual más nítido y una bruma leve | La más cercana a la base. Es la versión de control |
| 2 | **Conservadora** | Remolinos y estelas de humo como en la referencia, nítidos y contenidos | La ciudad se sigue reconociendo entera |
| 3 | **Bruma esmeralda** | Capas de niebla verde azulada cruzan la silueta urbana | Los edificios aparecen por tramos; la fortaleza queda despejada |
| 4 | **Corrientes de humo** | Las dos columnas de la derecha se estiran en estelas diagonales por el cielo | Solo rozan el borde de la luna; no la tapan |
| 5 | **Tormenta sobre la prisión** | Un techo de humo irregular, con aberturas oscuras alrededor de la luna roja | La fortaleza y su farol amarillo quedan despejados |

**El humo, en todas:**
- bandas planas y translúcidas con bordes definidos, como en el juego original;
- verde-amarillo y verde azulado;
- sin degradés de humo fotográfico ni pinceladas.

## 5. Cómo se produce (pasos y quién hace cada uno)

1. **ChatGPT, en modo plan:** hace las preguntas de la sección 6 y escribe un plan corto por versión: qué cambia y dónde, en píxeles del lienzo de 1672×941. Espera el «ok».
2. **ChatGPT genera una versión por vez:**
   - a partir de `PRISON_Z1.png`;
   - editando **solo el cielo y el fondo** (con máscara, si la herramienta lo permite);
   - salida en PNG opaco, sRGB, al tamaño más grande que dé, en 16:9.
3. **El usuario la sube a la repo**, en `fondos_hd/world_map/new_alcatraz_humo/` y sin comprimir, con el nombre `PRISON_Z1_v1_minima.png`, `…_v2_conservadora.png`, etc. No hace falta subirla al chat.
4. **Claude compone y amplía:**
   - **Ampliación:** toma la versión y la amplía ×4 con **Real-ESRGAN `realesr-animevideov3`**, con los pesos oficiales. Usa `trabajo/herramientas/esrgan_np.py`: numpy en precisión completa, por bloques solapados, **sin uniones**, comprobado. Después la baja con Lanczos a 2560×1440.
   - **Composición:** pega **solo la zona nueva** (cielo, humo, bruma, luna) sobre `PRISON_Z1_2560x1440.png`, con una máscara de borde suave. Todo lo protegido de la sección 3 queda **idéntico píxel por píxel** a la base.
   - **Luna:** la recolorea a rojo con una máscara local, si la versión no la trajo roja.
5. **Claude la prueba en el juego:**
   - la mete en `KrinScreen` (Zona 1), como `zona1.py` en I38, **sin pérdida** (`DefineBitsLossless2`);
   - la prueba en Ruffle, y el usuario en su app. Para eso está el botón **ZONAS** de NULL ZONE, que lleva directo a la Zona 1.

## 6. Preguntas que ChatGPT tiene que hacer antes de generar (en español, todas juntas, con 2–3 opciones y una recomendada)

1. ¿Tu herramienta puede editar solo una zona con máscara, o regenera la imagen entera? Si la regenera, Claude compone igual, pero conviene saberlo.
2. **Luna roja:**
   - (a) rojo intenso, como la luna del pueblo de nieve;
   - (b) rojo oscuro, casi granate;
   - (c) rojo anaranjado (lo mínimo).
3. **Bruma sobre la ciudad:**
   - (a) leve, en todas las versiones;
   - (b) solo desde la versión 3;
   - (c) ninguna en la versión 1.
4. **Estrellas:**
   - (a) las de la base;
   - (b) menos, tapadas por el humo;
   - (c) más, en las aberturas del humo.
5. **Grano de papel:**
   - (a) como el original;
   - (b) como el pueblo de nieve;
   - (c) casi nada.
6. ¿Hago las cinco o alguna primero? Recomendado: la 1 y después la que elijas.

## 7. Entrega y control

**Qué se entrega, todo en la repo (`fondos_hd/world_map/new_alcatraz_humo/`) y nunca en el chat:**
- cada versión en PNG opaco sRGB a **2560×1440** y a **1673×941**, es decir, diez PNG;
- una **comparativa aparte**, con las cinco junto a la base.

**Qué revisa Claude en cada versión:**
- **A la vista:** a los dos tamaños, que parezca del juego original.
- **Por píxeles:** que las zonas protegidas no cambiaron (diferencia 0 contra la base).
- **Uniones:** que no hay uniones del escalado ni del pegado.
- **Contenido:** que no aparecen HUD, texto, personajes ni anillos pintados.
- **En el juego:** con el botón **ZONAS** → Zona 1, que los tres anillos se leen bien.

**Cómo se decide:** el usuario elige una; esa queda como `PRISON_Z1` definitiva en el SWF. Las otras se guardan en la carpeta.
