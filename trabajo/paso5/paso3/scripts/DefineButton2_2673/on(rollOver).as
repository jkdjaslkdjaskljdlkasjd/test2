// on(rollOver)
// origen: boton 2673 (06053_DefineButton2_2673.bin)

if(_root.Krin.dataMode == "save")
{
   _root.thereIsASlotSelected = true;
   _root.KrinToolTipper.tt = _root.KrinLang[KLangChoosen].MENU[21];
   _root.KrinToolTipper.t = _root.KrinLang[KLangChoosen].MENU[25];
   _root.KrinToolTipper.gotoAndStop("GO");
}
