# order.py spec.json [--write] : side-occlusion pairs -> move front object earlier
import sys,json,numpy as np,cv2,shutil
from PIL import Image
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks']
L=np.array(Image.open(f'masks/{sid}_label.png'))
isr=lambda t:t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))=='r'
objs=[k for k,t in enumerate(T) if not t.get('final') and not isr(t)]
M={k:(L==k+1) for k in objs}
EL=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,61))
def amodal(m):
    u=m.astype(np.uint8);c=cv2.morphologyEx(cv2.copyMakeBorder(u,40,40,40,40,cv2.BORDER_CONSTANT,0),cv2.MORPH_CLOSE,EL)[40:-40,40:-40]
    ff=c.copy();h,w=ff.shape;msk=np.zeros((h+2,w+2),np.uint8)
    if ff[0,0]==0:cv2.floodFill(ff,msk,(0,0),1)
    return (c>0)|(ff==0)
K5=np.ones((5,5),np.uint8)
bot={k:(np.percentile(np.nonzero(M[k])[0],98) if M[k].any() else 0) for k in objs}
cons=[]
for i,k in enumerate(objs):
    if not M[k].any():continue
    am=amodal(M[k]);dk=cv2.dilate(M[k].astype(np.uint8),K5)>0
    for j in objs[i+1:]:
        if not M[j].any():continue
        b=(dk&M[j]).sum()
        if b<120:continue
        inside=(am&M[j]).sum()/M[j].sum()
        if inside>0.5:continue   # j sits on/in k -> keep k first (patched)
        if bot[j]>bot[k]+15 and M[j].sum()>1500:
            cons.append((j,k,b))
for j,k,b in cons:print(f"{sid}: '{T[j]['name']}'({j}) önce, '{T[k]['name']}'({k}) sonra  sınır={b}")
if '--write' in sys.argv and cons:
    order=list(range(len(T)))
    for j,k,b in sorted(cons,key=lambda c:-c[2]):
        pj,pk=order.index(j),order.index(k)
        if pj>pk:
            # move j right before k, only if no task between depends... (simple)
            order.pop(pj);order.insert(pk,j)
    shutil.copy(sys.argv[1],sys.argv[1]+'.orig') if not __import__('os').path.exists(sys.argv[1]+'.orig') else None
    spec['tasks']=[T[i] for i in order];json.dump(spec,open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
    print('reordered',order)
