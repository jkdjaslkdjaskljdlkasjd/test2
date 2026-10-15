zoomPointX = (_root.zoomPointX - _root.BATTLESCREEN.saverX) / zoomFactor;
zoomPointY = (_root.zoomPointY - _root.BATTLESCREEN.saverY) / zoomFactor;
zoomScaleX = scaleChange / zoomFactor;
zoomScaleY = scaleChange / zoomFactor;
zoomPoint = zoomTime;
zoomReverse = 1;
if(_root.KrinSettings.SFX2)
{
   _root.BATTLEBLUR.gotoAndPlay(2);
}
if(_root.KrinSettings.SFX3 == false)
{
   _root._quality = "LOW";
}
if(_root.__hdBattleOn == true && _root.__hdZoomF != undefined)
{
   zoomPointX *= _root.__hdZoomF;
   zoomPointY *= _root.__hdZoomF;
   zoomScaleX *= _root.__hdZoomF;
   zoomScaleY *= _root.__hdZoomF;
}
if(_root.__hdBattleOn == true && _root.KrinSettings.SFX3 == false)
{
   _root._quality = _root.KrinSettings.QUALITY;
}
