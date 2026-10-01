// DefineSprite_4107___Packages.mx.styles.CSSTextStyles
// origen: DoInitAction del sprite 4107 (03720_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.styles)
{
   _global.mx.styles = new Object();
}
if(!_global.mx.styles.CSSTextStyles)
{
   mx.styles.CSSTextStyles = _loc1_ = function()
   {
   };
   var _loc2_ = _loc1_.prototype;
   _loc1_.addTextStyles = function(o, bColor)
   {
      o.addProperty("textAlign", function()
      {
         return this._tf.align;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.align = x;
      });
      o.addProperty("fontWeight", function()
      {
         return this._tf.bold != undefined ? this._tf.bold ? "bold" : "none" : undefined;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.bold = x == "bold";
      });
      if(bColor)
      {
         o.addProperty("color", function()
         {
            return this._tf.color;
         }, function(x)
         {
            if(this._tf == undefined)
            {
               this._tf = new TextFormat();
            }
            this._tf.color = x;
         });
      }
      o.addProperty("fontFamily", function()
      {
         return this._tf.font;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.font = x;
      });
      o.addProperty("textIndent", function()
      {
         return this._tf.indent;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.indent = x;
      });
      o.addProperty("fontStyle", function()
      {
         return this._tf.italic != undefined ? this._tf.italic ? "italic" : "none" : undefined;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.italic = x == "italic";
      });
      o.addProperty("marginLeft", function()
      {
         return this._tf.leftMargin;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.leftMargin = x;
      });
      o.addProperty("marginRight", function()
      {
         return this._tf.rightMargin;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.rightMargin = x;
      });
      o.addProperty("fontSize", function()
      {
         return this._tf.size;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.size = x;
      });
      o.addProperty("textDecoration", function()
      {
         return this._tf.underline != undefined ? this._tf.underline ? "underline" : "none" : undefined;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.underline = x == "underline";
      });
      o.addProperty("embedFonts", function()
      {
         return this._tf.embedFonts;
      }, function(x)
      {
         if(this._tf == undefined)
         {
            this._tf = new TextFormat();
         }
         this._tf.embedFonts = x;
      });
   };
   ASSetPropFlags(mx.styles.CSSTextStyles.prototype, null, 1);
}
