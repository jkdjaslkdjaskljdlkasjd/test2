// DoAction
// origen: DefineSprite_4313 fotograma 1, DoAction (03316_DefineSprite_4313.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(829) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
