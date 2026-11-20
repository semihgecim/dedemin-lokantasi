import io,base64,json,sys,numpy as np
from PIL import Image
U='/mnt/user-data/uploads/resim 2/'
M=json.loads(sys.argv[1]);out={};pv=[]
for f,k in M.items():
  im=Image.open(U+f).convert('RGB');a=np.asarray(im).astype(int)
  nw=(np.abs(a-255).sum(2)>30);ys,xs=np.nonzero(nw)
  x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max();cx,cy=(x0+x1)/2,(y0+y1)/2;s=max(x1-x0,y1-y0)/2
  m=s*0.035;im=im.crop((int(cx-s+m),int(cy-s+m),int(cx+s-m),int(cy+s-m))).resize((160,160),Image.LANCZOS)
  pv.append(im);b=io.BytesIO();im.save(b,'WEBP',quality=80,method=6);out['face:'+k]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
sh=Image.new('RGB',(170*len(pv),170),'white')
for i,p in enumerate(pv):sh.paste(p,(i*170,5))
sh.save(sys.argv[2]+'.jpg');json.dump(out,open(sys.argv[2]+'.json','w'))
