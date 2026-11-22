import sys,json,os,numpy as np,cv2,onnxruntime as ort
from PIL import Image,ImageDraw
D='/root/.rembg/models/sam/'
enc=ort.InferenceSession(D+'sam_vit_b_01ec64.encoder.onnx',providers=['CPUExecutionProvider'])
dec=ort.InferenceSession(D+'sam_vit_b_01ec64.decoder.onnx',providers=['CPUExecutionProvider'])
spec=json.load(open(sys.argv[1]));A=np.array(Image.open(spec['after']).convert('RGB').resize((1200,900)))
IH,IW=684,1024;sc=min(IW/1200,IH/900)
inp=np.zeros((IH,IW,3),np.float32);r=cv2.resize(A,(int(1200*sc),int(900*sc)),interpolation=cv2.INTER_LINEAR);inp[:r.shape[0],:r.shape[1]]=r
emb=enc.run(None,{enc.get_inputs()[0].name:inp})[0]
def sam(pr):
    pts=[];lb=[]
    if 'box' in pr:x1,y1,x2,y2=pr['box'];pts=[[x1,y1],[x2,y2]];lb=[2,3]
    for q in pr.get('pts',[]):pts.append(q);lb.append(1)
    for q in pr.get('neg',[]):pts.append(q);lb.append(0)
    c=np.array(pts+[[0,0]],np.float32)*sc*(1024/1024);l=np.array(lb+[-1],np.float32)
    # apply_coords: input_size(684,1024)->target 1024: scale long side 1024 → factor 1
    m,_,_=dec.run(None,{"image_embeddings":emb,"point_coords":c[None],"point_labels":l[None],"mask_input":np.zeros((1,1,256,256),np.float32),"has_mask_input":np.zeros(1,np.float32),"orig_im_size":np.array([IH,IW],np.float32)})
    mm=m[0,0][:int(900*sc),:int(1200*sc)]
    return cv2.resize(mm,(1200,900),interpolation=cv2.INTER_LINEAR)
os.makedirs('masks',exist_ok=True);AUTO='--auto' in sys.argv;only=set(a for a in sys.argv[2:] if a!='--auto')
T=spec['tasks']
import functools
@functools.lru_cache(None)
def RAW(j):
    f=f"masks_bak/{spec['id']}_{j}.png"
    return (np.array(Image.open(f))>128) if os.path.exists(f) else np.zeros((900,1200),bool)
def anchor(j,q):
    x1,y1,x2,y2=q['box'];m=np.zeros((900,1200),np.uint8);sub=RAW(j)[max(0,y1):y2,max(0,x1):x2]
    if sub.sum()<40:return None
    d=cv2.distanceTransform(sub.astype(np.uint8),cv2.DIST_L2,5);yy,xx=np.unravel_index(d.argmax(),d.shape)
    if d.max()<4:return None
    return [int(xx+max(0,x1)),int(yy+max(0,y1))]
def cen(p):x1,y1,x2,y2=p['box'];return [(x1+x2)//2,(y1+y2)//2]
for k,t in enumerate(T):
    if only and str(k) not in only: continue
    M=np.zeros((900,1200),bool);LG=np.full((900,1200),-20,np.float32)
    for p in t.get('sam',[]):
        p=dict(p)
        if AUTO and 'box' in p and 'neg' not in p:
            x1,y1,x2,y2=p['box'];neg=[]
            for j,u in enumerate(T):
                if j==k or not u.get('sam'):continue
                for q in u['sam']:
                    if 'box' not in q:continue
                    pt=anchor(j,q)
                    if pt is None:continue
                    cx,cy=pt
                    if x1+3<cx<x2-3 and y1+3<cy<y2-3 and not RAW(k)[cy,cx]:
                        neg.append([cx,cy])
            if neg:p['neg']=neg
        lg=sam(p);m=lg>0
        if 'box' in p:
            x1,y1,x2,y2=p['box'];c=np.zeros_like(m);c[max(0,y1-12):y2+12,max(0,x1-12):x2+12]=1;m&=c.astype(bool);lg=np.where(c.astype(bool),lg,-20)
        M|=m;LG=np.maximum(LG,lg)
    if t.get('sam'):np.save(f"masks/{spec['id']}_{k}_lg.npy",LG.astype(np.float16))
    for pg in ([t['poly']] if 'poly' in t else [])+t.get('polys',[]):
        im=Image.new('L',(1200,900),0);ImageDraw.Draw(im).polygon([tuple(v) for v in pg],fill=255);M|=np.array(im)>128
    Image.fromarray((M*255).astype(np.uint8)).save(f"masks/{spec['id']}_{k}.png")
    print(k,t['name'],round(M.mean(),3),flush=True)
