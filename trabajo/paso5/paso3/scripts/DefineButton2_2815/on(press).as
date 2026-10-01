// on(press)
// origen: boton 2815 (06504_DefineButton2_2815.bin)

if(_root.Krin.PauseForScreen != true)
{
   trainFight2 = new Array();
   for(i in _root.trainFight[_root.Krin.sectionIn])
   {
      if(_root.Krin.questProgress[_root.Krin.sectionIn] > _root.trainFight[_root.Krin.sectionIn][i][1])
      {
         trainFight2.push(_root.trainFight[_root.Krin.sectionIn][i][0]);
      }
   }
   _root.Krin.BattlePick = trainFight2[Math.floor(Math.random() * trainFight2.length)];
   _root.Krin.progressFight = false;
   _root.finalTrainCap = _root.trainFightCap[_root.Krin.sectionIn];
   _root.Krin.usedTraining = true;
   _root.gotoAndPlay("LOADBATTLESCENE");
   _root.KrinScreen._visible = false;
}
