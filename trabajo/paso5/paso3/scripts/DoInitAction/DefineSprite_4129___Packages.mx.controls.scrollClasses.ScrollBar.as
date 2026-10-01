// DefineSprite_4129___Packages.mx.controls.scrollClasses.ScrollBar
// origen: DoInitAction del sprite 4129 (03786_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.controls)
{
   _global.mx.controls = new Object();
}
if(!_global.mx.controls.scrollClasses)
{
   _global.mx.controls.scrollClasses = new Object();
}
if(!_global.mx.controls.scrollClasses.ScrollBar)
{
   mx.controls.scrollClasses.ScrollBar = _loc1_ = function()
   {
      super();
   };
   mx.controls.scrollClasses.ScrollBar extends mx.core.UIComponent;
   var _loc2_ = _loc1_.prototype;
   _loc2_.__get__scrollPosition = function()
   {
      return this._scrollPosition;
   };
   _loc2_.__set__scrollPosition = function(pos)
   {
      this._scrollPosition = pos;
      if(this.isScrolling != true)
      {
         pos = Math.min(pos, this.maxPos);
         pos = Math.max(pos, this.minPos);
         var _loc3_ = (pos - this.minPos) * (this.scrollTrack_mc.height - this.scrollThumb_mc._height) / (this.maxPos - this.minPos) + this.scrollTrack_mc.top;
         this.scrollThumb_mc.move(0, _loc3_);
      }
      return this.__get__scrollPosition();
   };
   _loc2_.__get__pageScrollSize = function()
   {
      return this.largeScroll;
   };
   _loc2_.__set__pageScrollSize = function(lScroll)
   {
      this.largeScroll = lScroll;
      return this.__get__pageScrollSize();
   };
   _loc2_.__set__lineScrollSize = function(sScroll)
   {
      this.smallScroll = sScroll;
      return this.__get__lineScrollSize();
   };
   _loc2_.__get__lineScrollSize = function()
   {
      return this.smallScroll;
   };
   _loc2_.__get__virtualHeight = function()
   {
      return this.__height;
   };
   _loc2_.init = function(Void)
   {
      super.init();
      this._scrollPosition = 0;
      this.tabEnabled = false;
      this.focusEnabled = false;
      this.boundingBox_mc._visible = false;
      this.boundingBox_mc._width = this.boundingBox_mc._height = 0;
   };
   _loc2_.createChildren = function(Void)
   {
      if(this.scrollTrack_mc == undefined)
      {
         this.setSkin(mx.controls.scrollClasses.ScrollBar.skinIDTrack, this.scrollTrackName);
      }
      this.scrollTrack_mc.visible = false;
      var _loc3_ = new Object();
      _loc3_.enabled = false;
      _loc3_.preset = mx.controls.SimpleButton.falseDisabled;
      _loc3_.initProperties = 0;
      _loc3_.autoRepeat = true;
      _loc3_.tabEnabled = false;
      var _loc2_ = undefined;
      if(this.upArrow_mc == undefined)
      {
         _loc2_ = this.createButton(this.upArrowName, "upArrow_mc", mx.controls.scrollClasses.ScrollBar.skinIDUpArrow, _loc3_);
      }
      _loc2_.buttonDownHandler = this.onUpArrow;
      _loc2_.clickHandler = this.onScrollChanged;
      this._minHeight = _loc2_.height;
      this._minWidth = _loc2_.width;
      if(this.downArrow_mc == undefined)
      {
         _loc2_ = this.createButton(this.downArrowName, "downArrow_mc", mx.controls.scrollClasses.ScrollBar.skinIDDownArrow, _loc3_);
      }
      _loc2_.buttonDownHandler = this.onDownArrow;
      _loc2_.clickHandler = this.onScrollChanged;
      this._minHeight += _loc2_.height;
   };
   _loc2_.createButton = function(linkageName, id, skinID, o)
   {
      if(skinID == mx.controls.scrollClasses.ScrollBar.skinIDUpArrow)
      {
         o.falseUpSkin = this.upArrowUpName;
         o.falseDownSkin = this.upArrowDownName;
         o.falseOverSkin = this.upArrowOverName;
      }
      else
      {
         o.falseUpSkin = this.downArrowUpName;
         o.falseDownSkin = this.downArrowDownName;
         o.falseOverSkin = this.downArrowOverName;
      }
      var _loc3_ = this.createObject(linkageName, id, skinID, o);
      this[id].visible = false;
      this[id].useHandCursor = false;
      return _loc3_;
   };
   _loc2_.createThumb = function(Void)
   {
      var _loc2_ = new Object();
      _loc2_.validateNow = true;
      _loc2_.tabEnabled = false;
      _loc2_.leftSkin = this.thumbTopName;
      _loc2_.middleSkin = this.thumbMiddleName;
      _loc2_.rightSkin = this.thumbBottomName;
      _loc2_.gripSkin = this.thumbGripName;
      this.createClassObject(mx.controls.scrollClasses.ScrollThumb, "scrollThumb_mc", mx.controls.scrollClasses.ScrollBar.skinIDThumb, _loc2_);
   };
   _loc2_.setScrollProperties = function(pSize, mnPos, mxPos, ls)
   {
      var _loc4_ = undefined;
      var _loc2_ = this.scrollTrack_mc;
      this.pageSize = pSize;
      this.largeScroll = ls != undefined && ls > 0 ? ls : pSize;
      this.minPos = Math.max(mnPos, 0);
      this.maxPos = Math.max(mxPos, 0);
      this._scrollPosition = Math.max(this.minPos, this._scrollPosition);
      this._scrollPosition = Math.min(this.maxPos, this._scrollPosition);
      if(this.maxPos - this.minPos > 0 && this.enabled)
      {
         var _loc5_ = this._scrollPosition;
         if(!this.initializing)
         {
            this.upArrow_mc.enabled = true;
            this.downArrow_mc.enabled = true;
         }
         _loc2_.onPress = _loc2_.onDragOver = this.startTrackScroller;
         _loc2_.onRelease = this.releaseScrolling;
         _loc2_.onDragOut = _loc2_.stopScrolling = this.stopScrolling;
         _loc2_.onReleaseOutside = this.releaseScrolling;
         _loc2_.useHandCursor = false;
         if(this.scrollThumb_mc == undefined)
         {
            this.createThumb();
         }
         var _loc3_ = this.scrollThumb_mc;
         if(this.scrollTrackOverName.length > 0)
         {
            _loc2_.onRollOver = this.trackOver;
            _loc2_.onRollOut = this.trackOut;
         }
         _loc4_ = this.pageSize / (this.maxPos - this.minPos + this.pageSize) * _loc2_.height;
         if(_loc4_ < _loc3_.minHeight)
         {
            if(_loc2_.height < _loc3_.minHeight)
            {
               _loc3_.__set__visible(false);
            }
            else
            {
               _loc4_ = _loc3_.minHeight;
               _loc3_.__set__visible(true);
               _loc3_.setSize(this._minWidth, _loc3_.minHeight + 0);
            }
         }
         else
         {
            _loc3_.__set__visible(true);
            _loc3_.setSize(this._minWidth, _loc4_);
         }
         _loc3_.setRange(this.upArrow_mc.__get__height() + 0, this.__get__virtualHeight() - this.downArrow_mc.__get__height() - _loc3_.__get__height(), this.minPos, this.maxPos);
         _loc5_ = Math.min(_loc5_, this.maxPos);
         this.__set__scrollPosition(Math.max(_loc5_, this.minPos));
      }
      else
      {
         this.scrollThumb_mc.__set__visible(false);
         if(!this.initializing)
         {
            this.upArrow_mc.enabled = false;
            this.downArrow_mc.enabled = false;
         }
         delete _loc2_.onPress;
         delete _loc2_.onDragOver;
         delete _loc2_.onRelease;
         delete _loc2_.onDragOut;
         delete _loc2_.onRollOver;
         delete _loc2_.onRollOut;
         delete _loc2_.onReleaseOutside;
      }
      if(this.initializing)
      {
         this.scrollThumb_mc.__set__visible(false);
      }
   };
   _loc2_.setEnabled = function(enabledFlag)
   {
      super.setEnabled(enabledFlag);
      this.setScrollProperties(this.pageSize, this.minPos, this.maxPos, this.largeScroll);
   };
   _loc2_.draw = function(Void)
   {
      if(this.initializing)
      {
         this.initializing = false;
         this.scrollTrack_mc.visible = true;
         this.upArrow_mc.__set__visible(true);
         this.downArrow_mc.__set__visible(true);
      }
      this.size();
   };
   _loc2_.size = function(Void)
   {
      if(this._height == 1)
      {
         return;
      }
      if(this.upArrow_mc == undefined)
      {
         return;
      }
      var _loc3_ = this.upArrow_mc.__get__height();
      var _loc2_ = this.downArrow_mc.__get__height();
      this.upArrow_mc.move(0, 0);
      var _loc4_ = this.scrollTrack_mc;
      _loc4_._y = _loc3_;
      _loc4_._height = this.__get__virtualHeight() - _loc3_ - _loc2_;
      this.downArrow_mc.move(0, this.__get__virtualHeight() - _loc2_);
      this.setScrollProperties(this.pageSize, this.minPos, this.maxPos, this.largeScroll);
   };
   _loc2_.dispatchScrollEvent = function(detail)
   {
      this.dispatchEvent({type: "scroll", detail: detail});
   };
   _loc2_.isScrollBarKey = function(k)
   {
      if(k == 36)
      {
         if(this.__get__scrollPosition() != 0)
         {
            this.__set__scrollPosition(0);
            this.dispatchScrollEvent(this.minMode);
         }
         return true;
      }
      else if(k == 35)
      {
         if(this.__get__scrollPosition() < this.maxPos)
         {
            this.__set__scrollPosition(this.maxPos);
            this.dispatchScrollEvent(this.maxMode);
         }
         return true;
      }
      return false;
   };
   _loc2_.scrollIt = function(inc, mode)
   {
      var _loc3_ = this.smallScroll;
      if(inc != "Line")
      {
         _loc3_ = this.largeScroll == 0 ? this.pageSize : this.largeScroll;
      }
      var _loc2_ = this._scrollPosition + mode * _loc3_;
      if(_loc2_ > this.maxPos)
      {
         _loc2_ = this.maxPos;
      }
      else if(_loc2_ < this.minPos)
      {
         _loc2_ = this.minPos;
      }
      if(this.__get__scrollPosition() != _loc2_)
      {
         this.__set__scrollPosition(_loc2_);
         var _loc4_ = mode < 0 ? this.minusMode : this.plusMode;
         this.dispatchScrollEvent(inc + _loc4_);
      }
   };
   _loc2_.startTrackScroller = function(Void)
   {
      this._parent.pressFocus();
      if(this._parent.scrollTrackDownName.length > 0)
      {
         if(this._parent.scrollTrackDown_mc == undefined)
         {
            this._parent.setSkin(mx.controls.scrollClasses.ScrollBar.skinIDTrackDown, this.scrollTrackDownName);
         }
         else
         {
            this._parent.scrollTrackDown_mc.visible = true;
         }
      }
      this._parent.trackScroller();
      this._parent.scrolling = setInterval(this._parent, "scrollInterval", this.getStyle("repeatDelay"), "Page", -1);
   };
   _loc2_.scrollInterval = function(inc, mode)
   {
      clearInterval(this.scrolling);
      if(inc == "Page")
      {
         this.trackScroller();
      }
      else
      {
         this.scrollIt(inc, mode);
      }
      this.scrolling = setInterval(this, "scrollInterval", this.getStyle("repeatInterval"), inc, mode);
   };
   _loc2_.trackScroller = function(Void)
   {
      if(this.scrollThumb_mc._y + this.scrollThumb_mc.__get__height() < this._ymouse)
      {
         this.scrollIt("Page", 1);
      }
      else if(this.scrollThumb_mc._y > this._ymouse)
      {
         this.scrollIt("Page", -1);
      }
   };
   _loc2_.dispatchScrollChangedEvent = function(Void)
   {
      this.dispatchEvent({type: "scrollChanged"});
   };
   _loc2_.stopScrolling = function(Void)
   {
      clearInterval(this._parent.scrolling);
      this._parent.scrollTrackDown_mc.visible = false;
   };
   _loc2_.releaseScrolling = function(Void)
   {
      this._parent.releaseFocus();
      this.stopScrolling();
      this._parent.dispatchScrollChangedEvent();
   };
   _loc2_.trackOver = function(Void)
   {
      if(this._parent.scrollTrackOverName.length > 0)
      {
         if(this._parent.scrollTrackOver_mc == undefined)
         {
            this._parent.setSkin(mx.controls.scrollClasses.ScrollBar.skinIDTrackOver, this.scrollTrackOverName);
         }
         else
         {
            this._parent.scrollTrackOver_mc.visible = true;
         }
      }
   };
   _loc2_.trackOut = function(Void)
   {
      this._parent.scrollTrackOver_mc.visible = false;
   };
   _loc2_.onUpArrow = function(Void)
   {
      this._parent.scrollIt("Line", -1);
   };
   _loc2_.onDownArrow = function(Void)
   {
      this._parent.scrollIt("Line", 1);
   };
   _loc2_.onScrollChanged = function(Void)
   {
      this._parent.dispatchScrollChangedEvent();
   };
   _loc1_.symbolOwner = mx.core.UIComponent;
   _loc2_.className = "ScrollBar";
   _loc2_.minPos = 0;
   _loc2_.maxPos = 0;
   _loc2_.pageSize = 0;
   _loc2_.largeScroll = 0;
   _loc2_.smallScroll = 1;
   _loc2_._scrollPosition = 0;
   _loc2_.scrollTrackName = "ScrollTrack";
   _loc2_.scrollTrackOverName = "";
   _loc2_.scrollTrackDownName = "";
   _loc2_.upArrowName = "BtnUpArrow";
   _loc2_.upArrowUpName = "ScrollUpArrowUp";
   _loc2_.upArrowOverName = "ScrollUpArrowOver";
   _loc2_.upArrowDownName = "ScrollUpArrowDown";
   _loc2_.downArrowName = "BtnDownArrow";
   _loc2_.downArrowUpName = "ScrollDownArrowUp";
   _loc2_.downArrowOverName = "ScrollDownArrowOver";
   _loc2_.downArrowDownName = "ScrollDownArrowDown";
   _loc2_.thumbTopName = "ScrollThumbTopUp";
   _loc2_.thumbMiddleName = "ScrollThumbMiddleUp";
   _loc2_.thumbBottomName = "ScrollThumbBottomUp";
   _loc2_.thumbGripName = "ScrollThumbGripUp";
   _loc1_.skinIDTrack = 0;
   _loc1_.skinIDTrackOver = 1;
   _loc1_.skinIDTrackDown = 2;
   _loc1_.skinIDUpArrow = 3;
   _loc1_.skinIDDownArrow = 4;
   _loc1_.skinIDThumb = 5;
   _loc2_.idNames = new Array("scrollTrack_mc", "scrollTrackOver_mc", "scrollTrackDown_mc", "upArrow_mc", "downArrow_mc");
   _loc2_.clipParameters = {minPos: 1, maxPos: 1, pageSize: 1, scrollPosition: 1, lineScrollSize: 1, pageScrollSize: 1, visible: 1, enabled: 1};
   _loc1_.mergedClipParameters = mx.core.UIObject.mergeClipParameters(mx.controls.scrollClasses.ScrollBar.prototype.clipParameters, mx.core.UIComponent.prototype.clipParameters);
   _loc2_.initializing = true;
   _loc2_.addProperty("lineScrollSize", _loc2_.__get__lineScrollSize, _loc2_.__set__lineScrollSize);
   _loc2_.addProperty("pageScrollSize", _loc2_.__get__pageScrollSize, _loc2_.__set__pageScrollSize);
   _loc2_.addProperty("scrollPosition", _loc2_.__get__scrollPosition, _loc2_.__set__scrollPosition);
   _loc2_.addProperty("virtualHeight", _loc2_.__get__virtualHeight, function()
   {
   });
   ASSetPropFlags(mx.controls.scrollClasses.ScrollBar.prototype, null, 1);
}
