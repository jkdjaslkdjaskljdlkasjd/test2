// onClipEvent(enterFrame)
// origen: DefineSprite_3378 fotograma 1, clip en profundidad 2 (07253_DefineSprite_3378.bin, byte 42)

this._rotation = -180 + 180 * (_root.BattleTimeNow / (_root.BattleTimeLimit / 2));
if(!(this._rotation < 0))
{
   _rotation = 0;
}
