// DoAction
// origen: DefineSprite_4274 fotograma 1, DoAction (03277_DefineSprite_4274.bin, byte 22)

this.onEnterFrame = function()
{
   var target = !_root.__i18Mastered(816) ? 1 : 2;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
