// on(release)
// origen: boton 3381 (07258_DefineButton2_3381.bin)

if(_root.InBattle == false)
{
   _root.krinAddMove(Krin.playerNumber, Krin.playerNumber, 0);
   if(_root.InBattle == false && battleClocker.timerWait == 0 && _root.winCondition < 0 && _root.speechDone == true)
   {
      _root.moveChoosen = true;
      _root.UI_BAR.subAI_BAR.gotoAndStop("HIDE");
      if(!turnBasedKrin)
      {
         _root.BattleTimeNow = _root.BattleTimeLimit - 5;
      }
   }
}
