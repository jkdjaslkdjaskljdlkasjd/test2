// on(release)
// origen: boton 2913 (06610_DefineButton2_2913.bin)

if(_root.Krin.PauseForScreen != true)
{
   _root.Krin.shopId = 0;
   KRINMENU.gotoAndStop("data");
   Krin.dataMode = "save";
   _root.krinHandleData(1);
}
