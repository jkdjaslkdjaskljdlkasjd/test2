// onClipEvent(load)
// origen: DefineSprite_2800 fotograma 1, clip en profundidad 49 (06488_DefineSprite_2800.bin, byte 418)

function setAG(num)
{
   pN = num;
   nameText = _root["playerKrin" + pN].playerName;
   i = 1;
   while(i < 6)
   {
      this["b" + i].COVER.gotoAndStop("BLACK");
      i++;
   }
   if(!(_root["playerKrin" + pN].agMode < 0))
   {
      this["b" + (_root["playerKrin" + pN].agMode + 1)].COVER.gotoAndStop("WHITE");
   }
}
setAG(3);
