// I38 - selector de zona en NULL ZONE, para probar los fondos HD sin jugar hasta cada zona.
// No cambia la capa NULL ZONE del usuario: envuelve __nzZoneReady (llama a la original y despues agrega el boton
// «ZONAS»). Al elegir una zona hace lo mismo que el mapa del mundo: fija Krin.sectionIn, pasa por "overMap" y
// vuelve a "Navigation", asi el juego arma la pantalla de zona y la barra de abajo como siempre.
_root.__zsNombres = ["", "Zona 1 - New Alcatraz", "Zona 2 - Oberursel", "Zona 3 - Ivory Line", "Zona 4 - Labyrinth", "Zona 5 - Hew", "Zona 6 - Il Sanctus", "Zona 7 - Japon"];
_root.__zsNativeZoneReady = _root.__nzZoneReady;
_root.__nzZoneReady = function(zone)
{
   _root.__zsNativeZoneReady(zone);
   _root.__zsBoton(zone);
};
_root.__zsBotonNativo = function(holder, name, depth, x, y, w, h, texto)
{
   holder.createEmptyMovieClip(name, depth);
   var b = holder[name];
   b._x = x;
   b._y = y;
   b.attachMovie("__nzNativeButton", "bg", 0);
   b.bg._width = w;
   b.bg._height = h;
   var bounds = b.bg.getBounds(b);
   b.bg._x = 0 - bounds.xMin;
   b.bg._y = 0 - bounds.yMin;
   b.createTextField("caption", 1, 8, (h - 22) / 2, w - 14, 24);
   b.caption.setNewTextFormat(new TextFormat("_sans", 14, 14931404));
   b.caption.selectable = false;
   b.caption.text = texto;
   b.onRollOver = function()
   {
      this._alpha = 80;
   };
   b.onRollOut = function()
   {
      this._alpha = 100;
   };
   return b;
};
_root.__zsBoton = function(zone)
{
   // arriba a la izquierda de la pantalla de zona (zona en 400; 222,9): lejos de los tres orbes y del texto de ayuda
   var b = _root.__zsBotonNativo(zone, "zonas", 113, -495, -212, 150, 34, "ZONAS");
   b.onRelease = function()
   {
      _root.__zsAbrir();
   };
   b.onRollOver = function()
   {
      this._alpha = 80;
      zone.orbHint.text = "ELEGIR ZONA";
   };
   b.onRollOut = function()
   {
      this._alpha = 100;
      zone.orbHint.text = "";
   };
};
_root.__zsAbrir = function()
{
   _root.__zsPanel.removeMovieClip();
   _root.createEmptyMovieClip("__zsPanel", 100013);
   var p = _root.__zsPanel;
   p.attachMovie("__nzNativePanel", "background", 0);
   p.background._width = 400;
   p.background._height = 440;
   var bounds = p.background.getBounds(p);
   p.background._x = 200 - bounds.xMin;
   p.background._y = 50 - bounds.yMin;
   p.background.onRelease = function()
   {
   };
   p.background.useHandCursor = false;
   p.createTextField("title", 1, 238, 66, 330, 35);
   p.title.setNewTextFormat(new TextFormat("Rockwell", 24, 14931404));
   p.title.selectable = false;
   p.title.embedFonts = true;
   p.title.text = "ELEGIR ZONA";
   var fmt = new TextFormat("Rockwell", 24, 14931404);
   fmt.bold = true;
   p.title.setTextFormat(fmt);
   var i = 1;
   while(i <= 7)
   {
      var b = _root.__zsBotonNativo(p, "z" + i, 10 + i, 240, 76 + i * 42, 320, 34, _root.__zsNombres[i]);
      b.zid = i;
      b.onRelease = function()
      {
         _root.__zsIr(this.zid);
      };
      i++;
   }
   var v = _root.__zsBotonNativo(p, "back", 30, 300, 440, 200, 32, "Volver");
   v.onRelease = function()
   {
      _root.__zsPanel.removeMovieClip();
   };
};
_root.__zsIr = function(n)
{
   _root.__zsPanel.removeMovieClip();
   _root.__nzActive = false;
   _root.Krin.sectionIn = n;
   _root.gotoAndStop("overMap");
   _root.__zsSalto.removeMovieClip();
   _root.createEmptyMovieClip("__zsSalto", 100014);
   _root.__zsSalto.onEnterFrame = function()
   {
      this.removeMovieClip();
      _root.gotoAndStop("Navigation");
   };
};
