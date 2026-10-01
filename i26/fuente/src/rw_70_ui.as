// ------------------------------------------------------------------------------- interfaz
// Arbol en dos paginas dentro del menu de habilidades (KRINMENU fotograma 25, contenedor __v92Host).
// Primer clic en la pestana Mokoshotar: Pagina 1 (activas). Otro clic con el arbol abierto: Pagina 2
// (Instintos, pasivas). Los Aspectos y las definitivas solo se ven y se eligen en la NULL ZONE.
_root.__rwPage = 1;
_root.__rwColX = function(col)
{
   return 68 + 60 * col;
};
_root.__rwRowY = function(row)
{
   return 143 + 43 * row;
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
_root.__rwTreeNotice = function(s)
{
   var t = _root.__v9Tree;
   if(t && t.notice)
   {
      t.notice.text = s;
      _root.__rwNoticeT = 90;
   }
   var p = _root.__rwAspPanel;
   if(p && p.notice)
   {
      p.notice.text = s;
      _root.__rwNoticeT = 90;
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
   var names = ["Hunt", "Winter", "Pack", "Endurance"];
   var c = 0;
   while(c < 4)
   {
      var lb = _root.__rwText(T, "branch" + c, 10 + c, _root.__rwColX(c) - 32, 104, 64, 20, 11, 14931404, names[c]);
      var fmt = new TextFormat("_sans", 11, 14931404);
      fmt.align = "center";
      lb.setTextFormat(fmt);
      c++;
   }
   // cabecera propia: tapa el titulo nativo "Ability Tree" con el gris del panel
   T.createEmptyMovieClip("head", 5);
   T.head.beginFill(3618615, 100);
   T.head.moveTo(49, 78);
   T.head.lineTo(291, 78);
   T.head.lineTo(291, 101);
   T.head.lineTo(49, 101);
   T.head.lineTo(49, 78);
   T.head.endFill();
   _root.__rwText(T, "pageLabel", 16, 78, 82, 128, 18, 11, 14931404, pg == 1 ? "Página 1: Habilidades" : "Página 2: Instintos");
   _root.__rwText(T, "hint", 17, 44, 417, 250, 16, 9, 10066329, pg == 1 ? "Otro clic en Mokoshotar: Instintos (pasivas)." : "Otro clic en Mokoshotar: Habilidades.");
   _root.__rwText(T, "notice", 18, 44, 403, 250, 16, 10, 16763904, "");
   // lineas de cada rama (debajo de los nodos)
   T.createEmptyMovieClip("lines", 20);
   // emblema de Ancestral Wolf
   var e = T.createEmptyMovieClip("emblem", 21);
   e._x = 64;
   e._y = 90;
   T.createEmptyMovieClip("nodes", 30);
   T.nodes._x = 0;
   T.nodes._y = 0;
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
         n._xscale = 90;
         n._yscale = 90;
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
         var rt = _root.__rwText(T, "rank" + d.id, 200 + depth, n._x + 4, n._y + 5, 26, 14, 9, 16777215, "");
         depth++;
      }
      i++;
   }
   // reiniciar
   T.createEmptyMovieClip("reset", 90);
   T.reset._x = 208;
   T.reset._y = 83;
   T.reset.attachMovie("__nzNativeButton", "bg", 0);
   T.reset.bg._width = 80;
   T.reset.bg._height = 16;
   var bounds = T.reset.bg.getBounds(T.reset);
   T.reset.bg._x = 0 - bounds.xMin;
   T.reset.bg._y = 0 - bounds.yMin;
   _root.__rwText(T.reset, "caption", 1, 4, 1, 76, 14, 9, 14931404, "Reiniciar lobo");
   T.reset.onRelease = function()
   {
      var n = _root.__rwRefundAll();
      _root.__rwTreeNotice("Se devolvieron " + n + " puntos.");
   };
   T.onEnterFrame = function()
   {
      if(_root.__rwNoticeT > 0)
      {
         _root.__rwNoticeT--;
         if(_root.__rwNoticeT == 0 && this.notice)
         {
            this.notice.text = "";
         }
      }
   };
   _root.__rwTreeRefresh();
   if(_root.__rwMigratedPoints > 0)
   {
      _root.__rwTreeNotice("Árbol nuevo: se devolvieron " + _root.__rwMigratedPoints + " puntos del árbol anterior.");
      _root.__rwMigratedPoints = 0;
   }
};
_root.__rwLearnable = function(id)
{
   return _root.__rwCanLearn(id) == "" || _root.__rwCanLearn(id) == "You do not have enough Ability Points.";
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
   var pg = _root.__rwPage;
   var L = T.lines;
   L.clear();
   var i = 0;
   while(i < _root.__rwList.length)
   {
      var d = _root.__rwList[i];
      if(d.pg == pg)
      {
         var n = T["n" + d.id];
         var r = _root.__rwRank(d.id);
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
               if(a.bfilter)
               {
                  a.bfilter._visible = false;
               }
               a.toolTipTitle = "";
               a.toolTip = "";
            }
            n.OKAY = true;
            if(n.thingo2)
            {
               n.thingo2._visible = false;
            }
            if(n.thingoShow)
            {
               n.thingoShow._visible = false;
            }
            if(r > 0)
            {
               n._alpha = 100;
            }
            else if(_root.__rwLearnable(d.id))
            {
               n._alpha = 60;
            }
            else
            {
               n._alpha = 30;
            }
         }
         var rt = T["rank" + d.id];
         if(rt)
         {
            rt.text = r + "/" + d.max + (_root.__rwMastered(d.id) ? "★" : "");
            rt.textColor = _root.__rwMastered(d.id) ? 15317833 : (r > 0 ? 16777215 : 10066329);
         }
         // linea hacia el siguiente de la misma rama
         var j = 0;
         while(j < _root.__rwList.length)
         {
            var e = _root.__rwList[j];
            if(e.pg == pg && e.col == d.col && e.row == d.row + 1)
            {
               var on = r > 0 && _root.__rwRank(e.id) > 0;
               L.lineStyle(3, on ? 15317833 : 2105376, 100);
               L.moveTo(_root.__rwColX(d.col), _root.__rwRowY(d.row) + 14);
               L.lineTo(_root.__rwColX(e.col), _root.__rwRowY(e.row) - 14);
            }
            j++;
         }
         if(d.key)
         {
            L.lineStyle(2, 15317833, 100);
            var cx = _root.__rwColX(d.col);
            var cy = _root.__rwRowY(d.row);
            var rr = 19;
            L.moveTo(cx + rr, cy);
            var k = 1;
            while(k <= 16)
            {
               var ang = k * 3.141592653589793 / 8;
               L.lineTo(cx + rr * Math.cos(ang), cy + rr * Math.sin(ang));
               k++;
            }
         }
      }
      i++;
   }
   _root.__rwDrawEmblem();
};
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
   e.lineStyle(2, on ? 15317833 : 8421504, 100);
   e.beginFill(1381653, 100);
   e.moveTo(11, 0);
   var k = 1;
   while(k <= 16)
   {
      var ang = k * 3.141592653589793 / 8;
      e.lineTo(11 * Math.cos(ang), 11 * Math.sin(ang));
      k++;
   }
   e.endFill();
   e.lineStyle(0, 0, 0);
   e.beginFill(on ? 15317833 : 8421504, 100);
   var p = 0;
   while(p < 10)
   {
      var rad = p % 2 == 0 ? 7 : 3;
      var ang = -1.5707963267948966 + p * 3.141592653589793 / 5;
      if(p == 0)
      {
         e.moveTo(rad * Math.cos(ang), rad * Math.sin(ang));
      }
      else
      {
         e.lineTo(rad * Math.cos(ang), rad * Math.sin(ang));
      }
      p++;
   }
   e.endFill();
   e.onRollOver = function()
   {
      var on = _root.__rwAncestral();
      var body = "Mokoshotar descends from the first wolves of the eternal winter. Passively increases your Health, Strength, Instinct and Speed by 10%, and you gain 2 Ability Points per level instead of 1 (3 at levels 5, 10, 15 and 20). Every ability raised to its maximum rank awakens a Mastery (its rank is shown in gold).";
      var st = on ? "ACTIVE. Extra points granted so far: " + _root.__rwTal(_root.__rwSlotBonus) + "." : "INACTIVE: spend 1 point in Scent of Blood (Instincts page) to awaken it.";
      // titulo distinto de "Ancestral Wolf": la capa night lo cambia por "Ancestral Mark" (inactiva), y en la v4 esta activa
      _root.__uiShow(this, this, "Ancestral Wolf (Class Passive)", body, "Passive Class Effect. Requires Scent of Blood.", st, null);
   };
   e.onRollOut = function()
   {
      _root.__uiClose();
   };
};
_root.__rwReqText = function(d)
{
   var s = "";
   var i = 0;
   while(i < d.req.length)
   {
      var q = _root.__rwS[d.req[i]];
      if(q)
      {
         s += (s == "" ? "" : ", ") + q.n + (q.pg == 2 ? " (Instincts)" : "");
      }
      i++;
   }
   return s;
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
   var title = "(" + r + "/" + d.max + ")  " + d.n + (_root.__rwMastered(id) ? " ★" : "");
   var body = _root.__rwFullDesc(id, Math.max(1, r));
   var cost = d.pas ? (d.key ? "Key Passive. " : "Passive. ") + _root.__rwBranchName[d.br] + "." : _root.__rwCostText(id, Math.max(1, r)) + " " + _root.__rwBranchName[d.br] + ".";
   var next = "";
   if(r < d.max)
   {
      next = "Next rank " + (r + 1) + "/" + d.max + " (Lvl. " + _root.__rwAt(d.lv, r + 1) + ", 1 Ability Point): " + _root.__rwFullDesc(id, r + 1);
      if(d.free > r)
      {
         next = "";
      }
   }
   else
   {
      next = "Fully learned.";
   }
   var rq = _root.__rwReqText(d);
   if(rq != "")
   {
      next = "Requires " + rq + ". " + next;
   }
   var why = _root.__rwCanLearn(id);
   if(why != "" && r < d.max && why != "You do not have enough Ability Points.")
   {
      next = next + " [" + why + "]";
   }
   _root.__handoffReleaseCustom();
   _root.__uiShow(n, n, title, body, cost, next, null);
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
            n.buffCounter = String(num);
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
   if(_root.__uiOwner && _root.__uiStatus == "RWSPIRIT" && _root.KrinToolTipper)
   {
      _root.KrinToolTipper.t3 = "Until the end of the battle.";
      _root.__uiLayout(_root.KrinToolTipper);
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
_root.__rwButton = function(mc, name, depth, x, y, w, h, label, fn)
{
   var b = mc.createEmptyMovieClip(name, depth);
   b._x = x;
   b._y = y;
   b.attachMovie("__nzNativeButton", "bg", 0);
   b.bg._width = w;
   b.bg._height = h;
   var bounds = b.bg.getBounds(b);
   b.bg._x = 0 - bounds.xMin;
   b.bg._y = 0 - bounds.yMin;
   _root.__rwText(b, "caption", 1, 6, 2, w - 12, h - 2, 12, 14931404, label);
   b.onRelease = fn;
   b.onRollOver = function()
   {
      this._alpha = 80;
      if(this.__rwInfoTitle)
      {
         _root.__rwInfo(this.__rwInfoTitle, this.__rwInfoBody);
      }
   };
   b.onRollOut = function()
   {
      this._alpha = 100;
      if(this.__rwInfoTitle)
      {
         _root.__rwInfo("", "");
      }
   };
   return b;
};
// recuadro de descripcion del panel de Aspectos (el tooltip nativo sigue al mouse y se sale por la derecha)
_root.__rwInfo = function(title, body)
{
   var P = _root.__rwAspPanel;
   if(!P || !P.info)
   {
      return null;
   }
   if(title == "")
   {
      P.info.title.text = "Definitivas";
      P.info.body.text = "Pasa el mouse sobre una definitiva para leer qué hace.";
      return null;
   }
   P.info.title.text = title;
   P.info.body.text = body;
};
_root.__rwAspectPanel = function()
{
   _root.__rwMigrate();
   _root.__rwSyncBonus();
   _root.__rwAspPanel.removeMovieClip();
   var P = _root.createEmptyMovieClip("__rwAspPanel", 100013);
   _root.KrinScreen._visible = false;
   P.attachMovie("__nzNativePanel", "background", 0);
   P.background._width = 760;
   P.background._height = 435;
   var bounds = P.background.getBounds(P);
   P.background._x = 20 - bounds.xMin;
   P.background._y = 55 - bounds.yMin;
   P.background.onRelease = function()
   {
   };
   P.background.useHandCursor = false;
   P.createTextField("heading", 1, 45, 70, 400, 36);
   P.heading.setNewTextFormat(new TextFormat("Rockwell", 25, 14931404));
   P.heading.selectable = false;
   P.heading.embedFonts = true;
   P.heading.text = "ASPECTOS";
   _root.__rwText(P, "points", 2, 470, 80, 290, 22, 15, 14931404, "Puntos disponibles: " + _root.Krin.skillPoints);
   _root.__rwText(P, "sub", 3, 45, 104, 710, 32, 11, 13159632, "Solo un Aspecto activo a la vez. Elegirlo o cambiarlo es gratis. Cada definitiva cuesta 1 punto (Nivel " + _root.__rwUltLevel + "), se usa una vez por combate y solo con su Aspecto activo.");
   _root.__rwText(P, "notice", 4, 45, 456, 500, 20, 12, 16763904, "");
   var act = _root.__rwAspect();
   var i = 0;
   while(i < 4)
   {
      var A = _root.__rwAspects[i];
      var x = 45 + i % 2 * 360;
      var y = 138 + Math.floor(i / 2) * 124;
      var card = P.createEmptyMovieClip("card" + i, 10 + i);
      card._x = x;
      card._y = y;
      card.attachMovie("__nzNativeInset", "bg", 0);
      card.bg._width = 348;
      card.bg._height = 118;
      var b2 = card.bg.getBounds(card);
      card.bg._x = 0 - b2.xMin;
      card.bg._y = 0 - b2.yMin;
      var on = act == A.k;
      _root.__rwText(card, "name", 1, 8, 4, 330, 20, 14, on ? 15317833 : 14931404, A.n + (on ? "  (activo)" : ""));
      _root.__rwText(card, "desc", 2, 8, 22, 332, 70, 10, 14931404, _root.__rwAspectText(A.k));
      _root.__rwButton(card, "pick", 3, 8, 91, 120, 22, on ? "Activo" : "Elegir", function()
      {
         _root.__rwSetTal(_root.__rwSlotAspect, this._parent.__rwK);
         _root.__v8Sync();
         _root.__rwAspectPanel();
         _root.__rwTreeNotice(_root.__rwAspects[this._parent.__rwK - 1].n + " activo.");
      });
      card.__rwK = A.k;
      if(A.ult > 0)
      {
         var u = _root.__rwS[A.ult];
         var ur = _root.__rwRank(A.ult);
         var lab = ur > 0 ? u.n + " (aprendida)" : u.n + " (1 punto)";
         var bt = _root.__rwButton(card, "ult", 4, 136, 91, 204, 22, lab, function()
         {
            if(_root.__rwRank(this.__rwUlt) > 0)
            {
               _root.__rwTreeNotice("Ya aprendida.");
               return null;
            }
            if(_root.__rwLearn(this.__rwUlt))
            {
               _root.__rwAspectPanel();
               _root.__rwTreeNotice(_root.__rwS[this.__rwUlt].n + " aprendida.");
            }
         });
         bt.__rwUlt = A.ult;
         bt.__rwInfoTitle = u.n + (ur > 0 ? "  (aprendida)" : "  (1 punto, Nivel " + _root.__rwUltLevel + ", con " + A.n + " activo)");
         bt.__rwInfoBody = _root.__rwDesc(A.ult, 1) + " " + _root.__rwCostText(A.ult, 1);
      }
      else
      {
         _root.__rwText(card, "noult", 4, 140, 93, 200, 20, 10, 10066329, "Sin definitiva por ahora.");
      }
      i++;
   }
   var info = P.createEmptyMovieClip("info", 20);
   info._x = 45;
   info._y = 386;
   info.attachMovie("__nzNativeInset", "bg", 0);
   info.bg._width = 708;
   info.bg._height = 60;
   var b3 = info.bg.getBounds(info);
   info.bg._x = 0 - b3.xMin;
   info.bg._y = 0 - b3.yMin;
   _root.__rwText(info, "title", 1, 8, 2, 690, 18, 12, 15317833, "");
   _root.__rwText(info, "body", 2, 8, 19, 694, 42, 10, 14931404, "");
   _root.__rwInfo("", "");
   _root.__rwButton(P, "back", 30, 560, 452, 200, 26, "Volver", function()
   {
      _root.__uiClose();
      _root.__rwAspPanel.removeMovieClip();
      _root.KrinScreen._visible = true;
   });
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
      this.points.text = "Puntos disponibles: " + _root.Krin.skillPoints;
      if(_root._currentframe != 181)
      {
         this.removeMovieClip();
      }
   };
};
