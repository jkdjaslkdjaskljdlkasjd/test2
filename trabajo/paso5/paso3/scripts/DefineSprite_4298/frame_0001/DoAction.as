// DoAction
// origen: DefineSprite_4298 fotograma 1, DoAction (03301_DefineSprite_4298.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(824) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
