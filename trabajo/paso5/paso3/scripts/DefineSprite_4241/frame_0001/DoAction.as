// DoAction
// origen: DefineSprite_4241 fotograma 1, DoAction (03244_DefineSprite_4241.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(625) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
