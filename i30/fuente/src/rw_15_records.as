// ------------------------------------------------------------------------------- fichas KRINABILITY
// Cada activa del lobo tiene su ficha nativa (A = KRINABILITY<id>, B = KRINABILITYB<id>). El reloj de
// combate solo usa de ellas el coste, la recarga, la animacion y los objetivos: el efecto lo resuelve
// __rwCast (sin buff nativo en B[13] ni disipacion en B[16]).
_root.__rwIsWolfMove = function(id)
{
   var d = _root.__rwS[id];
   return d != undefined && !d.pas;
};
_root.__rwIsWolfRelated = function(id)
{
   return id == 623 || id >= 624 && id <= 628 || id >= 808 && id <= 870;
};
// ids viejos del lobo -> ids del rework (623 Werezombie, 624-628 las cinco libres de Mokoshotar)
_root.__rwOldIds = {};
_root.__rwOldIds[623] = 809;
_root.__rwOldIds[624] = 861;
_root.__rwOldIds[625] = 862;
_root.__rwOldIds[626] = 863;
_root.__rwOldIds[627] = 864;
_root.__rwOldIds[628] = 865;
_root.__rwMakeRecord = function(d)
{
   var id = d.id;
   var a = [];
   a[0] = d.n;
   a[1] = id;
   a[2] = d.t.indexOf("s") < 0 ? 0 : 1;
   a[3] = d.t.indexOf("e") < 0 ? 0 : 1;
   a[4] = d.t.indexOf("a") < 0 ? 0 : 1;
   a[5] = 0;
   a[6] = 0;
   a[7] = 0;
   a[8] = 1;
   a[9] = 1;
   a[10] = d.an;
   a[11] = d.color;
   a[12] = "Attack";
   a[13] = d.boom;
   a[14] = d.t == "e" ? "Full Damage" : "Heal";
   a[15] = 1;
   a[16] = 0;
   a[17] = d.n;
   a[18] = d.sfx;
   var b = [];
   b[0] = d.el;
   b[1] = 0;
   b[2] = 0;
   b[3] = 0;
   b[4] = 0;
   b[5] = 0;
   b[6] = 0;
   b[7] = 0;
   b[8] = 1;
   b[9] = 0;
   b[10] = 1;
   b[11] = 0;
   b[12] = 0;
   b[13] = 0;
   b[14] = 1;
   b[15] = [0];
   b[16] = 0;
   b[17] = "";
   b[18] = "";
   b[19] = 1;
   b[20] = 0;
   b[21] = 0;
   b[22] = 1;
   b[23] = "Physical";
   b[24] = 0;
   b[25] = 1;
   _root["KRINABILITY" + id] = a;
   _root["KRINABILITYB" + id] = b;
};
_root.__rwCostText = function(id, r)
{
   var d = _root.__rwS[id];
   var f = _root.__rwAt(d.foc, r);
   var c = _root.__rwAt(d.cd, r);
   if(d.pg == 3)
   {
      return (f > 0 ? "Costs " + f + " Focus. " : "Costs nothing. ") + "Once per battle.";
   }
   var s = "";
   if(id == 832)
   {
      s = "Costs 10% of your current Health";
   }
   else if(f > 0)
   {
      s = "Costs " + f + " Focus";
   }
   else
   {
      s = "Costs nothing";
   }
   return s + ". (CD: " + c + ")";
};
_root.__rwUpdateRecord = function(id)
{
   var d = _root.__rwS[id];
   if(!d || d.pas)
   {
      return null;
   }
   if(!_root["KRINABILITY" + id] || _root["KRINABILITY" + id][0] != d.n || _root["KRINABILITY" + id].__rw != true)
   {
      _root.__rwMakeRecord(d);
      _root["KRINABILITY" + id].__rw = true;
   }
   var r = _root.__rwRank(id);
   if(r < 1)
   {
      r = 1;
   }
   var a = _root["KRINABILITY" + id];
   var b = _root["KRINABILITYB" + id];
   a[5] = _root.__rwAt(d.foc, r);
   a[7] = _root.__rwAt(d.cd, r);
   b[17] = _root.__rwDesc(id, r);
   b[18] = _root.__rwCostText(id, r);
};
_root.__rwUpdateRecords = function()
{
   var i = 0;
   while(i < _root.__rwList.length)
   {
      _root.__rwUpdateRecord(_root.__rwList[i].id);
      i++;
   }
};
// ¿la activa esta disponible para la barra de combate?
_root.__rwAvailable = function(id)
{
   var d = _root.__rwS[id];
   if(!d || d.pas)
   {
      return false;
   }
   if(d.pg == 0)
   {
      return true;
   }
   if(d.pg == 3)
   {
      return _root.__rwRank(id) > 0 && _root.__rwAspect() == d.asp;
   }
   return _root.__rwRank(id) > 0;
};
// reemplaza a las versiones viejas: lista de habilidades disponibles (moveMatrix2) y barra (moveMatrix)
_root.__v8Sync = function()
{
   var k = _root.Krin;
   if(!k)
   {
      return null;
   }
   _root.__rwMigrate();
   _root.__rwSyncBonus();
   _root.__rwUpdateRecords();
   var clean = [];
   var seen = {};
   var old = k.moveMatrix2;
   if(!old)
   {
      old = [];
   }
   var i = 0;
   while(i < old.length)
   {
      var id = old[i];
      if(!_root.__rwIsWolfRelated(id) && !seen[id])
      {
         clean.push(id);
         seen[id] = true;
      }
      i++;
   }
   var order = ["hunt", "winter", "pack", "endurance"];
   var o = 0;
   while(o < order.length)
   {
      var j = 0;
      while(j < _root.__rwList.length)
      {
         var d = _root.__rwList[j];
         if(d.pg == 1 && d.br == order[o] && _root.__rwAvailable(d.id))
         {
            clean.push(d.id);
         }
         j++;
      }
      o++;
   }
   clean.push(857);
   var j = 0;
   while(j < _root.__rwList.length)
   {
      var d = _root.__rwList[j];
      if(d.pg == 3 && _root.__rwAvailable(d.id))
      {
         clean.push(d.id);
      }
      j++;
   }
   k.moveMatrix2 = clean;
   if(!k.moveMatrix)
   {
      k.moveMatrix = [0, 0, 0, 0, 0, 0, 0, 0];
   }
   var i = 0;
   while(i < k.moveMatrix.length)
   {
      var id = k.moveMatrix[i];
      // partidas de I25: la barra conserva las habilidades con su id nuevo
      var nid = _root.__rwOldIds[id];
      if(nid > 0)
      {
         id = nid;
         k.moveMatrix[i] = nid;
      }
      if(_root.__rwIsWolfRelated(id) && !_root.__rwAvailable(id))
      {
         k.moveMatrix[i] = 0;
      }
      i++;
   }
};
