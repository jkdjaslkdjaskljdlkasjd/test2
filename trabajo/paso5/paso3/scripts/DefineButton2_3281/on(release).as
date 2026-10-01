// on(release)
// origen: boton 3281 (07081_DefineButton2_3281.bin)

if(!PvPCodeLode)
{
   exportPvPCode(1);
   krinNavFadeSpeech.gotoAndStop("START");
   krinNavFadeSpeech._visible = true;
   krinNavFadeSpeech.navText = exportPvPArray;
   krinNavFadeSpeech.naxTevt.selectable = true;
   PvPCodeLode = true;
}
