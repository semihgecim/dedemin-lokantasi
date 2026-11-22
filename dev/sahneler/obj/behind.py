# behind.py spec.json -> masks/{sid}_behind.jpg, masks/{sid}_hole_{k}.png ; prints stats
import sys,json,numpy as np,cv2,torch,os
from PIL import Image
torch.set_num_threads(2)
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks']
A=np.array(Image.open(spec['after']).convert('RGB').resize((1200,900)))
L=np.array(Image.open(f'masks/{sid}_label.png'))
isr=lambda t:t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))=='r'
objs=[k for k,t in enumerate(T) if not t.get('final') and not isr(t)]
M={k:(L==k+1) for k in objs}
HULL='--hull' in sys.argv
EL=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,61))
def amodal(m):
    u=m.astype(np.uint8);c=cv2.morphologyEx(cv2.copyMakeBorder(u,40,40,40,40,cv2.BORDER_CONSTANT,0),cv2.MORPH_CLOSE,EL)[40:-40,40:-40]
    ff=c.copy();h,w=ff.shape;msk=np.zeros((h+2,w+2),np.uint8);cv2.floodFill(ff,msk,(0,0),1) if ff[0,0]==0 else None
    holes=(ff==0)
    cs,_=cv2.findContours(u,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);hl=np.zeros_like(u)
    for cc in cs:
        if cv2.contourArea(cc)>200:cv2.fillPoly(hl,[cv2.convexHull(cc)],1)
    near=cv2.dilate(u,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(91,91)))>0
    return (c>0)|holes|((hl>0)&near&HULL), (hl>0)
hole={};need=set()
for i,k in enumerate(objs):
    if not M[k].any():continue
    am,hull=amodal(M[k]);later=np.zeros_like(am)
    for j in objs[i+1:]:
        x=am&M[j]
        if M[j].sum()>0 and (hull&M[j]).sum()/M[j].sum()>0.6:x=x|(hull&M[j])
        if x.sum()>30:later|=x;need.add(j)
    if later.sum()>60:hole[k]=later
model=torch.jit.load('/tmp/big-lama.pt',map_location='cpu');model.eval()
B=A.copy()
for j in sorted(need):
    ys,xs=np.nonzero(M[j]);m=128
    y1,y2,x1,x2=max(0,ys.min()-m),min(900,ys.max()+m),max(0,xs.min()-m),min(1200,xs.max()+m)
    crop=A[y1:y2,x1:x2];mk=cv2.dilate(M[j][y1:y2,x1:x2].astype(np.uint8),np.ones((9,9),np.uint8))
    h,w=mk.shape;ph,pw=(8-h%8)%8,(8-w%8)%8
    ci=np.pad(crop,((0,ph),(0,pw),(0,0)),mode='reflect');mi=np.pad(mk,((0,ph),(0,pw)),mode='reflect')
    with torch.no_grad():
        o=model(torch.from_numpy(ci).permute(2,0,1)[None].float()/255,torch.from_numpy(mi)[None,None].float())
    o=(o[0].permute(1,2,0).numpy()*255).clip(0,255).astype(np.uint8)[:h,:w]
    sub=B[y1:y2,x1:x2];mm=M[j][y1:y2,x1:x2];sub[mm]=o[mm]
Image.fromarray(B).save(f'masks/{sid}_behind.jpg',quality=90)
for f in os.listdir('masks'):
    if f.startswith(f'{sid}_hole_'):os.remove('masks/'+f)
for k,h in hole.items():Image.fromarray((h*255).astype(np.uint8)).save(f'masks/{sid}_hole_{k}.png')
print(sid,'holes',len(hole),'inpainted',len(need))
