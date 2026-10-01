// DoAction
// origen: DefineSprite_4235 fotograma 1, DoAction (03238_DefineSprite_4235.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(809) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
