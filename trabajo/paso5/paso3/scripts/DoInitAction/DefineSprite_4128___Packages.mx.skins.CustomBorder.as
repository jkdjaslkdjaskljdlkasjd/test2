// DefineSprite_4128___Packages.mx.skins.CustomBorder
// origen: DoInitAction del sprite 4128 (03783_DoInitAction.bin)

if(!_global.mx)
{
   _global.mx = new Object();
}
if(!_global.mx.skins)
{
   _global.mx.skins = new Object();
}
if(!_global.mx.skins.CustomBorder)
{
   mx.skins.CustomBorder = _loc1_ = function()
   {
      super();
   };
   mx.skins.CustomBorder extends mx.skins.Border;
   var _loc2_ = _loc1_.prototype;
   _loc2_.__get__width = function()
   {
      return this.__width;
   };
   _loc2_.__get__height = function()
   {
      return this.__height;
   };
   _loc2_.init = function(Void)
   {
      super.init();
   };
   _loc2_.createChildren = function(Void)
   {
   };
   _loc2_.draw = function(Void)
   {
      if(this.l_mc == undefined)
      {
         var _loc2_ = this.setSkin(mx.skins.CustomBorder.tagL, this.leftSkin);
         if(this.horizontal)
         {
            this.minHeight = this.l_mc._height;
            this.minWidth = this.l_mc._width;
         }
         else
         {
            this.minHeight = this.l_mc._height;
            this.minWidth = this.l_mc._width;
         }
      }
      if(this.m_mc == undefined)
      {
         this.setSkin(mx.skins.CustomBorder.tagM, this.middleSkin);
         if(this.horizontal)
         {
            this.minHeight = this.m_mc._height;
            this.minWidth += this.m_mc._width;
         }
         else
         {
            this.minHeight += this.m_mc._height;
            this.minWidth = this.m_mc._width;
         }
      }
      if(this.r_mc == undefined)
      {
         this.setSkin(mx.skins.CustomBorder.tagR, this.rightSkin);
         if(this.horizontal)
         {
            this.minHeight = this.r_mc._height;
            this.minWidth += this.r_mc._width;
         }
         else
         {
            this.minHeight += this.r_mc._height;
            this.minWidth = this.r_mc._width;
         }
      }
      this.size();
   };
   _loc2_.size = function(Void)
   {
      this.l_mc.move(0, 0);
      if(this.horizontal)
      {
         this.r_mc.move(this.__get__width() - this.r_mc.width, 0);
         this.m_mc.move(this.l_mc.width, 0);
         this.m_mc.setSize(this.r_mc.x - this.m_mc.x, this.m_mc.height);
      }
      else
      {
         this.r_mc.move(0, this.__get__height() - this.r_mc.height, 0);
         this.m_mc.move(0, this.l_mc.height);
         this.m_mc.setSize(this.m_mc.width, this.r_mc.y - this.m_mc.y);
      }
   };
   _loc1_.symbolName = "CustomBorder";
   _loc1_.symbolOwner = mx.skins.CustomBorder;
   _loc1_.version = "2.0.2.127";
   _loc2_.className = "CustomBorder";
   _loc1_.tagL = 0;
   _loc1_.tagM = 1;
   _loc1_.tagR = 2;
   _loc2_.idNames = new Array("l_mc", "m_mc", "r_mc");
   _loc2_.leftSkin = "F3PieceLeft";
   _loc2_.middleSkin = "F3PieceMiddle";
   _loc2_.rightSkin = "F3PieceRight";
   _loc2_.horizontal = true;
   _loc2_.addProperty("height", _loc2_.__get__height, function()
   {
   });
   _loc2_.addProperty("width", _loc2_.__get__width, function()
   {
   });
   ASSetPropFlags(mx.skins.CustomBorder.prototype, null, 1);
}
