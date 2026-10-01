// on(press)
// origen: boton 3296 (07100_DefineButton2_3296.bin)

_root.loadPvPCode(navText2, _root.playerToLoadforPvP);
if(_root.PvP_LOAD_SUCCESS)
{
   this.gotoAndStop("START");
   _visible = false;
   _root.PvPCodeLode = false;
   _root.refreshArenaUI();
   navText2 = "";
}
else
{
   navText2 = _root.KrinLang[_root.KLangChoosen].MENU[71];
}
