// on(release)
// origen: boton 2911 (06606_DefineButton2_2911.bin)

if(_root.Krin.mouseItem == 0)
{
   if(_root.Krin.PauseForScreen != true)
   {
      KRINMENU.gotoAndStop("skills");
      KrinScreen._visible = false;
   }
}
else
{
   _root.KrinCombatText.play();
   _root.KrinCombatText.combatTexter = _root.KrinLang[_root.KLangChoosen].MENU[66];
}
