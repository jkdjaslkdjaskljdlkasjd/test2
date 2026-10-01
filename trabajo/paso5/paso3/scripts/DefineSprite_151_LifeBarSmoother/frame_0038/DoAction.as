// DoAction
// origen: DefineSprite_151_LifeBarSmoother fotograma 38, DoAction (00301_DefineSprite_151.bin, byte 1274)

if(_parent._parent._parent._alpha > 0)
{
   _parent._parent._parent._alpha -= 5;
   this.gotoAndPlay("dead");
}
else
{
   _parent._parent._visible = false;
   removeMovieClip(this);
}
