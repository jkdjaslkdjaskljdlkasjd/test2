// DefineSprite_4123___Packages.mx.skins.Border
// origen: DoInitAction del sprite 4123 (03768_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.skins)
{
   _global.mx.skins = new Object();
}
if(!_global.mx.skins.Border)
{
   mx.skins.Border = _loc1_ = function()
   {
      super();
   };
   mx.skins.Border extends mx.core.UIObject;
   var _loc2_ = _loc1_.prototype;
   _loc2_.init = function(Void)
   {
      super.init();
   };
   _loc1_.symbolName = "Border";
   _loc1_.symbolOwner = mx.skins.Border;
   _loc2_.className = "Border";
   _loc2_.tagBorder = 0;
   _loc2_.idNames = new Array("border_mc");
   ASSetPropFlags(mx.skins.Border.prototype, null, 1);
}
