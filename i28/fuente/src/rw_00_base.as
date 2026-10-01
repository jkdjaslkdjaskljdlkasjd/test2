// ===================================================================================================
// I26 - REWORK DEL LOBO (propuesta v4, "Mokoshotar: sangre y escarcha")
// Capa unica y autonoma. Prefijo: __rw. Todo lo del lobo nuevo vive aca; las capas viejas del lobo
// (v8..I19) siguen en el archivo pero quedan inertes: __v55Rank devuelve 0 para sus ids, asi que
// ninguna de sus reglas se dispara, y los ganchos de combate del lobo pasan primero por esta capa.
// Los enemigos, los aliados, la NULL ZONE, el 16:9 y las capas del usuario no cambian.
// ===================================================================================================
_root.__rwVersion = "I26_REWORK";

// ------------------------------------------------------------------------------- utilidades
_root.__rwNum = function(v)
{
   if(typeof v != "number" || v != v)
   {
      return 0;
   }
   return v;
};
_root.__rwMin = function(a, b)
{
   return a < b ? a : b;
};
_root.__rwMax = function(a, b)
{
   return a > b ? a : b;
};
// porcentaje legible: 0.2025 -> "20.25", 1.5 -> "150"
_root.__rwPct = function(x)
{
   var v = Math.round(x * 10000) / 100;
   return String(v);
};
_root.__rwFmt = function(x)
{
   var v = Math.round(x * 100) / 100;
   return String(v);
};
_root.__rwAlive = function(u)
{
   return u != undefined && u != null && u.active == true && u.LIFEN > 0;
};
_root.__rwHostile = function(a, b)
{
   if(!a || !b)
   {
      return false;
   }
   return a.playerID % 2 != b.playerID % 2;
};
_root.__rwWolf = function()
{
   return _root.playerKrin1;
};
// el lobo es el jugador 1 (Sonny/Mokoshotar); el arbol nuevo es suyo
_root.__rwIsWolf = function(u)
{
   return u != undefined && u != null && u.playerID == 1;
};
_root.__rwEnemies = function()
{
   var out = [];
   var i = 2;
   while(i < 7)
   {
      var u = _root["playerKrin" + i];
      if(_root.__rwAlive(u))
      {
         out.push(u);
      }
      i += 2;
   }
   return out;
};
// aliados vivos del lobo, el lobo incluido
_root.__rwTeam = function()
{
   var out = [];
   var i = 1;
   while(i < 7)
   {
      var u = _root["playerKrin" + i];
      if(_root.__rwAlive(u))
      {
         out.push(u);
      }
      i += 2;
   }
   return out;
};
// aliados vivos sin el lobo
_root.__rwAllies = function()
{
   var out = [];
   var i = 3;
   while(i < 7)
   {
      var u = _root["playerKrin" + i];
      if(_root.__rwAlive(u))
      {
         out.push(u);
      }
      i += 2;
   }
   return out;
};
// jefe: el enemigo principal (jugador 2) de un combate de jefe, o el que controla las fases
_root.__rwIsBoss = function(u)
{
   if(!u || u.playerID % 2 != 0)
   {
      return false;
   }
   if(_root.Krin.bossFight == true && u.playerID == 2)
   {
      return true;
   }
   var kb = _root["KBR" + _root.Krin.BattlePick];
   if(kb && kb.phases && kb.phases.length > 0)
   {
      var i = 0;
      while(i < kb.phases.length)
      {
         if(kb.phases[i] && kb.phases[i].player == u.playerID)
         {
            return true;
         }
         i++;
      }
   }
   return false;
};
_root.__rwNote = function(s)
{
   if(_root.KrinCombatText)
   {
      _root.KrinCombatText.combatTexter = s;
      _root.KrinCombatText.gotoAndPlay("GO");
   }
};
_root.__rwNumber = function(u, amount, color)
{
   if(u && amount > 0 && _root.KrinNumberShow && _root.BATTLESCREEN)
   {
      _root.KrinNumberShow(Math.round(amount), "player" + u.playerID, color);
   }
};
_root.__rwLifeBar = function(u)
{
   if(u && _root.lifeBarUpdate)
   {
      _root.lifeBarUpdate(u.playerID);
   }
};
// Instinto: el mayor entre Strength e Instinct x1,4 (ramas Winter, Pack y Endurance)
_root.__rwUseIns = function(c)
{
   if(!c)
   {
      return false;
   }
   return _root.__rwNum(c.MAGICU) * 1.4 > _root.__rwNum(c.STRENGTHU);
};
_root.__rwPower = function(c, m)
{
   if(!c)
   {
      return 0;
   }
   var s = _root.__rwNum(c.STRENGTHU) * m;
   var i = _root.__rwNum(c.MAGICU) * m * 1.4;
   return s > i ? s : i;
};

// ------------------------------------------------------------------------------- legado inerte
// Las capas viejas preguntan por rango con __v55Rank / __v10Owned. Con 0 no hacen nada.
_root.__rwOldRank = _root.__v55Rank;
_root.__v55Rank = function(id)
{
   return 0;
};
_root.__v10Owned = function(id)
{
   return false;
};
_root.__i1IsWolf = function(u)
{
   return false;
};
_root.__i1Ancestral = function()
{
   return null;
};
_root.__v55UpdateAll = function()
{
   return null;
};
_root.__v55UpdateSkill = function(id)
{
   return null;
};
_root.__i1Tick = function()
{
   return null;
};
_root.__i19Texts = function()
{
   return null;
};
_root.__v14Apply = function()
{
   return null;
};
_root.__i18Mastered = function(id)
{
   return _root.__rwMastered(id);
};
