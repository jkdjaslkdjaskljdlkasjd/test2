// on(release)
// origen: boton 3284 (07087_DefineButton2_3284.bin)

if(!PvPCodeLode)
{
   _root.playerToLoadforPvP = 2;
   krinNavFadeSpeech.gotoAndStop("LOAD");
   krinNavFadeSpeech._visible = true;
   krinNavFadeSpeech.naxTevt2.selectable = true;
   PvPCodeLode = true;
}
