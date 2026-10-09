# Sonny 2 a 16:9: I41 (nueva New Alcatraz HD)

| Archivo | SHA-256 |
|---|---|
| `SONNY2.swf` (I41) | `6b26ee6d5b1005a15824d10864941cee452072ef1942880aeb65fa6917738812` |
| Base: I40 | `0142abdd7da0e1c424508e86da123a5820d553fb0b76026dd41608d3fc92ed64` |

**Cómo instalarlo:** descarga `i41/SONNY2.swf` (42,2 MB) y usa `instalador/INSTALAR.bat`. El SHA que muestra al final tiene que empezar con `6b26ee6d`.

## Qué cambia

**La pantalla de la Zona 1 (New Alcatraz) usa la imagen nueva del usuario (v2, 02/10):**
- ampliada con Real-ESRGAN `realesr-animevideov3` a 2560×1440;
- guardada en JPEG 97 4:4:4;
- en la repo: `fondos_hd/world_map/PRISON_Z1.png` (1672×941) y `PRISON_Z1_2560x1440.png`;
- la anterior quedó como `PRISON_Z1_v1*.png`.

Todo lo demás sigue igual que I40.

## Probado

- **Regla de la capa 26:** `simular_2908.py` da bien todas las zonas.
- **Ruffle:** Zona 1 con la imagen nueva, y Hew después con su fondo (`capturas/`).
