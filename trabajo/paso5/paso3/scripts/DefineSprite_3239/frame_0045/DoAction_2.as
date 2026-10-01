// DoAction_2
// origen: DefineSprite_3239 fotograma 45, DoAction (06960_DefineSprite_3239.bin, byte 42167)

achTit = _root.KrinLang[_root.KLangChoosen].ACHSAY[1];
for(i in _root.achGet)
{
   this["achPlate" + i].achNum = i;
   this["achPlate" + i].achTit = _root.KrinLang[_root.KLangChoosen].ACH[i];
   if(_root.achGet[i] == 1)
   {
      this["achPlate" + i].gotoAndStop(2);
   }
}
