// DoAction
// origen: DefineSprite_4286 fotograma 1, DoAction (03289_DefineSprite_4286.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(820) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
