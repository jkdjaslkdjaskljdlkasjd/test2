// on(press)
// origen: boton 3085 (06801_DefineButton2_3085.bin)

if(_root.Krin.mouseItem != 0)
{
   _root.Krin.mouseItem = 0;
   _root.KrinToolTipper.inner.gotoAndStop(_root.KrinLang.ENGLISH.ITEMNAME[_root.Krin.mouseItem]);
}
