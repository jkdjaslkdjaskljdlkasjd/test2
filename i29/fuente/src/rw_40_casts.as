// ------------------------------------------------------------------------------- habilidades del lobo
// __rwCast recibe la jugada del reloj de combate (misma firma que executeMove) y llama a __rwDo<id>.
_root.__rwCast = function(a, b, c, t)
{
   var id = a[1];
   var d = _root.__rwS[id];
   if(!d || !c)
   {
      return null;
   }
   var r = _root.__rwRank(id);
   if(r < 1)
   {
      r = 1;
   }
   if(!t)
   {
      t = c;
   }
   _root.__rwCastSerial++;
   _root.__rwActor = c;
   _root.__rwInCast = true;
   _root.__rwCons = {sc: 0, w: 0, fb: 0};
   _root.__rwFrozeSerial = -1;
   var f = _root["__rwDo" + id];
   if(f)
   {
      f(c, t, r, id);
   }
   _root.__rwFinishAction(c);
   _root.__rwInCast = false;
   return null;
};
// al final de cada accion del lobo: Relentless Hunt, Winter Heart, Unyielding, Werezombie maestria
_root.__rwFinishAction = function(c)
{
   var cs = _root.__rwCons;
   // cada pasiva cuenta Scent o Wounds, no los dos: Relentless Hunt Scent y Frostbite, Winter Heart Wounds y
   // Frostbite, Unyielding solo Wounds
   var nh = cs.sc + cs.fb;
   var rh = _root.__rwRank(820);
   if(rh > 0 && nh > 0)
   {
      _root.__rwFocus(c, (rh > 1 ? 9 : 6) * nh);
   }
   var nw = cs.w + cs.fb;
   var wh = _root.__rwRank(829);
   if(wh > 0 && nw > 0 && _root.__rwAlive(c))
   {
      var pct = Math.min(wh > 1 ? 0.4 : 0.35, (wh > 1 ? 0.1 : 0.07) * nw);
      _root.__rwShieldAdd(c, "RWSH_HEART", c.LIFEU * pct, 2, c);
   }
   if(_root.__rwRank(828) > 0 && cs.w > 0)
   {
      _root.__rwRemoveDot(c);
      if(_root.__rwMastered(828) && cs.w >= 3)
      {
         _root.__rwAdd(c, "RWSTUNIMM", 1, c);
      }
   }
   if(cs.sc > 0 && _root.__rwMastered(809))
   {
      var wid = _root.__rwHas(c, "RWWERE2") ? "RWWERE2" : (_root.__rwHas(c, "RWWERE1") ? "RWWERE1" : "");
      if(wid != "")
      {
         var ext = Math.min(2 - _root.__rwNum(c.__rwWereExt), cs.sc);
         if(ext > 0)
         {
            _root.__rwSetLeft(c, wid, _root.__rwLeft(c, wid) + ext);
            c.__rwWereExt = _root.__rwNum(c.__rwWereExt) + ext;
         }
         _root.__rwHeal(c, c.LIFEU * 0.05 * cs.sc, c);
      }
   }
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      _root.__rwTerrorUpdate(es[i]);
      i++;
   }
   _root.__rwAncestorsCheck(c);
   _root.__rwPaintAll();
};
_root.__rwRushLevel = function(c)
{
   var i = 3;
   while(i > 0)
   {
      if(_root.__rwHas(c, "RWRUSH" + i))
      {
         return i;
      }
      i--;
   }
   return 0;
};
// ---------------------------------------------------------------- Hunt
_root.__rwDo861 = function(c, t, r, id)
{
   var had = _root.__rwWounds(t) > 0;
   var hunted = _root.__rwHunted(t);
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.7, 2, 2.35], r), "Physical", true);
   if(res.dead)
   {
      return null;
   }
   var w = _root.__rwAt([2, 2, 3], r);
   if(r == 2 && had)
   {
      w++;
   }
   var turns = 0;
   if(_root.__rwMastered(861) && hunted)
   {
      w++;
      turns = 5;
   }
   _root.__rwWound(t, w, c, turns);
   _root.__rwAddScent(t, had ? 2 : 1, c);
};
_root.__rwDo810 = function(c, t, r, id)
{
   var sc = _root.__rwScent(t);
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.65, 1.9], r) * (1 + 0.3 * sc), "Physical", true);
   if(sc > 0)
   {
      _root.__rwFocus(c, _root.__rwAt([8, 10], r) * sc);
   }
   var n = Math.min(3, _root.__rwRushLevel(c) + 1);
   var k = 1;
   while(k <= 3)
   {
      _root.__rwDel(c, "RWRUSH" + k);
      k++;
   }
   _root.__rwAdd(c, "RWRUSH" + n, 3, c);
   _root.applyChangesKrin(c);
   if(n >= 3 && _root.__rwMastered(810) && !res.dead)
   {
      _root.__rwWound(t, 1, c);
      _root.__rwAddScent(t, 1, c);
   }
};
_root.__rwCrippleTurn = -99;
_root.__rwDo812 = function(c, t, r, id)
{
   var had = _root.__rwWounds(t) > 0;
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.75, 2.05], r), "Physical", true);
   if(res.dead)
   {
      return null;
   }
   _root.__rwAdd(t, "RWHAM" + r, 2, c);
   _root.__rwWound(t, 1, c);
   _root.__rwAddScent(t, had ? 2 : 1, c);
   _root.applyChangesKrin(t);
   if(_root.__rwMastered(812) && _root.__rwHunted(t) && _root.__rwNum(t.SPEEDU) < _root.__rwNum(c.SPEEDU) && _root.__rwWolfTurn - _root.__rwCrippleTurn >= 4)
   {
      _root.__rwCrippleTurn = _root.__rwWolfTurn;
      _root.__rwAdd(t, "RWCRIPPLE", 1, c);
      _root.__rwNote(t.playerName + " loses its next turn!");
   }
};
_root.__rwDo831 = function(c, t, r, id)
{
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.5, 1.8], r), "Physical", true);
   if(res.dead)
   {
      return null;
   }
   var W = _root.__rwWounds(t);
   if(!(W > 0))
   {
      return null;
   }
   var bleed = _root.__rwBleedLeft(t);
   _root.__rwTakeWounds(t, W);
   _root.__rwConsumed("w", W);
   _root.__rwPure(c, t, bleed * _root.__rwAt([1.3, 1.5], r), "Physical", true);
   if(!_root.__rwAlive(t))
   {
      return null;
   }
   _root.__rwAddScent(t, Math.floor(W / 2), c);
   if(W >= 3)
   {
      var ht = 2;
      if(_root.__rwMastered(831) && W >= 5)
      {
         ht = 3;
         _root.__rwAdd(t, "RWTORN", 2, c);
      }
      _root.__rwAdd(t, "RWHEMO", ht, c);
      _root.applyChangesKrin(t);
   }
};
_root.__rwDo832 = function(c, t, r, id)
{
   var hp = Math.floor(c.LIFEN * 0.1);
   if(hp > 0 && c.LIFEN - hp >= 1)
   {
      c.LIFEN -= hp;
      _root.__rwNumber(c, hp, "Physical");
   }
   _root.__rwAddWounds(c, 2, c);
   _root.__rwDel(c, "RWKILLER1");
   _root.__rwDel(c, "RWKILLER2");
   _root.__rwAdd(c, "RWKILLER" + r, 3, c);
   _root.__rwFocus(c, _root.__rwAt([20, 25], r));
   _root.applyChangesKrin(c);
   _root.__rwLifeBar(c);
};
_root.__rwDo864 = function(c, t, r, id)
{
   var hunted = _root.__rwHunted(t);
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([2.8, 3.2], r), "Physical", true);
   if(res.dead)
   {
      return null;
   }
   _root.__rwDrain(t, _root.__rwAt([20, 30], r) * (hunted ? 2 : 1));
   _root.__rwAdd(t, "RWJAWS", 2, c);
   if(_root.__rwScent(t) > 0)
   {
      _root.__rwTakeScent(t, 1);
      _root.__rwAdd(t, "RWSILENCE", 2, c);
      if(_root.__rwMastered(864))
      {
         _root.__rwFocus(c, 25);
      }
   }
   _root.applyChangesKrin(t);
};
_root.__rwDo819 = function(c, t, r, id)
{
   var sc = _root.__rwScent(t);
   var W = _root.__rwWounds(t);
   var m = _root.__rwAt([2.6, 3, 3.4], r) * (1 + 0.8 * sc + 0.25 * W);
   if(t.LIFEN < 0.35 * t.LIFEU)
   {
      m *= 1.4;
   }
   var crit = r >= 3 && _root.__rwBrittle(t);
   var star = _root.__rwMastered(819);
   if(star)
   {
      t.__rwNoBurst = true;
   }
   var res = _root.__rwStrike(c, t, id, m, "Physical", true, crit);
   t.__rwNoBurst = false;
   if(res.dead)
   {
      _root.__rwConsumed("sc", sc);
      if(star)
      {
         _root.__rwFocus(c, _root["KRINABILITY" + id][5]);
         var nx = _root.__rwLowestEnemy(t);
         if(nx && W > 0)
         {
            _root.__rwAddWounds(nx, W, c);
         }
      }
      return null;
   }
   _root.__rwTakeScent(t, sc);
};
// ---------------------------------------------------------------- Winter
_root.__rwDo863 = function(c, t, r, id)
{
   var sc = _root.__rwScent(t);
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.8, 2.3, 2.8], r), "Ice", false);
   if(res.dead)
   {
      return null;
   }
   _root.__rwAdd(t, "RWSTUN", 2, c);
   var fb = _root.__rwAt([0, 2, 3], r);
   if(fb > 0)
   {
      _root.__rwAddFrost(t, fb, c);
   }
   if(sc >= 2)
   {
      _root.__rwTakeScent(t, 2);
      _root.__rwAdd(t, "RWDREAD", 2, c);
      if(_root.__rwMastered(863))
      {
         var es = _root.__rwEnemies();
         var i = 0;
         while(i < es.length)
         {
            if(es[i] != t)
            {
               _root.__rwAddFrost(es[i], 1, c);
               _root.__rwDrain(es[i], 15);
            }
            i++;
         }
      }
   }
   _root.applyChangesKrin(t);
};
_root.__rwDo865 = function(c, t, r, id)
{
   var pre = _root.__rwFrost(t);
   var W = _root.__rwWounds(t);
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.85, 2.15, 2.45], r), "Ice", false);
   if(res.dead)
   {
      return null;
   }
   _root.__rwAddFrost(t, _root.__rwAt([1, 2, 2], r) + Math.min(2, Math.floor(W / 2)), c);
   _root.__rwAdd(t, "RWWICKED", 3, c);
   _root.applyChangesKrin(t);
   if(_root.__rwMastered(865) && pre >= 3 && _root.__rwAlive(t) && res.d > 0)
   {
      _root.__rwRawHit(c, t, res.d * 0.6, "Ice");
      if(_root.__rwAlive(t))
      {
         _root.__rwAddFrost(t, 1, c);
      }
   }
};
_root.__rwDo815 = function(c, t, r, id)
{
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([2, 2.3, 2.6], r), "Ice", false);
   if(res.dead)
   {
      return null;
   }
   var W = _root.__rwWounds(t);
   var k = Math.min(W, _root.__rwAspect() == 1 ? 7 : 3);
   if(!(k > 0))
   {
      return null;
   }
   var raw = k * _root.__rwWoundPer(t) * _root.__rwWoundLeft(t);
   _root.__rwPure(c, t, raw, "Ice", true);
   if(!_root.__rwAlive(t))
   {
      return null;
   }
   _root.__rwAddFrost(t, k, c, "fang");
   var froze = _root.__rwFrozeSerial == _root.__rwCastSerial;
   if(froze && _root.__rwMastered(815))
   {
      _root.__rwFocus(c, 20);
   }
   else
   {
      _root.__rwTakeWounds(t, k);
      _root.__rwConsumed("w", k);
   }
};
_root.__rwDo816 = function(c, t, r, id)
{
   var fb = Math.min(_root.__rwFrost(t), _root.__rwFrostCap());
   var hits = fb > 0 ? fb : 1;
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.15, 1.45], r) * hits, "Ice", false);
   if(fb > 0)
   {
      if(res.dead)
      {
         _root.__rwConsumed("fb", fb);
      }
      else
      {
         _root.__rwTakeFrost(t, fb);
      }
   }
   if(!res.dead && fb >= 3)
   {
      _root.__rwDispel(t, r);
      _root.__rwWound(t, Math.floor(fb / 2), c);
   }
   if(fb >= 2)
   {
      _root.__rwAddShards(Math.floor(fb / 2));
   }
   if(!res.dead && fb >= 5 && _root.__rwMastered(816))
   {
      _root.__rwAdd(t, "RWFRAGILE", 3, c);
      _root.applyChangesKrin(t);
   }
};
_root.__rwDo818 = function(c, t, r, id)
{
   var es = _root.__rwEnemies();
   var ice = false;
   var i = 0;
   while(i < es.length)
   {
      if(_root.__rwHas(es[i], "RWBLACKICE"))
      {
         ice = true;
      }
      i++;
   }
   var star = _root.__rwMastered(818);
   var i = 0;
   while(i < es.length)
   {
      var u = es[i];
      var hadFB = _root.__rwFrost(u) > 0;
      var hadW = _root.__rwWounds(u) > 0;
      var res = _root.__rwStrike(c, u, id, _root.__rwAt([1.4, 1.6, 1.8], r), "Ice", false);
      if(!res.dead)
      {
         var fb = 1;
         if(ice)
         {
            fb++;
         }
         if(star && hadFB)
         {
            fb++;
         }
         _root.__rwAddFrost(u, fb, c);
         _root.__rwWound(u, star && hadW ? 2 : 1, c);
      }
      i++;
   }
   if(ice)
   {
      var es2 = _root.__rwEnemies();
      var j = 0;
      while(j < es2.length)
      {
         if(_root.__rwHas(es2[j], "RWBLACKICE"))
         {
            _root.__rwSetLeft(es2[j], "RWBLACKICE", _root.__rwLeft(es2[j], "RWBLACKICE") + 1);
         }
         j++;
      }
   }
};
_root.__rwDo833 = function(c, t, r, id)
{
   var S = _root.__rwTakeShards(99);
   var es = _root.__rwEnemies();
   var i = 0;
   while(i < es.length)
   {
      _root.__rwAdd(es[i], "RWBLACKICE", _root.__rwAt([2, 3], r), c);
      es[i].__rwIceShards = S;
      es[i].__rwIceRank = r;
      i++;
   }
};
// cada vez que un enemigo actua sobre el hielo: 1 Frostbite y dano por Shard esparcido
_root.__rwIceStep = function(u)
{
   if(!_root.__rwHas(u, "RWBLACKICE") || !_root.__rwAlive(u))
   {
      return null;
   }
   var w = _root.__rwWolf();
   var S = _root.__rwNum(u.__rwIceShards);
   var per = _root.__rwAt([0.15, 0.2], _root.__rwNum(u.__rwIceRank));
   if(S > 0)
   {
      _root.__rwPure(w, u, _root.__rwPower(w, per * S), "Ice", true);
   }
   if(_root.__rwAlive(u))
   {
      _root.__rwAddFrost(u, 1, w, "ice");
   }
};
// ---------------------------------------------------------------- Pack
_root.__rwDo862 = function(c, t, r, id)
{
   // una habilidad sube por Wounds o por Scent, no por los dos (decision del usuario, 26/09): solo Wounds
   var mm = _root.__rwMostWounded();
   var marks = mm ? _root.__rwWounds(mm) : 0;
   var turns = Math.min(_root.__rwAt([4, 5], r), 2 + Math.floor(marks / 2));
   _root.__rwDel(t, "RWCANINE1");
   _root.__rwDel(t, "RWCANINE2");
   _root.__rwDel(t, "RWCANINEH");
   _root.__rwAdd(t, "RWCANINE" + r, turns, c);
   _root.applyChangesKrin(t);
   if(_root.__rwMastered(862))
   {
      var tm = _root.__rwTeam();
      var i = 0;
      while(i < tm.length)
      {
         var u = tm[i];
         if(u != t && !_root.__rwHas(u, "RWCANINE1") && !_root.__rwHas(u, "RWCANINE2"))
         {
            _root.__rwAdd(u, "RWCANINEH", 3, c);
            _root.applyChangesKrin(u);
         }
         i++;
      }
   }
};
_root.__rwDo834 = function(c, t, r, id)
{
   var al = _root.__rwAllies();
   var i = 0;
   while(i < al.length)
   {
      _root.__rwAdd(al[i], "RWFRENZY", 3, c);
      al[i].__rwFrenzyR = r;
      i++;
   }
};
_root.__rwDo835 = function(c, t, r, id)
{
   var al = _root.__rwAllies();
   var i = 0;
   while(i < al.length)
   {
      _root.__rwAdd(al[i], "RWFROSTPACK", 3, c);
      al[i].__rwFrostPackR = r;
      al[i].__rwFPTurn = -1;
      i++;
   }
};
_root.__rwDo821 = function(c, t, r, id)
{
   // Wounds y Frostbite del equipo enemigo (sin Scent)
   var bonus = Math.min(0.8, 0.1 * _root.__rwMarksInPlay(true));
   var amt = (_root.__rwPower(c, _root.__rwAt([2.6, 3.1, 3.6], r)) + t.LIFEU * _root.__rwAt([0.1, 0.12, 0.15], r)) * (1 + bonus);
   var low = t.LIFEN < 0.3 * t.LIFEU;
   _root.__rwHeal(t, amt, c);
   _root.__rwCleanse(t, _root.__rwAt([1, 1, 2], r));
   t.__rwCourage = _root.__rwAt([0.15, 0.2, 0.25], r);
   _root.__rwAdd(t, "RWCOURAGE", 3, c);
   if(low && _root.__rwMastered(821))
   {
      _root.__rwHeal(t, amt * 0.5, c);
   }
};
_root.__rwDo822 = function(c, t, r, id)
{
   if(t == c)
   {
      return null;
   }
   var e = _root.__rwMostMarked(true);
   var got = e ? _root.__rwTakeScent(e, 2) : 0;
   var turns = 2 + got;
   var sh = _root.__rwPower(c, _root.__rwAt([1.7, 2.2], r)) * (1 + 0.35 * got);
   _root.__rwShieldAdd(c, "RWSH_GUARD", sh, turns, c);
   _root.__rwAdd(t, "RWGUARD", turns, c);
   t.__rwGuardShare = _root.__rwAt([0.3, 0.4], r);
   c.__rwGuarding = t;
};
_root.__rwDo824 = function(c, t, r, id)
{
   var got = 0;
   if(t && t.playerID % 2 == 0)
   {
      got = _root.__rwTakeScent(t, 2);
   }
   var sh = _root.__rwPower(c, _root.__rwAt([1.3, 1.65, 2], r));
   var tm = _root.__rwTeam();
   var i = 0;
   while(i < tm.length)
   {
      _root.__rwShieldAdd(tm[i], "RWSH_WARD", sh, 2, c);
      i++;
   }
   if(got > 0 && _root.__rwMastered(824) && _root.__rwAlive(t))
   {
      _root.__rwAddFrost(t, 2 * got, c);
   }
};
_root.__rwDo808 = function(c, t, r, id)
{
   var e = _root.__rwMostMarked(true);
   var got = e ? _root.__rwTakeScent(e, 2) : 0;
   var turns = 3 + got;
   var tm = _root.__rwTeam();
   var i = 0;
   while(i < tm.length)
   {
      var u = tm[i];
      _root.__rwDel(u, "RWPRIMAL1");
      _root.__rwDel(u, "RWPRIMAL2");
      _root.__rwAdd(u, "RWPRIMAL" + r, turns, c);
      _root.__rwFocus(u, _root.__rwAt([15, 20], r));
      if(r >= 2)
      {
         _root.__rwCleanse(u, 1);
      }
      u.__rwPrimalOn = true;
      _root.applyChangesKrin(u);
      i++;
   }
};
// ---------------------------------------------------------------- Endurance
_root.__rwDo809 = function(c, t, r, id)
{
   _root.__rwDel(c, "RWWERE1");
   _root.__rwDel(c, "RWWERE2");
   _root.__rwAdd(c, "RWWERE" + r, 3, c);
   c.__rwWereExt = 0;
   _root.applyChangesKrin(c);
};
_root.__rwDo826 = function(c, t, r, id)
{
   var e = _root.__rwMostWounded();
   var drunk = 0;
   if(e)
   {
      drunk = _root.__rwTakeWounds(e, 3);
      _root.__rwConsumed("w", drunk);
   }
   var pct = _root.__rwAt([0.1, 0.15], r) + _root.__rwAt([0.15, 0.2], r) * drunk;
   _root.__rwHeal(c, c.LIFEU * pct, c);
   if(r >= 2)
   {
      _root.__rwCleanse(c, 1);
   }
   if(drunk >= 3 && _root.__rwMastered(826))
   {
      _root.__rwCleanse(c, 99);
   }
};
_root.__rwDo836 = function(c, t, r, id)
{
   var hunted = _root.__rwHunted(t);
   var res = _root.__rwStrike(c, t, id, _root.__rwAt([1.8, 2.1], r), "Physical", true);
   var heal = 0;
   if(hunted && _root.__rwMastered(836))
   {
      heal = res.d;
   }
   else
   {
      if(!res.dead)
      {
         var dk = _root.__rwTakeWounds(t, 1);
         _root.__rwConsumed("w", dk);
      }
      heal = res.d * _root.__rwAt([0.6, 0.8], r);
   }
   if(!res.dead)
   {
      heal += c.LIFEU * 0.05 * _root.__rwWounds(t);
   }
   _root.__rwHeal(c, heal, c);
};
_root.__rwDo837 = function(c, t, r, id)
{
   var S = _root.__rwTakeShards(3);
   var red = Math.min(0.4, _root.__rwAt([0.15, 0.25], r) + 0.05 * S);
   c.__rwRimeRed = red;
   _root.__rwAdd(c, "RWRIME", 3, c);
};
_root.__rwDo827 = function(c, t, r, id)
{
   var e = _root.__rwMostMarked(true);
   var got = e ? _root.__rwTakeScent(e, 99) : 0;
   c.__rwStandRed = Math.min(0.85, _root.__rwAt([0.55, 0.7], r) + 0.05 * got);
   _root.__rwDel(c, "RWSTAND1");
   _root.__rwDel(c, "RWSTAND2");
   _root.__rwAdd(c, "RWSTAND" + r, 1, c);
   _root.applyChangesKrin(c);
};
_root.__rwDo838 = function(c, t, r, id)
{
   _root.__rwCleanse(t, 99);
   _root.__rwAdd(t, "RWTOMB", 1, c);
   t.__rwTombOn = true;
   _root.applyChangesKrin(t);
};
// ---------------------------------------------------------------- base y definitivas
_root.__rwMawMult = function()
{
   var L = _root.__rwNum(_root.Krin.Level);
   var f = (L - 1) / 19;
   if(f < 0)
   {
      f = 0;
   }
   if(f > 1)
   {
      f = 1;
   }
   return 1.6 + 0.8 * f;
};
_root.__rwDo857 = function(c, t, r, id)
{
   var brittle = _root.__rwBrittle(t);
   var res = _root.__rwStrike(c, t, id, _root.__rwMawMult(), "Ice", false);
   if(!res.dead)
   {
      _root.__rwAddFrost(t, brittle && _root.__rwNum(_root.Krin.Level) >= 10 ? 2 : 1, c);
   }
   _root.__rwFocus(c, brittle ? 10 : 5);
};
_root.__rwDo854 = function(c, t, r, id)
{
   _root.__rwAdd(c, "RWBMOON", 3, c);
   _root.__rwNote("The blood moon rises!");
};
_root.__rwDo855 = function(c, t, r, id)
{
   _root.__rwAdd(c, "RWEWINTER", 3, c);
   if(_root.__rwAdd(c, "RWSHARD", 4, c))
   {
      c.__rwSh = 5;
   }
   _root.__rwNote("An endless winter falls!");
};
_root.__rwDo856 = function(c, t, r, id)
{
   _root.__rwAdd(c, "RWCALL", 3, c);
   _root.__rwHeal(c, c.LIFEU * 0.65, c);
   c.FOCUSN = c.FOCUSU;
   _root.__rwExtraPending = true;
   var al = _root.__rwLowestAlly(false);
   if(al && !al.__rwSpirit)
   {
      _root.__rwAdd(al, "RWBLESS", 3, c);
   }
   _root.applyChangesKrin(c);
   _root.__rwLifeBar(c);
   _root.__rwNote("The ancestors answer the call!");
};
// golpe de una cantidad exacta (segundo golpe de Wicked Claws, estallidos que ya estan calculados)
_root.__rwRawHit = function(c, t, amount, el)
{
   if(!_root.__rwAlive(t) || !(amount > 0))
   {
      return 0;
   }
   var dmg = Math.ceil(amount);
   var sh = _root.__rwNum(t.SHIELD);
   if(sh > 0)
   {
      var a = Math.min(sh, dmg);
      t.SHIELD = sh - a;
      dmg -= a;
      if(a > 0)
      {
         _root.__rwShieldFx(t, el);
      }
   }
   if(dmg > 0)
   {
      var l0 = t.LIFEN;
      t.LIFEN = _root.__v10Life(t.LIFEN - dmg, t, c, false);
      _root.__rwNumber(t, l0 - t.LIFEN, el);
      _root.__rwCheckDeath(t, c);
   }
   _root.__rwLifeBar(t);
   return dmg;
};
