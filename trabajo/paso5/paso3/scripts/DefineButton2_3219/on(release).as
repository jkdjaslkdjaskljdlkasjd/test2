// on(release)
// origen: boton 3219 (06938_DefineButton2_3219.bin)

if(_root.Krin.qual == "LOW")
{
   _root.Krin.qual = "HIGH";
   _quality = "HIGH";
}
else
{
   _root.Krin.qual = "LOW";
   _quality = "LOW";
}
if(_root.Krin.qual == "HIGH")
{
   tit_11 = _root.KrinLang[_root.KLangChoosen].MENU[31];
}
else
{
   tit_11 = _root.KrinLang[_root.KLangChoosen].MENU[32];
}
