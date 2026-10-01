// DoAction
// origen: DefineSprite_4250 fotograma 1, DoAction (03253_DefineSprite_4250.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(628) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
