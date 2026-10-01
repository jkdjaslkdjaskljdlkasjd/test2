// DoAction
// origen: DefineSprite_4265 fotograma 1, DoAction (03268_DefineSprite_4265.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(813) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
