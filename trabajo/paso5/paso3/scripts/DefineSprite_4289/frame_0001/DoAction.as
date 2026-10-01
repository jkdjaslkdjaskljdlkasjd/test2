// DoAction
// origen: DefineSprite_4289 fotograma 1, DoAction (03292_DefineSprite_4289.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(821) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
