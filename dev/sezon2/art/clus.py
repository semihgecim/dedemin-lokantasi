import numpy as np,pickle,sys
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage as nd
from sklearn.cluster import KMeans
D='/home/claude/dedemin-lokantasi/dev/sahneler/s2/'
city=sys.argv[1];W,H=300,225;S=4
def load(f): return np.asarray(Image.open(f).convert('RGB').resize((W,H),Image.LANCZOS)).astype(float)/255
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
OUT={}
for j in (1,2):
  B,A=load(f'{D}{city}-{j}-once.jpg'),load(f'{D}{city}-{j}-sonra.jpg')
  d=np.abs(A-B).sum(2);loc=np.maximum(0,d-nd.gaussian_filter(d,20))
  hp=lambda X:X-np.stack([nd.gaussian_filter(X[...,k],4) for k in range(3)],2)
  st=np.abs(hp(A)-hp(B)).sum(2);Dm=nd.gaussian_filter(loc+st*1.5,1.5)
  thr=np.percentile(Dm,70);Dn=np.clip((Dm-thr)/(np.percentile(Dm,97)-thr),0,1)
  ys,xs=np.nonzero(Dn>0.15);w=Dn[ys,xs];vis=(xs*S>210)&(xs*S<990)
  X=np.stack([xs,ys],1).astype(float)
  cent=KMeans(26,n_init=4,random_state=1).fit(X[vis],sample_weight=w[vis]).cluster_centers_
  OUT[j]=cent.tolist()
  im=Image.open(f'{D}{city}-{j}-sonra.jpg').convert('RGB').resize((1200,900));dr=ImageDraw.Draw(im)
  dr.rectangle([210,0,990,899],outline=(255,0,0),width=3)
  for k,(x,y) in enumerate(cent):
    x*=S;y*=S;dr.ellipse([x-16,y-16,x+16,y+16],fill=(255,255,0),outline=(0,0,0),width=2);dr.text((x-12,y-13),str(k),fill=(0,0,0),font=F)
  im.save(f's2job/pv_{city}_{j}.jpg',quality=70)
pickle.dump(OUT,open(f's2job/clus_{city}.pkl','wb'))
