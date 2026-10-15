#!/bin/bash
J=/home/claude/jindrapetrik/jpexs-decompiler
exec java -Djava.awt.headless=true -Xmx6g -cp "/home/claude/build/app:/home/claude/build/lib:$J/lib/*" com.jpexs.decompiler.flash.gui.Main "$@" 2> >(grep -v "Picked up JAVA_TOOL" >&2)
