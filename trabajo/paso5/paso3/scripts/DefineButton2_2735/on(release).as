// on(release)
// origen: boton 2735 (06208_DefineButton2_2735.bin)

if(Krin.tutorOn == true)
{
   _root.gotoSceneKrin = "IntroSeq";
   gotoAndStop("CS_INTRO");
}
else
{
   _root.gotoSceneKrin = "IntroSeq2";
   gotoAndStop("CS_INTRO2");
}
