// ------------------------------------------------------------------------------- estados (marcadores)
// Cada estado es un buff nativo (KRINBUFF<id>) que el motor muestra como icono y descuenta solo:
// su CD es la duracion que queda. Las acumulaciones (Wounds, Frostbite, Scent, Ice Shards) guardan el
// numero en la unidad (u.__rwW, u.__rwFB, u.__rwSc, u.__rwSh) y valen 0 si su marcador ya no esta.
// Duraciones: el CD baja al final de cada turno de la unidad. Si el estado se pone sobre la unidad que
// esta actuando, se suma 1 para que dure los turnos anunciados (se descuenta enseguida).
_root.__rwActor = null;
_root.__rwBuffDef = function(id, name, el, kind, dur, idx, vals, desc)
{
   if(!_root["KRINBUFF" + id])
   {
      _root.addNewBuffKrin(id, name, el);
   }
   var b = _root["KRINBUFF" + id];
   b[0] = name;
   b[1] = el;
   b[16] = dur;
   b[20] = kind;
   b[25] = desc;
   b[27] = 0;
   var i = 0;
   while(i < idx.length)
   {
      b[idx[i]] = vals[i];
      i++;
   }
   return b;
};
// enemigos
_root.__rwBuffDef("RWWOUND", "Wounds", "Physical", -1, 3, [], [], "");
_root.__rwBuffDef("RWWOUNDH", "Wounds", "Physical", -1, 3, [32], [1], "");
_root.__rwBuffDef("RWSCENT", "Scent of Blood", "Physical", -1, 3, [], [], "");
_root.__rwBuffDef("RWHUNTED", "Hunted", "Physical", -1, 2, [13, 36], [0.15, 0.25], "");
_root.__rwI = 1;
while(_root.__rwI <= 7)
{
   _root.__rwBuffDef("RWFROST" + _root.__rwI, "Frostbite", "Ice", -1, 4, [7, 11], [-0.04 * _root.__rwI, -0.03 * _root.__rwI], "");
   _root.__rwI++;
}
_root.__rwBuffDef("RWSOLID", "Frozen Solid", "Ice", -1, 1, [17, 31], [1, 2], "");
_root.__rwBuffDef("RWFRAGILE", "Fragile", "Ice", -1, 3, [13], [0.25], "");
_root.__rwBuffDef("RWHEMO", "Hemorrhage", "Physical", -1, 2, [11], [-0.15], "");
_root.__rwBuffDef("RWTORN", "Torn", "Physical", -1, 2, [13], [0.2], "");
_root.__rwBuffDef("RWSILENCE", "Silenced", "Physical", -1, 2, [50], [1], "");
_root.__rwBuffDef("RWSTUN", "Stunned", "Ice", -1, 2, [17], [1], "");
_root.__rwBuffDef("RWCRIPPLE", "Crippled", "Physical", -1, 1, [17], [1], "");
_root.__rwBuffDef("RWDREAD", "Ancestral Dread", "Ice", -1, 2, [15], [25], "");
_root.__rwBuffDef("RWHAM1", "Hamstring", "Physical", -1, 2, [7], [-0.3], "");
_root.__rwBuffDef("RWHAM2", "Hamstring", "Physical", -1, 2, [7], [-0.4], "");
_root.__rwBuffDef("RWJAWS", "Iron Jaws", "Physical", -1, 2, [7, 13], [-0.25, 0.15], "");
_root.__rwBuffDef("RWWICKED", "Wicked Claws", "Ice", -1, 3, [36], [0.2], "");
_root.__rwBuffDef("RWBLACKICE", "Black Ice", "Ice", -1, 3, [], [], "");
_root.__rwBuffDef("RWTERROR", "Terrified", "Physical", -1, 99, [11], [-0.2], "");
_root.__rwBuffDef("RWWSLOW", "Endless Winter", "Ice", -1, 1, [7], [-0.3], "");
// lobo y aliados
_root.__rwBuffDef("RWRUSH1", "Blood Rush", "Physical", 1, 4, [11], [0.05], "");
_root.__rwBuffDef("RWRUSH2", "Blood Rush", "Physical", 1, 4, [11], [0.1], "");
_root.__rwBuffDef("RWRUSH3", "Blood Rush", "Physical", 1, 4, [11], [0.15], "");
_root.__rwBuffDef("RWKILLER1", "Killer Instinct", "Physical", 1, 4, [3, 5, 7, 13], [0.3, 0.3, 0.15, 0.15], "");
_root.__rwBuffDef("RWKILLER2", "Killer Instinct", "Physical", 1, 4, [3, 5, 7, 13], [0.4, 0.4, 0.2, 0.15], "");
_root.__rwBuffDef("RWSHARD", "Ice Shards", "Ice", 1, 4, [], [], "");
_root.__rwBuffDef("RWRIME", "Rime Coat", "Ice", 1, 4, [], [], "");
_root.__rwBuffDef("RWTOMB", "Ice Tomb", "Ice", 1, 1, [17, 31], [1, 6], "");
_root.__rwBuffDef("RWCANINE1", "Canine Instincts", "Physical", 1, 3, [3, 5, 7], [0.18, 0.18, 0.18], "");
_root.__rwBuffDef("RWCANINE2", "Canine Instincts", "Physical", 1, 3, [3, 5, 7], [0.25, 0.25, 0.25], "");
_root.__rwBuffDef("RWCANINEH", "Canine Instincts", "Physical", 1, 3, [3, 5, 7], [0.125, 0.125, 0.125], "");
_root.__rwBuffDef("RWFRENZY", "Feeding Frenzy", "Physical", 1, 3, [], [], "");
_root.__rwBuffDef("RWFROSTPACK", "Frostbound Pack", "Ice", 1, 3, [], [], "");
_root.__rwBuffDef("RWCOURAGE", "Courage", "Physical", 1, 3, [], [], "");
_root.__rwBuffDef("RWGUARD", "Guarded", "Physical", 1, 2, [], [], "");
_root.__rwBuffDef("RWGUARDSH", "Guardian's Call", "Physical", 1, 3, [], [], "");
_root.__rwBuffDef("RWWARD", "Echo Ward", "Physical", 1, 2, [], [], "");
_root.__rwBuffDef("RWPRIMAL1", "Primal Breath", "Physical", 1, 3, [7, 13, 15], [0.15, -0.08, -10], "");
_root.__rwBuffDef("RWPRIMAL2", "Primal Breath", "Physical", 1, 3, [7, 13, 15], [0.2, -0.1, -15], "");
_root.__rwBuffDef("RWPRIMALEND", "Primal Fury", "Physical", 1, 2, [11], [0.15], "");
_root.__rwBuffDef("RWWERE1", "Werezombie", "Physical", 1, 4, [3, 5], [0.25, 0.25], "");
_root.__rwBuffDef("RWWERE2", "Werezombie", "Physical", 1, 4, [3, 5], [0.35, 0.35], "");
_root.__rwBuffDef("RWSTAND1", "Last Stand", "Physical", 1, 2, [11], [-0.25], "");
_root.__rwBuffDef("RWSTAND2", "Last Stand", "Physical", 1, 2, [11], [-0.2], "");
_root.__rwBuffDef("RWANCFORM", "Ancestral Form", "Ice", 1, 4, [31], [6], "");
_root.__rwBuffDef("RWCALL", "Call of the Ancestors", "Ice", 1, 4, [31], [6], "");
_root.__rwBuffDef("RWSPENT", "Spent", "Physical", -1, 3, [11], [-0.2], "");
_root.__rwBuffDef("RWBLESS", "Ancestors' Blessing", "Ice", 1, 4, [], [], "");
_root.__rwBuffDef("RWBMOON", "Blood Moon Rising", "Physical", 1, 4, [], [], "");
_root.__rwBuffDef("RWEWINTER", "Endless Winter", "Ice", 1, 4, [], [], "");
_root.__rwBuffDef("RWSTUNIMM", "Unyielding", "Physical", 1, 2, [], [], "");
// escudos con valor propio (KRINBUFF[19] se fija justo antes de aplicarlos)
_root.__rwBuffDef("RWSH_WARD", "Echo Ward", "Physical", 1, 2, [], [], "");
_root.__rwBuffDef("RWSH_GUARD", "Guardian's Call", "Physical", 1, 3, [], [], "");
_root.__rwBuffDef("RWSH_HEART", "Winter Heart", "Ice", 1, 3, [], [], "");
_root.__rwBuffDef("RWSH_HUNGER", "Shared Hunger", "Physical", 1, 2, [], [], "");
_root.__rwBuffDef("RWSH_DRINK", "Blood Drinker", "Physical", 1, 3, [], [], "");
_root.__rwBuffDef("RWSH_UNDY", "Undying Will", "Physical", 1, 2, [], [], "");

// ---- acceso a marcadores
_root.__rwIx = function(u, id)
{
   if(!u || !u.BUFFARRAYK)
   {
      return -1;
   }
   var i = 0;
   while(i < u.BUFFARRAYK.length)
   {
      var b = u.BUFFARRAYK[i];
      if(b && b.CD > 0 && b.buffId == id)
      {
         return i;
      }
      i++;
   }
   return -1;
};
_root.__rwHas = function(u, id)
{
   return _root.__rwIx(u, id) >= 0;
};
_root.__rwLeft = function(u, id)
{
   var i = _root.__rwIx(u, id);
   if(i < 0)
   {
      return 0;
   }
   return u.BUFFARRAYK[i].CD;
};
_root.__rwSetLeft = function(u, id, cd)
{
   var i = _root.__rwIx(u, id);
   if(i >= 0)
   {
      u.BUFFARRAYK[i].CD = cd;
   }
};
_root.__rwFree = function(u)
{
   if(!u || !u.BUFFARRAYK)
   {
      return false;
   }
   var lim = Math.min(u.BUFFARRAYK.length, _root.__rwNum(_root.maxBuffLimit));
   if(lim < 1)
   {
      lim = u.BUFFARRAYK.length;
   }
   var i = 0;
   while(i < lim)
   {
      if(u.BUFFARRAYK[i] && !(u.BUFFARRAYK[i].CD > 0))
      {
         return true;
      }
      i++;
   }
   return false;
};
// quita el marcador; los cambios de estadisticas se aplican enseguida (salvo keep: lo hace quien llama)
_root.__rwDel = function(u, id, keep)
{
   if(u && u.BUFFARRAYK && _root.__rwHas(u, id))
   {
      _root.__v10Remove(u, id);
      if(!keep)
      {
         _root.applyChangesKrin(u);
      }
   }
};
// pone el marcador (reemplaza al anterior) con "turns" turnos de la unidad. Como __v10Add, aplica los cambios
// al momento: un Hunted puesto a mitad de la accion ya cuenta para el golpe siguiente.
_root.__rwAdd = function(u, id, turns, c)
{
   if(!u || !(u.LIFEN > 0))
   {
      return false;
   }
   _root.__rwDel(u, id, true);
   if(!_root.__rwFree(u))
   {
      _root.applyChangesKrin(u);
      return false;
   }
   _root.__v10NativeBuff(u, id, 1, !c ? u : c, 0, 0);
   var cd = turns;
   if(u == _root.__rwActor)
   {
      cd = turns + 1;
   }
   _root.__rwSetLeft(u, id, cd);
   _root.applyChangesKrin(u);
   return _root.__rwHas(u, id);
};
// escudo con valor: marcador nativo con KRINBUFF[19] = cantidad (el motor lo suma a SHIELD y lo quita al vencer)
_root.__rwShieldAdd = function(u, id, amount, turns, c)
{
   if(!u || !(u.LIFEN > 0) || !(amount > 0))
   {
      return 0;
   }
   var b = _root["KRINBUFF" + id];
   var old = b[19];
   b[19] = Math.ceil(amount);
   var ok = _root.__rwAdd(u, id, turns, c);
   b[19] = old;
   _root.applyChangesKrin(u);
   return ok ? Math.ceil(amount) : 0;
};

// ---- Wounds
_root.__rwWoundCap = function()
{
   if(_root.__rwAspect() == 1)
   {
      return 7;
   }
   if(_root.__rwRank(814) > 0)
   {
      return 5;
   }
   return 3;
};
_root.__rwWoundTurns = function()
{
   var t = 3;
   if(_root.__rwRank(814) > 1)
   {
      t = 4;
   }
   if(_root.__rwAspect() == 2)
   {
      t -= 1;
   }
   return t;
};
_root.__rwWoundId = function(u)
{
   if(_root.__rwHas(u, "RWWOUNDH"))
   {
      return "RWWOUNDH";
   }
   return "RWWOUND";
};
_root.__rwWounds = function(u)
{
   if(!u)
   {
      return 0;
   }
   if(!_root.__rwHas(u, "RWWOUND") && !_root.__rwHas(u, "RWWOUNDH"))
   {
      u.__rwW = 0;
      return 0;
   }
   return _root.__rwNum(u.__rwW);
};
_root.__rwWoundLeft = function(u)
{
   return _root.__rwLeft(u, _root.__rwWoundId(u));
};
// sangrado base por Wound y por turno (sin la defensa del objetivo): 15% de Strength del lobo x pasivas
_root.__rwWoundPer = function(u)
{
   var w = _root.__rwWolf();
   if(u == w)
   {
      return 0.15 * _root.__rwNum(u.__rwWStr);
   }
   var k = 1;
   var dw = _root.__rwRank(814);
   if(dw == 1)
   {
      k = 1.2;
   }
   if(dw > 1)
   {
      k = 1.35;
   }
   var fb = _root.__rwFrost(u);
   var fr = _root.__rwRank(841);
   if(fr > 0 && fb > 0)
   {
      var per = fr > 1 ? 0.1 : 0.06;
      var capf = fr > 1 ? 0.5 : 0.3;
      k *= 1 + Math.min(capf, per * fb);
   }
   if(_root.__rwMastered(814) && _root.__rwHunted(u))
   {
      k *= 1.5;
   }
   var s = _root.__rwNum(w.STRENGTHU);
   if(!(s > 0))
   {
      s = _root.__rwNum(u.__rwWStr);
   }
   return 0.15 * s * k;
};
// sangrado que le queda: Wounds x sangrado por Wound x turnos que quedan
_root.__rwBleedLeft = function(u)
{
   return _root.__rwWounds(u) * _root.__rwWoundPer(u) * _root.__rwWoundLeft(u);
};
// pone n Wounds (el lobo es la fuente). turns opcional. Devuelve cuantos entraron.
_root.__rwAddWounds = function(u, n, c, turns)
{
   if(!u || !(u.LIFEN > 0) || !(n > 0))
   {
      return 0;
   }
   var w = _root.__rwWolf();
   var self = u == w;
   var cap = self ? 99 : _root.__rwWoundCap();
   var cur = _root.__rwWounds(u);
   var nw = Math.min(cap, cur + n);
   var t = turns > 0 ? turns : _root.__rwWoundTurns();
   if(self)
   {
      t = 3;
      u.__rwWStr = _root.__rwNum(u.STRENGTHU);
   }
   var keep = _root.__rwWoundLeft(u);
   if(keep > t)
   {
      t = keep;
   }
   var id = "RWWOUND";
   if(!self && _root.__rwMastered(814) && _root.__rwHunted(u))
   {
      id = "RWWOUNDH";
   }
   _root.__rwDel(u, "RWWOUND");
   _root.__rwDel(u, "RWWOUNDH");
   if(_root.__rwAdd(u, id, t, c))
   {
      u.__rwW = nw;
   }
   else
   {
      u.__rwW = 0;
      return 0;
   }
   _root.__rwPaint(u);
   return nw - cur;
};
// quita hasta n Wounds (consumidos o bebidos). Devuelve cuantos se quitaron.
_root.__rwTakeWounds = function(u, n)
{
   var cur = _root.__rwWounds(u);
   var k = Math.min(cur, n);
   if(!(k > 0))
   {
      return 0;
   }
   u.__rwW = cur - k;
   if(!(u.__rwW > 0))
   {
      u.__rwW = 0;
      _root.__rwDel(u, "RWWOUND");
      _root.__rwDel(u, "RWWOUNDH");
   }
   _root.__rwPaint(u);
   return k;
};

// ---- Scent of Blood y Hunted
_root.__rwScentCap = function()
{
   var r = _root.__rwRank(811);
   if(r > 1)
   {
      return 3;
   }
   if(r > 0)
   {
      return 2;
   }
   return 0;
};
_root.__rwScent = function(u)
{
   if(!u)
   {
      return 0;
   }
   if(!_root.__rwHas(u, "RWSCENT"))
   {
      u.__rwSc = 0;
      return 0;
   }
   return _root.__rwNum(u.__rwSc);
};
_root.__rwHunted = function(u)
{
   return _root.__rwHas(u, "RWHUNTED");
};
// solo el lobo genera Scent; hace falta Scent of Blood (sin la pasiva el tope es 0)
_root.__rwAddScent = function(u, n, c)
{
   if(!u || !(u.LIFEN > 0) || !(n > 0) || u.playerID % 2 != 0)
   {
      return 0;
   }
   var cap = _root.__rwScentCap();
   if(cap < 1)
   {
      return 0;
   }
   var cur = _root.__rwScent(u);
   var nw = Math.min(cap, cur + n);
   if(_root.__rwAdd(u, "RWSCENT", 3, c))
   {
      u.__rwSc = nw;
   }
   if(nw >= 3 && cap >= 3)
   {
      _root.__rwMakeHunted(u, c);
   }
   _root.__rwPaint(u);
   return nw - cur;
};
_root.__rwTakeScent = function(u, n)
{
   var cur = _root.__rwScent(u);
   var k = Math.min(cur, n);
   if(!(k > 0))
   {
      return 0;
   }
   u.__rwSc = cur - k;
   if(!(u.__rwSc > 0))
   {
      u.__rwSc = 0;
      _root.__rwDel(u, "RWSCENT");
   }
   _root.__rwConsumed("sc", k);
   _root.__rwPaint(u);
   return k;
};
_root.__rwMakeHunted = function(u, c)
{
   var was = _root.__rwHunted(u);
   _root.__rwAdd(u, "RWHUNTED", 2, c);
   if(was)
   {
      return null;
   }
   _root.__rwNote(u.playerName + " is Hunted!");
   if(_root.__rwMastered(811))
   {
      _root.__rwAddWounds(u, 2, _root.__rwWolf());
   }
   _root.__rwHuntOrFreezeEvent();
};
// Relentless Hunt R2: +15 Focus al cazar o congelar; su maestria baja 1 turno todas las recargas
_root.__rwHuntOrFreezeEvent = function()
{
   var w = _root.__rwWolf();
   var r = _root.__rwRank(820);
   if(r > 1 && _root.__rwAlive(w))
   {
      _root.__rwFocus(w, 15);
   }
   if(_root.__rwMastered(820))
   {
      var cd = _root.Krin.abilityCoolDown;
      if(cd)
      {
         var i = 0;
         while(i < cd.length)
         {
            if(cd[i] > 0 && cd[i] < 90)
            {
               cd[i]--;
            }
            i++;
         }
      }
   }
};

// ---- Frostbite, Brittle y Frozen Solid
_root.__rwFrostCap = function()
{
   return _root.__rwAspect() == 2 ? 7 : 5;
};
_root.__rwFrost = function(u)
{
   if(!u)
   {
      return 0;
   }
   var n = _root.__rwNum(u.__rwFB);
   if(n > 0 && !_root.__rwHas(u, "RWFROST" + n))
   {
      u.__rwFB = 0;
      return 0;
   }
   return n;
};
_root.__rwBrittle = function(u)
{
   return _root.__rwFrost(u) >= 3;
};
_root.__rwSetFrost = function(u, n, c)
{
   var old = _root.__rwFrost(u);
   if(old > 0)
   {
      _root.__rwDel(u, "RWFROST" + old);
   }
   var cap = _root.__rwFrostCap();
   if(n > cap)
   {
      n = cap;
   }
   if(n < 0)
   {
      n = 0;
   }
   u.__rwFB = 0;
   if(n > 0 && _root.__rwAdd(u, "RWFROST" + n, 4, !c ? _root.__rwWolf() : c))
   {
      u.__rwFB = n;
   }
   _root.applyChangesKrin(u);
   _root.__rwPaint(u);
   return u.__rwFB;
};
_root.__rwFrozen = function(u)
{
   return _root.__rwHas(u, "RWSOLID");
};
_root.__rwFreezeImmune = function(u)
{
   return _root.__rwNum(u.__rwFrzImm) > 0 || _root.__rwFrozen(u);
};
// agrega n Frostbite. Blood Moon: cada aplicacion pone 1 menos (minimo 1). Pasar del tope congela.
_root.__rwAddFrost = function(u, n, c, src)
{
   if(!u || !(u.LIFEN > 0) || !(n > 0) || u.playerID % 2 != 0)
   {
      return 0;
   }
   if(_root.__rwAspect() == 1)
   {
      n = Math.max(1, n - 1);
   }
   var cur = _root.__rwFrost(u);
   var cap = _root.__rwFrostCap();
   var nw = cur + n;
   if(nw > cap)
   {
      if(_root.__rwFreezeImmune(u))
      {
         _root.__rwSetFrost(u, cap, c);
         _root.__rwBrittleCheck(u, cur, c);
         return cap - cur;
      }
      _root.__rwFreeze(u, c, src);
      return n;
   }
   _root.__rwSetFrost(u, nw, c);
   _root.__rwBrittleCheck(u, cur, c);
   return n;
};
_root.__rwTakeFrost = function(u, n)
{
   var cur = _root.__rwFrost(u);
   var k = Math.min(cur, n);
   if(!(k > 0))
   {
      return 0;
   }
   _root.__rwSetFrost(u, cur - k);
   _root.__rwConsumed("fb", k);
   return k;
};
// Cold Snap: la primera vez de cada turno que un enemigo queda Brittle
_root.__rwBrittleCheck = function(u, before, c)
{
   if(before >= 3 || _root.__rwFrost(u) < 3)
   {
      return null;
   }
   var r = _root.__rwRank(843);
   if(r < 1)
   {
      return null;
   }
   if(u.__rwSnapTurn == _root.__rwWolfTurn)
   {
      return null;
   }
   u.__rwSnapTurn = _root.__rwWolfTurn;
   var w = _root.__rwWolf();
   _root.__rwDrain(u, r > 1 ? 15 : 10);
   if(r > 1)
   {
      _root.__rwPure(w, u, _root.__rwPower(w, 0.6), "Ice", true);
   }
   if(_root.__rwMastered(843))
   {
      _root.__rwAddWounds(u, 1, w);
   }
};
// congela: pierde su proximo turno (2 con Winter's Grip maestria o Endless Winter; 1 en jefes),
// Frostbite a 0, no se puede volver a congelar hasta 3 turnos despues de descongelarse
_root.__rwFreeze = function(u, c, src)
{
   var boss = _root.__rwIsBoss(u);
   var turns = 1;
   if(!boss && _root.__rwMastered(842))
   {
      turns = 2;
   }
   if(_root.__rwHas(_root.__rwWolf(), "RWEWINTER"))
   {
      turns = boss ? 1 : 2;
   }
   _root.__rwSetFrost(u, 0);
   _root.__rwAdd(u, "RWSOLID", turns, c);
   u.__rwFrzImm = turns + 3;
   u.__rwWasFrozen = true;
   _root.__rwNote(u.playerName + " is frozen solid!");
   _root.__rwOnFreeze(u, c, src);
};
