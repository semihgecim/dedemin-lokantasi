# pack.py spec.json key(e.g. 5) before.jpg tag(a|c)  -> emits obj_<id>.json {names,pos,masks(dataurl),before(dataurl)}
import sys,json,base64,io,numpy as np,cv2
from PIL import Image
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks']
L=np.array(Image.open(f'masks/{sid}_label.png'))
out={'names':[],'pos':[],'masks':[],'k':''}
for k,t in enumerate(T):
    out['names'].append(t['name']);isr=(t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))=='r');out['k']+=('r' if isr else 'o')
    if t.get('final'):out['pos'].append([600,450]);out['masks'].append("");continue
    m=((np.array(Image.open(f'masks/{sid}_{k}.png'))>128) if isr else (L==k+1)).astype(np.uint8)*255
    ys,xs=np.nonzero(m)
    if len(xs)==0: out['pos'].append([600,450]);out['masks'].append("");continue
    # position: point inside mask nearest to centroid
    cx,cy=xs.mean(),ys.mean();i=np.argmin((xs-cx)**2+(ys-cy)**2);out['pos'].append([int(xs[i]),int(ys[i])])
    if isr and t.get('minus'):
        sub=np.isin(L,[j+1 for j in t['minus']]);m=(m>0)&~sub;m=m.astype(np.uint8)*255
    if t.get('diff'):
        Aa=np.array(Image.open(spec['after']).convert('RGB').resize((1200,900))).astype(int);Cc=np.array(Image.open(sys.argv[3]).convert('RGB').resize((1200,900))).astype(int)
        dd=(np.abs(Aa-Cc).sum(2)>60).astype(np.uint8);dd=cv2.dilate(dd,np.ones((5,5),np.uint8));m=(m>0)&(dd>0);m=m.astype(np.uint8)*255
    m=cv2.dilate(m,np.ones((5,5),np.uint8));m=cv2.GaussianBlur(m,(0,0),1.5)
    m=cv2.resize(m,(600,450),interpolation=cv2.INTER_AREA)
    b=io.BytesIO();im=Image.new('LA',(600,450),(255,0));im.putalpha(Image.fromarray(m));im.save(b,'PNG',optimize=True);out['masks'].append('data:image/png;base64,'+base64.b64encode(b.getvalue()).decode())
B=Image.open(sys.argv[2]).convert('RGB').resize((1200,900));b=io.BytesIO();B.save(b,'WEBP',quality=82)
out['before']='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
C=Image.open(sys.argv[3]).convert('RGB').resize((1200,900));b=io.BytesIO();C.save(b,'WEBP',quality=82);out['clean']='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
json.dump(out,open(f'obj_{sid}.json','w'),ensure_ascii=False)
print(sum(len(x) for x in out['masks'])//1024,'KB masks',len(out['before'])//1024,'KB before')
