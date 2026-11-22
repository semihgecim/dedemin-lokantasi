# sim.py spec clean.jpg done_count crop out [oldlabel]
import sys,json,numpy as np,os
from PIL import Image
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks'];n=int(sys.argv[3]);crop=tuple(int(x) for x in sys.argv[4].split(','))
A=np.array(Image.open(spec['after']).convert('RGB').resize((1200,900)));C=np.array(Image.open(sys.argv[2]).convert('RGB').resize((1200,900)))
def comp(L,useh):
    I=C.copy()
    if useh and os.path.exists(f'masks/{sid}_behind.jpg'):
        Bh=np.array(Image.open(f'masks/{sid}_behind.jpg'))
        for k in range(n):
            f=f'masks/{sid}_hole_{k}.png'
            if os.path.exists(f):h=np.array(Image.open(f))>128;I[h]=Bh[h]
    if False:
        meta=json.load(open(f'masks/{sid}_patch.json'))
        for k in range(n):
            if str(k) in meta:
                x,y,w,h=meta[str(k)];P=np.array(Image.open(f'masks/{sid}_patch_{k}.png'));a=P[...,3:]/255.
                I[y:y+h,x:x+w]=(P[...,:3]*a+I[y:y+h,x:x+w]*(1-a)).astype(np.uint8)
    for k in range(n):
        t=T[k]
        if t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))=='r':continue
        m=L==k+1;I[m]=A[m]
    return Image.fromarray(I).crop(crop)
L1=np.array(Image.open(sys.argv[6] if len(sys.argv)>6 else f'masks/{sid}_label.png'));L2=np.array(Image.open(f'masks/{sid}_label.png'))
a=comp(L1,False);b=comp(L2,True);w,h=a.size;o=Image.new('RGB',(w*2+6,h),'white');o.paste(a,(0,0));o.paste(b,(w+6,0));o.save(sys.argv[5])
