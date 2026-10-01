// DefineSprite_4104___Packages.mx.skins.ColoredSkinElement
// origen: DoInitAction del sprite 4104 (03711_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.skins)
{
   _global.mx.skins = new Object();
}
if(!_global.mx.skins.ColoredSkinElement)
{
   mx.skins.ColoredSkinElement = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc2_.setColor = function(c)
   {
      if(c != undefined)
      {
         var _loc2_ = new Color(this);
         _loc2_.setRGB(c);
      }
   };
   _loc2_.draw = function(Void)
   {
      this.setColor(this.getStyle(this._color));
      this.onEnterFrame = undefined;
   };
   _loc2_.invalidateStyle = function(Void)
   {
      this.onEnterFrame = this.draw;
   };
   _loc1_.setColorStyle = function(p, colorStyle)
   {
      if(p._color == undefined)
      {
         p._color = colorStyle;
      }
      p.setColor = mx.skins.ColoredSkinElement.mixins.setColor;
      p.invalidateStyle = mx.skins.ColoredSkinElement.mixins.invalidateStyle;
      p.draw = mx.skins.ColoredSkinElement.mixins.draw;
      p.setColor(p.getStyle(colorStyle));
   };
   _loc1_.mixins = new mx.skins.ColoredSkinElement();
   ASSetPropFlags(mx.skins.ColoredSkinElement.prototype, null, 1);
}
