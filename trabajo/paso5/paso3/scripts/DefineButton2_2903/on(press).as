// on(press)
// origen: boton 2903 (06592_DefineButton2_2903.bin)

if(_root.Krin.PauseForScreen != true)
{
   _root.Krin.BattlePick = 51;
   _root.Krin.progressFight = false;
   _root.gotoAndPlay("LOADBATTLESCENE");
   _root.KrinScreen._visible = false;
}
