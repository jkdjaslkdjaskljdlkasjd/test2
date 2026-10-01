// Gancho de depuracion para el banco en Ruffle (solo con --debug): ExternalInterface "dbg".
_root.__dbgResolve = function(path)
{
   var parts = path.split(".");
   var o = _root;
   var i = 0;
   if(parts[0] == "_root")
   {
      i = 1;
   }
   while(i < parts.length - 1)
   {
      o = o[parts[i]];
      if(o == undefined)
      {
         return null;
      }
      i++;
   }
   return {o: o, k: parts[parts.length - 1]};
};
_root.__dbgValue = function(s)
{
   if(s == "true")
   {
      return true;
   }
   if(s == "false")
   {
      return false;
   }
   if(s == "undefined")
   {
      return undefined;
   }
   var n = Number(s);
   if(!isNaN(n) && s != "")
   {
      return n;
   }
   return s;
};
_root.__dbgCmd = function(cmd)
{
   var p = cmd.split(" ");
   var op = p[0];
   if(op == "get")
   {
      var r = _root.__dbgResolve(p[1]);
      if(!r)
      {
         return "null";
      }
      return String(r.o[r.k]);
   }
   if(op == "set")
   {
      var r = _root.__dbgResolve(p[1]);
      if(!r)
      {
         return "null";
      }
      r.o[r.k] = _root.__dbgValue(p.slice(2).join(" "));
      return "ok";
   }
   if(op == "go")
   {
      _root.gotoAndPlay(p[1]);
      return "ok";
   }
   if(op == "gostop")
   {
      _root.gotoAndStop(p[1]);
      return "ok";
   }
   if(op == "call")
   {
      var r = _root.__dbgResolve(p[1]);
      if(!r)
      {
         return "null";
      }
      var args = [];
      var j = 2;
      while(j < p.length)
      {
         args.push(_root.__dbgValue(p[j]));
         j++;
      }
      var f = r.o[r.k];
      return String(f.apply(r.o, args));
   }
   if(op == "frame")
   {
      return String(_root._currentframe);
   }
   if(op == "wrap")
   {
      _root.__dbgWrap(p[1]);
      return "ok";
   }
   if(op == "log")
   {
      var s = _root.__dbgLog.join(" | ");
      _root.__dbgLog = [];
      return s;
   }
   if(op == "callo")
   {
      var r = _root.__dbgResolve(p[1]);
      if(!r)
      {
         return "null";
      }
      var args = [];
      var j = 2;
      while(j < p.length)
      {
         var q = _root.__dbgResolve(p[j]);
         args.push(p[j].substr(0, 6) == "_root." && q ? q.o[q.k] : _root.__dbgValue(p[j]));
         j++;
      }
      var f = r.o[r.k];
      return String(f.apply(r.o, args));
   }
   if(op == "js")
   {
      return "ok";
   }
   return "?";
};
flash.external.ExternalInterface.addCallback("dbg", null, function(cmd)
{
   return _root.__dbgCmd(cmd);
});
_root.__dbgVersion = 1;

_root.__dbgLog = [];
// envuelve _root[name] para registrar las llamadas (nombre, argumentos y resultado)
_root.__dbgWrap = function(name)
{
   var prev = _root[name];
   _root[name] = function()
   {
      var parts = [];
      var i = 0;
      while(i < arguments.length)
      {
         parts.push(String(arguments[i]).substr(0, 60));
         i++;
      }
      var res = prev.apply(this, arguments);
      if(_root.__dbgLog.length < 200 && (name != "__handoffCustomIcon" || String(arguments[0]).indexOf("__v9Tree") >= 0))
      {
         _root.__dbgLog.push(name + "(" + parts.join(",") + ")=" + String(res).substr(0, 40) + "@" + _root.__dbgFrameNo);
      }
      return res;
   };
};
_root.__dbgFrameNo = 0;
_root.createEmptyMovieClip("__dbgCounter", 980999);
_root.__dbgCounter.onEnterFrame = function()
{
   _root.__dbgFrameNo++;
};
// ¿el reloj de combate espera la jugada del jugador?
_root.__dbgAwaitingPlayer = function()
{
   var me = _root["playerKrin" + _root.Krin.playerNumber];
   return _root._currentframe == 217 && _root.InBattle == false && _root.speechDone == true && _root.winCondition < 0 && _root.moveChoosen != true && me != undefined && me.active == true && _root.TeamMoveNow == me.teamSide;
};
// jugada del jugador: casilla de la barra y objetivo (flags: 2 propio, 3 enemigo, 4 aliado)
_root.__dbgPlay = function(slot, target)
{
   var me = _root["playerKrin" + _root.Krin.playerNumber];
   var a = _root["KRINABILITY" + _root.Krin.moveMatrix[slot]];
   if(a[3] == 0 && a[2] == 1)
   {
      target = me.playerID;
   }
   var t = _root["playerKrin" + target];
   _root.theEnemyToMoveVS = target;
   _root.theEnemyToMoveVS2 = target == me.playerID ? 2 : (t.teamSide == me.teamSide ? 4 : 3);
   _root.addMoveForPlayer(slot);
   return _root.moveChoosen == true;
};
// resumen de una unidad: nombre, vida, Focus, marcas y estados
_root.__dbgUnit = function(pid)
{
   var u = _root["playerKrin" + pid];
   if(!u)
   {
      return "-";
   }
   var s = u.playerName + " act=" + u.active + " vida=" + Math.round(u.LIFEN) + "/" + Math.round(u.LIFEU) + " foc=" + Math.round(u.FOCUSN) + " esc=" + Math.round(u.SHIELD) + " stun=" + u.STUN;
   s += " W=" + _root.__rwWounds(u) + " FB=" + _root.__rwFrost(u) + " Sc=" + _root.__rwScent(u);
   if(_root.__rwIsWolf(u))
   {
      s += " Sh=" + _root.__rwShards(u);
   }
   var b = [];
   var i = 0;
   while(i < u.BUFFARRAYK.length)
   {
      var x = u.BUFFARRAYK[i];
      if(x.CD > 0)
      {
         b.push(x.buffId + ":" + x.CD);
      }
      i++;
   }
   return s + " [" + b.join(",") + "]";
};
// posicion global (coordenadas de _root) del origen de un clip y su tamano
_root.__dbgGlobal = function(path)
{
   var r = _root.__dbgResolve(path);
   if(!r)
   {
      return "null";
   }
   var c = r.o[r.k];
   if(!c)
   {
      return "null";
   }
   var b = c.getBounds(_root);
   return Math.round(b.xMin) + "," + Math.round(b.yMin) + "," + Math.round(b.xMax) + "," + Math.round(b.yMax) + " vis=" + c._visible;
};
// vida alta para un enemigo (para que el combate dure)
_root.__dbgTough = function(pid, hp)
{
   var u = _root["playerKrin" + pid];
   u.LIFE = hp;
   u.LIFEU = hp;
   u.LIFEN = hp;
   _root.applyChangesKrin(u);
   return u.LIFEN;
};
// hijos de un clip: nombre, profundidad, tipo y caja en coordenadas de _root
_root.__dbgKids = function(path)
{
   var r = _root.__dbgResolve(path);
   var c = r ? r.o[r.k] : null;
   if(path == "_root")
   {
      c = _root;
   }
   if(!c)
   {
      return "null";
   }
   var out = [];
   for(var k in c)
   {
      var o = c[k];
      if(typeof o == "movieclip" || o instanceof TextField || o instanceof Button)
      {
         if(o._parent == c)
         {
            var b = o.getBounds(_root);
            var tipo = typeof o == "movieclip" ? "mc" : (o instanceof TextField ? "tf" : "bt");
            var extra = o instanceof TextField ? " '" + String(o.text).substr(0, 24) + "'" : "";
            out.push(k + "@" + o.getDepth() + ":" + tipo + " " + Math.round(b.xMin) + "," + Math.round(b.yMin) + "," + Math.round(b.xMax) + "," + Math.round(b.yMax) + (o._visible ? "" : " oculto") + extra);
         }
      }
   }
   return out.join(" | ");
};
