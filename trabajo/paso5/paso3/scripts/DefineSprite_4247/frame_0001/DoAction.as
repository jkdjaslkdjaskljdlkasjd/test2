// DoAction
// origen: DefineSprite_4247 fotograma 1, DoAction (03250_DefineSprite_4247.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(627) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
