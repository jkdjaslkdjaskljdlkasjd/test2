// DefineSprite_4132___Packages.mx.controls.VScrollBar
// origen: DoInitAction del sprite 4132 (03795_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.controls)
{
   _global.mx.controls = new Object();
}
if(!_global.mx.controls.VScrollBar)
{
   mx.controls.VScrollBar = _loc1_ = function()
   {
      super();
   };
   mx.controls.VScrollBar extends mx.controls.scrollClasses.ScrollBar;
   var _loc2_ = _loc1_.prototype;
   _loc2_.init = function(Void)
   {
      super.init();
   };
   _loc2_.isScrollBarKey = function(k)
   {
      if(k == 38)
      {
         this.scrollIt("Line", -1);
         return true;
      }
      else if(k == 40)
      {
         this.scrollIt("Line", 1);
         return true;
      }
      else if(k == 33)
      {
         this.scrollIt("Page", -1);
         return true;
      }
      else if(k == 34)
      {
         this.scrollIt("Page", 1);
         return true;
      }
      return super.isScrollBarKey(k);
   };
   _loc1_.symbolName = "VScrollBar";
   _loc1_.symbolOwner = mx.core.UIComponent;
   _loc1_.version = "2.0.2.127";
   _loc2_.className = "VScrollBar";
   _loc2_.minusMode = "Up";
   _loc2_.plusMode = "Down";
   _loc2_.minMode = "AtTop";
   _loc2_.maxMode = "AtBottom";
   ASSetPropFlags(mx.controls.VScrollBar.prototype, null, 1);
}
