// DefineSprite_4131___Packages.mx.controls.HScrollBar
// origen: DoInitAction del sprite 4131 (03792_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.controls)
{
   _global.mx.controls = new Object();
}
if(!_global.mx.controls.HScrollBar)
{
   mx.controls.HScrollBar = _loc1_ = function()
   {
      super();
   };
   mx.controls.HScrollBar extends mx.controls.scrollClasses.ScrollBar;
   var _loc2_ = _loc1_.prototype;
   _loc2_.getMinWidth = function(Void)
   {
      return this._minHeight;
   };
   _loc2_.getMinHeight = function(Void)
   {
      return this._minWidth;
   };
   _loc2_.init = function(Void)
   {
      super.init();
      this._xscale = -100;
      this._rotation = -90;
   };
   _loc2_.__get__virtualHeight = function()
   {
      return this.__width;
   };
   _loc2_.isScrollBarKey = function(k)
   {
      if(k == 37)
      {
         this.scrollIt("Line", -1);
         return true;
      }
      else if(k == 39)
      {
         this.scrollIt("Line", 1);
         return true;
      }
      return super.isScrollBarKey(k);
   };
   _loc1_.symbolName = "HScrollBar";
   _loc1_.symbolOwner = mx.core.UIComponent;
   _loc1_.version = "2.0.2.127";
   _loc2_.className = "HScrollBar";
   _loc2_.minusMode = "Left";
   _loc2_.plusMode = "Right";
   _loc2_.minMode = "AtLeft";
   _loc2_.maxMode = "AtRight";
   _loc2_.addProperty("virtualHeight", _loc2_.__get__virtualHeight, function()
   {
   });
   ASSetPropFlags(mx.controls.HScrollBar.prototype, null, 1);
}
