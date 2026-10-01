// DoAction
// origen: DefineSprite_4292 fotograma 1, DoAction (03295_DefineSprite_4292.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(822) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
