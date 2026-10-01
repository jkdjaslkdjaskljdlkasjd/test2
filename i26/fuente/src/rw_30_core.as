// ------------------------------------------------------------------------------- nucleo de combate
_root.__rwWolfTurn = 0;
_root.__rwInCast = false;
_root.__rwCons = {sc: 0, w: 0, fb: 0};
_root.__rwConsumed = function(kind, k)
{
   if(_root.__rwInCast)
   {
      _root.__rwCons[kind] += k;
   }
};
_root.__rwFocus = function(u, n)
{
   if(!u || !(u.LIFEN > 0))
   {
      return 0;
   }
   var f0 = _root.__rwNum(u.FOCUSN);
   var f = f0 + n;
   var top = _root.__rwNum(u.FOCUSU);
   if(f > top)
   {
      f = top;
   }
   if(f < 0)
   {
      f = 0;
   }
   u.FOCUSN = f;
   _root.__rwLifeBar(u);
   return f - f0;
};
_root.__rwDrain = function(u, n)
{
   var d = 0 - _root.__rwFocus(u, 0 - n);
   _root.__rwTerrorUpdate(u);
   return d;
};
// multiplicador del lobo sobre su propio dano (direct: golpes; si no, sangrados y estallidos)
_root.__rwOutMult = function(c, t, direct)
{
   var k = 1;
   if(!_root.__rwIsWolf(c))
   {
      return k;
   }
   if(direct)
   {
      if(t && _root.__rwBrittle(t))
      {
         k *= _root.__rwAspect() == 2 ? 1.3 : 1.2;
      }
      if(_root.__rwAspect() == 3)
      {
         k *= 0.85;
      }
      if(_root.__rwHas(c, "RWCOURAGE"))
      {
         k *= 1 + _root.__rwNum(c.__rwCourage);
      }
   }
   if(_root.__rwHas(c, "RWANCFORM"))
   {
      k *= 1.4;
   }
   if(_root.__rwHas(c, "RWCALL"))
   {
      k *= 2;
   }
   return k;
};
// dano "puro" del lobo (sangrado, estallidos, esquirlas): formula de los DoT nativos (se reduce con la
// Defensa del elemento respecto del nivel y sube con el dano recibido del objetivo)
_root.__rwPure = function(c, t, raw, el, show)
{
   if(!_root.__rwAlive(t) || !(raw > 0))
   {
      return 0;
   }
   var e = !el ? "Physical" : el;
   var def = _root.__rwNum(t.DEFU[e]);
   if(!(def > 0))
   {
      def = 100;
   }
   var lvl = 100 + 15 * _root.__rwNum(t.plevel);
   var i2 = t.IDMG2 == undefined ? 0 : _root.__rwNum(t.IDMG2);
   var p2 = t.IDMGP2 == undefined ? 1 : _root.__rwNum(t.IDMGP2);
   var io = t.IDOT == undefined ? 1 : _root.__rwNum(t.IDOT);
   var dmg = Math.ceil(raw * _root.__rwOutMult(c, t, false) * (1 + i2) * p2 * io * lvl / def);
   if(!(dmg > 0))
   {
      return 0;
   }
   var sh = _root.__rwNum(t.SHIELD);
   if(sh > 0)
   {
      var a = Math.min(sh, dmg);
      t.SHIELD = sh - a;
      dmg -= a;
      if(a > 0 && show)
      {
         _root.__rwNumber(t, a, e);
      }
   }
   if(dmg > 0)
   {
      var l0 = t.LIFEN;
      t.LIFEN = _root.__v10Life(t.LIFEN - dmg, t, c, true);
      if(show)
      {
         _root.__rwNumber(t, l0 - t.LIFEN, e);
      }
      _root.__rwCheckDeath(t, c);
   }
   _root.__rwLifeBar(t);
   return dmg;
};
_root.__rwCheckDeath = function(t, c)
{
   if(!t || t.LIFEN > 0 || t.active != true)
   {
      return false;
   }
   t.LIFEN = 0;
   t.FOCUSN = 0;
   t.active = false;
   if(_root.BATTLESCREEN && _root.BATTLESCREEN["player" + t.playerID])
   {
      _root.BATTLESCREEN["player" + t.playerID].inner.gotoAndPlay("dead");
   }
   var k = 1;
   while(k < 7)
   {
      if(_root["KrinSelector" + k] && _root["KrinSelector" + k].TargetEr == t.playerID)
      {
         _root["KrinSelector" + k]._x = -300;
         _root["KrinSelector" + k]._y = -300;
      }
      k++;
   }
   if(_root.krinAddMove)
   {
      _root.krinAddMove(t.playerID, t.playerID, 0);
   }
   _root.__rwDeathScan(c);
   return true;
};
// curacion: usa los modificadores de curacion recibida del objetivo (Hunted, Wicked Claws) y
// Winter Heart R2 (+15% en el lobo). Devuelve {h: curado, over: exceso}
_root.__rwHeal = function(u, amt, src)
{
   if(!_root.__rwAlive(u) || !(amt > 0))
   {
      return {h: 0, over: 0};
   }
   var k = 1;
   if(u.HEALMOD_PLUS != undefined)
   {
      k *= _root.__rwNum(u.HEALMOD_PLUS);
   }
   if(u.HEALMOD_MINUS != undefined)
   {
      k *= _root.__rwNum(u.HEALMOD_MINUS);
   }
   if(_root.__rwIsWolf(u) && _root.__rwRank(829) > 1)
   {
      k *= 1.15;
   }
   var h = Math.ceil(amt * k);
   var room = u.LIFEU - u.LIFEN;
   var real = Math.min(h, room);
   if(real > 0)
   {
      u.LIFEN += real;
      _root.__rwNumber(u, real, "HEAL");
   }
   _root.__rwLifeBar(u);
   return {h: real, over: h - real};
};
// golpe directo del lobo con el executeMove nativo (critico, Piercing contra Defensa, escudos, muerte).
// m: multiplicador; hunt: solo Strength (si no, Instinct x1,4 cuando es mayor). Devuelve {d, crit, dead}
_root.__rwStrike = function(c, t, id, m, el, hunt, forceCrit)
{
   var res = {d: 0, crit: false, dead: false};
   if(!_root.__rwAlive(t) || !(m > 0))
   {
      return res;
   }
   var a = _root["KRINABILITY" + id];
   var bb = _root["KRINABILITYB" + id].slice(0);
   var e = !el ? "Physical" : el;
   bb[0] = e;
   bb[9] = 0;
   bb[13] = 0;
   bb[16] = 0;
   var k = _root.__rwOutMult(c, t, true) * m;
   if(hunt || !_root.__rwUseIns(c))
   {
      bb[2] = k;
      bb[4] = 0;
   }
   else
   {
      bb[2] = 0;
      bb[4] = k * 1.4;
   }
   if(forceCrit)
   {
      bb[7] = 1000;
   }
   // Predator's Patience: Piercing por Scent del objetivo
   var pp = _root.__rwRank(817);
   var per0 = c.PERU[e];
   if(pp > 0 && per0 != undefined)
   {
      var sc = _root.__rwScent(t);
      var bonus = Math.min(pp > 1 ? 0.3 : 0.21, (pp > 1 ? 0.1 : 0.07) * sc);
      c.PERU[e] = per0 * (1 + bonus);
   }
   // Shardfall maestria: con 5 Ice Shards los ataques de hielo ignoran 20% de la Defensa de Hielo
   var dIce = t.DEFU.Ice;
   var cutIce = e == "Ice" && _root.__rwMastered(840) && _root.__rwShards(c) >= 5 && dIce != undefined;
   if(cutIce)
   {
      t.DEFU.Ice = dIce * 0.8;
   }
   var l0 = _root.__rwNum(t.LIFEN);
   var s0 = _root.__rwNum(t.SHIELD);
   _root.perKSuccess = false;
   _root.__v10NativeExecute(a, bb, c, t);
   res.crit = _root.perKSuccess == true;
   if(per0 != undefined)
   {
      c.PERU[e] = per0;
   }
   if(cutIce)
   {
      t.DEFU.Ice = dIce;
   }
   res.d = Math.max(0, l0 - _root.__rwNum(t.LIFEN)) + Math.max(0, s0 - _root.__rwNum(t.SHIELD));
   res.dead = !(t.LIFEN > 0);
   if(_root.__rwHas(c, "RWCOURAGE"))
   {
      _root.__rwDel(c, "RWCOURAGE");
   }
   if(!res.dead)
   {
      // Werezombie: cada golpe directo pone 1 Wound
      if(_root.__rwHas(c, "RWWERE1") || _root.__rwHas(c, "RWWERE2"))
      {
         _root.__rwWound(t, 1, c);
      }
      // Predator's Patience maestria: los criticos ponen 1 Wound
      if(res.crit && _root.__rwMastered(817))
      {
         _root.__rwWound(t, 1, c);
      }
   }
   // Bloodhound maestria: los ataques contra un Terrified devuelven 5 Focus
   if(_root.__rwHas(t, "RWTERROR"))
   {
      _root.__rwFocus(c, 5);
   }
   _root.__rwDeathScan(c);
   return res;
};
// Wounds que pone una habilidad del lobo: Killer Instinct suma 1 por habilidad (una vez por objetivo)
_root.__rwWound = function(t, n, c, turns)
{
   if(!_root.__rwAlive(t) || !(n > 0))
   {
      return 0;
   }
   var k = n;
   if(_root.__rwIsWolf(c) && (_root.__rwHas(c, "RWKILLER1") || _root.__rwHas(c, "RWKILLER2")) && t.__rwKiCast != _root.__rwCastSerial)
   {
      t.__rwKiCast = _root.__rwCastSerial;
      k++;
   }
   return _root.__rwAddWounds(t, k, c, turns);
};
_root.__rwCastSerial = 0;
_root.__rwShards = function(u)
{
   if(!u)
   {
      return 0;
   }
   if(!_root.__rwHas(u, "RWSHARD"))
   {
      u.__rwSh = 0;
      return 0;
   }
   return _root.__rwNum(u.__rwSh);
};
_root.__rwShardCap = function()
{
   if(_root.__rwHas(_root.__rwWolf(), "RWEWINTER"))
   {
      return 5;
   }
   var r = _root.__rwRank(840);
   if(r > 1)
   {
      return 5;
   }
   if(r > 0)
   {
      return 3;
   }
   return 2;
};
_root.__rwAddShards = function(n)
{
   var w = _root.__rwWolf();
   if(!_root.__rwAlive(w) || !(n > 0))
   {
      return 0;
   }
   var cur = _root.__rwShards(w);
   var nw = Math.min(_root.__rwShardCap(), cur + n);
   if(nw < cur)
   {
      nw = cur;
   }
   if(_root.__rwAdd(w, "RWSHARD", 4, w))
   {
      w.__rwSh = nw;
   }
   _root.__rwPaint(w);
   return nw - cur;
};
_root.__rwTakeShards = function(n)
{
   var w = _root.__rwWolf();
   var cur = _root.__rwShards(w);
   var k = Math.min(cur, n);
   if(!(k > 0))
   {
      return 0;
   }
   w.__rwSh = cur - k;
   if(!(w.__rwSh > 0))
   {
      w.__rwSh = 0;
      _root.__rwDel(w, "RWSHARD");
   }
   _root.__rwPaint(w);
   return k;
};
// quita efectos daninos (debuffs) de una unidad; devuelve cuantos
_root.__rwCleanse = function(u, n)
{
   if(!u || !u.BUFFARRAYK)
   {
      return 0;
   }
   var k = 0;
   var i = 0;
   while(i < u.BUFFARRAYK.length && k < n)
   {
      var b = u.BUFFARRAYK[i];
      if(b && b.CD > 0)
      {
         var df = _root["KRINBUFF" + b.buffId];
         if(df && df[20] < 0 && b.buffId != "RWSOLID" && b.buffId != "RWTOMB")
         {
            _root.__v10Remove(u, b.buffId);
            k++;
         }
      }
      i++;
   }
   if(k > 0)
   {
      _root.applyChangesKrin(u);
      _root.__rwPaint(u);
   }
   return k;
};
// disipa efectos beneficiosos de un enemigo
_root.__rwDispel = function(u, n)
{
   if(!u || !u.BUFFARRAYK)
   {
      return 0;
   }
   var k = 0;
   var i = 0;
   while(i < u.BUFFARRAYK.length && k < n)
   {
      var b = u.BUFFARRAYK[i];
      if(b && b.CD > 0)
      {
         var df = _root["KRINBUFF" + b.buffId];
         if(df && df[20] > 0 && !(df[32] >= 1))
         {
            _root.__v10Remove(u, b.buffId);
            k++;
         }
      }
      i++;
   }
   if(k > 0)
   {
      _root.applyChangesKrin(u);
      _root.__rwPaint(u);
   }
   return k;
};
// quita un efecto de dano en el tiempo del lobo (Unyielding)
_root.__rwRemoveDot = function(u)
{
   if(!u || !u.BUFFARRAYK)
   {
      return 0;
   }
   if(_root.__rwWounds(u) > 0)
   {
      _root.__rwTakeWounds(u, 99);
      return 1;
   }
   return _root.__i15Dot ? _root.__i15Dot(u, 1) : 0;
};
// enemigo con mas marcas (Wounds + Scent) y el mas herido (mas Wounds)
_root.__rwMostMarked = function(onlyScent)
{
   var best = null;
   var bn = 0;
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      var u = es[i];
      var m = _root.__rwScent(u) + (onlyScent ? 0 : _root.__rwWounds(u));
      if(m > bn)
      {
         bn = m;
         best = u;
      }
      i++;
   }
   return best;
};
_root.__rwMostWounded = function()
{
   var best = null;
   var bn = 0;
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      var m = _root.__rwWounds(es[i]);
      if(m > bn)
      {
         bn = m;
         best = es[i];
      }
      i++;
   }
   return best;
};
_root.__rwLowestAlly = function(includeWolf)
{
   var best = null;
   var br = 2;
   var tm = _root.__rwTeam();
   var i = 0;
   while(i < tm.length)
   {
      var u = tm[i];
      if(includeWolf || !_root.__rwIsWolf(u))
      {
         var r = u.LIFEN / u.LIFEU;
         if(r < br)
         {
            br = r;
            best = u;
         }
      }
      i++;
   }
   return best;
};
_root.__rwLowestEnemy = function(except)
{
   var best = null;
   var bl = 0;
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      if(es[i] != except && (best == null || es[i].LIFEN < bl))
      {
         best = es[i];
         bl = es[i].LIFEN;
      }
      i++;
   }
   return best;
};
// marcas en juego del lado enemigo (Scent + Wounds + Frostbite)
_root.__rwMarksInPlay = function()
{
   var n = 0;
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      n += _root.__rwScent(es[i]) + _root.__rwWounds(es[i]) + _root.__rwFrost(es[i]);
      i++;
   }
   return n;
};
_root.__rwAnyFrost = function()
{
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      if(_root.__rwFrost(es[i]) > 0)
      {
         return true;
      }
      i++;
   }
   return false;
};
_root.__rwTerrorUpdate = function(u)
{
   if(!u || u.playerID % 2 != 0)
   {
      return null;
   }
   var want = _root.__rwMastered(839) && _root.__rwAlive(u) && _root.__rwNum(u.FOCUSN) < 20;
   var has = _root.__rwHas(u, "RWTERROR");
   if(want && !has)
   {
      _root.__rwAdd(u, "RWTERROR", 99, _root.__rwWolf());
      _root.applyChangesKrin(u);
   }
   if(!want && has)
   {
      _root.__rwDel(u, "RWTERROR");
      _root.applyChangesKrin(u);
   }
};
