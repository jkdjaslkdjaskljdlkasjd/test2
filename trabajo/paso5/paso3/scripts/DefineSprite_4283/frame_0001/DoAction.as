// DoAction
// origen: DefineSprite_4283 fotograma 1, DoAction (03286_DefineSprite_4283.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(819) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
