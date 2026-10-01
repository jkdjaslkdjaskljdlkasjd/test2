// DoAction
// origen: DefineSprite_4295 fotograma 1, DoAction (03298_DefineSprite_4295.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(823) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
