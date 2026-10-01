// on(release)
// origen: boton 2938 (06648_DefineButton2_2938.bin)

if(_root.Krin.mouseItem == 0)
{
   if(_root.Krin.PauseForScreen != true)
   {
      KRINMENU.gotoAndStop("ach");
      KrinScreen._visible = false;
   }
}
else
{
   _root.KrinCombatText.play();
   _root.KrinCombatText.combatTexter = _root.KrinLang[_root.KLangChoosen].MENU[66];
}
