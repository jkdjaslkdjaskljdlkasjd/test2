// on(press)
// origen: boton 2904 (06593_DefineButton2_2904.bin)

if(_root.Krin.PauseForScreen != true)
{
   _root.Krin.BattlePick = 52;
   _root.Krin.progressFight = false;
   _root.gotoAndPlay("LOADBATTLESCENE");
   _root.KrinScreen._visible = false;
}
