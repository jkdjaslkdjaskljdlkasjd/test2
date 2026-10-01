// on(press)
// origen: boton 2906 (06595_DefineButton2_2906.bin)

if(_root.Krin.PauseForScreen != true)
{
   _root.Krin.BattlePick = 54;
   _root.Krin.progressFight = false;
   _root.gotoAndPlay("LOADBATTLESCENE");
   _root.KrinScreen._visible = false;
}
