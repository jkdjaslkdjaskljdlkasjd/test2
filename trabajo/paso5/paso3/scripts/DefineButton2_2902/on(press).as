// on(press)
// origen: boton 2902 (06591_DefineButton2_2902.bin)

if(_root.Krin.PauseForScreen != true)
{
   _root.Krin.BattlePick = 50;
   _root.Krin.progressFight = false;
   _root.gotoAndPlay("LOADBATTLESCENE");
   _root.KrinScreen._visible = false;
}
