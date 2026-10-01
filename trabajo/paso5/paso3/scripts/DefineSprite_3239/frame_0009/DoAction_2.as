// DoAction_2
// origen: DefineSprite_3239 fotograma 9, DoAction (06960_DefineSprite_3239.bin, byte 14609)

_root.Krin.PauseForScreen = true;
_root.Krin.PauseForScreen2 = true;
_root.Krin.dataMode = "save";
itemsthatdropped = 0;
_root.KrinScreen._visible = false;
_root.Krin.EnemyXPFinal = _root.Krin.EnemyXP / _root.Krin.EnemyXP3;
for(w in _root.Krin.itemArray)
{
   this["itemSlot" + w].inner.gotoAndStop(_root.KrinLang[_root.KLangChoosen].ITEMNAME[_root.Krin.itemArray[w]]);
   this["itemSlot" + w].id = w;
   this["itemSlot" + w].slotType = "itemSlot";
}
w = 0;
while(w < 15)
{
   this["dropSlot" + w].inner.gotoAndStop(_root.KrinLang[_root.KLangChoosen].ITEMNAME[_root.Krin.dropArray[w]]);
   this["dropSlot" + w].id = w;
   this["dropSlot" + w].slotType = "drop";
   if(_root.Krin.dropArray[w] == 0)
   {
      this["dropSlot" + w]._visible = false;
   }
   else
   {
      itemsthatdropped = 1;
   }
   w++;
}
if(itemsthatdropped == 0)
{
   vb99 = _root.KrinLang[_root.KLangChoosen].MENU[12];
   vb2 = "";
}
else
{
   vb99 = "";
   vb2 = _root.KrinLang[_root.KLangChoosen].VICTORY[1];
}
tempGain = _root.moneyConstGain / _root.totalEnemyGain;
trace("TEMPGAIN " + tempGain);
trace("TEMPGAIN " + _root.respecValue(tempGain));
moneyGain = Math.round(0.7000000000000001 * _root.respecValue(tempGain));
_root.Krin.Euro += moneyGain;
dumbEuro = _root.Krin.Euro;
vb1 = _root.KrinLang[_root.KLangChoosen].VICTORY[0];
vb3 = _root.KrinLang[_root.KLangChoosen].VICTORY[2];
vb4 = _root.KrinLang[_root.KLangChoosen].VICTORY[3];
vb5 = "€" + moneyGain;
vbbc1 = _root.KrinLang[_root.KLangChoosen].MENU[15];
vb7 = _root.KrinLang[_root.KLangChoosen].VICTORY[4];
vb8 = _root.KrinLang[_root.KLangChoosen].MENU[13];
if(_root.achProgF)
{
   if(_root.Krin.BattlePick == 109)
   {
      _root.awardAch(0);
   }
   if(_root.Krin.difficulty > 0)
   {
      if(_root.Krin.BattlePick == 308)
      {
         if(!_root.AchVal2)
         {
            _root.awardAch(1);
         }
      }
      if(_root.Krin.BattlePick == 408)
      {
         if(_root.AchVal1 < 2000)
         {
            _root.awardAch(2);
         }
      }
   }
   if(_root.Krin.difficulty == 2)
   {
      if(_root.Krin.usedTraining == false)
      {
         if(_root.Krin.BattlePick == 212)
         {
            _root.awardAch(3);
         }
         if(_root.Krin.BattlePick == 513)
         {
            _root.awardAch(4);
         }
      }
   }
}
if(_root.Krin.BattlePick == 600)
{
   if(_root.AchVal3 == 1)
   {
      _root.awardAch(6);
   }
}
if(_root.Krin.BattlePick == 601)
{
   if(!(_root.AchVal4 > 40))
   {
      _root.awardAch(7);
   }
}
if(_root.Krin.BattlePick == 602)
{
   if(!_root.AchVal2)
   {
      _root.awardAch(8);
   }
}
if(_root.Krin.BattlePick == 703)
{
   _root.awardAch(9);
}
