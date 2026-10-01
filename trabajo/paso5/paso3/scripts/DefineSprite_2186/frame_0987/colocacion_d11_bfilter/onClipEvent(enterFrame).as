// onClipEvent(enterFrame)
// origen: DefineSprite_2186 fotograma 987, clip en profundidad 11 (03320_DefineSprite_2186.bin, byte 14203)

var n = this._parent;
if(_root.__v9Tree && n._parent && n._parent._parent == _root.__v9Tree)
{
   if(this.hitTest(_root._xmouse, _root._ymouse))
   {
      _root.__handoffReleaseCustom();
   }
}
else if(this.hitTest(_root._xmouse, _root._ymouse))
{
   var id = _root.__uiFrameIds[n._currentframe];
   var d = _root.__v10ById[id];
   if(d)
   {
      _root.__handoffReleaseCustom();
      var r = Math.max(1, _root.__v55Rank(id));
      var a = _root["KRINABILITY" + id];
      var b = _root["KRINABILITYB" + id];
      n.toolTipTitle = d.name;
      n.toolTip = _root.__v55Desc(id, r);
      if(b && typeof b[18] == "string")
      {
         n.toolTip3 = b[18];
      }
      else if(a)
      {
         n.toolTip3 = !d.passive ? "Costs " + a[5] + " Focus. Cooldown: " + a[7] + " turns." : "Passive Combat Effect";
      }
      n.chimney = false;
   }
}
if(this.hitTest(_root._xmouse, _root._ymouse))
{
   if(_parent._parent._visible && !_parent.zero)
   {
      if(_parent.chimney)
      {
         _root.KrinToolTipper.tt = _parent.toolTipTitle;
         _root.KrinToolTipper.t = _parent.toolTip;
         _root.KrinToolTipper.gotoAndPlay("GO");
      }
      else
      {
         _root.KrinToolTipper.tt = _parent.toolTipTitle;
         _root.KrinToolTipper.t = _parent.toolTip;
         _root.KrinToolTipper.t3 = _parent.toolTip3;
         if(hitter == 5)
         {
            if(_parent._parent.OKAY == true)
            {
               _root.KrinToolTipper.tyut = _parent.toolTip4;
               _root.KrinToolTipper.gotoAndPlay("GO7");
            }
            else
            {
               _root.KrinToolTipper.gotoAndPlay("GO2");
            }
         }
         else
         {
            hitter++;
            _root.KrinToolTipper.gotoAndPlay("GO3");
         }
      }
   }
}
else
{
   hitter = 0;
}
