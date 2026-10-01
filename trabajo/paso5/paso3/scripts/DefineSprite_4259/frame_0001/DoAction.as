// DoAction
// origen: DefineSprite_4259 fotograma 1, DoAction (03262_DefineSprite_4259.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(811) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
