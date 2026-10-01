// DefineSprite_4134___Packages.com.gskinner.utils.SWFBridgeAS2
// origen: DoInitAction del sprite 4134 (03801_DoInitAction.bin)

if(!_global.com)
{
   _global.com = new Object();
}
if(!_global.com.gskinner)
{
   _global.com.gskinner = new Object();
}
if(!_global.com.gskinner.utils)
{
   _global.com.gskinner.utils = new Object();
}
if(!_global.com.gskinner.utils.SWFBridgeAS2)
{
   com.gskinner.utils.SWFBridgeAS2 = _loc1_ = function(p_id, p_clientObj)
   {
      mx.events.EventDispatcher.initialize(this);
      this.baseID = p_id.split(":").join("");
      this.lc = new LocalConnection();
      var _this = this;
      this.lc.com_gskinner_utils_SWFBridge_init = function()
      {
         _this.com_gskinner_utils_SWFBridge_init();
      };
      this.lc.com_gskinner_utils_SWFBridge_receive = function()
      {
         _this.com_gskinner_utils_SWFBridge_receive.apply(_this, arguments);
      };
      this.clientObj = p_clientObj;
      this.host = this.lc.connect(this.baseID + "_host");
      this.myID = this.baseID + (this.host ? "_host" : "_guest");
      this.extID = this.baseID + (this.host ? "_guest" : "_host");
      if(!this.host)
      {
         this.lc.connect(this.myID);
         this.lc.send(this.extID, "com_gskinner_utils_SWFBridge_init");
      }
   };
   var _loc2_ = _loc1_.prototype;
   _loc2_.close = function()
   {
      this.lc.close();
      delete this.clientObj;
      delete this.lc;
      this._connected = false;
   };
   _loc2_.send = function()
   {
      if(!this._connected)
      {
         return;
      }
      var _loc3_ = arguments.slice(0);
      _loc3_.unshift("com_gskinner_utils_SWFBridge_receive");
      _loc3_.unshift(this.extID);
      this.lc.send.apply(this.lc, _loc3_);
   };
   _loc2_.__get__id = function()
   {
      return this.baseID;
   };
   _loc2_.__get__connected = function()
   {
      return this._connected;
   };
   _loc2_.com_gskinner_utils_SWFBridge_receive = function()
   {
      var _loc3_ = arguments.slice(0);
      var _loc4_ = String(_loc3_.shift());
      this.clientObj[_loc4_].apply(this.clientObj, _loc3_);
   };
   _loc2_.com_gskinner_utils_SWFBridge_init = function()
   {
      trace("SWFBridge (AS2) connected as " + (this.host ? "host" : "client"));
      if(this.host)
      {
         this.lc.send(this.extID, "com_gskinner_utils_SWFBridge_init");
      }
      this._connected = true;
      this.dispatchEvent({type: "connect"});
   };
   _loc2_._connected = false;
   _loc2_.addProperty("connected", _loc2_.__get__connected, function()
   {
   });
   _loc2_.addProperty("id", _loc2_.__get__id, function()
   {
   });
   ASSetPropFlags(com.gskinner.utils.SWFBridgeAS2.prototype, null, 1);
}
