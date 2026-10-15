function awardAch(achNum)
{
   updateSonny2AchByIndex(achNum);
   if(achGet[achNum] != 1)
   {
      achGet[achNum] = 1;
      achSlot.data.achGet[achNum] = 1;
      achSlot.flush();
      ach_Display.play();
      achGlobal = achNum;
   }
}
whatToSayX = _root.KrinLang[KLangChoosen].MENU[26];
arenaMode = false;
_root.winCondition = -1;
_root.Krin.bossMusic = false;
achGet = new Array();
achGet = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var achSlot = SharedObject.getLocal("achSlot");
if(achSlot.data.achState == true)
{
   for(i in achGet)
   {
      achGet[i] = achSlot.data.achGet[i];
      if(achGet[i] == 1)
      {
         updateSonny2AchByIndex(i);
      }
   }
}
else
{
   achSlot.data.achState = true;
   achSlot.data.achGet = new Array();
   for(i in achGet)
   {
      achSlot.data.achGet[i] = achGet[i];
   }
}
achSlot.flush();
stop();
whatToSay1 = _root.KrinLang[KLangChoosen].MENU[18];
whatToSay2 = _root.KrinLang[KLangChoosen].MENU[20];
whatToSay3 = _root.KrinLang[KLangChoosen].MENU[19];
whatToSay4 = _root.KrinLang[KLangChoosen].MENU[90];
whatToSay5 = _root.KrinLang[KLangChoosen].MENU[91];
