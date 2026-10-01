// DoAction
// origen: DefineSprite_4253 fotograma 1, DoAction (03256_DefineSprite_4253.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(808) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
