// on(rollOver)
// origen: boton 2672 (06051_DefineButton2_2672.bin)

if(_root.Krin.dataMode == "save")
{
   _root.thereIsASlotSelected = true;
   _root.KrinToolTipper.tt = _root.KrinLang[KLangChoosen].MENU[21];
   _root.KrinToolTipper.t = _root.KrinLang[KLangChoosen].MENU[25];
   _root.KrinToolTipper.gotoAndStop("GO");
}
