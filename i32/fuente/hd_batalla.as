// I32 - Fondos de combate HD a pantalla completa (capa __hd*).
// El contenedor __hdBattleBG (sprite nuevo, profundidad 58 del fotograma 217) tiene un fotograma por
// escenario de combate con imagen HD, con la misma etiqueta que BATTLESCREEN (_root.Krin.ZoneBG: SNOW, ...).
// Al empezar el combate llama a __hdBattleSetup. Si hay HD para _root.Krin.ZoneBG:
//   - se ve la imagen HD a pantalla completa y se ocultan el panel gris de arriba (3303), el marco de la
//     ventana (3309), el cielo original (3328) y el suelo original (BATTLESCREEN.__hdSuelo); las barras quedan;
//   - la mascara de la escena (__hdMask) pasa a cubrir toda la pantalla;
//   - el panel de abajo se achica y se centra como la barra del World Map (62 %, ancla (400, 575), -12).
// Si no hay HD, el combate queda clasico. Para apagarlo: _root.__hdBattleEnabled = false.
_root.__hdBattleEnabled = true;
_root.__hdBattleLayout = {s: 0.62, ax: 400, ay: 575, dy: -12};
_root.__hdDepthClip = function(d)
{
   var o = _root.getInstanceAtDepth(d - 16384);
   if(o == undefined || o == _root)
   {
      return null;
   }
   return o;
};
_root.__hdBattleSetup = function(c)
{
   _root.__hdBattleOn = false;
   if(!c)
   {
      return null;
   }
   c.gotoAndStop(1);
   if(_root.__hdBattleEnabled == true && _root.Krin.ZoneBG != undefined)
   {
      c.gotoAndStop(_root.Krin.ZoneBG);
   }
   var hd = c._currentframe > 1;
   _root.__hdHideSuelo = hd;
   if(_root.BATTLESCREEN.__hdSuelo)
   {
      _root.BATTLESCREEN.__hdSuelo._visible = !hd;
   }
   if(!hd)
   {
      c._visible = false;
      return null;
   }
   c._visible = true;
   _root.__hdBattleOn = true;
   var hide = [59, 70, 73];
   var i = 0;
   while(i < hide.length)
   {
      var h = _root.__hdDepthClip(hide[i]);
      if(h)
      {
         h._visible = false;
      }
      i++;
   }
   _root.__hdMarco._visible = false;
   var mk = _root.__hdMask;
   if(mk)
   {
      mk._x = -111.11;
      mk._y = 0;
      mk._xscale = 102222;
      mk._yscale = 57500;
   }
   var L = _root.__hdBattleLayout;
   var a = [_root.UI_BAR, _root.__hdDepthClip(65), _root.battleClocker, _root.krinToMove, _root.krinToMove2, _root.moveSelectBoomer, _root.__hdSkipX, _root.__hdSkipXbg];
   i = 0;
   while(i < a.length)
   {
      var o = a[i];
      if(o != undefined && o != _root)
      {
         o._x = L.ax + (o._x - L.ax) * L.s;
         o._y = L.ay + L.dy + (o._y - L.ay) * L.s;
         o._xscale *= L.s;
         o._yscale *= L.s;
      }
      i++;
   }
   return null;
};
_root.__hdBattleVersion = "I32_HD_BATALLA";
