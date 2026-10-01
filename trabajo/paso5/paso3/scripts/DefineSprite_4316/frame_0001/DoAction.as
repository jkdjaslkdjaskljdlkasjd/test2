// DoAction
// origen: DefineSprite_4316 fotograma 1, DoAction (03319_DefineSprite_4316.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(830) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
