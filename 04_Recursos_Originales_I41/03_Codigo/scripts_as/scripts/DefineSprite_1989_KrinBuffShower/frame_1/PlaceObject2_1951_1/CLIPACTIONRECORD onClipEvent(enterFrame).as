onClipEvent(enterFrame){
   if(this.hitTest(_root._xmouse,_root._ymouse))
   {
      _root.__a3StatusHover(this._parent);
   }
}
