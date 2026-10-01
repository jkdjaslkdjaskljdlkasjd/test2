// DefineSprite_4133___Packages.mx.controls.UIScrollBar
// origen: DoInitAction del sprite 4133 (03798_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.controls)
{
   _global.mx.controls = new Object();
}
if(!_global.mx.controls.UIScrollBar)
{
   mx.controls.UIScrollBar = _loc1_ = function()
   {
      super();
   };
   mx.controls.UIScrollBar extends mx.controls.scrollClasses.ScrollBar;
   var _loc2_ = _loc1_.prototype;
   _loc2_.init = function(Void)
   {
      super.init();
      this.textField.owner = this;
      this.__set__horizontal(this.wasHorizontal);
      if(this.__get__horizontal())
      {
         this.textField != undefined ? super.setSize(this.textField._width, 16) : super.setSize(this.__width, this.__height);
      }
      else
      {
         this.textField != undefined ? super.setSize(16, this.textField._height) : super.setSize(this.__width, this.__height);
      }
      if(this.__get__horizontal())
      {
         var _loc3_ = this.__width;
         this.__height = this.__width;
         this.width = _loc3_;
         this.__width = 16;
      }
      this.textField.onScroller = function()
      {
         this.hPosition = this.hscroll;
         this.vPosition = this.scroll - 1;
      };
      if(this.__get___targetInstanceName() != undefined)
      {
         this.setScrollTarget(this.__get___targetInstanceName());
         this.__get___targetInstanceName().addListener(this);
      }
   };
   _loc2_.__get___targetInstanceName = function()
   {
      return this.textField;
   };
   _loc2_.__get__height = function()
   {
      if(this.wasHorizontal)
      {
         return this.__width;
      }
      else
      {
         return this.__height;
      }
   };
   _loc2_.__get__width = function()
   {
      if(this.wasHorizontal)
      {
         return this.__height;
      }
      else
      {
         return this.__width;
      }
   };
   _loc2_.size = function(Void)
   {
      super.size();
      this.onTextChanged();
   };
   _loc2_.draw = function()
   {
      super.draw();
   };
   _loc2_.__set___targetInstanceName = function(t)
   {
      if(t == undefined)
      {
         this.textField.removeListener(this);
         delete this.textField[this.__get__horizontal() ? "hScroller" : "vScroller"];
         if(this.textField.hScroller != undefined && this.textField.vScroller != undefined)
         {
            this.textField.unwatch("text");
            this.textField.unwatch("htmltext");
         }
      }
      var _loc3_ = this._parent[t];
      this.textField = this._parent[t];
      this.onTextChanged();
      return this.__get___targetInstanceName();
   };
   _loc2_.setSize = function(w, h)
   {
      if(this.__get__horizontal())
      {
         super.setSize(h, w);
      }
      else
      {
         super.setSize(w, h);
      }
   };
   _loc2_.onTextChanged = function(Void)
   {
      if(this.textField == undefined)
      {
         return;
      }
      clearInterval(this.synchScroll);
      if(this.__get__horizontal())
      {
         var _loc3_ = this.textField.hscroll;
         this.setScrollProperties(this.textField._width, 0, this.textField.maxhscroll);
         this.__set__scrollPosition(Math.min(_loc3_, this.textField.maxhscroll));
      }
      else
      {
         _loc3_ = this.textField.scroll;
         var _loc2_ = this.textField.bottomScroll - this.textField.scroll;
         this.setScrollProperties(_loc2_, 1, this.textField.maxscroll);
         this.__set__scrollPosition(Math.min(_loc3_, this.textField.maxscroll));
      }
   };
   _loc2_.__get__horizontal = function()
   {
      return this.wasHorizontal;
   };
   _loc2_.__set__horizontal = function(v)
   {
      this.wasHorizontal = v;
      if(v and this.initializing)
      {
         if(this._rotation == 90)
         {
            return;
         }
         this._xscale = -100;
         this._rotation = -90;
      }
      if(!this.initializing)
      {
         if(v)
         {
            if(this._rotation == 0)
            {
               this._rotation = -90;
               this._xscale = -100;
            }
         }
         else if(this._rotation == -90)
         {
            this._rotation = 0;
            this._xscale = 100;
         }
      }
      return this.__get__horizontal();
   };
   _loc2_.callback = function(prop, oldval, newval)
   {
      clearInterval(this.hScroller.synchScroll);
      clearInterval(this.vScroller.synchScroll);
      this.hScroller.synchScroll = setInterval(this.hScroller, "onTextChanged", 50);
      this.vScroller.synchScroll = setInterval(this.vScroller, "onTextChanged", 50);
      return newval;
   };
   _loc2_.setScrollTarget = function(tF)
   {
      if(tF == undefined)
      {
         this.textField.removeListener(this);
         delete this.textField[this.__get__horizontal() ? "hScroller" : "vScroller"];
         if(this.textField.hScroller != undefined && this.textField.vScroller != undefined)
         {
            this.textField.unwatch("text");
            this.textField.unwatch("htmltext");
         }
      }
      this.textField = undefined;
      if(!(tF instanceof TextField))
      {
         return;
      }
      this.textField = tF;
      if(this.__get__horizontal())
      {
         this.textField.hScroller = this;
         this.textField.hScroller.lineScrollSize = 5;
      }
      else
      {
         this.textField.vScroller = this;
         this.textField.vScroller.lineScrollSize = 1;
      }
      this.onTextChanged();
      this.onChanged = function(Void)
      {
         this.onTextChanged();
      };
      this.onScroller = function(Void)
      {
         if(!this.isScrolling)
         {
            if(!this.horizontal)
            {
               this.scrollPosition = this.textField.scroll;
            }
            else
            {
               this.scrollPosition = this.textField.hscroll;
            }
         }
      };
      this.textField.addListener(this);
      this.textField.watch("text", this.callback);
      this.textField.watch("htmlText", this.callback);
   };
   _loc2_.scrollHandler = function(Void)
   {
      if(this.__get__horizontal())
      {
         var _loc2_ = this.textField.background;
         this.textField.hscroll = this.scrollPosition;
         this.textField.background = _loc2_;
      }
      else
      {
         this.textField.scroll = this.scrollPosition;
      }
   };
   _loc2_.setEnabled = function(enable)
   {
      super.setEnabled(enable);
      if(enable)
      {
         this.textField.addListener(this);
      }
      else
      {
         this.textField.removeListener();
      }
   };
   _loc2_.dispatchScrollEvent = function(detail)
   {
      this.dispatchEvent({type: "scroll"});
   };
   _loc1_.symbolName = "UIScrollBar";
   _loc1_.symbolOwner = mx.controls.UIScrollBar;
   _loc2_.className = "UIScrollBar";
   _loc2_.clipParameters = {_targetInstanceName: 1, horizontal: 1};
   _loc1_.mergedClipParameters = mx.core.UIObject.mergeClipParameters(mx.controls.UIScrollBar.prototype.clipParameters);
   _loc1_.version = "2.0.2.127";
   _loc2_.addProperty("_targetInstanceName", _loc2_.__get___targetInstanceName, _loc2_.__set___targetInstanceName);
   _loc2_.addProperty("height", _loc2_.__get__height, function()
   {
   });
   _loc2_.addProperty("horizontal", _loc2_.__get__horizontal, _loc2_.__set__horizontal);
   _loc2_.addProperty("width", _loc2_.__get__width, function()
   {
   });
   ASSetPropFlags(mx.controls.UIScrollBar.prototype, null, 1);
}
