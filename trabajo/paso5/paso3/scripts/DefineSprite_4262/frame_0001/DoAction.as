// DoAction
// origen: DefineSprite_4262 fotograma 1, DoAction (03265_DefineSprite_4262.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(812) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
