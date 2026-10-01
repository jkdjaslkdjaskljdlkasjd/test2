// DoAction
// origen: DefineSprite_4271 fotograma 1, DoAction (03274_DefineSprite_4271.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(815) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
