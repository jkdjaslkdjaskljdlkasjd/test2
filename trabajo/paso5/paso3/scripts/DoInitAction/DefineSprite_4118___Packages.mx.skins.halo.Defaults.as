// DefineSprite_4118___Packages.mx.skins.halo.Defaults
// origen: DoInitAction del sprite 4118 (03753_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.skins)
{
   _global.mx.skins = new Object();
}
if(!_global.mx.skins.halo)
{
   _global.mx.skins.halo = new Object();
}
if(!_global.mx.skins.halo.Defaults)
{
   mx.skins.halo.Defaults = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc1_.setThemeDefaults = function()
   {
      var _loc2_ = _global.style;
      _loc2_.themeColor = 8453965;
      _loc2_.disabledColor = 8684164;
      _loc2_.modalTransparency = 0;
      _loc2_.filled = true;
      _loc2_.stroked = true;
      _loc2_.strokeWidth = 1;
      _loc2_.strokeColor = 0;
      _loc2_.fillColor = 16777215;
      _loc2_.repeatInterval = 35;
      _loc2_.repeatDelay = 500;
      _loc2_.fontFamily = "_sans";
      _loc2_.fontSize = 12;
      _loc2_.selectionColor = 13500353;
      _loc2_.rollOverColor = 14942166;
      _loc2_.useRollOver = true;
      _loc2_.backgroundDisabledColor = 14540253;
      _loc2_.selectionDisabledColor = 14540253;
      _loc2_.selectionDuration = 200;
      _loc2_.openDuration = 250;
      _loc2_.borderStyle = "inset";
      _loc2_.color = 734012;
      _loc2_.textSelectedColor = 24371;
      _loc2_.textRollOverColor = 2831164;
      _loc2_.textDisabledColor = 16777215;
      _loc2_.vGridLines = true;
      _loc2_.hGridLines = false;
      _loc2_.vGridLineColor = 6710886;
      _loc2_.hGridLineColor = 6710886;
      _loc2_.headerColor = 15395562;
      _loc2_.indentation = 17;
      _loc2_.folderOpenIcon = "TreeFolderOpen";
      _loc2_.folderClosedIcon = "TreeFolderClosed";
      _loc2_.defaultLeafIcon = "TreeNodeIcon";
      _loc2_.disclosureOpenIcon = "TreeDisclosureOpen";
      _loc2_.disclosureClosedIcon = "TreeDisclosureClosed";
      _loc2_.popupDuration = 150;
      _loc2_.todayColor = 6710886;
      _global.styles.ScrollSelectList = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc2_ = _loc0_;
      _loc2_.backgroundColor = 16777215;
      _loc2_.borderColor = 13290186;
      _loc2_.borderStyle = "inset";
      _global.styles.ComboBox = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc2_ = _loc0_;
      _loc2_.borderStyle = "inset";
      _global.styles.NumericStepper = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc2_ = _loc0_;
      _loc2_.textAlign = "center";
      _global.styles.RectBorder = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc2_ = _loc0_;
      _loc2_.borderColor = 14015965;
      _loc2_.buttonColor = 7305079;
      _loc2_.shadowColor = 15658734;
      _loc2_.highlightColor = 12897484;
      _loc2_.shadowCapColor = 14015965;
      _loc2_.borderCapColor = 9542041;
      var _loc4_ = new Object();
      _loc4_.borderColor = 16711680;
      _loc4_.buttonColor = 16711680;
      _loc4_.shadowColor = 16711680;
      _loc4_.highlightColor = 16711680;
      _loc4_.shadowCapColor = 16711680;
      _loc4_.borderCapColor = 16711680;
      mx.core.UIComponent.prototype.origBorderStyles = _loc4_;
      var _loc3_ = undefined;
      _global.styles.TextInput = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.backgroundColor = 16777215;
      _loc3_.borderStyle = "inset";
      _global.styles.TextArea = _global.styles.TextInput;
      _global.styles.Window = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.borderStyle = "default";
      _global.styles.windowStyles = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.fontWeight = "bold";
      _global.styles.dataGridStyles = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.fontWeight = "bold";
      _global.styles.Alert = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.borderStyle = "alert";
      _global.styles.ScrollView = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.borderStyle = "inset";
      _global.styles.View = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.borderStyle = "none";
      _global.styles.ProgressBar = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.color = 11187123;
      _loc3_.fontWeight = "bold";
      _global.styles.AccordionHeader = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.fontWeight = "bold";
      _loc3_.fontSize = "11";
      _global.styles.Accordion = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.borderStyle = "solid";
      _loc3_.backgroundColor = 16777215;
      _loc3_.borderColor = 9081738;
      _loc3_.headerHeight = 22;
      _loc3_.marginLeft = _loc3_.marginRight = _loc3_.marginTop = _loc3_.marginBottom = -1;
      _loc3_.verticalGap = -1;
      _global.styles.DateChooser = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.borderColor = 9542041;
      _loc3_.headerColor = 16777215;
      _global.styles.CalendarLayout = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.fontSize = 10;
      _loc3_.textAlign = "right";
      _loc3_.color = 2831164;
      _global.styles.WeekDayStyle = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.fontWeight = "bold";
      _loc3_.fontSize = 11;
      _loc3_.textAlign = "center";
      _loc3_.color = 2831164;
      _global.styles.TodayStyle = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.color = 16777215;
      _global.styles.HeaderDateText = _loc0_ = new mx.styles.CSSStyleDeclaration();
      _loc3_ = _loc0_;
      _loc3_.fontSize = 12;
      _loc3_.fontWeight = "bold";
      _loc3_.textAlign = "center";
   };
   _loc2_.drawRoundRect = function(x, y, w, h, r, c, alpha, rot, gradient, ratios)
   {
      if(typeof r == "object")
      {
         var _loc18_ = r.br;
         var _loc16_ = r.bl;
         var _loc15_ = r.tl;
         var _loc10_ = r.tr;
      }
      else
      {
         _loc18_ = _loc16_ = _loc15_ = _loc10_ = r;
      }
      if(typeof c == "object")
      {
         if(typeof alpha != "object")
         {
            var _loc9_ = [alpha, alpha];
         }
         else
         {
            _loc9_ = alpha;
         }
         if(ratios == undefined)
         {
            ratios = [0, 255];
         }
         var _loc14_ = h * 0.7;
         if(typeof rot != "object")
         {
            var _loc11_ = {matrixType: "box", x: 0 - _loc14_, y: _loc14_, w: w * 2, h: h * 4, r: rot * 0.0174532925199433};
         }
         else
         {
            _loc11_ = rot;
         }
         if(gradient == "radial")
         {
            this.beginGradientFill("radial", c, _loc9_, ratios, _loc11_);
         }
         else
         {
            this.beginGradientFill("linear", c, _loc9_, ratios, _loc11_);
         }
      }
      else if(c != undefined)
      {
         this.beginFill(c, alpha);
      }
      r = _loc18_;
      var _loc13_ = r - r * 0.707106781186547;
      var _loc12_ = r - r * 0.414213562373095;
      this.moveTo(x + w, y + h - r);
      this.lineTo(x + w, y + h - r);
      this.curveTo(x + w, y + h - _loc12_, x + w - _loc13_, y + h - _loc13_);
      this.curveTo(x + w - _loc12_, y + h, x + w - r, y + h);
      r = _loc16_;
      _loc13_ = r - r * 0.707106781186547;
      _loc12_ = r - r * 0.414213562373095;
      this.lineTo(x + r, y + h);
      this.curveTo(x + _loc12_, y + h, x + _loc13_, y + h - _loc13_);
      this.curveTo(x, y + h - _loc12_, x, y + h - r);
      r = _loc15_;
      _loc13_ = r - r * 0.707106781186547;
      _loc12_ = r - r * 0.414213562373095;
      this.lineTo(x, y + r);
      this.curveTo(x, y + _loc12_, x + _loc13_, y + _loc13_);
      this.curveTo(x + _loc12_, y, x + r, y);
      r = _loc10_;
      _loc13_ = r - r * 0.707106781186547;
      _loc12_ = r - r * 0.414213562373095;
      this.lineTo(x + w - r, y);
      this.curveTo(x + w - _loc12_, y, x + w - _loc13_, y + _loc13_);
      this.curveTo(x + w, y + _loc12_, x + w, y + r);
      this.lineTo(x + w, y + h - r);
      if(c != undefined)
      {
         this.endFill();
      }
   };
   _loc1_.classConstruct = function()
   {
      mx.core.ext.UIObjectExtensions.Extensions();
      mx.skins.halo.Defaults.setThemeDefaults();
      mx.core.UIObject.prototype.drawRoundRect = mx.skins.halo.Defaults.prototype.drawRoundRect;
      return true;
   };
   _loc1_.classConstructed = mx.skins.halo.Defaults.classConstruct();
   _loc1_.CSSStyleDeclarationDependency = mx.styles.CSSStyleDeclaration;
   _loc1_.UIObjectExtensionsDependency = mx.core.ext.UIObjectExtensions;
   _loc1_.UIObjectDependency = mx.core.UIObject;
   ASSetPropFlags(mx.skins.halo.Defaults.prototype, null, 1);
}
