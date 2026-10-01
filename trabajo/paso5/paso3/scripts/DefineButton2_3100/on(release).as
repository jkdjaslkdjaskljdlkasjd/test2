// on(release)
// origen: boton 3100 (06816_DefineButton2_3100.bin)

if(_root.Krin.PauseForScreen2 != true)
{
   if(_root.Krin.autoSaver)
   {
      _root.krinHandleData(_root.Krin.slotInUse);
   }
   if(_root.afterCut != "None")
   {
      stopAllSounds();
      _root.gotoAndStop(_root.afterCut);
   }
   else if(_root.Krin.bossJustPwned2)
   {
      _root.gotoAndStop("overMap");
   }
   else
   {
      _root.Krin.PauseForScreen = false;
      if(playerLeveled == true)
      {
         gotoAndStop("skills");
      }
      else
      {
         gotoAndStop("hide");
         _root.krinNavTutSpeech();
         _root.KrinScreen._visible = true;
      }
   }
}
