// onClipEvent(enterFrame)
// origen: DefineSprite_3135 fotograma 1, clip en profundidad 3 (06851_DefineSprite_3135.bin, byte 55)

if(!(_y > 0) && _xmove > 0 || !(_y < 0 - maxH) && _xmove < 0)
{
   this._y += _xmove;
}
