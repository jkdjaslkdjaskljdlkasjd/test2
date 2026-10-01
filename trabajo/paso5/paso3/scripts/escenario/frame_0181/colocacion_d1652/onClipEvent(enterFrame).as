// onClipEvent(enterFrame)
// origen: escenario fotograma 181, clip en profundidad 1652 (06982_PlaceObject2.bin)

if(frameGo == undefined)
{
   if(_alpha > 0)
   {
      _alpha -= 15;
   }
}
else if(_alpha < 100)
{
   _alpha += 15;
}
else
{
   _root.gotoAndStop(frameGo);
}
