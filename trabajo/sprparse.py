import sys,json,struct,glob
sys.path.insert(0,'/home/claude/w/paso5/tools')
from swfsplit import read_tags
from swfshape import Bits
def place(code,d,o,ln):
    r={}
    f=d[o]; i=o+1; f2=0
    if code==70: f2=d[i]; i+=1
    r['move']=bool(f&1)
    r['depth']=struct.unpack_from('<H',d,i)[0]; i+=2
    if code==70 and (f2&8):
        j=d.index(b'\0',i); i=j+1
    if f&2: r['char']=struct.unpack_from('<H',d,i)[0]; i+=2
    if f&4:
        b=Bits(d,i); r['m']=b.matrix(); b.align(); i=b.p
    if f&32:
        pass
    return r
def sprite_frames(path):
    d=open(path,'rb').read()
    tags=read_tags(d,4,len(d))
    frames=[[]]
    for code,lh,o,ln in tags:
        if code==1: frames.append([])
        elif code in (26,70): frames[-1].append(('P',place(code,d,o,ln)))
        elif code==28: frames[-1].append(('R',struct.unpack_from('<H',d,o)[0]))
        elif code==43: frames[-1].append(('L',d[o:o+ln].split(b'\0')[0].decode()))
        elif code==12: frames[-1].append(('A',ln))
        elif code==0: pass
        else: frames[-1].append(('T',code))
    return frames
def spr_file(root,cid):
    return glob.glob(root+'/tags/*_DefineSprite_%d.bin'%cid)[0]
if __name__=='__main__':
    root,cid=sys.argv[1],int(sys.argv[2])
    fr=sprite_frames(spr_file(root,cid))
    for n,f in enumerate(fr,1):
        if f: print(n,f)
