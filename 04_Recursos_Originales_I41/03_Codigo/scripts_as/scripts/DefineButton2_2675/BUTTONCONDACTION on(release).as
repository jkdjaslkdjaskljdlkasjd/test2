on(release){
   _root.Krin.slotInUse = 4;
   if(_root.Krin.dataMode == "save")
   {
      _root.Krin.nameUser = _root.krinNameUser;
      _root.thereIsASlotSelected = false;
      _root.KrinToolTipper.tt = "";
      _root.KrinToolTipper.t = "";
      _root.KrinToolTipper.gotoAndStop(1);
      if(_root.isDebugMode)
      {
         var debugLevel = 50;
         _root.Krin.Level = debugLevel;
         _root.Krin.LevelStats[0] = debugLevel;
         _root.Krin.skillPoints = debugLevel;
         _root.Krin.statPoints = debugLevel * 20;
         _root.Krin.Euro = 1000000;
         _root.Krin.questProgress = ["EMPTY",10,13,9,10,13,0,0,0,0,0,0,0,0];
         _root.Krin.LevelStats = [debugLevel,debugLevel,debugLevel,debugLevel,debugLevel,debugLevel];
      }
      gotoAndStop("classMenu");
   }
   else if(_root["slot" + _root.Krin.slotInUse].data.nameUser != undefined)
   {
      _root.krinNameUser = _root["slot" + _root.Krin.slotInUse].data.nameUser;
      _root.krinHandleData(_root.Krin.slotInUse);
      _root["slot" + _root.Krin.slotInUse].flush();
      if(arenaMode == true)
      {
         _root["arenaPlayer" + currentArenaPlayer].krinNameUser = _root.krinNameUser;
         if(currentArenaPlayer == 1)
         {
            currentArenaPlayer++;
            pickText = _root.KrinLang[KLangChoosen].MENU[73];
         }
         else
         {
            gotoAndStop("ArenaNav");
         }
      }
      else
      {
         gotoAndStop("Navigation");
      }
   }
}
