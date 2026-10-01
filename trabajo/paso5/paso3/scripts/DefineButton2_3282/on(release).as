// on(release)
// origen: boton 3282 (07083_DefineButton2_3282.bin)

if(!PvPCodeLode)
{
   _root.playerToLoadforPvP = 1;
   krinNavFadeSpeech.gotoAndStop("LOAD");
   krinNavFadeSpeech._visible = true;
   krinNavFadeSpeech.naxTevt2.selectable = true;
   PvPCodeLode = true;
}
