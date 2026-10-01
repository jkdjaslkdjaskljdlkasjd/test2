#!/bin/sh
# Prepara las carpetas de trabajo que usan los build.py (no se suben: ver .gitignore).
#   act1  = SONNY2.swf del usuario del 29/09 (I30) separado con swfsplit   (bca5eea5...)
#   act3  = act1 descompilado con swfcode
#   base1 = juego base del paso 5, recompilado (f6a98433...), separado con swfsplit
# Uso:  cd trabajo && sh preparar.sh
#       python3 i35/build.py SONNY2_I35.swf      (sale 5d5a9beb...576e)
set -e
cd "$(dirname "$0")"
python3 paso5/tools/swfsplit.py bases/SONNY2_29-09.swf act1
python3 paso5/tools/swfcode.py act1 act3
python3 paso5/tools/swfsplit.py paso5/SONNY2_recompilado.swf base1
# las imagenes ya preparadas estan en i31/build/ e i35/build/ (imagenes.py las regenera desde fuente/imagenes)
