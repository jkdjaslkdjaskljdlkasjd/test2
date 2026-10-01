// DoAction
// origen: DefineSprite_4304 fotograma 1, DoAction (03307_DefineSprite_4304.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(826) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
