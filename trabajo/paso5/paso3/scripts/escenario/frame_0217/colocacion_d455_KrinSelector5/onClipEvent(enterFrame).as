// onClipEvent(enterFrame)
// origen: escenario fotograma 217, clip en profundidad 455 (07245_PlaceObject3.bin)

if(this.hitter.hitTest(_root._xmouse, _root._ymouse))
{
   if(_alpha < 100 && _root.InBattle == false)
   {
      _alpha += 20;
   }
   _root.hitTarget[4] = 1;
   _root.HTX = _x;
   _root.HTY = _y;
}
else
{
   if(_alpha > 0)
   {
      _alpha -= 5;
   }
   _root.hitTarget[4] = 0;
}
