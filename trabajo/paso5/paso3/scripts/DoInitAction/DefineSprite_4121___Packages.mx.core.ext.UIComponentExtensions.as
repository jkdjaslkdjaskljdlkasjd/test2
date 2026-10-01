// DefineSprite_4121___Packages.mx.core.ext.UIComponentExtensions
// origen: DoInitAction del sprite 4121 (03762_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.core)
{
   _global.mx.core = new Object();
}
if(!_global.mx.core.ext)
{
   _global.mx.core.ext = new Object();
}
if(!_global.mx.core.ext.UIComponentExtensions)
{
   mx.core.ext.UIComponentExtensions = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc1_.Extensions = function()
   {
      if(mx.core.ext.UIComponentExtensions.bExtended == true)
      {
         return true;
      }
      mx.core.ext.UIComponentExtensions.bExtended = true;
      TextField.prototype.setFocus = function()
      {
         Selection.setFocus(this);
      };
      TextField.prototype.onSetFocus = function(oldFocus)
      {
         if(this.tabEnabled != false)
         {
            if(this.getFocusManager().bDrawFocus)
            {
               this.drawFocus(true);
            }
         }
      };
      TextField.prototype.onKillFocus = function(oldFocus)
      {
         if(this.tabEnabled != false)
         {
            this.drawFocus(false);
         }
      };
      TextField.prototype.drawFocus = mx.core.UIComponent.prototype.drawFocus;
      TextField.prototype.getFocusManager = mx.core.UIComponent.prototype.getFocusManager;
      mx.managers.OverlappedWindows.enableOverlappedWindows();
      mx.styles.CSSSetStyle.enableRunTimeCSS();
      mx.managers.FocusManager.enableFocusManagement();
   };
   _loc1_.bExtended = false;
   _loc1_.UIComponentExtended = mx.core.ext.UIComponentExtensions.Extensions();
   _loc1_.UIComponentDependency = mx.core.UIComponent;
   _loc1_.FocusManagerDependency = mx.managers.FocusManager;
   _loc1_.OverlappedWindowsDependency = mx.managers.OverlappedWindows;
   ASSetPropFlags(mx.core.ext.UIComponentExtensions.prototype, null, 1);
}
