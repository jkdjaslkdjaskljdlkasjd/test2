// onClipEvent(enterFrame)
// origen: DefineSprite_3378 fotograma 1, clip en profundidad 6 (07253_DefineSprite_3378.bin, byte 265)

this._rotation = 180 * (_root.BattleTimeNow / (_root.BattleTimeLimit / 2)) - 180;
if(_rotation < 0)
{
   _rotation = 0;
}
