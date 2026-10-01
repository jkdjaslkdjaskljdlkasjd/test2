// DoAction
// origen: DefineSprite_4244 fotograma 1, DoAction (03247_DefineSprite_4244.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(626) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
