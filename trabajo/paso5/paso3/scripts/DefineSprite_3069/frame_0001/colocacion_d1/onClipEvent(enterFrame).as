// onClipEvent(enterFrame)
// origen: DefineSprite_3069 fotograma 1, clip en profundidad 1 (06785_DefineSprite_3069.bin, byte 20)

if(this.hitTest(_root._xmouse, _root._ymouse))
{
   _root.KrinToolTipper.colorChange = "Common";
   _root.krinChangeColor(_root.KrinToolTipper.fontBacker2, _root.KrinToolTipper.colorChange);
   _root.KrinToolTipper.gotoAndPlay("GO");
   _root.KrinToolTipper.tt = _parent.toolTipTitle;
   _root.KrinToolTipper.t = _parent.toolTip;
}
