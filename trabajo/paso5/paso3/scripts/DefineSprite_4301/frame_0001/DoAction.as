// DoAction
// origen: DefineSprite_4301 fotograma 1, DoAction (03304_DefineSprite_4301.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(825) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
