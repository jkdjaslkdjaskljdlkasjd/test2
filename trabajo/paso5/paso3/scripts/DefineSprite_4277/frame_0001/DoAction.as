// DoAction
// origen: DefineSprite_4277 fotograma 1, DoAction (03280_DefineSprite_4277.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(817) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
