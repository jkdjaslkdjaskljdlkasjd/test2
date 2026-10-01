// DoAction
// origen: DefineSprite_4307 fotograma 1, DoAction (03310_DefineSprite_4307.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(827) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
