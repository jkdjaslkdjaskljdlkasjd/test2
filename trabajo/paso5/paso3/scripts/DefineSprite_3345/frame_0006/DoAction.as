// DoAction
// origen: DefineSprite_3345 fotograma 6, DoAction (07203_DefineSprite_3345.bin, byte 1364)

zoomPauseCounter++;
if(_root.KrinSettings.SFX3 == false)
{
   _root._quality = _root.KrinSettings.QUALITY;
}
if(zoomPauseCounter == _root.zoomPause)
{
   gotoAndStop("KrinZoomPlay");
   play();
   if(_root.KrinSettings.SFX3 == false)
   {
      _root._quality = "LOW";
   }
}
else
{
   gotoAndStop("KrinZoomPause");
   play();
}
