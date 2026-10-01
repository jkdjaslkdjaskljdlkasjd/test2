// DefineSprite_4111___Packages.mx.events.UIEventDispatcher
// origen: DoInitAction del sprite 4111 (03732_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.events)
{
   _global.mx.events = new Object();
}
if(!_global.mx.events.UIEventDispatcher)
{
   mx.events.UIEventDispatcher = _loc1_ = function()
   {
      super();
   };
   mx.events.UIEventDispatcher extends mx.events.EventDispatcher;
   var _loc2_ = _loc1_.prototype;
   _loc1_.addKeyEvents = function(obj)
   {
      if(obj.keyHandler == undefined)
      {
         obj.keyHandler = _loc0_ = new Object();
         var _loc1_ = _loc0_;
         _loc1_.owner = obj;
         _loc1_.onKeyDown = mx.events.UIEventDispatcher._fEventDispatcher.onKeyDown;
         _loc1_.onKeyUp = mx.events.UIEventDispatcher._fEventDispatcher.onKeyUp;
      }
      Key.addListener(obj.keyHandler);
   };
   _loc1_.removeKeyEvents = function(obj)
   {
      Key.removeListener(obj.keyHandler);
   };
   _loc1_.addLoadEvents = function(obj)
   {
      if(obj.onLoad == undefined)
      {
         obj.onLoad = mx.events.UIEventDispatcher._fEventDispatcher.onLoad;
         obj.onUnload = mx.events.UIEventDispatcher._fEventDispatcher.onUnload;
         if(obj.getBytesTotal() == obj.getBytesLoaded())
         {
            obj.doLater(obj, "onLoad");
         }
      }
   };
   _loc1_.removeLoadEvents = function(obj)
   {
      delete obj.onLoad;
      delete obj.onUnload;
   };
   _loc1_.initialize = function(obj)
   {
      if(mx.events.UIEventDispatcher._fEventDispatcher == undefined)
      {
         mx.events.UIEventDispatcher._fEventDispatcher = new mx.events.UIEventDispatcher();
      }
      obj.addEventListener = mx.events.UIEventDispatcher._fEventDispatcher.__addEventListener;
      obj.__origAddEventListener = mx.events.UIEventDispatcher._fEventDispatcher.addEventListener;
      obj.removeEventListener = mx.events.UIEventDispatcher._fEventDispatcher.removeEventListener;
      obj.dispatchEvent = mx.events.UIEventDispatcher._fEventDispatcher.dispatchEvent;
      obj.dispatchQueue = mx.events.UIEventDispatcher._fEventDispatcher.dispatchQueue;
   };
   _loc2_.dispatchEvent = function(eventObj)
   {
      if(eventObj.target == undefined)
      {
         eventObj.target = this;
      }
      this[eventObj.type + "Handler"](eventObj);
      this.dispatchQueue(mx.events.EventDispatcher, eventObj);
      this.dispatchQueue(this, eventObj);
   };
   _loc2_.onKeyDown = function(Void)
   {
      this.owner.dispatchEvent({type: "keyDown", code: Key.getCode(), ascii: Key.getAscii(), shiftKey: Key.isDown(16), ctrlKey: Key.isDown(17)});
   };
   _loc2_.onKeyUp = function(Void)
   {
      this.owner.dispatchEvent({type: "keyUp", code: Key.getCode(), ascii: Key.getAscii(), shiftKey: Key.isDown(16), ctrlKey: Key.isDown(17)});
   };
   _loc2_.onLoad = function(Void)
   {
      if(this.__sentLoadEvent != true)
      {
         this.dispatchEvent({type: "load"});
      }
      this.__sentLoadEvent = true;
   };
   _loc2_.onUnload = function(Void)
   {
      this.dispatchEvent({type: "unload"});
   };
   _loc2_.__addEventListener = function(event, handler)
   {
      this.__origAddEventListener(event, handler);
      var _loc3_ = mx.events.UIEventDispatcher.lowLevelEvents;
      for(var _loc5_ in _loc3_)
      {
         if(mx.events.UIEventDispatcher[_loc5_][event] != undefined)
         {
            var _loc2_ = _loc3_[_loc5_][0];
            mx.events.UIEventDispatcher[_loc2_](this);
         }
      }
   };
   _loc2_.removeEventListener = function(event, handler)
   {
      var _loc6_ = "__q_" + event;
      mx.events.EventDispatcher._removeEventListener(this[_loc6_], event, handler);
      if(this[_loc6_].length == 0)
      {
         var _loc2_ = mx.events.UIEventDispatcher.lowLevelEvents;
         for(var _loc5_ in _loc2_)
         {
            if(mx.events.UIEventDispatcher[_loc5_][event] != undefined)
            {
               var _loc3_ = _loc2_[_loc5_][1];
               mx.events.UIEventDispatcher[_loc2_[_loc5_][1]](this);
            }
         }
      }
   };
   _loc1_.keyEvents = {keyDown: 1, keyUp: 1};
   _loc1_.loadEvents = {load: 1, unload: 1};
   _loc1_.lowLevelEvents = {keyEvents: ["addKeyEvents", "removeKeyEvents"], loadEvents: ["addLoadEvents", "removeLoadEvents"]};
   _loc1_._fEventDispatcher = undefined;
   ASSetPropFlags(mx.events.UIEventDispatcher.prototype, null, 1);
}
