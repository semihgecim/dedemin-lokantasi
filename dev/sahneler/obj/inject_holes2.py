import sys,json,re,io,base64,os,numpy as np
from PIL import Image
F='/home/claude/dedemin-lokantasi.html';h=open(F,encoding='utf8').read()
if 'OBJC={},OBH={};' not in h:
    h=h.replace('const OBJ1={},OBJ2={},OBJC={};','const OBJ1={},OBJ2={},OBJC={},OBH={};',1);assert 'OBJC={},OBH={};' in h
tot=0
for sp in sys.argv[1:]:
    spec=json.load(open(sp));sid=spec['id']
    n=re.match(r'\d+',sid).group(0);sc='c' if sid.endswith('c') else ('o' if n in ('1','2') else 'a');key=n+sc
    h=re.sub(r'\n/\*OBH%s\*/[^\n]*'%key,'',h)
    mf=f'masks/{sid}_patch.json'
    if not os.path.exists(mf):continue
    meta=json.load(open(mf));keys={};P={}
    for k,(x,y,w,hh) in meta.items():
        im=Image.open(f'masks/{sid}_patch_{k}.png').convert('RGBA');a=np.array(im)
        ys,xs=np.nonzero(a[...,3]>8)
        if len(xs)==0:continue
        x1,x2,y1,y2=xs.min(),xs.max()+1,ys.min(),ys.max()+1
        im=im.crop((x1,y1,x2,y2));b=io.BytesIO();im.save(b,'WEBP',quality=82)
        gk=f'mk:{key}p_{k}';keys[gk]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
        P[int(k)]=[gk,int(x+x1),int(y+y1),int(x2-x1),int(y2-y1)]
    if not P:continue
    line=f'/*OBH{key}*/Object.assign(GIMG,'+json.dumps(keys)+f');OBH["{key}"]={{p:'+json.dumps(P)+'};'
    tot+=len(line)
    i=h.index('\n',h.index('/*S2ART19*/'));h=h[:i+1]+line+'\n'+h[i+1:]
open(F,'w',encoding='utf8').write(h);print('patches KB',tot//1024)
