// onClipEvent(enterFrame)
// origen: DefineSprite_3239 fotograma 1, clip en profundidad 995 (06960_DefineSprite_3239.bin, byte 11712)

if(_parent.teamChangeCD == false)
{
   bobbybobby++;
   if(bobbybobby == 5)
   {
      _parent.teamChangeCD = true;
      bobbybobby = 0;
   }
}
