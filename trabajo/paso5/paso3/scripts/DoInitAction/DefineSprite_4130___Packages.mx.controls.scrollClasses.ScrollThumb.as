// DefineSprite_4130___Packages.mx.controls.scrollClasses.ScrollThumb
// origen: DoInitAction del sprite 4130 (03789_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.controls)
{
   _global.mx.controls = new Object();
}
if(!_global.mx.controls.scrollClasses)
{
   _global.mx.controls.scrollClasses = new Object();
}
if(!_global.mx.controls.scrollClasses.ScrollThumb)
{
   mx.controls.scrollClasses.ScrollThumb = _loc1_ = function()
   {
      super();
   };
   mx.controls.scrollClasses.ScrollThumb extends mx.skins.CustomBorder;
   var _loc2_ = _loc1_.prototype;
   _loc2_.createChildren = function(Void)
   {
      super.createChildren();
      this.useHandCursor = false;
   };
   _loc2_.setRange = function(_ymin, _ymax, _datamin, _datamax)
   {
      this.ymin = _ymin;
      this.ymax = _ymax;
      this.datamin = _datamin;
      this.datamax = _datamax;
   };
   _loc2_.dragThumb = function(Void)
   {
      this.scrollMove = this._ymouse - this.lastY;
      this.scrollMove += this._y;
      if(this.scrollMove < this.ymin)
      {
         this.scrollMove = this.ymin;
      }
      else if(this.scrollMove > this.ymax)
      {
         this.scrollMove = this.ymax;
      }
      this._parent.isScrolling = true;
      this._y = this.scrollMove;
      var _loc2_ = Math.round((this.datamax - this.datamin) * (this._y - this.ymin) / (this.ymax - this.ymin)) + this.datamin;
      this._parent.scrollPosition = _loc2_;
      this._parent.dispatchScrollEvent("ThumbTrack");
      updateAfterEvent();
   };
   _loc2_.stopDragThumb = function(Void)
   {
      this._parent.isScrolling = false;
      this._parent.dispatchScrollEvent("ThumbPosition");
      this._parent.dispatchScrollChangedEvent();
      delete this.onMouseMove;
   };
   _loc2_.onPress = function(Void)
   {
      this._parent.pressFocus();
      this.lastY = this._ymouse;
      this.onMouseMove = this.dragThumb;
      super.onPress();
   };
   _loc2_.onRelease = function(Void)
   {
      this._parent.releaseFocus();
      this.stopDragThumb();
      super.onRelease();
   };
   _loc2_.onReleaseOutside = function(Void)
   {
      this._parent.releaseFocus();
      this.stopDragThumb();
      super.onReleaseOutside();
   };
   _loc2_.draw = function()
   {
      super.draw();
      if(this.grip_mc == undefined)
      {
         this.setSkin(3, this.gripSkin);
      }
   };
   _loc2_.size = function()
   {
      super.size();
      this.grip_mc.move((this.__get__width() - this.grip_mc.width) / 2, (this.__get__height() - this.grip_mc.height) / 2);
   };
   _loc1_.symbolOwner = mx.skins.CustomBorder.symbolOwner;
   _loc2_.className = "ScrollThumb";
   _loc2_.btnOffset = 0;
   _loc2_.horizontal = false;
   _loc2_.idNames = new Array("l_mc", "m_mc", "r_mc", "grip_mc");
   ASSetPropFlags(mx.controls.scrollClasses.ScrollThumb.prototype, null, 1);
}
