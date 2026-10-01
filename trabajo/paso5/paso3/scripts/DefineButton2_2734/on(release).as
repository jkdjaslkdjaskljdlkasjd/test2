// on(release)
// origen: boton 2734 (06206_DefineButton2_2734.bin)

if(_root.Krin.qual == "HIGH")
{
   _root.Krin.qual = "LOW";
   _quality = "LOW";
}
else
{
   _root.Krin.qual = "HIGH";
   _quality = "HIGH";
}
if(_root.Krin.qual == "HIGH")
{
   tit_11 = _root.KrinLang[_root.KLangChoosen].MENU[31];
}
else
{
   tit_11 = _root.KrinLang[_root.KLangChoosen].MENU[32];
}
