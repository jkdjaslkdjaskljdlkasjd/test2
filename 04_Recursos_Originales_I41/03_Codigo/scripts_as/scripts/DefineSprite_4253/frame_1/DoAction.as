this.onEnterFrame = function()
{
   var target = _root.__i18Mastered(808) ? 2 : 1;
   if(this._currentframe != target)
   {
      this.gotoAndStop(target);
   }
};
this.stop();
this.onEnterFrame();
