import numpy as np,json,io,base64
from PIL import Image,ImageDraw
from scipy import ndimage as nd
from sklearn.cluster import KMeans
D0='/home/claude/dedemin-lokantasi/dev/sahneler/lokanta/'
W,H=300,225
ld=lambda f:np.asarray(Image.open(D0+f).convert('RGB').resize((W,H),Image.LANCZOS)).astype(float)/255
B,A=ld('bos.jpg'),ld('dolu.jpg')
d=np.abs(A-B).sum(2);loc=np.maximum(0,d-nd.gaussian_filter(d,20))
hp=lambda X:X-np.stack([nd.gaussian_filter(X[...,c],4) for c in range(3)],2)
D=nd.gaussian_filter(loc+1.5*np.abs(hp(A)-hp(B)).sum(2),1.5)
thr=np.percentile(D,70);Dn=np.clip((D-thr)/(np.percentile(D,97)-thr),0,1)
ys,xs=np.nonzero(Dn>.15);w=Dn[ys,xs];X=np.stack([xs,ys],1).astype(float)
km=KMeans(20,n_init=4,random_state=2).fit(X,sample_weight=w);C=km.cluster_centers_
yy,xx=np.mgrid[0:H,0:W];Lab=((xx[...,None]-C[:,0])**2+(yy[...,None]-C[:,1])**2).argmin(2)
mass=[(Dn*(Lab==k)).sum() for k in range(20)];order=np.argsort(mass)[::-1]
def png(m):
  a=(m*255).astype(np.uint8);im=Image.fromarray(np.stack([np.full_like(a,255),a],2),'LA').resize((200,150),Image.BILINEAR)
  b=io.BytesIO();im.save(b,'PNG',optimize=True);return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
masks=[];out=[]
for k in order:
  m=nd.gaussian_filter((Lab==k).astype(float),5);m=np.clip((m-.5)*1.6+.5,0,1);masks.append(m);out.append(png(m))
def webp(f,q=72):
  b=io.BytesIO();Image.open(D0+f).convert('RGB').resize((1200,900),Image.LANCZOS).save(b,'WEBP',quality=q,method=6);return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
json.dump({'b':webp('bos.jpg'),'a':webp('dolu.jpg'),'m':out},open('lok.json','w'))
Bi=Image.fromarray((B*255).astype(np.uint8));Ai=Image.fromarray((A*255).astype(np.uint8))
sh=Image.new('RGB',(5*300,4*225))
for i in range(20):
  mk=Image.fromarray((np.clip(sum(masks[:i+1]),0,1)*255).astype(np.uint8));sh.paste(Image.composite(Ai,Bi,mk),((i%5)*300,(i//5)*225))
sh.save('lok_prog.jpg',quality=75)
