// ------------------------------------------------------------------------------- interfaz
// Arbol en dos paginas dentro del menu de habilidades (KRINMENU fotograma 25, contenedor __v92Host), con la
// forma del arbol de clase: la misma grilla de 4x7, el icono oscuro hasta tener un punto y un cano entre cada
// nodo y su requisito (dorado cuando el requisito ya tiene un punto). Primer clic en la pestana Mokoshotar:
// Abilities (activas); otro clic, o el selector del pie: Instincts (pasivas). Los Aspectos y las definitivas se
// eligen en la NULL ZONE.
_root.__rwPage = 1;
// colores de la interfaz del juego, muestreados del menu de personaje: recuadro gris, panel oscuro, pestanas,
// texto, titulos grises de los recuadros, dorado y el verde del aviso "You have upgrade points available!"
_root.__rwUi = {inset: 0x373737, dark: 0x1A1A1A, tab: 0x404040, tabOff: 0x2E2E2E, tabHi: 0x4A4A4A, edge: 0x111111, text: 0xE3DDD6, dim: 0x8A8A8A, head: 0x5E5E5E, gold: 0xFFCB00, green: 0xB4FF45, pipe: 0x2B2B2B, lvOn: 0x9A9A9A};
// grilla del arbol de clase (talenttreefull, en coordenadas de _root): columnas cada 52 y filas cada 40,3
_root.__rwColX = function(col)
{
   return 87 + 52 * col;
};
_root.__rwRowY = function(row)
{
   return Math.round(124 + 40.3 * row);
};
_root.__rwText = function(mc, name, depth, x, y, w, h, size, color, txt)
{
   mc.createTextField(name, depth, x, y, w, h);
   var f = mc[name];
   f.selectable = false;
   f.multiline = true;
   f.wordWrap = true;
   var fmt = new TextFormat("_sans", size, color);
   f.setNewTextFormat(fmt);
   f.text = txt;
   return f;
};
_root.__rwAlign = function(f, align)
{
   var fmt = f.getNewTextFormat();
   fmt.align = align;
   f.setNewTextFormat(fmt);
   f.setTextFormat(fmt);
};
// achica la letra hasta que el texto entra en el alto dado (como el ajuste de titulos de la capa night)
_root.__rwFit = function(f, maxH, minSize)
{
   var fmt = f.getTextFormat();
   var sz = fmt.size;
   while(f.textHeight + 4 > maxH && sz > minSize)
   {
      sz -= 0.5;
      fmt.size = sz;
      f.setTextFormat(fmt);
   }
   return f;
};
// rectangulo con borde, como los recuadros y las pestanas del menu
_root.__rwRect = function(mc, x, y, w, h, fill, edge, thick)
{
   if(thick > 0)
   {
      mc.lineStyle(thick, edge, 100, true);
   }
   else
   {
      mc.lineStyle();
   }
   mc.beginFill(fill, 100);
   mc.moveTo(x, y);
   mc.lineTo(x + w, y);
   mc.lineTo(x + w, y + h);
   mc.lineTo(x, y + h);
   mc.lineTo(x, y);
   mc.endFill();
};
// brillo verde del juego (el del aviso de puntos para gastar): marca lo que se puede aprender ahora
_root.__rwGlow = function()
{
   return [new flash.filters.GlowFilter(_root.__rwUi.green, 0.85, 8, 8, 2, 2, false, false)];
};
// avisos: en el panel de Aspectos, su renglon; en el arbol, el cartel del juego (como el arbol de clase)
_root.__rwTreeNotice = function(s)
{
   var p = _root.__rwAspPanel;
   if(p && p.notice)
   {
      p.notice.text = s;
      _root.__rwNoticeT = 90;
      return null;
   }
   if(_root.KrinCombatText)
   {
      _root.KrinCombatText.combatTexter = s;
      _root.KrinCombatText.play();
   }
};
_root.__v8OpenTree = function()
{
   var open = _root.__v9Tree && _root.__v9Tree._parent && _root.__v9Active;
   if(open)
   {
      _root.__rwPage = _root.__rwPage == 1 ? 2 : 1;
   }
   else if(!_root.__v9Active)
   {
      _root.__rwPage = 1;
   }
   _root.__rwBuildTree();
};
_root.__rwBuildTree = function()
{
   _root.__rwMigrate();
   _root.__rwSyncBonus();
   _root.__v8Sync();
   // sin onUnload en el arbol: un clip con onUnload se borra al final del fotograma y el nuevo, con el mismo
   // nombre, se resolveria al viejo (pagina 2 en blanco)
   _root.__uiClose();
   _root.__v9Tree.removeMovieClip();
   _root.__v9Active = true;
   _root.KRINMENU._visible = true;
   _root.KrinScreen._visible = false;
   if(_root.KRINMENU._currentframe != 25)
   {
      _root.KRINMENU.gotoAndStop("normal");
      _root.KRINMENU.gotoAndStop("skills");
   }
   var tf = _root.KRINMENU.talenttreefull;
   tf._visible = false;
   var s = 0;
   while(s < 40)
   {
      tf["st" + s]._visible = false;
      s++;
   }
   _root.KRINMENU.__v92Host.createEmptyMovieClip("__v9Tree", 100009);
   var T = _root.KRINMENU.__v92Host.__v9Tree;
   _root.__v9Tree = T;
   T._x = 0 - _root.KRINMENU._x;
   T._y = 0 - _root.KRINMENU._y;
   _root.KRINMENU.__v92Host._visible = true;
   var pg = _root.__rwPage;
   // canos (debajo), niveles de cada fila, nodos, anillos de las pasivas clave (encima), emblema y selector de pagina
   T.createEmptyMovieClip("lines", 20);
   T.createEmptyMovieClip("tiers", 25);
   T.createEmptyMovieClip("nodes", 30);
   T.createEmptyMovieClip("keys", 35);
   var e = T.createEmptyMovieClip("emblem", 40);
   e._x = 62;
   e._y = 89;
   var used = [];
   var depth = 1;
   var i = 0;
   while(i < _root.__rwList.length)
   {
      var d = _root.__rwList[i];
      if(d.pg == pg)
      {
         var n = T.nodes.attachMovie("__v9NativeNode", "n" + d.id, depth);
         n._x = _root.__rwColX(d.col);
         n._y = _root.__rwRowY(d.row);
         n.__rwId = d.id;
         n.onRelease = function()
         {
            _root.__rwLearn(this.__rwId);
            _root.__rwTreeHover(this.__rwId);
         };
         n.onRollOver = function()
         {
            _root.__rwTreeHover(this.__rwId);
         };
         n.onRollOut = function()
         {
            _root.__uiClose();
         };
         T["n" + d.id] = n;
         used[d.row] = true;
         depth++;
      }
      i++;
   }
   // nivel de cada fila, a la derecha de la grilla (solo las filas que tienen nodos)
   var r = 0;
   while(r < 7)
   {
      if(used[r])
      {
         var f = _root.__rwText(T.tiers, "t" + r, r + 1, 259, _root.__rwRowY(r) - 8, 34, 16, 9, _root.__rwUi.head, "Lvl. " + _root.__rwTiers[r]);
         f.__rwLv = _root.__rwTiers[r];
      }
      r++;
   }
   _root.__rwBuildPager(T);
   _root.__rwTreeRefresh();
   if(_root.__rwMigratedPoints > 0)
   {
      _root.__rwTreeNotice("New wolf tree: " + _root.__rwMigratedPoints + " Ability Points from the old tree were refunded.");
      _root.__rwMigratedPoints = 0;
   }
};
// selector de pagina al pie del arbol: "Abilities · Instincts"; la pagina activa en claro y subrayada en dorado
_root.__rwBuildPager = function(T)
{
   var P = T.createEmptyMovieClip("pager", 50);
   var labels = ["Abilities", "Instincts"];
   var xs = [110, 176];
   var k = 0;
   while(k < 2)
   {
      var b = P.createEmptyMovieClip("p" + (k + 1), k + 1);
      b._x = xs[k];
      b._y = 391;
      b.beginFill(0, 0);
      b.moveTo(-4, -1);
      b.lineTo(60, -1);
      b.lineTo(60, 19);
      b.lineTo(-4, 19);
      b.lineTo(-4, -1);
      b.endFill();
      var f = _root.__rwText(b, "label", 1, 0, 0, 56, 18, 11, 14931404, labels[k]);
      var fmt = new TextFormat("_sans", 11, 14931404);
      fmt.align = "center";
      f.setTextFormat(fmt);
      b.__rwPg = k + 1;
      b.onRelease = function()
      {
         if(_root.__rwPage != this.__rwPg)
         {
            _root.__rwPage = this.__rwPg;
            _root.__rwBuildTree();
         }
      };
      b.onRollOver = function()
      {
         this.label.textColor = 16777215;
      };
      b.onRollOut = function()
      {
         _root.__rwPaintPager();
      };
      k++;
   }
   _root.__rwText(P, "dot", 5, 164, 391, 12, 18, 11, 8421504, "·");
   P.createEmptyMovieClip("bar", 6);
   _root.__rwPaintPager();
};
_root.__rwPaintPager = function()
{
   var P = _root.__v9Tree.pager;
   if(!P)
   {
      return null;
   }
   var k = 1;
   while(k <= 2)
   {
      P["p" + k].label.textColor = _root.__rwPage == k ? 14931404 : 8421504;
      k++;
   }
   var a = P["p" + _root.__rwPage];
   P.bar.clear();
   P.bar.lineStyle(2, 16763904, 100);
   P.bar.moveTo(a._x + 12, 410);
   P.bar.lineTo(a._x + 44, 410);
};
_root.__rwTreeRefresh = function()
{
   var T = _root.__v9Tree;
   if(_root.KRINMENU)
   {
      _root.KRINMENU.skillPoints = _root.Krin.skillPoints;
   }
   if(!T || !T.nodes)
   {
      return null;
   }
   var U = _root.__rwUi;
   var pg = _root.__rwPage;
   var L = T.lines;
   var K = T.keys;
   L.clear();
   K.clear();
   var lvl = _root.__rwNum(_root.Krin.Level);
   var i = 0;
   while(i < _root.__rwList.length)
   {
      var d = _root.__rwList[i];
      if(d.pg == pg)
      {
         var n = T["n" + d.id];
         var r = _root.__rwRank(d.id);
         // tres estados: aprendida (icono claro), abierta (oscuro; con brillo verde si hay puntos para aprenderla
         // ya) y bloqueada por nivel o por requisito (oscuro y atenuado)
         var why = r < 1 ? _root.__rwCanLearn(d.id) : "";
         var open = r > 0 || why == "" || why == _root.__rwErr(1);
         if(n)
         {
            var a = n.thing2;
            if(a)
            {
               a.gotoAndStop(d.n);
               a.dontHide = true;
               a.chimney = false;
               // zero: el script del icono no abre el tooltip nativo; el del arbol lo abre el nodo (onRollOver)
               a.zero = true;
               a.ACD = "";
               // como el arbol de clase: el filtro oscuro del icono hasta tener un punto
               if(a.bfilter)
               {
                  a.bfilter._visible = r < 1;
                  a.bfilter._alpha = 80;
               }
               a.toolTipTitle = "";
               a.toolTip = "";
            }
            n.OKAY = true;
            n._alpha = open ? 100 : 38;
            n.filters = r < 1 && why == "" ? _root.__rwGlow() : [];
            if(n.thingo2)
            {
               n.thingo2._visible = false;
            }
            if(n.thingoShow)
            {
               n.thingoShow._visible = false;
            }
         }
         // cano hacia cada requisito de la misma pagina: negro de 6 y dentro uno de 2, dorado si el requisito
         // ya tiene un punto (igual que el arbol de clase)
         var j = 0;
         while(j < d.pre.length)
         {
            var p = _root.__rwS[d.pre[j]];
            if(p && p.pg == pg)
            {
               var x0 = _root.__rwColX(d.col);
               var y0 = _root.__rwRowY(d.row);
               var x1 = _root.__rwColX(p.col);
               var y1 = _root.__rwRowY(p.row);
               L.lineStyle(6, 0, 100);
               L.moveTo(x0, y0);
               L.lineTo(x1, y1);
               L.lineStyle(2, _root.__rwRank(p.id) > 0 ? 0xFFCC00 : U.pipe, 100);
               L.moveTo(x0, y0);
               L.lineTo(x1, y1);
            }
            j++;
         }
         // pasiva clave: anillo dorado fino pegado al borde del icono (atenuado si esta bloqueada)
         if(d.key)
         {
            _root.__rwRing(K, _root.__rwColX(d.col), _root.__rwRowY(d.row), open ? 100 : 38);
         }
      }
      i++;
   }
   // niveles de fila: claros los ya alcanzados
   var t = 0;
   while(t < 7)
   {
      var f = T.tiers["t" + t];
      if(f)
      {
         f.textColor = lvl >= f.__rwLv ? U.lvOn : U.head;
      }
      t++;
   }
   _root.__rwDrawEmblem();
   _root.__rwPaintPager();
};
// el icono mide unas 24 unidades: el anillo de radio 14 queda pegado a su borde
_root.__rwRing = function(mc, cx, cy, alpha)
{
   mc.lineStyle(2, 0xFFCC00, alpha == undefined ? 100 : alpha);
   mc.moveTo(cx + 14, cy);
   var k = 1;
   while(k <= 24)
   {
      var ang = k * 3.141592653589793 / 12;
      mc.lineTo(cx + 14 * Math.cos(ang), cy + 14 * Math.sin(ang));
      k++;
   }
};
// emblema de Ancestral Wolf: la marca ancestral de la capa night (las runas azules, "nightAncestralMark"),
// clara con un brillo azul si esta activa (Scent of Blood) y atenuada si no. Sin la imagen, un circulo.
_root.__rwDrawEmblem = function()
{
   var T = _root.__v9Tree;
   if(!T || !T.emblem)
   {
      return null;
   }
   var e = T.emblem;
   e.clear();
   var on = _root.__rwAncestral();
   if(!_root.__nightMarkBitmap)
   {
      _root.__nightMarkBitmap = flash.display.BitmapData.loadBitmap("nightAncestralMark");
   }
   var bmp = _root.__nightMarkBitmap;
   if(bmp && bmp.width > 0)
   {
      var sc = 24 / bmp.width;
      var mat = new flash.geom.Matrix(sc, 0, 0, sc, -12, -12);
      e.lineStyle();
      e.beginBitmapFill(bmp, mat, false, true);
      e.moveTo(-12, -12);
      e.lineTo(12, -12);
      e.lineTo(12, 12);
      e.lineTo(-12, 12);
      e.lineTo(-12, -12);
      e.endFill();
   }
   else
   {
      e.lineStyle(2, on ? 0x33CCFF : 0x808080, 100);
      e.beginFill(0x151515, 100);
      e.moveTo(11, 0);
      var k = 1;
      while(k <= 16)
      {
         var ang = k * 3.141592653589793 / 8;
         e.lineTo(11 * Math.cos(ang), 11 * Math.sin(ang));
         k++;
      }
      e.endFill();
   }
   e._alpha = on ? 100 : 45;
   e.filters = on ? [new flash.filters.GlowFilter(0x33CCFF, 0.55, 7, 7, 2, 2, false, false)] : [];
   e.onRollOver = function()
   {
      var on2 = _root.__rwAncestral();
      var pc = Math.round(_root.__rwAncBonus() * 100);
      var body = "Mokoshotar descends from the first wolves of the eternal winter. " + (pc > 0 ? "Passively increases your Health, Strength, Instinct and Speed by " + pc + "%, and you" : "You") + " gain 2 Ability Points per level instead of 1 (3 at levels 5, 10, 15 and 20). Every ability raised to its maximum rank awakens a Mastery.";
      var st = on2 ? "ACTIVE. Extra points granted so far: " + _root.__rwTal(_root.__rwSlotBonus) + "." : "INACTIVE. It awakens with the first point in Scent of Blood (Instincts).";
      // titulo distinto de "Ancestral Wolf": la capa night lo cambia por "Ancestral Mark" (inactiva), y en la v4 esta activa
      _root.__rwShowTip(this, "Ancestral Wolf (Class Passive)", body, "Passive Class Effect", st);
   };
   e.onRollOut = function()
   {
      _root.__uiClose();
   };
};
// tooltip propio (nodos del arbol y emblema). El tooltip trae adentro un icono (inner2) con el script nativo de
// los iconos: si queda bajo el mouse, escribe su titulo y su texto (vacios) encima de los nuestros. Con zero no
// lo hace, y __uiTick vuelve a poner los textos guardados mientras el mouse siga sobre el dueno.
_root.__rwShowTip = function(n, title, body, cost, next)
{
   var t = _root.KrinToolTipper;
   if(t && t.inner2)
   {
      t.inner2.zero = true;
   }
   _root.__rwTipTexts = [title, body, cost, next];
   _root.__uiShow(n, n, title, body, cost, next, null);
};
// tooltip del nodo con la forma del arbol de clase: "(0/2)  Hamstring", el costo, el rango actual (o "You have no
// points in this ability yet.") y abajo "Next Tier (Lvl. 3): ..." con el rango siguiente, o "This ability is at its
// maximum tier.". Los requisitos no se escriben: el arbol no deja aprender y avisa con el cartel del juego.
_root.__rwLang = function(k, def)
{
   var L = _root.KrinLang ? _root.KrinLang[_root.KLangChoosen] : undefined;
   var s = L ? L[k] : undefined;
   return typeof s == "string" && s != "" ? s : def;
};
_root.__rwTreeHover = function(id)
{
   var T = _root.__v9Tree;
   var d = _root.__rwS[id];
   if(!T || !d)
   {
      return null;
   }
   var n = T["n" + id];
   if(!n || !n.hitTest(_root._xmouse, _root._ymouse))
   {
      return null;
   }
   var r = _root.__rwRank(id);
   var title = "(" + r + "/" + d.max + ")  " + d.n;
   var body = r < 1 ? _root.__rwLang("SKILLTALENTTIP2", "You have no points in this ability yet.") : _root.__rwFullDesc(id, r);
   var cost = d.pas ? (d.key ? "Key " : "") + _root.__rwLang("SKILLAURA", "Passive Combat Effect") : _root.__rwCostText(id, Math.max(1, r));
   var next = r < d.max ? _root.__rwLang("SKILLTALENTTIP", "Next Tier (Lvl. ") + _root.__rwAt(d.lv, r + 1) + "): " + _root.__rwFullDesc(id, r + 1) : _root.__rwLang("SKILLTALENTTIP3", "This ability is at its maximum tier.");
   _root.__handoffReleaseCustom();
   _root.__rwShowTip(n, title, body, cost, next);
};
_root.__v10Hover = _root.__rwTreeHover;
// Los iconos del lobo (fotogramas 987 en adelante del sprite 2186) y los iconos ocultos del arbol nativo llaman a
// __handoffReleaseCustom en cada fotograma que el mouse esta encima. No se suelta un tooltip del arbol nuevo o
// del panel de Aspectos mientras el mouse siga sobre su dueno (si no, el tooltip queda sin dueno y no se cierra).
_root.__rwPrevRelease = _root.__handoffReleaseCustom;
_root.__rwOwnTip = function()
{
   var o = _root.__uiOwner;
   var h = _root.__uiHit;
   if(!o || !h || !h.hitTest(_root._xmouse, _root._ymouse))
   {
      return false;
   }
   var c = o;
   var k = 0;
   while(c && k < 12)
   {
      if(c == _root.__v9Tree || c == _root.__rwAspPanel)
      {
         return true;
      }
      c = c._parent;
      k++;
   }
   return false;
};
_root.__handoffReleaseCustom = function()
{
   if(_root.__rwOwnTip())
   {
      return null;
   }
   return _root.__rwPrevRelease();
};
_root.__v9Refresh = function()
{
   _root.__rwTreeRefresh();
};
_root.__treeLines = function()
{
   return null;
};
_root.__i1Shade = function()
{
   return null;
};
// iconos de habilidades: fotograma del sprite de iconos -> id (lo completa el build con los fotogramas nuevos)
_root.__uiFrameIds = {};
_root.__rwFrameIdsSet = function(map)
{
   _root.__uiFrameIds = map;
};
_root.__uiAbilityHover = function(n, hit)
{
   if(!n || n.zero || !_root.__uiVisible(n))
   {
      return null;
   }
   var id = _root.__uiFrameIds[n._currentframe];
   if(_root.__v9Tree && n._parent && _root.__v9Tree.nodes && n._parent._parent == _root.__v9Tree.nodes)
   {
      _root.__rwTreeHover(n._parent.__rwId);
      return null;
   }
   var d = _root.__rwS[id];
   var title = n.toolTipTitle;
   var body = n.toolTip;
   var cost = n.toolTip3;
   if(d)
   {
      var r = Math.max(1, _root.__rwRank(id));
      title = d.n + (_root.__rwMastered(id) ? " ★" : "");
      body = _root.__rwFullDesc(id, r);
      cost = d.pas ? "Passive." : _root.__rwCostText(id, r);
   }
   if(typeof title != "string" || title == "")
   {
      return null;
   }
   _root.__uiShow(n, hit, title, body, cost, "", null);
};
// cantidad de un estado que se acumula (Wounds, Frostbite, Scent, Ice Shards): numero dorado con contorno negro
// arriba a la derecha del icono; el contador del juego sigue mostrando los turnos
_root.__rwStackBadge = function(n, num)
{
   var f = n.__rwStk;
   if(!f)
   {
      // borde del dibujo del icono (el clip entero incluye el campo del contador, mas ancho)
      var bb = n.buffIcon ? n.buffIcon.getBounds(n) : n.getBounds(n);
      n.createTextField("__rwStk", 100, bb.xMax - 16, bb.yMin - 6, 18, 14);
      f = n.__rwStk;
      f.selectable = false;
      var fmt = new TextFormat("_sans", 9, 0xFFCB00, true);
      fmt.align = "right";
      f.setNewTextFormat(fmt);
      f.filters = [new flash.filters.GlowFilter(0, 1, 3, 3, 6, 1, false, false)];
   }
   f.text = String(num);
};
// iconos de estado en combate: contador y texto exacto
_root.__rwPrevPaint = _root.__a3PaintStatuses;
_root.__a3PaintStatuses = function(u)
{
   _root.__rwPrevPaint(u);
   if(!u || !u.BUFFARRAYK)
   {
      return null;
   }
   var bar = _root["p" + u.playerID + "BAR"];
   if(!bar)
   {
      return null;
   }
   var i = 0;
   while(i < 7 && i < u.BUFFARRAYK.length)
   {
      var b = u.BUFFARRAYK[i];
      var n = bar["bshr" + i];
      if(n && b && b.CD > 0 && typeof b.buffId == "string" && b.buffId.substr(0, 2) == "RW")
      {
         var nm = _root["KRINBUFF" + b.buffId][0];
         // en el icono solo la cantidad (un "7/7" pisa al icono vecino); el tope va en el titulo del tooltip
         var num = 0 - 1;
         var cap = 0;
         if(b.buffId == "RWWOUND" || b.buffId == "RWWOUNDH")
         {
            num = _root.__rwWounds(u);
            cap = _root.__rwIsWolf(u) ? 0 : _root.__rwWoundCap();
         }
         else if(b.buffId.substr(0, 7) == "RWFROST")
         {
            num = _root.__rwFrost(u);
            cap = _root.__rwFrostCap();
            if(num >= 3)
            {
               nm = "Frostbite · Brittle";
            }
         }
         else if(b.buffId == "RWSCENT")
         {
            num = _root.__rwScent(u);
            cap = _root.__rwScentCap();
         }
         else if(b.buffId == "RWSHARD")
         {
            num = _root.__rwShards(u);
            cap = _root.__rwShardCap();
         }
         var cnt = num < 0 ? "" : String(num) + (cap > 0 ? "/" + cap : "");
         if(cnt != "")
         {
            // en el icono, los turnos en el contador del juego (abajo) y la cantidad en dorado (arriba a la derecha)
            _root.__rwStackBadge(n, num);
            n.toolTipTitle = nm + " (" + cnt + ")";
         }
         else if(b.CD >= 99)
         {
            // estado de todo el combate (lobo ancestral): sin contador
            n.buffCounter = "";
            n.toolTipTitle = nm;
         }
         else
         {
            n.toolTipTitle = nm;
         }
         n.toolTip = _root.__rwStatusText(u, b.buffId);
      }
      i++;
   }
};
// tooltip de un estado de todo el combate: "Duration: 999 turns." -> hasta el final del combate
_root.__rwPrevUiTick = _root.__uiTick;
_root.__uiTick = function()
{
   _root.__rwPrevUiTick();
   var t = _root.KrinToolTipper;
   if(_root.__uiOwner && _root.__uiStatus == "RWSPIRIT" && t)
   {
      t.t3 = "Until the end of the battle.";
      _root.__uiLayout(t);
   }
   // tooltip del arbol o del emblema: si algo piso los textos, se vuelven a poner
   var x = _root.__rwTipTexts;
   if(x && t && _root.__rwOwnTip() && (t.tt != x[0] || t.t3 != x[2]))
   {
      t.tt = x[0];
      t.t = _root.__uiClean(x[1]);
      t.t3 = x[2];
      t.tyut = x[3];
      if(t._currentframe != 17)
      {
         t.gotoAndStop(17);
      }
      _root.__uiLayout(t);
   }
};
_root.__rwPaint = function(u)
{
   if(u)
   {
      _root.__a3PaintStatuses(u);
   }
};
_root.__rwPaintAll = function()
{
   var i = 1;
   while(i < 7)
   {
      var u = _root["playerKrin" + i];
      if(u && u.active == true)
      {
         _root.__a3PaintStatuses(u);
      }
      i++;
   }
};
// ---- NULL ZONE: Aspectos y definitivas
_root.__rwPrevHub = _root.__v8Hub;
_root.__v8Hub = function()
{
   _root.__rwPrevHub();
   var P = _root.__v8HubPanel;
   if(!P)
   {
      return null;
   }
   P.tree._y = 252;
   P.back._y = 372;
   P.createEmptyMovieClip("asp", 5);
   P.asp._x = 240;
   P.asp._y = 306;
   P.asp.attachMovie("__nzNativeButton", "bg", 0);
   P.asp.bg._width = 320;
   P.asp.bg._height = 42;
   var bounds = P.asp.bg.getBounds(P.asp);
   P.asp.bg._x = 0 - bounds.xMin;
   P.asp.bg._y = 0 - bounds.yMin;
   P.asp.createTextField("caption", 1, 8, 3, 306, 40);
   P.asp.caption.setNewTextFormat(new TextFormat("_sans", 14, 14931404));
   P.asp.caption.selectable = false;
   P.asp.caption.text = "Aspectos y definitivas";
   P.asp.onRelease = function()
   {
      _root.__v8HubPanel.removeMovieClip();
      _root.__rwAspSel = 0;
      _root.__rwAspectPanel();
   };
   P.asp.onRollOver = function()
   {
      this._alpha = 80;
   };
   P.asp.onRollOut = function()
   {
      this._alpha = 100;
   };
};
// ---- Panel de Aspectos, con la forma del menu de personaje: a la izquierda la lista de Aspectos (recuadro gris),
// en el centro el elegido (panel oscuro, como el de Sonny) y a la derecha su definitiva. Lo que se puede hacer se
// marca con el verde del juego.
_root.__rwAspSel = 0;
// icono de cada Aspecto: el dibujo sin tinte de su definitiva (Pack Leader, sin definitiva: Pack Tactics)
_root.__rwAspIcon = ["", "Scent of Blood", "Cold Trail", "Pack Tactics", "Howl of the Ancestors"];
_root.__rwAspectBody = function(k)
{
   var t = _root.__rwAspectText(k);
   if(t.substr(0, 16) == "Passive Aspect. ")
   {
      t = t.substr(16);
   }
   var u = t.lastIndexOf(" Unlocks ");
   if(u > 0)
   {
      t = t.substr(0, u);
   }
   return t;
};
// icono de habilidad con el marco redondo del arbol, sin tooltip propio
_root.__rwIcon = function(mc, name, depth, x, y, scale, label)
{
   var n = mc.attachMovie("__v9NativeNode", name, depth);
   n._x = x;
   n._y = y;
   n._xscale = n._yscale = scale;
   n.OKAY = true;
   var a = n.thing2;
   if(a)
   {
      a.gotoAndStop(label);
      a.dontHide = true;
      a.chimney = false;
      a.zero = true;
      a.ACD = "";
      a.toolTipTitle = "";
      a.toolTip = "";
      if(a.bfilter)
      {
         a.bfilter._visible = false;
      }
   }
   if(n.thingo2)
   {
      n.thingo2._visible = false;
   }
   if(n.thingoShow)
   {
      n.thingoShow._visible = false;
   }
   n.enabled = false;
   return n;
};
// titulo gris de un recuadro ("Ability Tree", "Combat Action Bar")
_root.__rwHeader = function(mc, name, depth, x, y, w, txt)
{
   var f = _root.__rwText(mc, name, depth, x, y, w, 22, 14, _root.__rwUi.head, txt);
   _root.__rwAlign(f, "center");
   return f;
};
// boton con la forma de las pestanas Class / Mokoshotar. main: con el marco verde del juego (accion posible)
_root.__rwNativeBtn = function(mc, name, depth, x, y, w, h, label, main, fn)
{
   var U = _root.__rwUi;
   var b = mc.createEmptyMovieClip(name, depth);
   b._x = x;
   b._y = y;
   b.createEmptyMovieClip("bg", 0);
   var f = _root.__rwText(b, "label", 1, 0, Math.round((h - 18) / 2), w, 20, 12, U.text, label);
   _root.__rwAlign(f, "center");
   b.__rwW = w;
   b.__rwH = h;
   b.__rwMain = main;
   b.__rwPaint = function(hv)
   {
      var V = _root.__rwUi;
      this.bg.clear();
      if(this.__rwMain)
      {
         _root.__rwRect(this.bg, 0, 0, this.__rwW, this.__rwH, hv ? V.tabHi : V.tab, V.green, 2);
      }
      else
      {
         _root.__rwRect(this.bg, 0, 0, this.__rwW, this.__rwH, hv ? V.tabHi : V.tab, V.edge, 1);
      }
   };
   b.__rwPaint(false);
   if(main)
   {
      b.filters = _root.__rwGlow();
   }
   b.onRelease = fn;
   b.onRollOver = function()
   {
      this.__rwPaint(true);
   };
   b.onRollOut = function()
   {
      this.__rwPaint(false);
   };
   b.onReleaseOutside = b.onRollOut;
   return b;
};
// estado sin boton (por ejemplo "Activo"): el mismo marco, sin clic
_root.__rwStateBox = function(mc, name, depth, x, y, w, h, label, color)
{
   var U = _root.__rwUi;
   var b = mc.createEmptyMovieClip(name, depth);
   b._x = x;
   b._y = y;
   _root.__rwRect(b, 0, 0, w, h, U.dark, U.edge, 1);
   var f = _root.__rwText(b, "label", 1, 0, Math.round((h - 18) / 2), w, 20, 12, color, label);
   _root.__rwAlign(f, "center");
   return b;
};
_root.__rwAspectPanel = function()
{
   _root.__rwMigrate();
   _root.__rwSyncBonus();
   _root.__uiClose();
   _root.__rwAspPanel.removeMovieClip();
   var U = _root.__rwUi;
   var act = _root.__rwAspect();
   if(_root.__rwAspSel < 1 || _root.__rwAspSel > 4)
   {
      _root.__rwAspSel = act > 0 ? act : 1;
   }
   var sel = _root.__rwAspSel;
   var P = _root.createEmptyMovieClip("__rwAspPanel", 100013);
   _root.KrinScreen._visible = false;
   // fondo rojo del menu, en el mismo lugar que el menu de personaje
   P.attachMovie("__nzNativePanel", "background", 0);
   P.background._width = 767;
   P.background._height = 423;
   var bounds = P.background.getBounds(P);
   P.background._x = 15 - bounds.xMin;
   P.background._y = 16 - bounds.yMin;
   P.background.onRelease = function()
   {
   };
   P.background.useHandCursor = false;
   // titulo dorado con contorno, como "Achievements"
   var h = _root.__rwText(P, "heading", 1, 45, 30, 400, 32, 20, U.gold, "Aspectos de Mokoshotar");
   h.filters = [new flash.filters.GlowFilter(0, 1, 3, 3, 6, 2, false, false)];
   _root.__rwNativeBtn(P, "back", 2, 640, 36, 115, 22, "Volver", false, function()
   {
      _root.__uiClose();
      _root.__rwAspPanel.removeMovieClip();
      _root.KrinScreen._visible = true;
      if(_root.__v8Hub)
      {
         _root.__v8Hub();
      }
   });
   // ---- izquierda: los cuatro Aspectos
   var L = P.createEmptyMovieClip("list", 10);
   _root.__rwRect(L, 45, 73, 250, 346, U.inset, 0, 2);
   _root.__rwHeader(L, "head", 1, 45, 80, 250, "Aspectos");
   var i = 0;
   while(i < 4)
   {
      var A = _root.__rwAspects[i];
      var row = L.createEmptyMovieClip("a" + A.k, 10 + i);
      row._x = 55;
      row._y = 110 + i * 76;
      row.createEmptyMovieClip("bg", 0);
      row.__rwK = A.k;
      var on = act == A.k;
      _root.__rwIcon(row, "ico", 1, 26, 34, 125, _root.__rwAspIcon[A.k]);
      var nm = _root.__rwText(row, "nm", 2, 50, 12, 180, 22, 13, on ? U.gold : 0xFFFFFF, A.n);
      var st = "Inactivo";
      var sc = U.dim;
      if(on)
      {
         st = "Activo";
         sc = U.green;
      }
      if(A.ult > 0 && _root.__rwRank(A.ult) > 0)
      {
         st += " · definitiva aprendida";
      }
      _root.__rwText(row, "st", 3, 50, 33, 180, 18, 11, sc, st);
      row.__rwPaintRow = function(hv)
      {
         var V = _root.__rwUi;
         this.bg.clear();
         this.filters = [];
         if(_root.__rwAspSel == this.__rwK)
         {
            _root.__rwRect(this.bg, 0, 0, 230, 68, 0x2C2C2C, V.green, 2);
            this.filters = _root.__rwGlow();
         }
         else
         {
            _root.__rwRect(this.bg, 0, 0, 230, 68, hv ? 0x424242 : V.inset, hv ? V.edge : V.inset, 1);
         }
      };
      row.__rwPaintRow(false);
      row.onRelease = function()
      {
         if(_root.__rwAspSel != this.__rwK)
         {
            _root.__rwAspSel = this.__rwK;
            _root.__rwAspectPanel();
         }
      };
      row.onRollOver = function()
      {
         this.__rwPaintRow(true);
      };
      row.onRollOut = function()
      {
         this.__rwPaintRow(false);
      };
      row.onReleaseOutside = row.onRollOut;
      i++;
   }
   // ---- centro: el Aspecto elegido (panel oscuro, como el de Sonny)
   var S = _root.__rwAspects[sel - 1];
   var M = P.createEmptyMovieClip("mid", 20);
   _root.__rwRect(M, 304, 73, 190, 346, U.dark, 0, 2);
   var pre = S.n.substr(0, 14) == "Aspect of the " ? "Aspect of the" : "";
   var t0 = _root.__rwText(M, "pre", 1, 310, 80, 178, 18, 11, U.dim, pre);
   _root.__rwAlign(t0, "center");
   var t1 = _root.__rwText(M, "nm", 2, 306, 94, 186, 26, 18, 0xFFFFFF, pre == "" ? S.n : S.n.substr(14));
   _root.__rwAlign(t1, "center");
   var t2 = _root.__rwText(M, "sub", 3, 310, 122, 178, 20, 12, act == sel ? U.green : U.dim, act == sel ? "Aspecto activo" : "Aspecto inactivo");
   _root.__rwAlign(t2, "center");
   _root.__rwText(M, "ptl", 4, 314, 148, 140, 20, 13, 0xFFFFFF, "Puntos de habilidad:");
   var pv = _root.__rwText(M, "points", 5, 440, 148, 44, 20, 13, 0xFFFFFF, String(_root.Krin.skillPoints));
   _root.__rwAlign(pv, "right");
   _root.__rwFit(_root.__rwText(M, "desc", 6, 314, 178, 172, 150, 12, U.text, _root.__rwAspectBody(sel)), 150, 9);
   var hint = _root.__rwText(M, "hint", 7, 310, 330, 178, 20, 10, U.dim, "Cambiar de Aspecto es gratis.");
   _root.__rwAlign(hint, "center");
   var nt = _root.__rwText(P, "notice", 21, 308, 350, 182, 32, 11, U.gold, "");
   _root.__rwAlign(nt, "center");
   if(act == sel)
   {
      _root.__rwStateBox(P, "pick", 22, 314, 386, 170, 24, "Activo", U.green);
   }
   else
   {
      var pb = _root.__rwNativeBtn(P, "pick", 22, 314, 386, 170, 24, "Activar", true, function()
      {
         var k = this.__rwK;
         _root.__rwSetTal(_root.__rwSlotAspect, k);
         _root.__v8Sync();
         _root.__rwAspectPanel();
         _root.__rwTreeNotice(_root.__rwAspects[k - 1].n + " activo.");
      });
      pb.__rwK = sel;
   }
   // ---- derecha: la definitiva del Aspecto elegido
   var R = P.createEmptyMovieClip("ult", 30);
   _root.__rwRect(R, 505, 73, 250, 346, U.inset, 0, 2);
   _root.__rwHeader(R, "head", 1, 505, 80, 250, "Definitiva");
   if(S.ult > 0)
   {
      var u = _root.__rwS[S.ult];
      var ur = _root.__rwRank(S.ult);
      _root.__rwIcon(R, "ico", 2, 538, 124, 150, u.n);
      _root.__rwText(R, "nm", 3, 562, 106, 188, 24, 16, ur > 0 ? U.gold : 0xFFFFFF, u.n);
      _root.__rwText(R, "info", 4, 562, 128, 188, 18, 11, U.dim, _root.__rwCostText(S.ult, 1));
      _root.__rwFit(_root.__rwText(R, "desc", 5, 517, 152, 228, 200, 12, U.text, _root.__rwDesc(S.ult, 1)), 200, 9);
      var lv = _root.__rwUltLevel;
      var why = "";
      if(ur < 1)
      {
         if(_root.__rwNum(_root.Krin.Level) < lv)
         {
            why = "Requiere Nivel " + lv + ".";
         }
         else if(act != sel)
         {
            why = "Primero activa este Aspecto.";
         }
         else if(_root.__rwNum(_root.Krin.skillPoints) < 1)
         {
            why = "No tienes puntos de habilidad.";
         }
      }
      else if(act != sel)
      {
         why = "Solo se usa con este Aspecto activo.";
      }
      var uw = _root.__rwText(R, "why", 6, 515, 358, 230, 20, 11, U.gold, why);
      _root.__rwAlign(uw, "center");
      if(ur > 0)
      {
         _root.__rwStateBox(P, "learn", 31, 545, 386, 170, 24, "Aprendida", U.gold);
      }
      else if(why == "")
      {
         var lb = _root.__rwNativeBtn(P, "learn", 31, 545, 386, 170, 24, "Aprender (1 punto)", true, function()
         {
            var id = this.__rwUlt;
            if(_root.__rwLearn(id))
            {
               _root.__rwAspectPanel();
               _root.__rwTreeNotice(_root.__rwS[id].n + " aprendida: ya está en la Ability Pool.");
            }
         });
         lb.__rwUlt = S.ult;
      }
      else
      {
         _root.__rwStateBox(P, "learn", 31, 545, 386, 170, 24, "Aprender (1 punto)", U.dim);
      }
   }
   else
   {
      var nu = _root.__rwText(R, "none", 2, 525, 190, 210, 60, 13, U.dim, "Este Aspecto no tiene definitiva.");
      _root.__rwAlign(nu, "center");
   }
   P.onEnterFrame = function()
   {
      if(_root.__rwNoticeT > 0)
      {
         _root.__rwNoticeT--;
         if(_root.__rwNoticeT == 0)
         {
            this.notice.text = "";
         }
      }
      this.mid.points.text = String(_root.Krin.skillPoints);
      if(_root._currentframe != 181)
      {
         this.removeMovieClip();
      }
   };
};
