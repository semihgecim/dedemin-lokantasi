# usage: proc_city.py <city> <n> face1,face2,face3,face4
import sys,io,base64,json,glob,os
from PIL import Image,ImageDraw
import numpy as np
CN,n,fk=sys.argv[1],int(sys.argv[2]),sys.argv[3].split(',')
D='/home/claude/dedemin-lokantasi/dev/sezon2/'
for f in ['cities1','cities2','cities3','cities4']:exec(open(D+f+'.py').read())
c=[x for x in S2 if x['n']==n][0]
ch=list(c['chains'].values());pet=[k for k,v in c['people'].items() if len(v)>5 and v[5]][0]
keys=['gen:'+v[1][1] for v in ch]+['name:'+it[0] for v in ch for it in v[2]]+['pet:'+pet]
U='/mnt/user-data/uploads/resim 2/'
def f(i):
  g=sorted(glob.glob(U+f'{CN}-{i:02d}b-*.png'))or sorted(glob.glob(U+f'{CN}-{i:02d}-*.png'));return g[0] if g else None
from rembg import remove,new_session
ses=new_session("isnet-general-use");out={};pv=[];miss=[]
for i,k in enumerate(keys,1):
  p=f(i)
  if not p:miss.append(k);continue
  cut=remove(Image.open(p).convert('RGB'),session=ses)
  a=cut.split()[3].point(lambda v:255 if v>128 else 0);cut=cut.crop(a.getbbox());w,h=cut.size
  if k.startswith('pet:'):
    s=min(128/w,138/h);cut=cut.resize((int(w*s),int(h*s)),Image.LANCZOS)
    circ=Image.new('L',(160,160),0);ImageDraw.Draw(circ).ellipse([1,1,158,158],fill=255)
    bg=Image.new('RGBA',(160,160),(246,240,224,255));bg.paste(cut,((160-cut.width)//2,150-cut.height),cut)
    can=Image.new('RGBA',(160,160),(0,0,0,0));can.paste(bg,(0,0),circ);k='face:'+k[4:];q=85
  else:
    s=min(144/(w*h)**.5,170/w,140/h);cut=cut.resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS);can=Image.new('RGBA',(176,176),(0,0,0,0));can.paste(cut,((176-cut.width)//2,172-cut.height),cut);q=95
  pv.append(can);b=io.BytesIO();can.save(b,'WEBP',quality=q);out[k]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
for i,k in enumerate(fk,1):
  g=glob.glob(U+f'{CN}-Y{i}-*.png')
  if not g:miss.append('face:'+k);continue
  im=Image.open(g[0]).convert('RGB');a=np.asarray(im).astype(int);ys,xs=np.nonzero(np.abs(a-255).sum(2)>30)
  cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2;s=max(xs.max()-xs.min(),ys.max()-ys.min())/2;m=s*0.035
  im=im.crop((int(cx-s+m),int(cy-s+m),int(cx+s-m),int(cy+s-m))).resize((160,160),Image.LANCZOS)
  pv.append(im.convert('RGBA'));b=io.BytesIO();im.save(b,'WEBP',quality=80,method=6);out['face:'+k]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
os.makedirs(f's2img/{CN}',exist_ok=True)
json.dump(out,open(f's2img/{CN}/items.json','w'),ensure_ascii=False);json.dump({},open(f's2img/{CN}/faces.json','w'))
sh=Image.new('RGB',(176*12,176*2),(90,140,90))
for i,p in enumerate(pv):sh.paste(p,((i%12)*176,(i//12)*176),p)
sh.save(f's2img/{CN}/items.jpg');print(len(out),'missing',miss)
