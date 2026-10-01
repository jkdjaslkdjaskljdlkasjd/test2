// DoAction
// origen: DefineSprite_4268 fotograma 1, DoAction (03271_DefineSprite_4268.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(814) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
