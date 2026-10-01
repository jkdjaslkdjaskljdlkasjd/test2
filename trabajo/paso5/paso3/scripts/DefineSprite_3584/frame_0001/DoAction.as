// DoAction
// origen: DefineSprite_3584 fotograma 1, DoAction (07650_DefineSprite_3584.bin, byte 20)

function camControl()
{
   parentColor.setTransform(camColor.getTransform());
   var _loc3_ = sX / this._width;
   var _loc4_ = sY / this._height;
   _parent._x = cX - this._x * _loc3_;
   _parent._y = cY - this._y * _loc4_;
   _parent._xscale = 100 * _loc3_;
   _parent._yscale = 100 * _loc4_;
}
function resetStage()
{
   var _loc2_ = {ra: 100, rb: 0, ga: 100, gb: 0, ba: 100, bb: 0, aa: 100, ab: 0};
   parentColor.setTransform(_loc2_);
   _parent._xscale = 100;
   _parent._yscale = 100;
   _parent._x = 0;
   _parent._y = 0;
}
this._visible = false;
var oldMode = Stage.scaleMode;
Stage.scaleMode = "exactFit";
var cX = 266.5;
var cY = 150;
var sX = 533;
var sY = 300;
Stage.scaleMode = oldMode;
var camColor = new Color(this);
var parentColor = new Color(_parent);
this.onEnterFrame = camControl;
camControl();
this.onUnload = resetStage;
