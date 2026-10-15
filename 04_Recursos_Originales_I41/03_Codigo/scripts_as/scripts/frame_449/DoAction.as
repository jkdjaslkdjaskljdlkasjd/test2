thingerDepthK = 0;
stop();
toGive = 0;
toGive = questHub.length;
if(achGet[4] == 0)
{
   toGive = questHub.length - 1;
}
if(Krin.difficulty == 1)
{
   toGive = questHub.length - 1;
}
if(Krin.difficulty == 0)
{
   toGive = questHub.length - 2;
}
i = 1;
while(i < toGive)
{
   krinMapper["mb" + i].sectionID = i;
   if(i > 1)
   {
      krinMapper.lineMC.createEmptyMovieClip("line_mc" + thingerDepthK,thingerDepthK);
      krinMapper.lineMC["line_mc" + thingerDepthK].lineStyle(6,0,100);
      krinMapper.lineMC["line_mc" + thingerDepthK].moveTo(krinMapper["mb" + i]._x,krinMapper["mb" + i]._y);
      krinMapper.lineMC["line_mc" + thingerDepthK].lineTo(krinMapper["mb" + questHub[i].linked]._x,krinMapper["mb" + questHub[i].linked]._y);
      thingerDepthK++;
   }
   if(i == 1 || questHub[questHub[i].linked].progressMax < Krin.questProgress[questHub[i].linked])
   {
      krinMapper["mb" + i].canUse = true;
      if(i > 1)
      {
         krinMapper.lineMC.createEmptyMovieClip("line_mc" + thingerDepthK,thingerDepthK);
         krinMapper.lineMC["line_mc" + thingerDepthK].lineStyle(2,3246559,100);
         krinMapper.lineMC["line_mc" + thingerDepthK].moveTo(krinMapper["mb" + i]._x,krinMapper["mb" + i]._y);
         krinMapper.lineMC["line_mc" + thingerDepthK].lineTo(krinMapper["mb" + questHub[i].linked]._x,krinMapper["mb" + questHub[i].linked]._y);
         thingerDepthK++;
      }
   }
   else
   {
      if(i > 1)
      {
         krinMapper.lineMC.createEmptyMovieClip("line_mc" + thingerDepthK,thingerDepthK);
         krinMapper.lineMC["line_mc" + thingerDepthK].lineStyle(2,3355443,100);
         krinMapper.lineMC["line_mc" + thingerDepthK].moveTo(krinMapper["mb" + i]._x,krinMapper["mb" + i]._y);
         krinMapper.lineMC["line_mc" + thingerDepthK].lineTo(krinMapper["mb" + questHub[i].linked]._x,krinMapper["mb" + questHub[i].linked]._y);
         thingerDepthK++;
      }
      krinMapper["mb" + i].underGF.gotoAndStop("blank");
      krinMapper["mb" + i].canUse = false;
   }
   i++;
}
if(!_root.__nzCatalog)
{
   _root.__nzBuildCatalog();
}
_root.__nzController.removeMovieClip();
_root.createEmptyMovieClip("__nzController",100020);
_root.__nzController.onEnterFrame = function()
{
   _root.__nzTick();
};
_root.createEmptyMovieClip("__nzGate",100000);
_root.__nzGate._x = 400;
_root.__nzGate._y = 285;
_root.__nzGate.attachMovie("__nzMapMarker","icon",1);
_root.__nzGate.icon._width = 44;
_root.__nzGate.icon._height = 44;
var bounds = _root.__nzGate.icon.getBounds(_root.__nzGate);
_root.__nzGate.icon._x = -22 - bounds.xMin;
_root.__nzGate.icon._y = -22 - bounds.yMin;
_root.__nzGate.onRelease = function()
{
   _root.__nzActive = true;
   _root.__nzGate.removeMovieClip();
   _root.gotoAndStop("Navigation");
};
_root.__nzGate.onRollOver = function()
{
   _root.navTitle = "NULL ZONE";
};
_root.__nzGate.onEnterFrame = function()
{
   if(_root._currentframe != 449)
   {
      this.removeMovieClip();
   }
};
_root.__nzGate.createTextField("label",100,-59,29,140,24);
_root.__nzGate.label.setNewTextFormat(new TextFormat("Rockwell",14,14931404));
_root.__nzGate.label.selectable = false;
_root.__nzGate.label.text = "NULL ZONE";
_root.__nzGate.label.embedFonts = true;
var fmt = new TextFormat("Rockwell",14,14931404);
fmt.bold = true;
_root.__nzGate.label.setTextFormat(fmt);
