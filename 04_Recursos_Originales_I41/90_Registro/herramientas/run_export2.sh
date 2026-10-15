#!/bin/bash
T=/home/claude/tools/ffdec.sh; F=/home/claude/work/src/SONNY2_I41.swf; L=/home/claude/work/full/logs
run(){ n=$1; shift; s=$(date +%s); "$T" "$@" > $L/$n.log 2>&1; echo "$n rc=$? $(( $(date +%s)-s ))s" >> $L/_resumen.txt; }
while ! grep -q FIN $L/_resumen.txt; do sleep 10; done
run morph_png_retry -onerror ignore -format morphshape:png_start_end -zoom 2 -export morphshape morph_png_x2 $F
run sprite_svg_f1_retry -onerror ignore -select $(cat /home/claude/work/inv/sprites_all_f1_select.txt) -selectid $(cat /home/claude/work/inv/sprites_all.txt) -format sprite:svg -export sprite sprite_svg_f1 $F
run sprite_png_f1_retry -onerror ignore -select $(cat /home/claude/work/inv/sprites_all_f1_select.txt) -selectid $(cat /home/claude/work/inv/sprites_all.txt) -format sprite:png -zoom 2 -export sprite sprite_png_f1_x2 $F
echo FIN2 >> $L/_resumen.txt
bash /home/claude/work/scripts/render_chars.sh /home/claude/work/chars/specs /home/claude/work/chars/render > /home/claude/work/chars/render.out 2>&1
echo FIN3 >> $L/_resumen.txt
