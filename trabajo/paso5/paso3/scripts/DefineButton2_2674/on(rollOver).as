// on(rollOver)
// origen: boton 2674 (06055_DefineButton2_2674.bin)

if(_root.Krin.dataMode == "save")
{
   _root.thereIsASlotSelected = true;
   _root.KrinToolTipper.tt = _root.KrinLang[KLangChoosen].MENU[21];
   _root.KrinToolTipper.t = _root.KrinLang[KLangChoosen].MENU[25];
   _root.KrinToolTipper.gotoAndStop("GO");
}
