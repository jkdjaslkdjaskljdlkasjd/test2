// ------------------------------------------------------------------------------- datos del arbol
// Cada habilidad: id, n (nombre = etiqueta del icono), pg (pagina 1 activas, 2 instintos, 3 definitivas,
// 0 base), br (rama), col/row (grilla 4x7), max, lv (nivel por rango), foc (Focus por rango),
// cd (recarga por rango), pas (pasiva), req (ids que hay que tener), free (rangos gratis), key (pasiva
// clave), t (objetivos: s propio, e enemigo, a aliado), an (animacion), el (elemento), ico (icono de
// prueba: nombre de una habilidad existente cuyo dibujo se copia en un fotograma nuevo).
// Los rangos se guardan en Krin.talentMainArray[slot] como rangos COMPRADOS (sin contar los gratis).
_root.__rwS = {};
_root.__rwList = [];
_root.__rwDef = function(o)
{
   if(o.free == undefined)
   {
      o.free = 0;
   }
   if(o.req == undefined)
   {
      o.req = [];
   }
   if(o.key == undefined)
   {
      o.key = false;
   }
   _root.__rwS[o.id] = o;
   _root.__rwList.push(o);
   return o;
};
_root.__rwD = _root.__rwDef;
// ---- Pagina 1: Hunt (solo Strength)
_root.__rwD({id: 861, n: "Rake", pg: 1, br: "hunt", col: 0, row: 0, slot: 100, max: 3, free: 1, lv: [1, 2, 3], foc: [10, 10, 10], cd: [0, 0, 0], t: "e", an: "Melee", el: "Physical", boom: "BOOM_STAR_YELLOW", sfx: "sfx_hit2", color: "0xFF0000"});
_root.__rwD({id: 810, n: "Pounce", pg: 1, br: "hunt", col: 0, row: 1, slot: 101, max: 2, lv: [1, 3], foc: [0, 0], cd: [0, 0], t: "e", an: "Melee", el: "Physical", boom: "BOOM_STAR_YELLOW", sfx: "sfx_hit2", color: "0xFF0000"});
_root.__rwD({id: 812, n: "Hamstring", pg: 1, br: "hunt", col: 0, row: 2, slot: 102, max: 2, lv: [3, 4], foc: [10, 10], cd: [2, 2], t: "e", an: "Melee", el: "Physical", boom: "BOOM_SLASHRED", sfx: "sfx_slash", color: "0xFF0000"});
_root.__rwD({id: 864, n: "Iron Jaws", pg: 1, br: "hunt", col: 0, row: 3, slot: 105, max: 2, free: 1, lv: [1, 6], foc: [12, 12], cd: [3, 3], t: "e", an: "Melee", el: "Physical", boom: "BOOM2", sfx: "sfx_bite", color: "0x00CCFF"});
_root.__rwD({id: 831, n: "Rupture", pg: 1, br: "hunt", col: 0, row: 4, slot: 103, max: 2, lv: [5, 6], foc: [15, 15], cd: [3, 3], req: [814], t: "e", an: "Melee", el: "Physical", boom: "BOOM_SLASHRED", sfx: "sfx_slash", color: "0xFF0000", ico: "Deep Wounds"});
_root.__rwD({id: 819, n: "Cull the Weak", pg: 1, br: "hunt", col: 0, row: 5, slot: 106, max: 3, lv: [8, 9, 10], foc: [25, 20, 20], cd: [4, 4, 4], t: "e", an: "Melee", el: "Physical", boom: "BOOM2", sfx: "sfx_bite", color: "0xFF0000"});
_root.__rwD({id: 832, n: "Killer Instinct", pg: 1, br: "hunt", col: 0, row: 6, slot: 104, max: 2, lv: [8, 10], foc: [0, 0], cd: [6, 6], t: "s", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000", ico: "Werezombie"});
// ---- Pagina 1: Winter (el mayor entre Strength e Instinct x1,4)
_root.__rwD({id: 865, n: "Wicked Claws", pg: 1, br: "winter", col: 1, row: 0, slot: 108, max: 3, free: 1, lv: [1, 3, 5], foc: [10, 10, 10], cd: [1, 1, 1], t: "e", an: "Melee", el: "Ice", boom: "BOOM_STAR_BLUE", sfx: "sfx_slash", color: "0x00CCFF"});
_root.__rwD({id: 863, n: "Howl of the Ancestors", pg: 1, br: "winter", col: 1, row: 1, slot: 107, max: 3, free: 1, lv: [1, 4, 7], foc: [10, 10, 10], cd: [4, 4, 4], t: "e", an: "Shock", el: "Ice", boom: "BOOM_SPARKBLUE", sfx: "sfx_howl", color: "0x00CCFF"});
_root.__rwD({id: 815, n: "Frost Fang", pg: 1, br: "winter", col: 1, row: 2, slot: 109, max: 3, lv: [5, 6, 7], foc: [12, 12, 12], cd: [2, 2, 2], req: [814], t: "e", an: "Melee", el: "Ice", boom: "BOOM_STAR_BLUE", sfx: "sfx_bite", color: "0x00CCFF"});
_root.__rwD({id: 816, n: "Shatter Guard", pg: 1, br: "winter", col: 1, row: 3, slot: 110, max: 2, lv: [6, 7], foc: [0, 0], cd: [1, 1], t: "e", an: "Melee", el: "Ice", boom: "BOOM_STAR_BLUE", sfx: "sfx_slash", color: "0x00CCFF"});
_root.__rwD({id: 818, n: "Cold Trail", pg: 1, br: "winter", col: 1, row: 4, slot: 111, max: 3, lv: [8, 9, 10], foc: [20, 20, 20], cd: [5, 5, 5], t: "e", an: "Shock", el: "Ice", boom: "BOOM_SPARKBLUE", sfx: "sfx_howl", color: "0x00CCFF"});
_root.__rwD({id: 833, n: "Black Ice", pg: 1, br: "winter", col: 1, row: 5, slot: 112, max: 2, lv: [8, 9], foc: [18, 18], cd: [6, 6], req: [840], t: "e", an: "Shock", el: "Ice", boom: "BOOM_SPARKBLUE", sfx: "sfx_howl", color: "0x00CCFF", ico: "Cold Trail"});
// ---- Pagina 1: Pack
_root.__rwD({id: 862, n: "Canine Instincts", pg: 1, br: "pack", col: 2, row: 0, slot: 113, max: 2, free: 1, lv: [1, 4], foc: [15, 15], cd: [5, 4], t: "sa", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000"});
_root.__rwD({id: 821, n: "Rallying Cry", pg: 1, br: "pack", col: 2, row: 1, slot: 116, max: 3, lv: [3, 4, 5], foc: [15, 12, 12], cd: [4, 3, 3], t: "sa", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000"});
_root.__rwD({id: 808, n: "Primal Breath", pg: 1, br: "pack", col: 2, row: 2, slot: 119, max: 2, lv: [3, 5], foc: [0, 0], cd: [6, 6], t: "s", an: "Shock", el: "Physical", boom: "BOOM_SPARKBLUE", sfx: "sfx_restore", color: "0x0099FF"});
_root.__rwD({id: 822, n: "Guardian's Call", pg: 1, br: "pack", col: 2, row: 3, slot: 117, max: 2, lv: [5, 6], foc: [20, 20], cd: [5, 5], t: "a", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000"});
_root.__rwD({id: 834, n: "Feeding Frenzy", pg: 1, br: "pack", col: 2, row: 4, slot: 114, max: 2, lv: [6, 7], foc: [20, 20], cd: [5, 5], t: "s", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000", ico: "Pack Tactics"});
_root.__rwD({id: 835, n: "Frostbound Pack", pg: 1, br: "pack", col: 2, row: 5, slot: 115, max: 2, lv: [7, 8], foc: [20, 20], cd: [5, 5], t: "s", an: "Shock", el: "Ice", boom: "BOOM_SPARKBLUE", sfx: "sfx_howl", color: "0x00CCFF", ico: "Winter Heart"});
_root.__rwD({id: 824, n: "Echo Ward", pg: 1, br: "pack", col: 2, row: 6, slot: 118, max: 3, lv: [8, 9, 10], foc: [30, 28, 28], cd: [6, 5, 5], t: "e", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000"});
// ---- Pagina 1: Endurance
_root.__rwD({id: 809, n: "Werezombie", pg: 1, br: "endurance", col: 3, row: 0, slot: 120, max: 2, free: 1, lv: [1, 6], foc: [25, 25], cd: [7, 5], t: "s", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000"});
_root.__rwD({id: 826, n: "Second Wind", pg: 1, br: "endurance", col: 3, row: 1, slot: 123, max: 2, lv: [3, 4], foc: [0, 0], cd: [6, 6], t: "s", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_restore", color: "0xFF0000"});
_root.__rwD({id: 836, n: "Taste of Blood", pg: 1, br: "endurance", col: 3, row: 2, slot: 121, max: 2, lv: [5, 6], foc: [12, 12], cd: [3, 3], req: [814], t: "e", an: "Melee", el: "Physical", boom: "BOOM2", sfx: "sfx_bite", color: "0xFF0000", ico: "Iron Jaws"});
_root.__rwD({id: 827, n: "Last Stand", pg: 1, br: "endurance", col: 3, row: 3, slot: 124, max: 2, lv: [6, 7], foc: [15, 15], cd: [6, 6], t: "s", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000"});
_root.__rwD({id: 837, n: "Rime Coat", pg: 1, br: "endurance", col: 3, row: 4, slot: 122, max: 2, lv: [6, 7], foc: [15, 15], cd: [5, 5], req: [840], t: "s", an: "Shock", el: "Ice", boom: "BOOM_SPARKBLUE", sfx: "sfx_restore", color: "0x00CCFF", ico: "Thick Hide"});
_root.__rwD({id: 838, n: "Ice Tomb", pg: 1, br: "endurance", col: 3, row: 5, slot: 125, max: 1, lv: [10], foc: [20], cd: [7], t: "sa", an: "Shock", el: "Ice", boom: "BOOM_SPARKBLUE", sfx: "sfx_restore", color: "0x00CCFF", ico: "Last Stand"});
// ---- Pagina 2: Instintos (pasivas)
_root.__rwD({id: 811, n: "Scent of Blood", pg: 2, br: "hunt", col: 0, row: 0, slot: 130, max: 2, lv: [1, 4], pas: true, key: true});
_root.__rwD({id: 814, n: "Deep Wounds", pg: 2, br: "hunt", col: 0, row: 1, slot: 131, max: 2, lv: [4, 5], pas: true, key: true});
_root.__rwD({id: 817, n: "Predator's Patience", pg: 2, br: "hunt", col: 0, row: 2, slot: 132, max: 2, lv: [6, 7], pas: true});
_root.__rwD({id: 839, n: "Bloodhound", pg: 2, br: "hunt", col: 0, row: 3, slot: 133, max: 2, lv: [7, 8], pas: true, ico: "Predator's Patience"});
_root.__rwD({id: 820, n: "Relentless Hunt", pg: 2, br: "hunt", col: 0, row: 4, slot: 134, max: 2, lv: [6, 7], pas: true});
_root.__rwD({id: 840, n: "Shardfall", pg: 2, br: "winter", col: 1, row: 0, slot: 135, max: 2, lv: [5, 6], pas: true, key: true, ico: "Shatter Guard"});
_root.__rwD({id: 841, n: "Frozen Blood", pg: 2, br: "winter", col: 1, row: 1, slot: 136, max: 2, lv: [6, 7], pas: true, ico: "Frost Fang"});
_root.__rwD({id: 842, n: "Winter's Grip", pg: 2, br: "winter", col: 1, row: 2, slot: 137, max: 2, lv: [8, 9], pas: true, ico: "Wicked Claws"});
_root.__rwD({id: 843, n: "Cold Snap", pg: 2, br: "winter", col: 1, row: 3, slot: 138, max: 2, lv: [9, 10], pas: true, ico: "Howl of the Ancestors"});
_root.__rwD({id: 823, n: "Pack Tactics", pg: 2, br: "pack", col: 2, row: 0, slot: 139, max: 2, lv: [5, 6], pas: true});
_root.__rwD({id: 844, n: "Shared Hunger", pg: 2, br: "pack", col: 2, row: 1, slot: 140, max: 2, lv: [7, 8], pas: true, ico: "Rallying Cry"});
_root.__rwD({id: 845, n: "Cold Comfort", pg: 2, br: "pack", col: 2, row: 2, slot: 141, max: 2, lv: [6, 7], pas: true, ico: "Echo Ward"});
_root.__rwD({id: 825, n: "Thick Hide", pg: 2, br: "endurance", col: 3, row: 0, slot: 142, max: 2, lv: [1, 2], pas: true});
_root.__rwD({id: 846, n: "Blood Drinker", pg: 2, br: "endurance", col: 3, row: 1, slot: 143, max: 2, lv: [5, 6], pas: true, ico: "Second Wind"});
_root.__rwD({id: 828, n: "Unyielding", pg: 2, br: "endurance", col: 3, row: 2, slot: 144, max: 2, lv: [5, 6], pas: true});
_root.__rwD({id: 829, n: "Winter Heart", pg: 2, br: "endurance", col: 3, row: 3, slot: 145, max: 2, lv: [6, 7], pas: true});
_root.__rwD({id: 830, n: "Undying Will", pg: 2, br: "endurance", col: 3, row: 4, slot: 146, max: 1, lv: [12], pas: true});
// ---- Definitivas (una por Aspecto, 1 punto, una vez por combate; se aprenden en la NULL ZONE)
_root.__rwD({id: 854, n: "Blood Moon Rising", pg: 3, br: "aspect", asp: 1, col: 0, row: 0, slot: 150, max: 1, lv: [12], foc: [30], cd: [99], t: "e", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0xFF0000", ico: "Scent of Blood"});
_root.__rwD({id: 855, n: "Endless Winter", pg: 3, br: "aspect", asp: 2, col: 1, row: 0, slot: 151, max: 1, lv: [12], foc: [30], cd: [99], t: "e", an: "Shock", el: "Ice", boom: "BOOM_SPARKBLUE", sfx: "sfx_howl", color: "0x00CCFF", ico: "Cold Trail"});
_root.__rwD({id: 856, n: "Call of the Ancestors", pg: 3, br: "aspect", asp: 4, col: 3, row: 0, slot: 152, max: 1, lv: [12], foc: [0], cd: [99], t: "s", an: "Shock", el: "Physical", boom: "BOOM_POWERUP", sfx: "sfx_howl", color: "0x0099FF", ico: "Howl of the Ancestors"});
// ---- Base: fuera del arbol, siempre disponible
_root.__rwD({id: 857, n: "Frozen Maw", pg: 0, br: "base", col: 0, row: 0, slot: -1, max: 1, lv: [1], foc: [0], cd: [0], t: "e", an: "Melee", el: "Ice", boom: "BOOM_STAR_BLUE", sfx: "sfx_bite", color: "0x00CCFF", ico: "Wicked Claws"});
delete _root.__rwD;

_root.__rwBranchName = {hunt: "Hunt", winter: "Winter", pack: "Pack", endurance: "Endurance", aspect: "Aspect", base: "Base"};
// Aspectos (se eligen en la NULL ZONE, uno activo; ranura 160)
_root.__rwAspects = [{k: 1, n: "Aspect of the Blood Moon", ult: 854}, {k: 2, n: "Aspect of the Long Winter", ult: 855}, {k: 3, n: "Aspect of the Pack Leader", ult: 0}, {k: 4, n: "Aspect of the Ancestors", ult: 856}];
_root.__rwSlotAspect = 160;
_root.__rwSlotBonus = 161;
_root.__rwUltLevel = 12;

// ------------------------------------------------------------------------------- rangos y puntos
_root.__rwTal = function(slot)
{
   var t = _root.Krin.talentMainArray;
   if(!t)
   {
      return 0;
   }
   var v = t[slot];
   if(typeof v != "number" || v != v || v < 0)
   {
      return 0;
   }
   return Math.floor(v);
};
_root.__rwSetTal = function(slot, v)
{
   if(!_root.Krin.talentMainArray)
   {
      _root.Krin.talentMainArray = [];
   }
   _root.Krin.talentMainArray[slot] = v;
};
_root.__rwBought = function(id)
{
   var d = _root.__rwS[id];
   if(!d || d.slot < 0)
   {
      return 0;
   }
   return _root.__rwTal(d.slot);
};
_root.__rwRank = function(id)
{
   var d = _root.__rwS[id];
   if(!d)
   {
      return 0;
   }
   if(d.pg == 0)
   {
      return 1;
   }
   var r = d.free + _root.__rwBought(id);
   if(r > d.max)
   {
      r = d.max;
   }
   return r;
};
_root.__rwMastered = function(id)
{
   var d = _root.__rwS[id];
   return d != undefined && d.pg > 0 && d.pg < 3 && _root.__rwRank(id) >= d.max;
};
// valor por rango: arr[rango-1], con el rango acotado a [1, largo]
_root.__rwAt = function(arr, r)
{
   var k = r;
   if(k < 1)
   {
      k = 1;
   }
   if(k > arr.length)
   {
      k = arr.length;
   }
   return arr[k - 1];
};
_root.__rwAspect = function()
{
   var a = _root.__rwTal(_root.__rwSlotAspect);
   if(a < 1 || a > 4)
   {
      return 0;
   }
   return a;
};
// Ancestral Wolf: pasiva de clase, activa con al menos 1 punto en Scent of Blood
_root.__rwAncestral = function()
{
   return _root.__rwRank(811) > 0;
};
// puntos extra de Ancestral Wolf: 2 por nivel (1 del juego + 1 extra) y 3 en los niveles 5, 10, 15 y 20
_root.__rwBonusTarget = function()
{
   if(!_root.__rwAncestral())
   {
      return 0;
   }
   var L = _root.__rwNum(_root.Krin.Level);
   if(L < 1)
   {
      L = 1;
   }
   var n = L - 1;
   if(L >= 5)
   {
      n++;
   }
   if(L >= 10)
   {
      n++;
   }
   if(L >= 15)
   {
      n++;
   }
   if(L >= 20)
   {
      n++;
   }
   return n;
};
_root.__rwSyncBonus = function()
{
   if(!_root.Krin || !_root.Krin.talentMainArray)
   {
      return 0;
   }
   var have = _root.__rwTal(_root.__rwSlotBonus);
   var want = _root.__rwBonusTarget();
   if(want == have)
   {
      return 0;
   }
   var sp = _root.__rwNum(_root.Krin.skillPoints);
   var delta = want - have;
   if(delta < 0 && sp + delta < 0)
   {
      delta = 0 - sp;
   }
   _root.Krin.skillPoints = sp + delta;
   _root.__rwSetTal(_root.__rwSlotBonus, have + delta);
   if(_root.KRINMENU)
   {
      _root.KRINMENU.skillPoints = _root.Krin.skillPoints;
   }
   return delta;
};
// Guardados de I19 o anteriores: los puntos del arbol viejo (ranuras 38 a 64) se devuelven y las
// ranuras quedan en 0. Como quedan en 0, no se puede devolver dos veces.
_root.__rwMigrate = function()
{
   if(!_root.Krin || !_root.Krin.talentMainArray)
   {
      return 0;
   }
   var refund = 0;
   var s = 38;
   while(s <= 64)
   {
      var v = _root.__rwTal(s);
      if(v > 0)
      {
         refund += v;
         _root.Krin.talentMainArray[s] = 0;
      }
      s++;
   }
   if(refund > 0)
   {
      _root.Krin.skillPoints = _root.__rwNum(_root.Krin.skillPoints) + refund;
      _root.__rwMigratedPoints = _root.__rwNum(_root.__rwMigratedPoints) + refund;
   }
   return refund;
};
_root.__rwCanLearn = function(id)
{
   var d = _root.__rwS[id];
   if(!d || d.pg == 0)
   {
      return "";
   }
   var r = _root.__rwRank(id);
   if(r >= d.max)
   {
      return "This ability cannot be developed further.";
   }
   var req = _root.__rwAt(d.lv, r + 1);
   if(_root.__rwNum(_root.Krin.Level) < req)
   {
      return "Requires Level " + req + ".";
   }
   var i = 0;
   while(i < d.req.length)
   {
      if(_root.__rwRank(d.req[i]) < 1)
      {
         return "Requires " + _root.__rwS[d.req[i]].n + ".";
      }
      i++;
   }
   if(d.asp > 0 && _root.__rwAspect() != d.asp)
   {
      return "Requires " + _root.__rwAspects[d.asp - 1].n + ".";
   }
   if(_root.__rwNum(_root.Krin.skillPoints) < 1)
   {
      return "You do not have enough Ability Points.";
   }
   return "";
};
_root.__rwLearn = function(id)
{
   var why = _root.__rwCanLearn(id);
   if(why != "")
   {
      _root.__rwTreeNotice(why);
      return false;
   }
   var d = _root.__rwS[id];
   _root.__rwSetTal(d.slot, _root.__rwBought(id) + 1);
   _root.Krin.skillPoints = _root.__rwNum(_root.Krin.skillPoints) - 1;
   _root.__rwSyncBonus();
   _root.__v8Sync();
   if(_root.KRINMENU && _root.KRINMENU.KrinCreateAbilityMatrix)
   {
      _root.KRINMENU.KrinCreateAbilityMatrix();
   }
   _root.__rwTreeRefresh();
   return true;
};
// devuelve todos los puntos del arbol nuevo (paginas 1 y 2 y definitivas); el Aspecto elegido se mantiene
_root.__rwRefundAll = function()
{
   var refund = 0;
   var i = 0;
   while(i < _root.__rwList.length)
   {
      var d = _root.__rwList[i];
      if(d.slot >= 0)
      {
         refund += _root.__rwBought(d.id);
         _root.__rwSetTal(d.slot, 0);
      }
      i++;
   }
   _root.Krin.skillPoints = _root.__rwNum(_root.Krin.skillPoints) + refund;
   _root.__rwSyncBonus();
   _root.__v8Sync();
   if(_root.KRINMENU && _root.KRINMENU.KrinCreateAbilityMatrix)
   {
      _root.KRINMENU.KrinCreateAbilityMatrix();
   }
   _root.__rwTreeRefresh();
   return refund;
};
_root.__v8Refund = _root.__rwRefundAll;
_root.__v9Learn = _root.__rwLearn;
