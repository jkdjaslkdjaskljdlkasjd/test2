// ------------------------------------------------------------------------------- menu de habilidades en 2K
// La pagina de habilidades del menu (KRINMENU fotograma 25) ocupa el ancho 16:9 (x de -111 a 911 en coordenadas de
// _root) en lugar del recuadro de 800 con las bandas borrosas a los costados:
//  - el panel rojo se estira hasta 14 unidades del borde y baja hasta 470 (la barra de navegacion empieza en 480);
//  - los recuadros laterales se ensanchan (el del arbol hacia la izquierda y el de la barra de combate hacia la
//    derecha) y los tres bajan hasta 449,5; el del centro conserva su ancho y el de atributos baja con su contenido;
//  - el arbol (el de clase y el del lobo) usa la grilla __rw2kGrid, con los iconos al 140 %; la barra de combate
//    crece al 118 % y el Ability Pool al 119 %;
//  - mientras el menu esta abierto se ocultan los reflejos de la capa 16:9 (__wsFondo.L y .R);
//  - el panel de Aspectos de la NULL ZONE (rw_70_ui.as, __rwAspGeo) usa el mismo panel y los mismos recuadros.
// El panel, los recuadros y la cruz son las mismas piezas de las otras paginas del menu (inventario, tienda, datos,
// opciones, logros): al cambiar de pagina vuelven a su lugar (__v92Cleanup, que llama cada pagina al entrar). Todo
// se aplica por codigo sobre las piezas del juego, sin tocar sus dibujos; con __rw2kEnabled = false queda el menu
// de 800 de I29.
_root.__rw2kEnabled = true;
// geometria en coordenadas de _root (bordes visibles de cada pieza)
_root.__rw2kL = {panel: [-97, 14.95, 897, 470], left: [-68, 73.4, 293.95, 449.5], right: [506.3, 73.4, 868, 449.5], midTop: [74.09, 320.45], dyAttr: 29.9, dyUp: 14.95, dxClose: 114.25, dxTabs: -112.9, treeCx: 112.975, rightCx: 687.15, selY: 179.5, selK: 1.18, poolY: 287, poolK: 1.19};
// grilla del arbol en 2K: columnas cada 70 centradas en el recuadro, filas cada 45 y nodos al 140 %; el resto
// (canos, anillo, emblema, niveles y selector de pagina) en proporcion
_root.__rw2kGrid = {x0: 7.975, dx: 70, y0: 121, dy: 45, ns: 140, pipe: 8, core: 3, ring: 19.6, ringW: 3, ex: -49, ey: 91, esz: 28, tx: 245, tw: 46, tsz: 10, px: [46.975, 118.975], pdot: 106.975, pw: 60, py: 420, pbar: 439, pu0: 14, pu1: 46, psz: 12};
_root.__rw2kPage = function()
{
   var K = _root.KRINMENU;
   return _root.__rw2kEnabled == true && K != undefined && K._currentframe == 25;
};
// hijos del menu por profundidad de la linea de tiempo (clips, textos y botones; las formas no se pueden mover)
_root.__rw2kKids = function(K)
{
   var m = {};
   for(var k in K)
   {
      var o = K[k];
      if((typeof o == "movieclip" || o instanceof TextField || o instanceof Button) && o._parent == K)
      {
         m[o.getDepth() + 16384] = o;
      }
   }
   // los clips tambien por profundidad (por si el recorrido no los lista)
   var D = [2, 5, 7, 21, 23, 657, 675, 1431];
   var i = 0;
   while(i < D.length)
   {
      if(m[D[i]] == undefined)
      {
         var c = K.getInstanceAtDepth(D[i] - 16384);
         if(typeof c == "movieclip" && c._parent == K)
         {
            m[D[i]] = c;
         }
      }
      i++;
   }
   return m;
};
// transformacion original de una pieza (se guarda la primera vez que se toca)
_root.__rw2kOrig = function(mc)
{
   if(mc.__rw2kO == undefined)
   {
      mc.__rw2kO = [mc._x, mc._y, mc._xscale, mc._yscale];
   }
   return mc.__rw2kO;
};
_root.__rw2kPut = function(mc, x, y, sx, sy)
{
   if(!mc)
   {
      return null;
   }
   _root.__rw2kOrig(mc);
   mc._x = x;
   mc._y = y;
   if(sx != undefined)
   {
      mc._xscale = sx;
      mc._yscale = sy;
   }
};
// mueve una pieza respecto de su lugar original (dx, dy en unidades del menu)
_root.__rw2kShift = function(mc, dx, dy)
{
   if(!mc)
   {
      return null;
   }
   var o = _root.__rw2kOrig(mc);
   mc._x = o[0] + dx;
   mc._y = o[1] + dy;
};
// estira una pieza para que sus bordes visibles queden en el rectangulo dado (coordenadas de _root)
_root.__rw2kFit = function(K, mc, r)
{
   if(!mc)
   {
      return null;
   }
   _root.__rw2kOrig(mc);
   var b = mc.getBounds(mc);
   var kx = K._xscale / 100;
   var ky = K._yscale / 100;
   var x0 = (r[0] - K._x) / kx;
   var y0 = (r[1] - K._y) / ky;
   var sx = ((r[2] - K._x) / kx - x0) / (b.xMax - b.xMin);
   var sy = ((r[3] - K._y) / ky - y0) / (b.yMax - b.yMin);
   mc._xscale = sx * 100;
   mc._yscale = sy * 100;
   mc._x = x0 - sx * b.xMin;
   mc._y = y0 - sy * b.yMin;
};
// estira solo en vertical (el recuadro de arriba del centro)
_root.__rw2kFitY = function(K, mc, y0r, y1r)
{
   if(!mc)
   {
      return null;
   }
   _root.__rw2kOrig(mc);
   var b = mc.getBounds(mc);
   var ky = K._yscale / 100;
   var y0 = (y0r - K._y) / ky;
   var sy = ((y1r - K._y) / ky - y0) / (b.yMax - b.yMin);
   mc._yscale = sy * 100;
   mc._y = y0 - sy * b.yMin;
};
// centra un titulo (campo de texto centrado) en x (coordenadas de _root); dy respecto de su lugar original
_root.__rw2kTitle = function(K, f, cx, dy)
{
   if(!f)
   {
      return null;
   }
   var o = _root.__rw2kOrig(f);
   f._x = (cx - K._x) / (K._xscale / 100) - f._width / 2 + 2;
   f._y = o[1] + dy;
};
// piezas que comparten las otras paginas: vuelven a su transformacion original
_root.__rw2kRestore = function(K)
{
   var m = _root.__rw2kKids(K);
   var D = [2, 5, 7, 21, 23, 1431, 1434];
   var i = 0;
   while(i < D.length)
   {
      var mc = m[D[i]];
      if(mc && mc.__rw2kO != undefined)
      {
         var o = mc.__rw2kO;
         mc._x = o[0];
         mc._y = o[1];
         mc._xscale = o[2];
         mc._yscale = o[3];
         mc.__rw2kO = undefined;
      }
      i++;
   }
   K.__rw2kGen = undefined;
};
_root.__rw2kApply = function()
{
   var K = _root.KRINMENU;
   var on = _root.__rw2kPage();
   // reflejos de los costados: ocultos con la pagina de habilidades o el panel de Aspectos (tambien en 2K) abiertos
   var W = _root.__wsFondo;
   if(W)
   {
      var AP = _root.__rwAspPanel;
      var refl = !((on && K._visible) || (_root.__rw2kEnabled == true && AP != undefined && AP._parent == _root));
      if(W.L._visible != refl)
      {
         W.L._visible = refl;
         W.R._visible = refl;
      }
   }
   if(!K)
   {
      return null;
   }
   if(!on)
   {
      if(K.__rw2kGen != undefined)
      {
         _root.__rw2kRestore(K);
      }
      return null;
   }
   var L = _root.__rw2kL;
   // las piezas de la pagina se crean de nuevo cada vez que se entra al fotograma 25 (el Ability Pool es una de
   // ellas): una vez por entrada se acomoda todo; en cada fotograma, las pestanas y el arbol de clase
   if(K.__rw2kGen !== K.talentPool)
   {
      var m = _root.__rw2kKids(K);
      _root.__rw2kFit(K, m[2], L.panel);
      _root.__rw2kFit(K, m[7], L.left);
      _root.__rw2kFit(K, m[5], L.right);
      _root.__rw2kFitY(K, m[23], L.midTop[0], L.midTop[1]);
      _root.__rw2kShift(m[21], 0, L.dyAttr);
      var a = [643, 644, 645, 646, 647, 648, 649, 650, 657, 659, 662, 665, 668, 671];
      var i = 0;
      while(i < a.length)
      {
         _root.__rw2kShift(m[a[i]], 0, L.dyAttr);
         i++;
      }
      _root.__rw2kShift(m[675], 0, L.dyUp);
      _root.__rw2kShift(m[1431], L.dxClose, 0);
      _root.__rw2kShift(m[1434], L.dxClose, 0);
      _root.__rw2kTitle(K, m[673], L.treeCx, 0);
      _root.__rw2kTitle(K, m[672], L.rightCx, 0);
      // Ability Pool: su mascara mide 217,35 x 133,05 desde el origen; el titulo baja lo mismo que la lista
      var pool = K.talentPool;
      if(pool)
      {
         var po = _root.__rw2kOrig(pool);
         _root.__rw2kTitle(K, m[674], L.rightCx, L.poolY - (K._y + po[1]));
         var ps = po[2] * L.poolK;
         _root.__rw2kPut(pool, L.rightCx - K._x - 217.35 * ps / 200, L.poolY - K._y, ps, ps);
      }
      var sel = K.selector;
      if(sel)
      {
         var so = _root.__rw2kOrig(sel);
         _root.__rw2kPut(sel, L.rightCx - K._x, L.selY - K._y, so[2] * L.selK, so[3] * L.selK);
      }
      K.__rw2kGen = K.talentPool;
   }
   // pestanas Class / Mokoshotar (las crea __nzTick en coordenadas de _root)
   var T9 = _root.__v9Tabs;
   if(T9 && T9._parent)
   {
      T9._x = L.dxTabs - K._x;
   }
   // arbol de clase: la misma grilla que el del lobo, con los nodos y los canos al 140 %
   var tf = K.talenttreefull;
   if(tf)
   {
      var G = _root.__rw2kGrid;
      var s = G.ns / 100;
      _root.__rw2kPut(tf, G.x0 - K._x, G.y0 - K._y, G.ns, G.ns);
      var moved = false;
      var n = 0;
      while(n < 40)
      {
         var st = tf["st" + n];
         if(st)
         {
            var o = _root.__rw2kOrig(st);
            var tx = Math.round((o[0] - 41.4) / 52) * G.dx / s;
            var ty = Math.round((o[1] - 49.9) / 40) * G.dy / s;
            if(Math.abs(st._x - tx) > 0.2 || Math.abs(st._y - ty) > 0.2)
            {
               st._x = tx;
               st._y = ty;
               moved = true;
            }
         }
         n++;
      }
      if(moved && typeof tf.krinRemakeTree == "function")
      {
         tf.krinRemakeTree();
      }
   }
};
// al entrar a otra pagina del menu (cada una llama a __v92Cleanup) las piezas compartidas vuelven a su lugar antes
// de dibujarse; al entrar a la de habilidades, __v8Sync (KrinCreateAbilityMatrix) acomoda la pagina
_root.__rw2kPrevCleanup = _root.__v92Cleanup;
_root.__v92Cleanup = function()
{
   _root.__rw2kApply();
   return _root.__rw2kPrevCleanup.apply(this, arguments);
};
_root.__rw2kPrevSync = _root.__v8Sync;
_root.__v8Sync = function()
{
   var r = _root.__rw2kPrevSync.apply(this, arguments);
   _root.__rw2kApply();
   return r;
};
_root.__rw2kPrevTick = _root.__rwTick;
_root.__rwTick = function()
{
   _root.__rw2kPrevTick();
   _root.__rw2kApply();
};
