import sys,json,numpy as np,os
from PIL import Image,ImageDraw
SC=json.load(open('scenes.json'))
def run(sid):
    sc=SC[sid];spec=json.load(open(sc['spec']));T=spec['tasks']
    A=np.array(Image.open(spec['after']).convert('RGB').resize((1200,900)));C=np.array(Image.open(sc['clean']).convert('RGB').resize((1200,900)))
    OLD=os.environ.get('OLD');L=np.array(Image.open((f'masks_bak/{sid}_label.png') if OLD else f'masks/{sid}_label.png'))
    Bh=np.array(Image.open(f'masks/{sid}_behind.jpg')) if os.path.exists(f'masks/{sid}_behind.jpg') else A
    isr=lambda t:t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))=='r'
    H={}
    for k in range(len(T)):
        f=f'masks/{sid}_hole_{k}.png'
        if os.path.exists(f):pass
    tiles=[]
    for k,t in enumerate(T):
        if t.get('final') or isr(t):continue
        m=L==k+1
        if not m.any():tiles.append((k,t['name'],None));continue
        I=C.copy()
        PM=json.load(open(f'masks/{sid}_patch.json')) if (os.path.exists(f'masks/{sid}_patch.json') and not OLD) else {}
        for j in range(k+1):
            if str(j) in PM:
                x,y,w,h=PM[str(j)];P=np.array(Image.open(f'masks/{sid}_patch_{j}.png'));al=P[...,3:]/255.
                I[y:y+h,x:x+w]=(P[...,:3]*al+I[y:y+h,x:x+w]*(1-al)).astype(np.uint8)
        for j in range(k+1):
            if not isr(T[j]):mm=L==j+1;I[mm]=A[mm]
        ys,xs=np.nonzero(m);cx,cy=(xs.min()+xs.max())//2,(ys.min()+ys.max())//2;s=max(xs.max()-xs.min(),ys.max()-ys.min())+80;s=max(s,180)
        x1,y1=max(0,cx-s//2),max(0,cy-s//2);x2,y2=min(1200,x1+s),min(900,y1+s)
        a=Image.fromarray(A[y1:y2,x1:x2]).resize((220,220));b=Image.fromarray(I[y1:y2,x1:x2]).resize((220,220))
        tiles.append((k,t['name'],(a,b)))
    W=3;tw=450;th=245;rows=(len(tiles)+W-1)//W
    o=Image.new('RGB',(W*tw,rows*th),'white');d=ImageDraw.Draw(o)
    for i,(k,nm,ab) in enumerate(tiles):
        x,y=(i%W)*tw,(i//W)*th
        d.text((x+4,y+2),f"{k} {nm}".encode('ascii','replace').decode(),fill='black')
        if ab:o.paste(ab[0],(x+2,y+20));o.paste(ab[1],(x+226,y+20))
        else:d.text((x+40,y+100),"EMPTY",fill='red')
    o.save(f'qa_{sid}{"_old" if OLD else ""}.jpg',quality=80)
for s in sys.argv[1:]:run(s)
