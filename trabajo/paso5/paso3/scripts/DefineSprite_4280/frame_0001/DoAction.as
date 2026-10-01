// DoAction
// origen: DefineSprite_4280 fotograma 1, DoAction (03283_DefineSprite_4280.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(818) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
