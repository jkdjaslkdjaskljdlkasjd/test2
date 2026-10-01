// DefineSprite_4106___Packages.mx.skins.SkinElement
// origen: DoInitAction del sprite 4106 (03717_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.skins)
{
   _global.mx.skins = new Object();
}
if(!_global.mx.skins.SkinElement)
{
   mx.skins.SkinElement = _loc1_ = function()
   {
      super();
   };
   mx.skins.SkinElement extends MovieClip;
   var _loc2_ = _loc1_.prototype;
   _loc1_.registerElement = function(name, className)
   {
      Object.registerClass(name, className == undefined ? mx.skins.SkinElement : className);
      _global.skinRegistry[name] = true;
   };
   _loc2_.__set__visible = function(visible)
   {
      this._visible = visible;
   };
   _loc2_.move = function(x, y)
   {
      this._x = x;
      this._y = y;
   };
   _loc2_.setSize = function(w, h)
   {
      this._width = w;
      this._height = h;
   };
   ASSetPropFlags(mx.skins.SkinElement.prototype, null, 1);
}
