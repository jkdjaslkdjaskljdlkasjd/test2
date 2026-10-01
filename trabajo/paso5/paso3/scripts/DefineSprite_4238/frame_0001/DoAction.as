// DoAction
// origen: DefineSprite_4238 fotograma 1, DoAction (03241_DefineSprite_4238.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(624) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
