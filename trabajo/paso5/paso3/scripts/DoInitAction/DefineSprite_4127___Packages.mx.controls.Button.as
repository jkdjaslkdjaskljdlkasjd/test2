// DefineSprite_4127___Packages.mx.controls.Button
// origen: DoInitAction del sprite 4127 (03780_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.controls)
{
   _global.mx.controls = new Object();
}
if(!_global.mx.controls.Button)
{
   mx.controls.Button = _loc1_ = function()
   {
      super();
   };
   mx.controls.Button extends mx.controls.SimpleButton;
   var _loc2_ = _loc1_.prototype;
   _loc2_.init = function(Void)
   {
      super.init();
   };
   _loc2_.draw = function()
   {
      if(this.initializing)
      {
         this.labelPath.visible = true;
      }
      super.draw();
      if(this.initIcon != undefined)
      {
         this._setIcon(this.initIcon);
      }
      delete this.initIcon;
   };
   _loc2_.onRelease = function(Void)
   {
      super.onRelease();
   };
   _loc2_.createChildren = function(Void)
   {
      super.createChildren();
   };
   _loc2_.setSkin = function(tag, linkageName, initobj)
   {
      return super.setSkin(tag, linkageName, initobj);
   };
   _loc2_.viewSkin = function(varName)
   {
      var _loc3_ = this.getState() ? "true" : "false";
      _loc3_ += this.enabled ? this.phase : "disabled";
      super.viewSkin(varName, {styleName: this, borderStyle: _loc3_});
   };
   _loc2_.invalidateStyle = function(c)
   {
      this.labelPath.invalidateStyle(c);
      super.invalidateStyle(c);
   };
   _loc2_.setColor = function(c)
   {
      var _loc2_ = 0;
      while(_loc2_ < 8)
      {
         this[this.idNames[_loc2_]].redraw(true);
         _loc2_++;
      }
   };
   _loc2_.setEnabled = function(enable)
   {
      this.labelPath.enabled = enable;
      super.setEnabled(enable);
   };
   _loc2_.calcSize = function(tag, ref)
   {
      if(this.__width == undefined || this.__height == undefined)
      {
         return;
      }
      if(tag < 7)
      {
         ref.setSize(this.__width, this.__height, true);
      }
   };
   _loc2_.size = function(Void)
   {
      this.setState(this.getState());
      this.setHitArea(this.__width, this.__height);
      var _loc3_ = 0;
      while(_loc3_ < 8)
      {
         var _loc4_ = this.idNames[_loc3_];
         if(typeof this[_loc4_] == "movieclip")
         {
            this[_loc4_].setSize(this.__width, this.__height, true);
         }
         _loc3_++;
      }
      super.size();
   };
   _loc2_.__set__labelPlacement = function(val)
   {
      this.__labelPlacement = val;
      this.invalidate();
      return this.__get__labelPlacement();
   };
   _loc2_.__get__labelPlacement = function()
   {
      return this.__labelPlacement;
   };
   _loc2_.getLabelPlacement = function(Void)
   {
      return this.__labelPlacement;
   };
   _loc2_.setLabelPlacement = function(val)
   {
      this.__labelPlacement = val;
      this.invalidate();
   };
   _loc2_.getBtnOffset = function(Void)
   {
      if(this.getState())
      {
         var _loc2_ = this.btnOffset;
      }
      else if(this.phase == "down")
      {
         _loc2_ = this.btnOffset;
      }
      else
      {
         _loc2_ = 0;
      }
      return _loc2_;
   };
   _loc2_.setView = function(offset)
   {
      var _loc16_ = offset ? this.btnOffset : 0;
      var _loc12_ = this.getLabelPlacement();
      var _loc7_ = 0;
      var _loc6_ = 0;
      var _loc11_ = 0;
      var _loc8_ = 0;
      var _loc5_ = 0;
      var _loc4_ = 0;
      var _loc3_ = this.labelPath;
      var _loc2_ = this.iconName;
      var _loc15_ = _loc3_.textWidth;
      var _loc14_ = _loc3_.textHeight;
      var _loc9_ = this.__width - this.borderW - this.borderW;
      var _loc10_ = this.__height - this.borderW - this.borderW;
      if(_loc2_ != undefined)
      {
         _loc7_ = _loc2_._width;
         _loc6_ = _loc2_._height;
      }
      if(_loc12_ == "left" || _loc12_ == "right")
      {
         if(_loc3_ != undefined)
         {
            _loc3_._width = _loc11_ = Math.min(_loc9_ - _loc7_, _loc15_ + 5);
            _loc3_._height = _loc8_ = Math.min(_loc10_, _loc14_ + 5);
         }
         if(_loc12_ == "right")
         {
            _loc5_ = _loc7_;
            if(this.centerContent)
            {
               _loc5_ += (_loc9_ - _loc11_ - _loc7_) / 2;
            }
            _loc2_._x = _loc5_ - _loc7_;
         }
         else
         {
            _loc5_ = _loc9_ - _loc11_ - _loc7_;
            if(this.centerContent)
            {
               _loc5_ /= 2;
            }
            _loc2_._x = _loc5_ + _loc11_;
         }
         _loc2_._y = _loc4_ = 0;
         if(this.centerContent)
         {
            _loc2_._y = (_loc10_ - _loc6_) / 2;
            _loc4_ = (_loc10_ - _loc8_) / 2;
         }
         if(!this.centerContent)
         {
            _loc2_._y += Math.max(0, (_loc8_ - _loc6_) / 2);
         }
      }
      else
      {
         if(_loc3_ != undefined)
         {
            _loc3_._width = _loc11_ = Math.min(_loc9_, _loc15_ + 5);
            _loc3_._height = _loc8_ = Math.min(_loc10_ - _loc6_, _loc14_ + 5);
         }
         _loc5_ = (_loc9_ - _loc11_) / 2;
         _loc2_._x = (_loc9_ - _loc7_) / 2;
         if(_loc12_ == "top")
         {
            _loc4_ = _loc10_ - _loc8_ - _loc6_;
            if(this.centerContent)
            {
               _loc4_ /= 2;
            }
            _loc2_._y = _loc4_ + _loc8_;
         }
         else
         {
            _loc4_ = _loc6_;
            if(this.centerContent)
            {
               _loc4_ += (_loc10_ - _loc8_ - _loc6_) / 2;
            }
            _loc2_._y = _loc4_ - _loc6_;
         }
      }
      var _loc13_ = this.borderW + _loc16_;
      _loc3_._x = _loc5_ + _loc13_;
      _loc3_._y = _loc4_ + _loc13_;
      _loc2_._x += _loc13_;
      _loc2_._y += _loc13_;
   };
   _loc2_.__set__label = function(lbl)
   {
      this.setLabel(lbl);
      return this.__get__label();
   };
   _loc2_.setLabel = function(label)
   {
      if(label == "")
      {
         this.labelPath.removeTextField();
         this.refresh();
         return;
      }
      if(this.labelPath == undefined)
      {
         var _loc2_ = this.createLabel("labelPath", 200, label);
         _loc2_._width = _loc2_.textWidth + 5;
         _loc2_._height = _loc2_.textHeight + 5;
         if(this.initializing)
         {
            _loc2_.visible = false;
         }
      }
      else
      {
         delete this.labelPath.__text;
         this.labelPath.text = label;
         this.refresh();
      }
   };
   _loc2_.getLabel = function(Void)
   {
      return this.labelPath.__text != undefined ? this.labelPath.__text : this.labelPath.text;
   };
   _loc2_.__get__label = function()
   {
      return this.getLabel();
   };
   _loc2_._getIcon = function(Void)
   {
      return this._iconLinkageName;
   };
   _loc2_.__get__icon = function()
   {
      if(this.initializing)
      {
         return this.initIcon;
      }
      return this._iconLinkageName;
   };
   _loc2_._setIcon = function(linkage)
   {
      if(this.initializing)
      {
         if(linkage == "")
         {
            return;
         }
         this.initIcon = linkage;
      }
      else
      {
         if(linkage == "")
         {
            this.removeIcons();
            return;
         }
         super.changeIcon(0, linkage);
         super.changeIcon(1, linkage);
         super.changeIcon(3, linkage);
         super.changeIcon(4, linkage);
         super.changeIcon(5, linkage);
         this._iconLinkageName = linkage;
         this.refresh();
      }
   };
   _loc2_.__set__icon = function(linkage)
   {
      this._setIcon(linkage);
      return this.__get__icon();
   };
   _loc2_.setHitArea = function(w, h)
   {
      if(this.hitArea_mc == undefined)
      {
         this.createEmptyObject("hitArea_mc", 100);
      }
      var _loc2_ = this.hitArea_mc;
      _loc2_.clear();
      _loc2_.beginFill(16711680);
      _loc2_.drawRect(0, 0, w, h);
      _loc2_.endFill();
      _loc2_.setVisible(false);
   };
   _loc1_.symbolName = "Button";
   _loc1_.symbolOwner = mx.controls.Button;
   _loc2_.className = "Button";
   _loc1_.version = "2.0.2.127";
   _loc2_.btnOffset = 0;
   _loc2_._color = "buttonColor";
   _loc2_.__label = "default value";
   _loc2_.__labelPlacement = "right";
   _loc2_.falseUpSkin = "ButtonSkin";
   _loc2_.falseDownSkin = "ButtonSkin";
   _loc2_.falseOverSkin = "ButtonSkin";
   _loc2_.falseDisabledSkin = "ButtonSkin";
   _loc2_.trueUpSkin = "ButtonSkin";
   _loc2_.trueDownSkin = "ButtonSkin";
   _loc2_.trueOverSkin = "ButtonSkin";
   _loc2_.trueDisabledSkin = "ButtonSkin";
   _loc2_.falseUpIcon = "";
   _loc2_.falseDownIcon = "";
   _loc2_.falseOverIcon = "";
   _loc2_.falseDisabledIcon = "";
   _loc2_.trueUpIcon = "";
   _loc2_.trueDownIcon = "";
   _loc2_.trueOverIcon = "";
   _loc2_.trueDisabledIcon = "";
   _loc2_.clipParameters = {labelPlacement: 1, icon: 1, toggle: 1, selected: 1, label: 1};
   _loc1_.mergedClipParameters = mx.core.UIObject.mergeClipParameters(mx.controls.Button.prototype.clipParameters, mx.controls.SimpleButton.prototype.clipParameters);
   _loc2_.centerContent = true;
   _loc2_.borderW = 1;
   _loc2_.addProperty("icon", _loc2_.__get__icon, _loc2_.__set__icon);
   _loc2_.addProperty("label", _loc2_.__get__label, _loc2_.__set__label);
   _loc2_.addProperty("labelPlacement", _loc2_.__get__labelPlacement, _loc2_.__set__labelPlacement);
   ASSetPropFlags(mx.controls.Button.prototype, null, 1);
}
