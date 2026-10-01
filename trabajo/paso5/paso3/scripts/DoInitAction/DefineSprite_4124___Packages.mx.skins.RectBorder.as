// DefineSprite_4124___Packages.mx.skins.RectBorder
// origen: DoInitAction del sprite 4124 (03771_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.skins)
{
   _global.mx.skins = new Object();
}
if(!_global.mx.skins.RectBorder)
{
   mx.skins.RectBorder = _loc1_ = function()
   {
      super();
   };
   mx.skins.RectBorder extends mx.skins.Border;
   var _loc2_ = _loc1_.prototype;
   _loc2_.__get__width = function()
   {
      return this.__width;
   };
   _loc2_.__get__height = function()
   {
      return this.__height;
   };
   _loc2_.init = function(Void)
   {
      super.init();
   };
   _loc2_.draw = function(Void)
   {
      this.size();
   };
   _loc2_.getBorderMetrics = function(Void)
   {
      var _loc2_ = this.offset;
      if(this.__borderMetrics == undefined)
      {
         this.__borderMetrics = {left: _loc2_, top: _loc2_, right: _loc2_, bottom: _loc2_};
      }
      else
      {
         this.__borderMetrics.left = _loc2_;
         this.__borderMetrics.top = _loc2_;
         this.__borderMetrics.right = _loc2_;
         this.__borderMetrics.bottom = _loc2_;
      }
      return this.__borderMetrics;
   };
   _loc2_.__get__borderMetrics = function()
   {
      return this.getBorderMetrics();
   };
   _loc2_.drawBorder = function(Void)
   {
   };
   _loc2_.size = function(Void)
   {
      this.drawBorder();
   };
   _loc2_.setColor = function(Void)
   {
      this.drawBorder();
   };
   _loc1_.symbolName = "RectBorder";
   _loc1_.symbolOwner = mx.skins.RectBorder;
   _loc1_.version = "2.0.2.127";
   _loc2_.className = "RectBorder";
   _loc2_.borderStyleName = "borderStyle";
   _loc2_.borderColorName = "borderColor";
   _loc2_.shadowColorName = "shadowColor";
   _loc2_.highlightColorName = "highlightColor";
   _loc2_.buttonColorName = "buttonColor";
   _loc2_.backgroundColorName = "backgroundColor";
   _loc2_.addProperty("borderMetrics", _loc2_.__get__borderMetrics, function()
   {
   });
   _loc2_.addProperty("height", _loc2_.__get__height, function()
   {
   });
   _loc2_.addProperty("width", _loc2_.__get__width, function()
   {
   });
   ASSetPropFlags(mx.skins.RectBorder.prototype, null, 1);
}
