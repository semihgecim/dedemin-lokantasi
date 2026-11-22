import sys,json,numpy as np
from PIL import Image,ImageDraw
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks']
A=Image.open(spec['after']).convert('RGB').resize((1200,900))
L=np.zeros((900,1200),np.uint8);ms={}
for k,t in enumerate(T):
    if t.get('final'):continue
    ms[k]=np.array(Image.open(f'masks/{sid}_{k}.png'))>128
regions=[k for k in ms if T[k].get('kind',('r' if ('poly' in T[k] and 'sam' not in T[k]) else 'o'))=='r']
objs=[k for k in ms if k not in regions]
for k in sorted(regions,key=lambda k:-ms[k].sum()): L[ms[k]]=k+1
import os
if all(os.path.exists(f'masks/{sid}_{k}_lg.npy') for k in objs) and objs:
    LG=np.stack([np.where(ms[k],np.load(f'masks/{sid}_{k}_lg.npy').astype(np.float32),-99) for k in objs])
    best=LG.argmax(0);anyo=LG.max(0)>-99
    for i,k in enumerate(objs): L[anyo&(best==i)]=k+1
else:
    for k in sorted(objs,key=lambda k:-ms[k].sum()): L[ms[k]]=k+1
# low-coverage objects: fill from after/clean difference inside their boxes
SC=json.load(open('scenes.json')).get(sid)
if SC:
    import cv2 as _c2
    Cc=np.array(Image.open(SC['clean']).convert('RGB').resize((1200,900))).astype(int);Aa=np.array(A).astype(int)
    dd=(np.abs(Aa-Cc).sum(2)>70).astype(np.uint8);dd=_c2.morphologyEx(dd,_c2.MORPH_OPEN,np.ones((3,3),np.uint8))
    regl=set(k+1 for k in regions)
    for k in objs:
        B=np.zeros((900,1200),bool)
        for p in T[k].get('sam',[]):
            if 'box' in p:
                x1,y1,x2,y2=p['box'];bb=np.zeros_like(B);bb[y1:y2,x1:x2]=1
                cov=((L==k+1)&bb).sum()/max(1,bb.sum())
                if cov<0.15:B|=bb
        if not B.any():continue
        free=(L==0)|np.isin(L,list(regl))
        add=B&(dd>0)&free
        add=_c2.morphologyEx(add.astype(np.uint8),_c2.MORPH_CLOSE,np.ones((7,7),np.uint8))>0
        add&=B&free
        L[add]=k+1
# drop thin slivers / tiny fragments of object labels
import cv2 as _cv
for k in objs:
    m=(L==k+1).astype(np.uint8)
    if not m.any():continue
    op=_cv.morphologyEx(m,_cv.MORPH_OPEN,_cv.getStructuringElement(_cv.MORPH_ELLIPSE,(7,7)))
    n,cc,st,_=_cv.connectedComponentsWithStats(op)
    if n<=1:continue
    mx=st[1:,4].max();keep=np.zeros(n,bool)
    for i in range(1,n):keep[i]=st[i,4]>=max(250,0.06*mx)
    good=keep[cc]
    good=(_cv.dilate(good.astype(np.uint8),np.ones((7,7),np.uint8))>0)&(m>0)
    L[(m>0)&~good]=0
# per-box hull fill: region/unassigned pixels inside an object's own hull that differ from clean belong to it
if SC:
    for k in objs:
        for p in T[k].get('sam',[]):
            if 'box' not in p:continue
            x1,y1,x2,y2=p['box'];x1=max(0,x1);y1=max(0,y1)
            sub=(L[y1:y2,x1:x2]==k+1).astype(np.uint8)
            if sub.sum()<300:continue
            cs,_=_c2.findContours(sub,_c2.RETR_EXTERNAL,_c2.CHAIN_APPROX_SIMPLE)
            cs=[c for c in cs if _c2.contourArea(c)>150]
            if not cs:continue
            hl=np.zeros_like(sub);_c2.fillPoly(hl,[_c2.convexHull(np.concatenate(cs))],1)
            Ls=L[y1:y2,x1:x2];fr=(Ls==0)|np.isin(Ls,list(regl))
            add=(hl>0)&fr&(dd[y1:y2,x1:x2]>0)
            Ls[add]=k+1
# fill unassigned pixels inside object boxes (smallest box wins)
bx=[]
for k in objs:
    for p in T[k].get('sam',[]):
        if 'box' in p: x1,y1,x2,y2=p['box'];bx.append(((x2-x1)*(y2-y1),k,x1,y1,x2,y2))
for _,k,x1,y1,x2,y2 in sorted(bx,reverse=True):
    sub=L[y1:y2,x1:x2];z=(sub==0)
    # only fill holes near the object: within dilated object mask
    import cv2
    near=cv2.dilate((sub==k+1).astype(np.uint8),np.ones((25,25),np.uint8))>0
    sub[z&near]=k+1
Image.fromarray(L).save(f'masks/{sid}_label.png')
# sheet
tiles=[]
for k,t in enumerate(T):
    if t.get('final'):continue
    m=Image.fromarray(((L==k+1)*255).astype(np.uint8))
    tl=Image.composite(A,Image.new('RGB',A.size,(30,30,30)),m).resize((300,225));ImageDraw.Draw(tl).text((4,4),f"{k} {t['name']}".encode('ascii','replace').decode(),fill='yellow');tiles.append(tl)
W=6;c=Image.new('RGB',(W*300,((len(tiles)+W-1)//W)*225))
for i,tl in enumerate(tiles):c.paste(tl,((i%W)*300,(i//W)*225))
c.save(f'lab_{sid}.jpg',quality=80);print('unassigned',round((L==0).mean(),3))
