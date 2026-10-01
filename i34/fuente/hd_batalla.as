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
   _root.__hdCamSync();
   _root.__hdDialogo();
   c.onEnterFrame = function()
   {
      _root.__hdCamSync();
      _root.__hdDialogo();
   };
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
// --- Camara (I33-I34): como en el juego original, el cielo queda quieto y el suelo sigue a la camara.
// El juego hace zoom (hasta x1,19 hacia el objetivo) y sacude solo BATTLESCREEN (personajes y suelo original).
// La imagen HD va en dos capas (capas.py): el cielo (la imagen entera) queda quieta y el suelo
// (__hdGround, la misma imagen con alfa por encima del pie de las montanas) copia la transformacion de
// BATTLESCREEN. Si un fondo no tiene capa de suelo, se mueve el contenedor entero (como I33).
_root.__hdCamR = 1.03;
_root.__hdCamSync = function()
{
   if(_root.__hdBattleOn != true)
   {
      return null;
   }
   var c = _root.__hdBattleBG;
   var B = _root.BATTLESCREEN;
   if(!c || !B || B.saverX == undefined)
   {
      return null;
   }
   var g = c.__hdGround;
   var R = 1;
   if(!g)
   {
      g = c;
      R = _root.__hdCamR;
   }
   var kx = B._xscale / 100;
   var ky = B._yscale / 100;
   g._x = B._x + (400 * (1 - R) - B.saverX) * kx;
   g._y = B._y + (287.5 * (1 - R) - B.saverY) * ky;
   g._xscale = 100 * R * kx;
   g._yscale = 100 * R * ky;
   return null;
};
// --- Dialogo (I34): el cuadro de dialogo (combatScript) se achica y va sobre su cuadro del panel de abajo,
// igual que el resto del panel (62 %). El juego lo pone en (21,8 | 473,3; 460,7) cada vez que alguien habla.
_root.__hdDialogo = function()
{
   var cs = _root.combatScript;
   if(_root.__hdBattleOn != true || !cs)
   {
      return null;
   }
   if(cs._y > 459 && cs._y < 462)
   {
      var L = _root.__hdBattleLayout;
      cs._x = L.ax + (cs._x - L.ax) * L.s;
      cs._y = L.ay + L.dy + (cs._y - L.ay) * L.s;
      cs._xscale = 100 * L.s;
      cs._yscale = 100 * L.s;
   }
   return null;
};
_root.__hdBattleVersion = "I34_HD_BATALLA_CAPAS";
