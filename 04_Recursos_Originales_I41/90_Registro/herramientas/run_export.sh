#!/bin/bash
T=/home/claude/tools/ffdec.sh; F=/home/claude/work/src/SONNY2_I41.swf; L=/home/claude/work/full/logs; mkdir -p $L
run(){ n=$1; shift; s=$(date +%s); "$T" "$@" > $L/$n.log 2>&1; echo "$n rc=$? $(( $(date +%s)-s ))s" >> $L/_resumen.txt; }
run shape_svg -format shape:svg -export shape shape_svg $F
run shape_png -format shape:png -zoom 2 -export shape shape_png_x2 $F
run morph_svg -format morphshape:svg -export morphshape morph_svg $F
run morph_png -format morphshape:png_start_end -zoom 2 -export morphshape morph_png_x2 $F
run image_orig -format image:png_gif_jpeg_alpha -export image image_original $F
run image_png -format image:png -export image image_png $F
run sound_orig -format sound:mp3_wav -export sound sound_original $F
run sound_wav -format sound:wav -export sound sound_wav $F
run font -format font:ttf -export font font_ttf $F
run text_plain -format text:plain -export text text_plain $F
run text_fmt -format text:formatted -export text text_formatted $F
run button_png -format button:png -zoom 2 -export button button_png_x2 $F
run button_svg -format button:svg -export button button_svg $F
run sprite_svg_f1 -select all:1 -format sprite:svg -export sprite sprite_svg_f1 $F
run sprite_png_f1 -select all:1 -format sprite:png -zoom 2 -export sprite sprite_png_f1_x2 $F
run sprite_png_full -selectid $(cat /home/claude/work/inv/sprites_full.txt) -format sprite:png -zoom 2 -export sprite sprite_png_frames_x2 $F
run sprite_png_big -select $(cat /home/claude/work/inv/sprites_big_select.txt) -selectid $(cat /home/claude/work/inv/sprites_big.txt) -format sprite:png -export sprite sprite_png_muestreo_x1 $F
run frames_root -select 0:1- -format frame:png -export frame root_frames_png $F
run script_pcode -timeout 120 -format script:pcode -export script scripts_pcode $F
run symbolclass -export symbolClass symbolclass $F
echo FIN >> $L/_resumen.txt
