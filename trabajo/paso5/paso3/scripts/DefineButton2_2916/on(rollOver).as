// on(rollOver)
// origen: boton 2916 (06616_DefineButton2_2916.bin)

ui_but5.gotoAndPlay("START");
_root.thereIsASlotSelected = true;
_root.KrinToolTipper.colorChange = "Common";
_root.krinChangeColor(_root.KrinToolTipper.fontBacker2, _root.KrinToolTipper.colorChange);
_root.KrinToolTipper.tt = _root.KrinLang[KLangChoosen].SYSTEM[32] + ": €" + Math.round(0.7000000000000001 * _root.respecValue(Krin.Level));
_root.KrinToolTipper.t = _root.KrinLang[KLangChoosen].SYSTEM[33];
_root.KrinToolTipper.gotoAndStop("GO");
