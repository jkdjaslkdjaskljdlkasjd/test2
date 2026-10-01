// DoAction
// origen: DefineSprite_4256 fotograma 1, DoAction (03259_DefineSprite_4256.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(810) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
