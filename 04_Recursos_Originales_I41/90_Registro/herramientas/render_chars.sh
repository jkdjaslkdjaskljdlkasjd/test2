#!/bin/bash
# Para cada apariencia: SWF de reconstrucción + render JPEXS del primer fotograma de cada etiqueta (PNG x2)
# y fotograma 1 en SVG. uso: render_chars.sh specs_dir out_dir
SPECS=$1; OUT=$2; T=/home/claude/tools/ffdec.sh; F=/home/claude/work/src/SONNY2_I41.swf; INV=/home/claude/work/inv/inventory.json
mkdir -p $OUT
for s in $SPECS/AP*.json; do
  n=$(basename $s .json); d=$OUT/$n; mkdir -p $d
  [ -f $d/done ] && continue
  python3 -I /home/claude/work/scripts/build_assembly.py $F $INV $s $d/$n.swf $d/informe_ensamblaje.json > $d/build.log 2>&1 || { echo "$n BUILD_FAIL" >> $OUT/_errores.txt; continue; }
  RID=$(python3 -I -c "import json;print(json.load(open('$d/informe_ensamblaje.json'))['model_reconstruido_id'])")
  FR=$(python3 -I -c "
import json
C=json.load(open('$INV'))['characters']; r=json.load(open('$d/informe_ensamblaje.json'))
m=C[str(r['model_id_original'])]; fr=sorted({1}|{l['f'] for l in m['labels']}); print(','.join(map(str,fr)))")
  $T -select $RID:$FR -selectid $RID -format sprite:png -zoom 2 -export sprite $d/poses_png_x2 $d/$n.swf > $d/render.log 2>&1
  $T -select $RID:1 -selectid $RID -format sprite:svg -export sprite $d/f1_svg $d/$n.swf >> $d/render.log 2>&1
  echo "$FR" > $d/fotogramas_poses.txt
  touch $d/done
done
echo FIN >> $OUT/_errores.txt
