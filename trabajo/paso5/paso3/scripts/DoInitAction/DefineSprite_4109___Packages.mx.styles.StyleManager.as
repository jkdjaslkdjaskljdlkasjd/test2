// DefineSprite_4109___Packages.mx.styles.StyleManager
// origen: DoInitAction del sprite 4109 (03726_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.styles)
{
   _global.mx.styles = new Object();
}
if(!_global.mx.styles.StyleManager)
{
   mx.styles.StyleManager = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc1_.registerInheritingStyle = function(styleName)
   {
      mx.styles.StyleManager.inheritingStyles[styleName] = true;
   };
   _loc1_.isInheritingStyle = function(styleName)
   {
      return mx.styles.StyleManager.inheritingStyles[styleName] == true;
   };
   _loc1_.registerColorStyle = function(styleName)
   {
      mx.styles.StyleManager.colorStyles[styleName] = true;
   };
   _loc1_.isColorStyle = function(styleName)
   {
      return mx.styles.StyleManager.colorStyles[styleName] == true;
   };
   _loc1_.registerColorName = function(colorName, colorValue)
   {
      mx.styles.StyleManager.colorNames[colorName] = colorValue;
   };
   _loc1_.isColorName = function(colorName)
   {
      return mx.styles.StyleManager.colorNames[colorName] != undefined;
   };
   _loc1_.getColorName = function(colorName)
   {
      return mx.styles.StyleManager.colorNames[colorName];
   };
   _loc1_.inheritingStyles = {color: true, direction: true, fontFamily: true, fontSize: true, fontStyle: true, fontWeight: true, textAlign: true, textIndent: true};
   _loc1_.colorStyles = {barColor: true, trackColor: true, borderColor: true, buttonColor: true, color: true, dateHeaderColor: true, dateRollOverColor: true, disabledColor: true, fillColor: true, highlightColor: true, scrollTrackColor: true, selectedDateColor: true, shadowColor: true, strokeColor: true, symbolBackgroundColor: true, symbolBackgroundDisabledColor: true, symbolBackgroundPressedColor: true, symbolColor: true, symbolDisabledColor: true, themeColor: true, todayIndicatorColor: true, shadowCapColor: true, borderCapColor: true, focusColor: true};
   _loc1_.colorNames = {black: 0, white: 16777215, red: 16711680, green: 65280, blue: 255, magenta: 16711935, yellow: 16776960, cyan: 65535, haloGreen: 8453965, haloBlue: 2881013, haloOrange: 16761344};
   _loc1_.TextFormatStyleProps = {font: true, size: true, color: true, leftMargin: false, rightMargin: false, italic: true, bold: true, align: true, indent: true, underline: false, embedFonts: false};
   _loc1_.TextStyleMap = {textAlign: true, fontWeight: true, color: true, fontFamily: true, textIndent: true, fontStyle: true, lineHeight: true, marginLeft: true, marginRight: true, fontSize: true, textDecoration: true, embedFonts: true};
   ASSetPropFlags(mx.styles.StyleManager.prototype, null, 1);
}
