// on(release)
// origen: boton 3180 (06897_DefineButton2_3180.bin)

if(_root.Krin.statPoints > 0)
{
   _root.Krin.StatSets0[0] += 1;
   _root.Krin.statPoints--;
   statPoints--;
   yut_lif2++;
   _root.Krin.LIFE += 1;
   if(_root.Krin.statPoints == 0)
   {
      statColor.gotoAndStop("dead");
   }
}
