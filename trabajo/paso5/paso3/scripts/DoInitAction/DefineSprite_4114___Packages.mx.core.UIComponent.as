// DefineSprite_4114___Packages.mx.core.UIComponent
// origen: DoInitAction del sprite 4114 (03741_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.core)
{
   _global.mx.core = new Object();
}
if(!_global.mx.core.UIComponent)
{
   mx.core.UIComponent = _loc1_ = function()
   {
      super();
   };
   mx.core.UIComponent extends mx.core.UIObject;
   var _loc2_ = _loc1_.prototype;
   _loc2_.__get__width = function()
   {
      return this.__width;
   };
   _loc2_.__get__height = function()
   {
      return this.__height;
   };
   _loc2_.setVisible = function(x, noEvent)
   {
      super.setVisible(x, noEvent);
   };
   _loc2_.enabledChanged = function(id, oldValue, newValue)
   {
      this.setEnabled(newValue);
      this.invalidate();
      delete this.stylecache.tf;
      return newValue;
   };
   _loc2_.setEnabled = function(enabled)
   {
      this.invalidate();
   };
   _loc2_.getFocus = function()
   {
      var selFocus = Selection.getFocus();
      return selFocus === null ? null : eval(selFocus);
   };
   _loc2_.setFocus = function()
   {
      Selection.setFocus(this);
   };
   _loc2_.getFocusManager = function()
   {
      var _loc2_ = this;
      while(_loc2_ != undefined)
      {
         if(_loc2_.focusManager != undefined)
         {
            return _loc2_.focusManager;
         }
         _loc2_ = _loc2_._parent;
      }
      return;
   };
   _loc2_.onKillFocus = function(newFocus)
   {
      this.removeEventListener("keyDown", this);
      this.removeEventListener("keyUp", this);
      this.dispatchEvent({type: "focusOut"});
      this.drawFocus(false);
   };
   _loc2_.onSetFocus = function(oldFocus)
   {
      this.addEventListener("keyDown", this);
      this.addEventListener("keyUp", this);
      this.dispatchEvent({type: "focusIn"});
      if(this.getFocusManager().bDrawFocus != false)
      {
         this.drawFocus(true);
      }
   };
   _loc2_.findFocusInChildren = function(o)
   {
      if(o.focusTextField != undefined)
      {
         return o.focusTextField;
      }
      if(o.tabEnabled == true)
      {
         return o;
      }
      return;
   };
   _loc2_.findFocusFromObject = function(o)
   {
      if(o.tabEnabled != true)
      {
         if(o._parent == undefined)
         {
            return;
         }
         if(o._parent.tabEnabled == true)
         {
            o = o._parent;
         }
         else if(o._parent.tabChildren)
         {
            o = this.findFocusInChildren(o._parent);
         }
         else
         {
            o = this.findFocusFromObject(o._parent);
         }
      }
      return o;
   };
   _loc2_.pressFocus = function()
   {
      var _loc3_ = this.findFocusFromObject(this);
      var _loc2_ = this.getFocus();
      if(_loc3_ != _loc2_)
      {
         _loc2_.drawFocus(false);
         if(this.getFocusManager().bDrawFocus != false)
         {
            _loc3_.drawFocus(true);
         }
      }
   };
   _loc2_.releaseFocus = function()
   {
      var _loc2_ = this.findFocusFromObject(this);
      if(_loc2_ != this.getFocus())
      {
         _loc2_.setFocus();
      }
   };
   _loc2_.isParent = function(o)
   {
      while(o != undefined)
      {
         if(o == this)
         {
            return true;
         }
         o = o._parent;
      }
      return false;
   };
   _loc2_.size = function()
   {
   };
   _loc2_.init = function()
   {
      super.init();
      this._xscale = 100;
      this._yscale = 100;
      this._focusrect = _global.useFocusRect == false;
      this.watch("enabled", this.enabledChanged);
      if(this.enabled == false)
      {
         this.setEnabled(false);
      }
   };
   _loc2_.dispatchValueChangedEvent = function(value)
   {
      this.dispatchEvent({type: "valueChanged", value: value});
   };
   _loc1_.symbolName = "UIComponent";
   _loc1_.symbolOwner = mx.core.UIComponent;
   _loc1_.version = "2.0.2.127";
   _loc1_.kStretch = 5000;
   _loc2_.focusEnabled = true;
   _loc2_.tabEnabled = true;
   _loc2_.origBorderStyles = {themeColor: 16711680};
   _loc2_.clipParameters = {};
   _loc1_.mergedClipParameters = mx.core.UIObject.mergeClipParameters(mx.core.UIComponent.prototype.clipParameters, mx.core.UIObject.prototype.clipParameters);
   _loc2_.addProperty("height", _loc2_.__get__height, function()
   {
   });
   _loc2_.addProperty("width", _loc2_.__get__width, function()
   {
   });
   ASSetPropFlags(mx.core.UIComponent.prototype, null, 1);
}
