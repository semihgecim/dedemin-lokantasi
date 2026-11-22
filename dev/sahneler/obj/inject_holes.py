# inject_holes.py spec.json  -> adds /*OBH<id>*/ line with hole masks + behind image
import sys,json,re,io,base64,os,numpy as np,cv2
from PIL import Image
F='/home/claude/dedemin-lokantasi.html';h=open(F,encoding='utf8').read()
spec=json.load(open(sys.argv[1]));sid=spec['id']
n=re.match(r'\d+',sid).group(0);sc='c' if sid.endswith('c') else ('o' if n in ('1','2') else 'a')
key=n+sc
h=re.sub(r'\n/\*OBH%s\*/[^\n]*'%key,'',h)
if 'OBJC={},OBH={};' not in h:
    h=h.replace('const OBJ1={},OBJ2={},OBJC={};','const OBJ1={},OBJ2={},OBJC={},OBH={};',1)
    assert 'OBJC={},OBH={};' in h
hs={}
U=np.zeros((900,1200),bool)
for f in sorted(os.listdir('masks')):
    m=re.match(rf'{re.escape(sid)}_hole_(\d+)\.png$',f)
    if not m:continue
    k=int(m.group(1));a=(np.array(Image.open('masks/'+f))>128);U|=a
    a=cv2.dilate(a.astype(np.uint8)*255,np.ones((3,3),np.uint8));a=cv2.GaussianBlur(a,(0,0),1.5);a=cv2.resize(a,(600,450),interpolation=cv2.INTER_AREA)
    b=io.BytesIO();im=Image.new('LA',(600,450),(255,0));im.putalpha(Image.fromarray(a));im.save(b,'PNG',optimize=True)
    hs[k]='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
if hs:
    B=np.array(Image.open(f'masks/{sid}_behind.jpg').convert('RGB'))
    keep=cv2.dilate(U.astype(np.uint8),np.ones((15,15),np.uint8))>0
    B[~keep]=128
    b=io.BytesIO();Image.fromarray(B).save(b,'WEBP',quality=84)
    keys={f'mk:{key}h_{k}':v for k,v in hs.items()};keys[f'mk:{key}hb']='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    line=f'/*OBH{key}*/Object.assign(GIMG,'+json.dumps(keys)+f');OBH["{key}"]={{b:"mk:{key}hb",m:'+json.dumps({k:f'mk:{key}h_{k}' for k in hs})+'};'
    i=h.index('\n',h.index('/*S2ART19*/'));h=h[:i+1]+line+'\n'+h[i+1:]
open(F,'w',encoding='utf8').write(h);print(sid,'holes',len(hs),(len(line)//1024 if hs else 0),'KB')
