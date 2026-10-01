// on(release)
// origen: boton 3283 (07085_DefineButton2_3283.bin)

if(!PvPCodeLode)
{
   exportPvPCode(2);
   krinNavFadeSpeech.gotoAndStop("START");
   krinNavFadeSpeech._visible = true;
   krinNavFadeSpeech.navText = exportPvPArray;
   krinNavFadeSpeech.naxTevt.selectable = true;
   PvPCodeLode = true;
}
