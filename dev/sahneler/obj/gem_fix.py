# gem_fix.py sid k x1,y1,x2,y2 gemini.png
import sys,json,numpy as np,cv2
from PIL import Image
from scipy import ndimage
sid,k=sys.argv[1],int(sys.argv[2]);x1,y1,x2,y2=map(int,sys.argv[3].split(','));gf=sys.argv[4]
SC=json.load(open('scenes.json'))[sid];spec=json.load(open(SC['spec']))
A=np.array(Image.open(spec['after']).convert('RGB').resize((1200,900)))
L=np.array(Image.open(f'masks/{sid}_label.png'))
G=np.array(Image.open(gf).convert('RGB').resize((x2-x1,y2-y1),Image.LANCZOS));Ac=A[y1:y2,x1:x2]
s=cv2.SIFT_create(3000);ka,da=s.detectAndCompute(cv2.cvtColor(Ac,cv2.COLOR_RGB2GRAY),None);kg,dg=s.detectAndCompute(cv2.cvtColor(G,cv2.COLOR_RGB2GRAY),None)
m=cv2.BFMatcher().knnMatch(dg,da,k=2);g=[a for a,b in m if a.distance<0.7*b.distance]
M,inl=cv2.estimateAffinePartial2D(np.float32([kg[a.queryIdx].pt for a in g]),np.float32([ka[a.trainIdx].pt for a in g]),method=cv2.RANSAC,ransacReprojThreshold=3)
print('matches',len(g),int(inl.sum()),M.round(3).tolist())
G=cv2.warpAffine(G,M,(x2-x1,y2-y1),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
GG=A.copy();GG[y1:y2,x1:x2]=G
T=spec['tasks'];isr=lambda t:t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))=='r'
tm=(L==k+1).astype(np.uint8)
cs,_=cv2.findContours(tm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);hull=np.zeros_like(tm)
pts=np.concatenate([c for c in cs if cv2.contourArea(c)>300]);cv2.fillPoly(hull,[cv2.convexHull(pts)],1)
later=[j for j in range(k+1,len(T)) if not isr(T[j]) and not T[j].get('final') and ((L==j+1)&(hull>0)).sum()>200]
print('on-table later objs',[(j,T[j]['name']) for j in later])
inbox=np.zeros((900,1200),bool);inbox[y1+3:y2-3,x1+3:x2-3]=1
diff=np.abs(GG.astype(int)-A.astype(int)).sum(2)
R=((diff>70)&(hull>0)&inbox).astype(np.uint8)
R=cv2.morphologyEx(R,cv2.MORPH_OPEN,np.ones((3,3),np.uint8));R=cv2.morphologyEx(R,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
R=cv2.dilate(R,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))&(hull>0)&inbox
lab,n=ndimage.label(R);sz=ndimage.sum(R,lab,range(1,n+1));keep=np.isin(lab,[i+1 for i,v in enumerate(sz) if v>40]);R=keep
cand=np.isin(L,[j+1 for j in later])|(L==k+1)
R&=cand|(L==0)
# reassign table pixels in R to nearest later object
if later:
    lm=np.isin(L,[j+1 for j in later])
    d,(iy,ix)=ndimage.distance_transform_edt(~lm,return_indices=True)
    tr=R&(L==k+1)&(d<60)
    L[tr]=L[iy[tr],ix[tr]]
    print('reassigned px',int(tr.sum()))
Image.fromarray(L).save(f'masks/{sid}_label.png')
# rebuild patch k: hole (later objects in old hole) ∪ R
meta=json.load(open(f'masks/{sid}_patch.json'));full=np.zeros((900,1200,4),np.uint8)
if str(k) in meta:
    px,py,pw,ph=meta[str(k)];full[py:py+ph,px:px+pw]=np.array(Image.open(f'masks/{sid}_patch_{k}.png'))
w=cv2.GaussianBlur((R*255).astype(np.uint8),(0,0),2.5)/255.
full[...,:3]=(full[...,:3]*(1-w[...,None])+GG*w[...,None]).astype(np.uint8)
full[...,3]=np.maximum(full[...,3],((R&(L!=k+1))*255).astype(np.uint8))
ys,xs=np.nonzero(full[...,3]);px,py=int(xs.min()),int(ys.min());pw,ph=int(xs.max()+1-px),int(ys.max()+1-py)
Image.fromarray(full[py:py+ph,px:px+pw]).save(f'masks/{sid}_patch_{k}.png');meta[str(k)]=[px,py,pw,ph];json.dump(meta,open(f'masks/{sid}_patch.json','w'))
h=np.array(Image.open(f'masks/{sid}_hole_{k}.png'))>128 if __import__('os').path.exists(f'masks/{sid}_hole_{k}.png') else np.zeros((900,1200),bool)
Image.fromarray(((h|(R&(L!=k+1)))*255).astype(np.uint8)).save(f'masks/{sid}_hole_{k}.png')
print('R px',int(R.sum()))
