// DefineSprite_4117___Packages.mx.managers.SystemManager
// origen: DoInitAction del sprite 4117 (03750_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.managers)
{
   _global.mx.managers = new Object();
}
if(!_global.mx.managers.SystemManager)
{
   mx.managers.SystemManager = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc1_.init = function(Void)
   {
      if(mx.managers.SystemManager._initialized == false)
      {
         mx.managers.SystemManager._initialized = true;
         mx.events.EventDispatcher.initialize(mx.managers.SystemManager);
         Mouse.addListener(mx.managers.SystemManager);
         Stage.addListener(mx.managers.SystemManager);
         mx.managers.SystemManager._xAddEventListener = mx.managers.SystemManager.addEventListener;
         mx.managers.SystemManager.addEventListener = mx.managers.SystemManager.__addEventListener;
         mx.managers.SystemManager._xRemoveEventListener = mx.managers.SystemManager.removeEventListener;
         mx.managers.SystemManager.removeEventListener = mx.managers.SystemManager.__removeEventListener;
      }
   };
   _loc1_.addFocusManager = function(f)
   {
      mx.managers.SystemManager.form = f;
      f.focusManager.activate();
   };
   _loc1_.removeFocusManager = function(f)
   {
   };
   _loc1_.onMouseDown = function(Void)
   {
      var _loc1_ = mx.managers.SystemManager.form;
      _loc1_.focusManager._onMouseDown();
   };
   _loc1_.onResize = function(Void)
   {
      var _loc7_ = Stage.width;
      var _loc6_ = Stage.height;
      var _loc9_ = _global.origWidth;
      var _loc8_ = _global.origHeight;
      var _loc3_ = Stage.align;
      var _loc5_ = (_loc9_ - _loc7_) / 2;
      var _loc4_ = (_loc8_ - _loc6_) / 2;
      if(_loc3_ == "T")
      {
         _loc4_ = 0;
      }
      else if(_loc3_ == "B")
      {
         _loc4_ = _loc8_ - _loc6_;
      }
      else if(_loc3_ == "L")
      {
         _loc5_ = 0;
      }
      else if(_loc3_ == "R")
      {
         _loc5_ = _loc9_ - _loc7_;
      }
      else if(_loc3_ == "LT")
      {
         _loc4_ = 0;
         _loc5_ = 0;
      }
      else if(_loc3_ == "TR")
      {
         _loc4_ = 0;
         _loc5_ = _loc9_ - _loc7_;
      }
      else if(_loc3_ == "LB")
      {
         _loc4_ = _loc8_ - _loc6_;
         _loc5_ = 0;
      }
      else if(_loc3_ == "RB")
      {
         _loc4_ = _loc8_ - _loc6_;
         _loc5_ = _loc9_ - _loc7_;
      }
      if(mx.managers.SystemManager.__screen == undefined)
      {
         mx.managers.SystemManager.__screen = new Object();
      }
      mx.managers.SystemManager.__screen.x = _loc5_;
      mx.managers.SystemManager.__screen.y = _loc4_;
      mx.managers.SystemManager.__screen.width = _loc7_;
      mx.managers.SystemManager.__screen.height = _loc6_;
      _root.focusManager.relocate();
      mx.managers.SystemManager.dispatchEvent({type: "resize"});
   };
   _loc1_.__get__screen = function()
   {
      mx.managers.SystemManager.init();
      if(mx.managers.SystemManager.__screen == undefined)
      {
         mx.managers.SystemManager.onResize();
      }
      return mx.managers.SystemManager.__screen;
   };
   _loc1_._initialized = false;
   _loc1_.idleFrames = 0;
   _loc1_.isMouseDown = false;
   _loc1_.forms = new Array();
   _loc1_.addProperty("screen", _loc1_.__get__screen, function()
   {
   });
   ASSetPropFlags(mx.managers.SystemManager.prototype, null, 1);
}
