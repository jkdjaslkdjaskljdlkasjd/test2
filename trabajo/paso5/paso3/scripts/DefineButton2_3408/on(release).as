// on(release)
// origen: boton 3408 (07293_DefineButton2_3408.bin)

if(_root.winCondition == -1)
{
   if(_root.Krin.PauseForScreen != true)
   {
      Mouse.removeListener(someListenerKrin);
      gotoAndStop("resetHere");
      play();
   }
}
