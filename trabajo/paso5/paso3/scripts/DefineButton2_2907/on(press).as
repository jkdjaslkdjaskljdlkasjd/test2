// on(press)
// origen: boton 2907 (06596_DefineButton2_2907.bin)

if(_root.Krin.PauseForScreen != true)
{
   _root.Krin.BattlePick = 55;
   _root.Krin.progressFight = false;
   _root.gotoAndPlay("LOADBATTLESCENE");
   _root.KrinScreen._visible = false;
}
