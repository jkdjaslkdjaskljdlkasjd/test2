navTitle = "";
navText = "";
Krin.PauseForScreen = false;
Krin.wSaver = krinXbarPro.bar._width;
Krin.levelMaxProgress = parseInt(questHub[Krin.sectionIn].progressMax);
Krin.levelMinProgress = parseInt(Krin.questProgress[Krin.sectionIn]);
if(Krin.levelMinProgress > Krin.levelMaxProgress)
{
   Krin.levelMinProgress = Krin.levelMaxProgress;
}
krinXbarPro.bar._width = Krin.levelMinProgress / Krin.levelMaxProgress * Krin.wSaver;
klt1 = _root.KrinLang[KLangChoosen].SYSTEM[9] + Krin.sectionIn;
klt2 = _root.KrinLang[KLangChoosen].ZONES[Krin.sectionIn] + ": " + _root.KrinLang[KLangChoosen].ZONES2[Krin.sectionIn];
klt3 = _root.KrinLang[KLangChoosen].SYSTEM[10] + (parseInt(Krin.questProgress[Krin.sectionIn]) + 1);
addSound("Music",1);
_root.slotSaveGO = Krin.slotInUse;
stop();
menuMode = true;
Krin.Pause = false;
_root.Krin.mouseItem = 0;
KrinToolTipper.inner.gotoAndStop(_root.KrinLang.ENGLISH.ITEMNAME[_root.Krin.mouseItem]);
_root.thereIsASlotSelected = false;
whatToSay3 = _root.KrinLang[KLangChoosen].MENU[19];
onMouseDown = function()
{
   if(UITmouseHold > 0)
   {
      if(UITdrop != true)
      {
         UITmouseHold = 0;
         _root.KrinToolTipper.inner2.gotoAndStop("Empty2");
      }
   }
   if(!_root.thereIsASlotSelected)
   {
      itemReturned = false;
      if(_root.Krin.mouseItem != 0)
      {
         if(_root.Krin.previousItemSlot.slotType == "itemSlot")
         {
            itemReturned = true;
            _root.Krin.itemArray[_root.Krin.previousItemSlot.id] = _root.Krin.mouseItem;
            _root.Krin.previousItemSlot.inner.gotoAndStop(_root.KrinLang.ENGLISH.ITEMNAME[_root.Krin.itemArray[_root.Krin.previousItemSlot.id]]);
         }
         else
         {
            by = 0;
            while(by < _root.Krin.itemArray.length)
            {
               if(_root.Krin.itemArray[by] == 0 && itemReturned == false)
               {
                  itemReturned = true;
                  _root.Krin.itemArray[by] = _root.Krin.mouseItem;
                  _root.KRINMENU["itemSlot" + by].inner.gotoAndStop(_root.KrinLang.ENGLISH.ITEMNAME[_root.Krin.itemArray[by]]);
               }
               by++;
            }
         }
         if(itemReturned == true)
         {
            _root.Krin.mouseItem = 0;
            _root.KrinToolTipper.inner.gotoAndStop("None");
         }
         else
         {
            _root.KrinCombatText.play();
            _root.KrinCombatText.combatTexter = "No more empty slots to return item to.";
         }
      }
   }
};
var BATNUMO = new Number(600);
