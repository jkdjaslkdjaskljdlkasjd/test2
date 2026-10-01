// DefineSprite_4120___Packages.mx.managers.OverlappedWindows
// origen: DoInitAction del sprite 4120 (03759_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.managers)
{
   _global.mx.managers = new Object();
}
if(!_global.mx.managers.OverlappedWindows)
{
   mx.managers.OverlappedWindows = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc1_.checkIdle = function(Void)
   {
      if(mx.managers.SystemManager.idleFrames > 10)
      {
         mx.managers.SystemManager.dispatchEvent({type: "idle"});
      }
      else
      {
         mx.managers.SystemManager.idleFrames++;
      }
   };
   _loc1_.__addEventListener = function(e, o, l)
   {
      if(e == "idle")
      {
         if(mx.managers.SystemManager.interval == undefined)
         {
            mx.managers.SystemManager.interval = setInterval(mx.managers.SystemManager.checkIdle, 100);
         }
      }
      mx.managers.SystemManager._xAddEventListener(e, o, l);
   };
   _loc1_.__removeEventListener = function(e, o, l)
   {
      if(e == "idle")
      {
         if(mx.managers.SystemManager._xRemoveEventListener(e, o, l) == 0)
         {
            clearInterval(mx.managers.SystemManager.interval);
         }
      }
      else
      {
         mx.managers.SystemManager._xRemoveEventListener(e, o, l);
      }
   };
   _loc1_.onMouseDown = function(Void)
   {
      mx.managers.SystemManager.idleFrames = 0;
      mx.managers.SystemManager.isMouseDown = true;
      var _loc5_ = _root;
      var _loc3_ = undefined;
      var _loc8_ = _root._xmouse;
      var _loc7_ = _root._ymouse;
      if(mx.managers.SystemManager.form.modalWindow == undefined)
      {
         if(mx.managers.SystemManager.forms.length > 1)
         {
            var _loc6_ = mx.managers.SystemManager.forms.length;
            var _loc4_ = undefined;
            _loc4_ = 0;
            while(_loc4_ < _loc6_)
            {
               var _loc2_ = mx.managers.SystemManager.forms[_loc4_];
               if(_loc2_._visible)
               {
                  if(_loc2_.hitTest(_loc8_, _loc7_))
                  {
                     if(_loc3_ == undefined)
                     {
                        _loc3_ = _loc2_.getDepth();
                        _loc5_ = _loc2_;
                     }
                     else if(_loc3_ < _loc2_.getDepth())
                     {
                        _loc3_ = _loc2_.getDepth();
                        _loc5_ = _loc2_;
                     }
                  }
               }
               _loc4_++;
            }
            if(_loc5_ != mx.managers.SystemManager.form)
            {
               mx.managers.SystemManager.activate(_loc5_);
            }
         }
      }
      var _loc9_ = mx.managers.SystemManager.form;
      _loc9_.focusManager._onMouseDown();
   };
   _loc1_.onMouseMove = function(Void)
   {
      mx.managers.SystemManager.idleFrames = 0;
   };
   _loc1_.onMouseUp = function(Void)
   {
      mx.managers.SystemManager.isMouseDown = false;
      mx.managers.SystemManager.idleFrames = 0;
   };
   _loc1_.activate = function(f)
   {
      if(mx.managers.SystemManager.form != undefined)
      {
         if(mx.managers.SystemManager.form != f && mx.managers.SystemManager.forms.length > 1)
         {
            var _loc1_ = mx.managers.SystemManager.form;
            _loc1_.focusManager.deactivate();
         }
      }
      mx.managers.SystemManager.form = f;
      f.focusManager.activate();
   };
   _loc1_.deactivate = function(f)
   {
      if(mx.managers.SystemManager.form != undefined)
      {
         if(mx.managers.SystemManager.form == f && mx.managers.SystemManager.forms.length > 1)
         {
            var _loc5_ = mx.managers.SystemManager.form;
            _loc5_.focusManager.deactivate();
            var _loc3_ = mx.managers.SystemManager.forms.length;
            var _loc1_ = undefined;
            var _loc2_ = undefined;
            _loc1_ = 0;
            while(_loc1_ < _loc3_)
            {
               if(mx.managers.SystemManager.forms[_loc1_] == f)
               {
                  _loc1_ += 1;
                  while(_loc1_ < _loc3_)
                  {
                     if(mx.managers.SystemManager.forms[_loc1_]._visible == true)
                     {
                        _loc2_ = mx.managers.SystemManager.forms[_loc1_];
                     }
                     _loc1_++;
                  }
                  mx.managers.SystemManager.form = _loc2_;
                  break;
               }
               else if(mx.managers.SystemManager.forms[_loc1_]._visible == true)
               {
                  _loc2_ = mx.managers.SystemManager.forms[_loc1_];
               }
               _loc1_++;
            }
            _loc5_ = mx.managers.SystemManager.form;
            _loc5_.focusManager.activate();
         }
      }
   };
   _loc1_.addFocusManager = function(f)
   {
      mx.managers.SystemManager.forms.push(f);
      mx.managers.SystemManager.activate(f);
   };
   _loc1_.removeFocusManager = function(f)
   {
      var _loc3_ = mx.managers.SystemManager.forms.length;
      var _loc1_ = undefined;
      _loc1_ = 0;
      while(_loc1_ < _loc3_)
      {
         if(mx.managers.SystemManager.forms[_loc1_] == f)
         {
            if(mx.managers.SystemManager.form == f)
            {
               mx.managers.SystemManager.deactivate(f);
            }
            mx.managers.SystemManager.forms.splice(_loc1_, 1);
            return;
         }
         _loc1_++;
      }
   };
   _loc1_.enableOverlappedWindows = function()
   {
      if(!mx.managers.OverlappedWindows.initialized)
      {
         mx.managers.OverlappedWindows.initialized = true;
         mx.managers.SystemManager.checkIdle = mx.managers.OverlappedWindows.checkIdle;
         mx.managers.SystemManager.__addEventListener = mx.managers.OverlappedWindows.__addEventListener;
         mx.managers.SystemManager.__removeEventListener = mx.managers.OverlappedWindows.__removeEventListener;
         mx.managers.SystemManager.onMouseDown = mx.managers.OverlappedWindows.onMouseDown;
         mx.managers.SystemManager.onMouseMove = mx.managers.OverlappedWindows.onMouseMove;
         mx.managers.SystemManager.onMouseUp = mx.managers.OverlappedWindows.onMouseUp;
         mx.managers.SystemManager.activate = mx.managers.OverlappedWindows.activate;
         mx.managers.SystemManager.deactivate = mx.managers.OverlappedWindows.deactivate;
         mx.managers.SystemManager.addFocusManager = mx.managers.OverlappedWindows.addFocusManager;
         mx.managers.SystemManager.removeFocusManager = mx.managers.OverlappedWindows.removeFocusManager;
      }
   };
   _loc1_.initialized = false;
   _loc1_.SystemManagerDependency = mx.managers.SystemManager;
   ASSetPropFlags(mx.managers.OverlappedWindows.prototype, null, 1);
}
