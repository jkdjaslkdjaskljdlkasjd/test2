// DefineSprite_4108___Packages.mx.styles.CSSStyleDeclaration
// origen: DoInitAction del sprite 4108 (03723_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.styles)
{
   _global.mx.styles = new Object();
}
if(!_global.mx.styles.CSSStyleDeclaration)
{
   mx.styles.CSSStyleDeclaration = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc2_.__getTextFormat = function(tf, bAll)
   {
      var _loc5_ = false;
      if(this._tf != undefined)
      {
         var _loc2_ = undefined;
         for(_loc2_ in mx.styles.StyleManager.TextFormatStyleProps)
         {
            if(bAll || mx.styles.StyleManager.TextFormatStyleProps[_loc2_])
            {
               if(tf[_loc2_] == undefined)
               {
                  var _loc3_ = this._tf[_loc2_];
                  if(_loc3_ != undefined)
                  {
                     tf[_loc2_] = _loc3_;
                  }
                  else
                  {
                     _loc5_ = true;
                  }
               }
            }
         }
      }
      else
      {
         _loc5_ = true;
      }
      return _loc5_;
   };
   _loc2_.getStyle = function(styleProp)
   {
      var _loc2_ = this[styleProp];
      var _loc3_ = mx.styles.StyleManager.getColorName(_loc2_);
      return _loc3_ == undefined ? _loc2_ : _loc3_;
   };
   _loc1_.classConstruct = function()
   {
      mx.styles.CSSTextStyles.addTextStyles(mx.styles.CSSStyleDeclaration.prototype, true);
      return true;
   };
   _loc1_.classConstructed = mx.styles.CSSStyleDeclaration.classConstruct();
   _loc1_.CSSTextStylesDependency = mx.styles.CSSTextStyles;
   ASSetPropFlags(mx.styles.CSSStyleDeclaration.prototype, null, 1);
}
