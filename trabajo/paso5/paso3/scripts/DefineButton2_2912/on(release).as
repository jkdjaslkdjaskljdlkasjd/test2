// on(release)
// origen: boton 2912 (06608_DefineButton2_2912.bin)

if(_root.Krin.mouseItem == 0)
{
   if(_root.Krin.PauseForScreen != true)
   {
      _root.Krin.dataMode = "save";
      _root.krinHandleData(_root.Krin.slotInUse);
      trace(_root.Krin.slotInUse);
      _root.krinNavHideUI(0);
   }
}
else
{
   _root.KrinCombatText.play();
   _root.KrinCombatText.combatTexter = _root.KrinLang[_root.KLangChoosen].MENU[66];
}
