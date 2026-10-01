// DoAction
// origen: DefineSprite_3409 fotograma 85, DoAction (07297_DefineSprite_3409.bin, byte 1675)

if(_root.arenaMode)
{
   _root.gotoAndStop("arenaEnd");
}
if(_root.winCondition == 0)
{
   _root.gotoAndStop("loseCombat");
}
if(_root.winCondition == 1)
{
   _root.gotoAndStop("winCombat");
}
if(_root.winCondition == 2)
{
   _root.gotoAndStop("drawCombat");
}
