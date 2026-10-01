// DoAction
// origen: DefineSprite_4310 fotograma 1, DoAction (03313_DefineSprite_4310.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(828) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
