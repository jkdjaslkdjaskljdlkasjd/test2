// ------------------------------------------------------------------------------- ganchos del motor
// executeMove: las habilidades del lobo van a __rwCast; el resto sigue por la cadena de antes, con los
// efectos del lobo sobre enemigos y aliados antes y despues del golpe.
_root.__rwPrevExec = _root.executeMove;
_root.executeMove = function(a, b, c, t)
{
   if(!a || !c)
   {
      return _root.__rwPrevExec(a, b, c, t);
   }
   if(_root.__rwIsWolf(c) && _root.__rwIsWolfMove(a[1]))
   {
      return _root.__rwCast(a, b, c, t);
   }
   return _root.__rwOther(a, b, c, t);
};
// resto de la cadena. Los movimientos de la tabla vieja del lobo (623-628, 808-840) usados por otra unidad
// (Mokoshotar KNU55 o un aliado) saltan las capas viejas del lobo: esas capas los descartaban con rango 0.
_root.__rwInner = function(a, b, c, t)
{
   if(a && c && !_root.__rwIsWolf(c) && _root.__v10ById[a[1]] && _root.__v55PrevExecute)
   {
      if(!(c.LIFEN > 0))
      {
         return null;
      }
      if(_root.__a35Training && c.playerID % 2 == 0)
      {
         return null;
      }
      return _root.__v55PrevExecute(a, b, c, t);
   }
   return _root.__rwPrevExec(a, b, c, t);
};
_root.__rwIsDirect = function(a, b)
{
   if(!a || !b || a[14] != "Full Damage")
   {
      return false;
   }
   return _root.__rwNum(b[2]) > 0 || _root.__rwNum(b[4]) > 0 || _root.__rwNum(b[6]) > 0 || _root.__rwNum(b[9]) > 0;
};
// reduccion de dano recibido del lado del lobo (multiplicativa); dot: dano en el tiempo
_root.__rwTakenMult = function(t, c, dot)
{
   var k = 1;
   if(!t)
   {
      return k;
   }
   if(_root.__rwIsWolf(t))
   {
      var th = _root.__rwRank(825);
      if(th > 0)
      {
         k *= th > 1 ? 0.88 : 0.92;
         if(_root.__rwMastered(825) && _root.__rwAnyFrost())
         {
            k *= 0.9;
         }
      }
      var S = _root.__rwShards(t);
      if(S > 0)
      {
         k *= 1 - 0.03 * S;
      }
      if(_root.__rwHas(t, "RWRIME"))
      {
         k *= 1 - _root.__rwNum(t.__rwRimeRed);
      }
      if(_root.__rwHas(t, "RWSTAND1") || _root.__rwHas(t, "RWSTAND2"))
      {
         k *= 1 - _root.__rwNum(t.__rwStandRed);
      }
      if(_root.__rwHas(t, "RWANCFORM") || _root.__rwHas(t, "RWCALL"))
      {
         k *= 0.75;
      }
      if(dot)
      {
         var un = _root.__rwRank(828);
         if(un > 0)
         {
            k *= un > 1 ? 0.75 : 0.85;
         }
      }
   }
   else if(t.playerID % 2 == 1)
   {
      var cc = _root.__rwRank(845);
      if(cc > 0 && c && c.playerID % 2 == 0)
      {
         k *= 1 - Math.min(cc > 1 ? 0.15 : 0.1, (cc > 1 ? 0.03 : 0.02) * _root.__rwFrost(c));
      }
   }
   if(_root.__rwHas(t, "RWTOMB"))
   {
      k *= 0.1;
   }
   return k;
};
// bonos de los aliados contra enemigos (Pack Tactics, Canine, Feeding Frenzy, Frostbound Pack, Courage)
_root.__rwAllyMult = function(c, t)
{
   var add = 0;
   var sc = _root.__rwScent(t);
   var W = _root.__rwWounds(t);
   var fb = _root.__rwFrost(t);
   var pt = _root.__rwRank(823);
   if(pt > 0)
   {
      // Pack Tactics: solo por Wound (sin el bono por Scent)
      add += Math.min(pt > 1 ? 0.15 : 0.1, (pt > 1 ? 0.03 : 0.02) * W);
   }
   if(_root.__rwHas(c, "RWCANINE1") || _root.__rwHas(c, "RWCANINE2"))
   {
      add += Math.min(0.25, 0.05 * W);
   }
   if(_root.__rwHas(c, "RWFRENZY"))
   {
      var fr = _root.__rwNum(c.__rwFrenzyR);
      add += Math.min(fr > 1 ? 0.4 : 0.3, (fr > 1 ? 0.08 : 0.06) * W);
   }
   if(_root.__rwHas(c, "RWFROSTPACK"))
   {
      var fp = _root.__rwNum(c.__rwFrostPackR);
      add += Math.min(fp > 1 ? 0.3 : 0.2, (fp > 1 ? 0.06 : 0.04) * fb);
   }
   if(_root.__rwHas(c, "RWCOURAGE"))
   {
      add += _root.__rwNum(c.__rwCourage);
   }
   var k = 1 + add;
   c.__rwFrenzyEat = false;
   if(_root.__rwHas(c, "RWFRENZY") && _root.__rwMastered(834) && W >= 5)
   {
      k *= 1.5;
      c.__rwFrenzyEat = true;
   }
   return k;
};
_root.__rwOther = function(a, b, c, t)
{
   if(!t)
   {
      return _root.__rwInner(a, b, c, t);
   }
   // primera parte de la accion de esta unidad: Black Ice y Bloodhound (una vez por accion)
   if(c.playerID % 2 == 0 && c.__rwActSeen != c.__rwTurnNo)
   {
      c.__rwActSeen = c.__rwTurnNo;
      _root.__rwIceStep(c);
      var bh = _root.__rwRank(839);
      var W = _root.__rwWounds(c);
      if(bh > 0 && W > 0 && _root.__rwAlive(c))
      {
         _root.__rwDrain(c, Math.min(15, (bh > 1 ? 3 : 2) * W));
      }
      _root.__rwTerrorUpdate(c);
      if(!_root.__rwAlive(c))
      {
         _root.__rwDeathScan(_root.__rwWolf());
         return null;
      }
   }
   var hostile = _root.__rwHostile(c, t);
   var direct = _root.__rwIsDirect(a, b);
   var bb = b;
   var ally = hostile && direct && c.playerID % 2 == 1 && !_root.__rwIsWolf(c);
   if(ally)
   {
      var k = _root.__rwAllyMult(c, t);
      if(k != 1)
      {
         bb = b.slice(0);
         bb[2] = _root.__rwNum(bb[2]) * k;
         bb[4] = _root.__rwNum(bb[4]) * k;
         bb[6] = _root.__rwNum(bb[6]) * k;
         bb[9] = _root.__rwNum(bb[9]) * k;
      }
   }
   var foe = hostile && c.playerID % 2 == 0 && t.playerID % 2 == 1;
   var keep = null;
   var share = 0;
   var w = _root.__rwWolf();
   var wardBefore = foe && _root.__rwHas(t, "RWSH_WARD") && _root.__rwNum(t.SHIELD) > 0;
   if(foe)
   {
      var red = _root.__rwTakenMult(t, c, false);
      if(t != w && _root.__rwHas(t, "RWGUARD") && _root.__rwAlive(w) && _root.__rwNum(w.SHIELD) > 0)
      {
         share = _root.__rwNum(t.__rwGuardShare);
         red *= 1 - share;
      }
      if(red != 1)
      {
         keep = t.IDMGP2;
         t.IDMGP2 = (t.IDMGP2 == undefined ? 1 : _root.__rwNum(t.IDMGP2)) * red;
      }
   }
   var l0 = _root.__rwNum(t.LIFEN);
   var s0 = _root.__rwNum(t.SHIELD);
   _root.perKSuccess = false;
   var res = _root.__rwInner(a, bb, c, t);
   var crit = _root.perKSuccess == true;
   if(keep != null)
   {
      t.IDMGP2 = keep;
   }
   var dealt = Math.max(0, l0 - _root.__rwNum(t.LIFEN)) + Math.max(0, s0 - _root.__rwNum(t.SHIELD));
   if(foe && direct)
   {
      _root.__rwReactive(c, t, dealt, share, wardBefore);
   }
   if(ally)
   {
      _root.__rwAllyPost(c, t, dealt, crit);
   }
   _root.__rwDeathScan(c);
   _root.__rwAncestorsCheck(w);
   return res;
};
// el enemigo c golpeo con un ataque directo a t (lobo o aliado)
_root.__rwReactive = function(c, t, dealt, share, wardBefore)
{
   var w = _root.__rwWolf();
   if(!_root.__rwAlive(c))
   {
      return null;
   }
   if(t == w)
   {
      if(_root.__rwHas(w, "RWRIME"))
      {
         _root.__rwAddFrost(c, 1, w, "rime");
      }
      if(_root.__rwRank(840) > 1 && _root.__rwShards(w) >= 3 && _root.__rwAlive(c))
      {
         _root.__rwAddFrost(c, 1, w);
      }
      if((_root.__rwHas(w, "RWSTAND1") || _root.__rwHas(w, "RWSTAND2")) && _root.__rwMastered(827) && _root.__rwAlive(c))
      {
         if(_root.__rwBrittle(c) && !_root.__rwFreezeImmune(c))
         {
            _root.__rwFreeze(c, w, "stand");
         }
         else
         {
            _root.__rwAddFrost(c, 2, w);
         }
      }
   }
   if(t != w && _root.__rwHas(t, "RWGUARD"))
   {
      _root.__rwAddFrost(c, 1, w);
      if(share > 0 && dealt > 0 && _root.__rwAlive(w))
      {
         var abs = dealt * share / (1 - share);
         var sh = _root.__rwNum(w.SHIELD);
         var took = Math.min(sh, abs);
         w.SHIELD = sh - took;
         if(took > 0)
         {
            _root.__rwShieldFx(w, "Physical");
         }
         var rest = abs - took;
         if(rest > 0 && _root.__rwAlive(t))
         {
            _root.__rwRawHit(c, t, rest, "Physical");
         }
         if(!(w.SHIELD > 0))
         {
            _root.__rwDel(t, "RWGUARD");
            _root.__rwDel(w, "RWSH_GUARD");
            if(_root.__rwMastered(822) && _root.__rwAlive(c))
            {
               _root.__rwStrike(w, c, 822, 1.2, "Physical", true);
               _root.__rwAddWounds(c, 2, w);
            }
         }
         _root.__rwLifeBar(w);
      }
   }
   if(wardBefore && _root.__rwAlive(c))
   {
      _root.__rwAddWounds(c, 1, w);
   }
};
_root.__rwAllyPost = function(c, t, dealt, crit)
{
   var w = _root.__rwWolf();
   if(_root.__rwHas(c, "RWCOURAGE"))
   {
      _root.__rwDel(c, "RWCOURAGE");
   }
   if(c.__rwFrenzyEat && _root.__rwAlive(t))
   {
      _root.__rwTakeWounds(t, 1);
   }
   c.__rwFrenzyEat = false;
   var hp = 0;
   if(_root.__rwHas(c, "RWFRENZY"))
   {
      hp += dealt * (_root.__rwNum(c.__rwFrenzyR) > 1 ? 0.15 : 0.1);
   }
   var hunted = _root.__rwHunted(t);
   if(_root.__rwRank(823) > 1 && hunted)
   {
      hp += dealt * 0.15;
   }
   if(hp > 0)
   {
      _root.__rwHeal(c, hp, c);
   }
   if(hunted && _root.__rwMastered(823) && c.__rwPTTurn != c.__rwTurnNo)
   {
      c.__rwPTTurn = c.__rwTurnNo;
      _root.__rwFocus(w, 5);
   }
   if(_root.__rwHas(c, "RWFROSTPACK") && c.__rwFPTurn != c.__rwTurnNo && _root.__rwAlive(t))
   {
      c.__rwFPTurn = c.__rwTurnNo;
      _root.__rwAddFrost(t, crit && _root.__rwBrittle(t) && _root.__rwMastered(835) ? 2 : 1, w);
   }
};

// ---- buffTicker: tic de Wounds antes del tic nativo; efectos por turno despues
_root.__rwPrevTicker = _root.buffTicker;
_root.buffTicker = function(u)
{
   if(!u)
   {
      return _root.__rwPrevTicker(u);
   }
   if(_root.__rwExtraHalf && u.playerID % 2 == 1 && !_root.__rwIsWolf(u))
   {
      _root.buffTickChecker = false;
      return null;
   }
   _root.__rwActor = u;
   _root.__rwWoundTick(u);
   if(u.playerID % 2 == 1 && _root.__rwAlive(u))
   {
      var k = _root.__rwTakenMult(u, null, true);
      if(k != 1)
      {
         u.IDMGP2 = (u.IDMGP2 == undefined ? 1 : _root.__rwNum(u.IDMGP2)) * k;
      }
   }
   var z = _root.__rwPrevTicker(u);
   _root.__rwActor = null;
   _root.__rwAfterTurn(u);
   return z;
};
_root.__rwWoundTick = function(u)
{
   var W = _root.__rwWounds(u);
   if(!(W > 0) || !_root.__rwAlive(u))
   {
      return 0;
   }
   var w = _root.__rwWolf();
   var self = u == w;
   var raw = W * _root.__rwWoundPer(u);
   var times = 1;
   if(!self)
   {
      if(_root.__rwHas(w, "RWBMOON"))
      {
         times *= 2;
      }
      if(_root.__rwMastered(841) && _root.__rwFrozen(u))
      {
         times *= 2;
      }
   }
   var total = 0;
   var i = 0;
   while(i < times && _root.__rwAlive(u))
   {
      total += _root.__rwPure(self ? null : w, u, raw, "Physical", true);
      i++;
   }
   if(self || !(total > 0))
   {
      return total;
   }
   if(_root.__rwHas(w, "RWBMOON"))
   {
      _root.__rwHeal(w, total * 0.3, w);
   }
   var sh = _root.__rwRank(844);
   if(sh > 0)
   {
      var low = _root.__rwLowestAlly(true);
      if(low)
      {
         var h = _root.__rwHeal(low, total * (sh > 1 ? 0.3 : 0.2), w);
         if(h.over > 0 && _root.__rwMastered(844))
         {
            _root.__rwShieldAdd(low, "RWSH_HUNGER", Math.min(h.over, low.LIFEU * 0.15), 2, w);
         }
      }
   }
   var bd = _root.__rwRank(846);
   if(bd > 0 && _root.__rwAlive(w))
   {
      var h2 = _root.__rwHeal(w, total * (bd > 1 ? 0.25 : 0.15), w);
      if(h2.over > 0 && _root.__rwMastered(846))
      {
         _root.__rwShieldAdd(w, "RWSH_DRINK", Math.min(h2.over, w.LIFEU * 0.2), 2, w);
      }
   }
   if(_root.__rwRank(811) > 0 && _root.__rwFrost(u) > 0 && _root.__rwAlive(u))
   {
      _root.__rwAddScent(u, 1, w);
   }
   _root.__rwDeathScan(w);
   return total;
};
// despues del tic nativo de la unidad u (fin de su turno)
_root.__rwAfterTurn = function(u)
{
   u.__rwTurnNo = _root.__rwNum(u.__rwTurnNo) + 1;
   var w = _root.__rwWolf();
   if(u == w)
   {
      _root.__rwWolfTurn++;
      if(_root.__rwAlive(w))
      {
         if(_root.__rwHas(w, "RWWERE1") || _root.__rwHas(w, "RWWERE2"))
         {
            _root.__rwHeal(w, w.LIFEU * (_root.__rwHas(w, "RWWERE2") ? 0.12 : 0.08), w);
         }
         var sf = _root.__rwRank(840);
         var S = _root.__rwShards(w);
         if(sf > 0 && S > 0)
         {
            _root.__rwFocus(w, 2 * S);
         }
         if(_root.__rwRank(828) > 1)
         {
            _root.__rwFocus(w, 5);
         }
         if(_root.__rwHas(w, "RWEWINTER") && _root.__rwHas(w, "RWSHARD"))
         {
            _root.__rwSetLeft(w, "RWSHARD", 4);
         }
      }
      if(w.__rwBMoonOn && !_root.__rwHas(w, "RWBMOON"))
      {
         w.__rwBMoonOn = false;
         _root.__rwBloodMoonSet();
      }
      if(_root.__rwHas(w, "RWBMOON"))
      {
         w.__rwBMoonOn = true;
      }
      if(w.__rwEWinterOn && !_root.__rwHas(w, "RWEWINTER"))
      {
         w.__rwEWinterOn = false;
         _root.__rwWinterEnd();
      }
      if(_root.__rwHas(w, "RWEWINTER"))
      {
         w.__rwEWinterOn = true;
      }
      if(w.__rwAncOn && !_root.__rwHas(w, "RWANCFORM"))
      {
         w.__rwAncOn = false;
         _root.__rwAdd(w, "RWSPENT", 2, w);
         _root.applyChangesKrin(w);
      }
   }
   if(u.__rwWasFrozen && !_root.__rwFrozen(u))
   {
      u.__rwWasFrozen = false;
      var wg = _root.__rwRank(842);
      if(wg > 0 && _root.__rwAlive(u))
      {
         _root.__rwSetFrost(u, wg > 1 ? 2 : 1, w);
      }
   }
   else if(_root.__rwNum(u.__rwFrzImm) > 0)
   {
      u.__rwFrzImm--;
   }
   if(u.__rwTombOn && !_root.__rwHas(u, "RWTOMB"))
   {
      u.__rwTombOn = false;
      if(_root.__rwAlive(u))
      {
         _root.__rwHeal(u, u.LIFEU * 0.15, w);
      }
      if(_root.__rwMastered(838))
      {
         var es = _root.__rwEnemies();
         var i = 0;
         while(i < es.length)
         {
            _root.__rwAddFrost(es[i], 1, w);
            i++;
         }
      }
   }
   if(u.__rwPrimalOn && !_root.__rwHas(u, "RWPRIMAL1") && !_root.__rwHas(u, "RWPRIMAL2"))
   {
      u.__rwPrimalOn = false;
      if(_root.__rwMastered(808) && _root.__rwAlive(u))
      {
         _root.__rwHeal(u, u.LIFEU * 0.15, w);
         _root.__rwAdd(u, "RWPRIMALEND", 2, w);
         _root.applyChangesKrin(u);
      }
   }
   _root.__rwTerrorUpdate(u);
   _root.__rwDeathScan(w);
   _root.__rwAncestorsCheck(w);
   _root.__rwPaint(u);
};
// Blood Moon Rising al terminar: todos los Wounds de todos los enemigos estallan al 100%
_root.__rwBloodMoonSet = function()
{
   var w = _root.__rwWolf();
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      var u = es[i];
      var bl = _root.__rwBleedLeft(u);
      if(bl > 0)
      {
         _root.__rwTakeWounds(u, 99);
         _root.__rwPure(w, u, bl, "Physical", true);
      }
      i++;
   }
   _root.__rwDeathScan(w);
};
// Endless Winter al terminar: todo el Frostbite estalla (60% de Strength, 84% de Instinct si es mayor, por acumulacion)
_root.__rwWinterEnd = function()
{
   var w = _root.__rwWolf();
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      var u = es[i];
      var fb = _root.__rwFrost(u);
      if(fb > 0)
      {
         _root.__rwSetFrost(u, 0);
         _root.__rwPure(w, u, _root.__rwPower(w, 0.6 * fb), "Ice", true);
      }
      i++;
   }
   _root.__rwDeathScan(w);
};
_root.__rwOnFreeze = function(u, c, src)
{
   var w = _root.__rwWolf();
   _root.__rwFrozeSerial = _root.__rwCastSerial;
   _root.__rwAddShards(2);
   _root.__rwHuntOrFreezeEvent();
   if(_root.__rwMastered(845))
   {
      var tm = _root.__rwTeam();
      var i = 0;
      while(i < tm.length)
      {
         _root.__rwFocus(tm[i], 10);
         i++;
      }
   }
   if(_root.__rwMastered(829) && _root.__rwAlive(w))
   {
      _root.__rwShieldAdd(w, "RWSH_HEART", w.LIFEU * 0.15, 2, w);
   }
   if(src == "rime" && _root.__rwMastered(837))
   {
      _root.__rwPure(w, u, _root.__rwPower(w, 1.5), "Ice", true);
   }
   if(_root.__rwHas(u, "RWBLACKICE") && _root.__rwMastered(833))
   {
      _root.__rwPure(w, u, _root.__rwPower(w, 1.5), "Ice", true);
      _root.__rwAddShards(2);
   }
};
// muertes: estallido de Deep Wounds, Killer Instinct maestria, Ancestors' Blessing
_root.__rwDeathScan = function(killer)
{
   var i = 1;
   while(i < 7)
   {
      var u = _root["playerKrin" + i];
      if(u)
      {
         var alive = u.active == true && u.LIFEN > 0;
         if(u.__rwWasAlive == true && !alive)
         {
            u.__rwWasAlive = false;
            _root.__rwOnDeath(u, killer);
         }
         else
         {
            u.__rwWasAlive = alive;
         }
      }
      i++;
   }
};
_root.__rwOnDeath = function(u, killer)
{
   var w = _root.__rwWolf();
   if(u.playerID % 2 == 0)
   {
      var W = _root.__rwWounds(u);
      if(W > 0 && _root.__rwRank(814) > 1 && !u.__rwNoBurst)
      {
         var bl = _root.__rwBleedLeft(u) * 0.5;
         u.__rwW = 0;
         var es = _root.__rwEnemies();
         var k = 0;
         while(k < es.length)
         {
            _root.__rwPure(w, es[k], bl, "Physical", true);
            k++;
         }
      }
      if(_root.__rwMastered(832) && _root.__rwAlive(w))
      {
         var kid = _root.__rwHas(w, "RWKILLER2") ? "RWKILLER2" : (_root.__rwHas(w, "RWKILLER1") ? "RWKILLER1" : "");
         if(kid != "")
         {
            _root.__rwSetLeft(w, kid, _root.__rwLeft(w, kid) + 1);
            _root.__rwHeal(w, w.LIFEU * 0.15, w);
         }
      }
   }
   else if(!_root.__rwIsWolf(u) && _root.__rwHas(u, "RWBLESS") && !u.__rwSpirit)
   {
      _root.__rwSpiritWolf(u);
   }
};
// Ancestors' Blessing: el aliado caido vuelve como lobo ancestral (valores provisionales)
_root.__rwBuffDef("RWSPIRIT", "Ancestral Wolf", "Ice", 1, 999, [31], [16], "");
_root.__rwSpiritWolf = function(u)
{
   var w = _root.__rwWolf();
   u.__rwSpirit = true;
   var i = 0;
   while(i < u.BUFFARRAYK.length)
   {
      if(u.BUFFARRAYK[i].CD > 0)
      {
         _root.__v10Remove(u, u.BUFFARRAYK[i].buffId);
      }
      i++;
   }
   u.active = true;
   u.STRENGTH = _root.__rwNum(w.STRENGTHU);
   u.MAGIC = _root.__rwNum(w.MAGICU);
   u.LIFEN = Math.ceil(u.LIFEU * 0.5);
   u.FOCUSN = u.FOCUSU;
   u.playerName = "Ancestral Wolf";
   u.moveArrayA = [624, 628];
   u.CDArrayA = [0, 0];
   u.moveArrayD = [625];
   u.CDArrayD = [0];
   u.moveArrayABS = [];
   u.CDArrayABS = [];
   u.STUN = 0;
   u.__rwWasAlive = true;
   _root.__rwAdd(u, "RWSPIRIT", 999, w);
   _root.applyChangesKrin(u);
   _root.__rwLifeBar(u);
   _root.__rwNote("An ancestral wolf takes " + u.__rwOldName + "'s place!");
};
// Aspect of the Ancestors: una vez por combate, por debajo del 40% de vida
_root.__rwAncestorsCheck = function(w)
{
   if(!w || _root.__rwAspect() != 4 || _root.__rwAncUsed || !_root.__rwAlive(w))
   {
      return null;
   }
   if(w.LIFEN < 0.4 * w.LIFEU)
   {
      _root.__rwAncUsed = true;
      _root.__rwAdd(w, "RWANCFORM", 3, w);
      w.__rwAncOn = true;
      _root.applyChangesKrin(w);
      _root.__rwNote("The ancestors take Mokoshotar's body!");
   }
};
// ---- applyChangesKrin: Defensa (Thick Hide, Hemorrhage)
_root.__rwPrevChanges = _root.applyChangesKrin;
_root.applyChangesKrin = function(u)
{
   var z = _root.__rwPrevChanges(u);
   if(!u || !u.DEFU)
   {
      return z;
   }
   if(_root.__rwIsWolf(u))
   {
      var th = _root.__rwRank(825);
      if(th > 0)
      {
         var q = th > 1 ? 1.28 : 1.18;
         if(u.DEFU.Physical != undefined)
         {
            u.DEFU.Physical *= q;
         }
         if(u.DEFU.Ice != undefined)
         {
            u.DEFU.Ice *= q;
         }
      }
   }
   if(_root.__rwHas(u, "RWHEMO"))
   {
      if(u.DEFU.Physical != undefined)
      {
         u.DEFU.Physical *= 0.8;
      }
      if(u.DEFU.Ice != undefined)
      {
         u.DEFU.Ice *= 0.8;
      }
   }
   return z;
};
// ---- __v10Life: Undying Will
_root.__rwPrevLife = _root.__v10Life;
_root.__v10Life = function(next, u, source, dot)
{
   var r = _root.__rwPrevLife(next, u, source, dot);
   if(u && _root.__rwIsWolf(u) && !(r > 0) && u.LIFEN > 0 && _root.__rwRank(830) > 0 && !u.__rwUndyingUsed)
   {
      u.__rwUndyingUsed = true;
      r = Math.ceil(u.LIFEU * 0.25);
      _root.__rwCleanse(u, 99);
      _root.__rwShieldAdd(u, "RWSH_UNDY", u.LIFEU * 0.2, 2, u);
      _root.__rwNote("Mokoshotar refuses to fall!");
      if(_root.__rwMastered(830) && source && _root.__rwHostile(source, u) && _root.__rwAlive(source))
      {
         _root.__rwAddScent(source, 3, u);
         _root.__rwAddFrost(source, 3, u);
         _root.__rwAddWounds(source, 3, u);
      }
   }
   return r;
};
// ---- applyBuffKrin: inmunidad a aturdimientos (Ancestral Form, Unyielding maestria)
_root.__rwPrevApplyBuff = _root.applyBuffKrin;
_root.applyBuffKrin = function(u, bn, sign, c, v, ix)
{
   if(sign == 1 && u && _root.__rwIsWolf(u) && c && c != u && _root.__rwHostile(c, u))
   {
      var df = _root["KRINBUFF" + bn];
      if(df && df[17] > 0 && (_root.__rwHas(u, "RWANCFORM") || _root.__rwHas(u, "RWSTUNIMM")))
      {
         return null;
      }
   }
   return _root.__rwPrevApplyBuff(u, bn, sign, c, v, ix);
};
// ---- inicio del turno de cada enemigo (el reloj llama a LowerCD y AImoveAdder al planificar)
_root.__rwPrevLowerCD = _root.LowerCD;
_root.LowerCD = function(p)
{
   var u = _root["playerKrin" + p];
   if(_root.__rwExtraHalf && u && u.playerID % 2 == 1 && !_root.__rwIsWolf(u))
   {
      return null;
   }
   var z = _root.__rwPrevLowerCD(p);
   if(u && u.playerID % 2 == 0 && _root.__rwAlive(u))
   {
      var w = _root.__rwWolf();
      if(_root.__rwHas(w, "RWBMOON"))
      {
         _root.__rwAddWounds(u, 1, w);
      }
      if(_root.__rwHas(w, "RWEWINTER"))
      {
         _root.__rwAddFrost(u, 2, w);
         if(_root.__rwAlive(u))
         {
            _root.__rwAdd(u, "RWWSLOW", 1, w);
            _root.applyChangesKrin(u);
         }
      }
      _root.__rwTerrorUpdate(u);
   }
   return z;
};
_root.__rwPrevAI = _root.AImoveAdder;
_root.AImoveAdder = function(p)
{
   var u = _root["playerKrin" + p];
   if(_root.__rwExtraHalf && u && u.playerID % 2 == 1 && !_root.__rwIsWolf(u))
   {
      _root.krinAddMove(p, p, 0);
      return null;
   }
   return _root.__rwPrevAI(p);
};
// ---- reloj de combate (fotograma 217): esquiva y turno extra
_root.__rwNoDodge = function(c, t, a)
{
   if(!c || !t || !a || !_root.__rwIsWolf(c) || !_root.__rwIsWolfMove(a[1]))
   {
      return false;
   }
   return _root.__rwHas(c, "RWKILLER1") || _root.__rwHas(c, "RWKILLER2") || _root.__rwHunted(t);
};
_root.__rwExtraTurn = function()
{
   if(_root.__rwExtraHalf)
   {
      _root.__rwExtraHalf = false;
      return false;
   }
   if(!_root.__rwExtraPending)
   {
      return false;
   }
   _root.__rwExtraPending = false;
   if(!_root.__rwAlive(_root.__rwWolf()) || _root.__rwEnemies().length < 1)
   {
      return false;
   }
   _root.__rwExtraHalf = true;
   _root.__rwNote("Mokoshotar acts again!");
   return true;
};
// ---- inicio de combate
_root.__rwBattleStart = function()
{
   _root.__rwWolfTurn = 0;
   _root.__rwCrippleTurn = -99;
   _root.__rwExtraPending = false;
   _root.__rwExtraHalf = false;
   _root.__rwAncUsed = false;
   var w = _root.__rwWolf();
   var i = 1;
   while(i < 7)
   {
      var u = _root["playerKrin" + i];
      if(u)
      {
         u.__rwW = 0;
         u.__rwFB = 0;
         u.__rwSc = 0;
         u.__rwSh = 0;
         u.__rwFrzImm = 0;
         u.__rwWasFrozen = false;
         u.__rwTombOn = false;
         u.__rwPrimalOn = false;
         u.__rwTurnNo = 0;
         u.__rwSpirit = false;
         u.__rwOldName = u.playerName;
         u.__rwWasAlive = u.active == true && u.LIFEN > 0;
      }
      i++;
   }
   if(w && w.changeArray && !w.__rwAncApplied)
   {
      w.__rwUndyingUsed = false;
      w.__rwBMoonOn = false;
      w.__rwEWinterOn = false;
      w.__rwAncOn = false;
      if(_root.__rwAncestralStats())
      {
         var ab = _root.__rwAncBonus();
         w.changeArray[1] = _root.__rwNum(w.changeArray[1]) + ab;
         w.changeArray[3] = _root.__rwNum(w.changeArray[3]) + ab;
         w.changeArray[5] = _root.__rwNum(w.changeArray[5]) + ab;
         w.changeArray[7] = _root.__rwNum(w.changeArray[7]) + ab;
      }
      w.__rwAncApplied = true;
      _root.applyChangesKrin(w);
      if(_root.__rwAspect() == 3)
      {
         var al = _root.__rwAllies();
         var j = 0;
         while(j < al.length)
         {
            var x = al[j];
            if(x.changeArray)
            {
               x.changeArray[1] = _root.__rwNum(x.changeArray[1]) + 0.1;
               x.changeArray[3] = _root.__rwNum(x.changeArray[3]) + 0.1;
               x.changeArray[5] = _root.__rwNum(x.changeArray[5]) + 0.1;
               _root.applyChangesKrin(x);
            }
            j++;
         }
      }
   }
   var cd = _root.Krin.abilityCoolDown;
   var mm = _root.Krin.moveMatrix;
   if(cd && mm)
   {
      var k = 0;
      while(k < mm.length)
      {
         var d = _root.__rwS[mm[k]];
         if(d && d.pg == 3)
         {
            cd[k] = 0;
         }
         k++;
      }
   }
   _root.__v8Sync();
};
_root.__rwTick = function()
{
   if(_root._currentframe == 217)
   {
      if(!_root.__rwInBattle)
      {
         _root.__rwBattleWait = _root.__rwNum(_root.__rwBattleWait) + 1;
         if(_root.__rwBattleWait > 2)
         {
            _root.__rwInBattle = true;
            _root.__rwBattleWait = 0;
            _root.__rwBattleStart();
         }
      }
   }
   else
   {
      _root.__rwInBattle = false;
      _root.__rwBattleWait = 0;
      if(_root._currentframe == 181)
      {
         _root.__rwTickN = _root.__rwNum(_root.__rwTickN) + 1;
         if(_root.__rwTickN % 15 == 0)
         {
            _root.__rwMigrate();
            if(_root.__rwSyncBonus() != 0 && _root.__v9Tree)
            {
               _root.__rwTreeRefresh();
            }
         }
      }
   }
};
if(!_root.__rwCtl)
{
   _root.createEmptyMovieClip("__rwCtl", 980460);
   _root.__rwCtl.onEnterFrame = function()
   {
      _root.__rwTick();
   };
}
