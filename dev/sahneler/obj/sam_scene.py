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
    return cv2.resize(mm,(1200,900),interpolation=cv2.INTER_LINEAR)>0
os.makedirs('masks',exist_ok=True);only=set(sys.argv[2:])
for k,t in enumerate(spec['tasks']):
    if only and str(k) not in only: continue
    M=np.zeros((900,1200),bool)
    for p in t.get('sam',[]):
        m=sam(p)
        if 'box' in p:
            x1,y1,x2,y2=p['box'];c=np.zeros_like(m);c[max(0,y1-12):y2+12,max(0,x1-12):x2+12]=1;m&=c.astype(bool)
        M|=m
    if 'poly' in t:
        im=Image.new('L',(1200,900),0);ImageDraw.Draw(im).polygon([tuple(v) for v in t['poly']],fill=255);M|=np.array(im)>128
    Image.fromarray((M*255).astype(np.uint8)).save(f"masks/{spec['id']}_{k}.png")
    print(k,t['name'],round(M.mean(),3),flush=True)
