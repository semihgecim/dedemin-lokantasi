import sys,os,glob,json,base64,io,re
from rembg import remove,new_session
from PIL import Image
s=new_session('isnet-general-use')
SRC='/mnt/user-data/uploads/resim 2/'
out={}
if os.path.exists('bodies.json'): out=json.load(open('bodies.json'))
for k in sys.argv[1:]:
    p=SRC+'yarim-'+k+'.png'
    if not os.path.exists(p): print('missing',k);continue
    im=Image.open(p).convert('RGB')
    o=remove(im,session=s)
    a=o.split()[3].point(lambda v:0 if v<20 else v);o.putalpha(a)
    o=o.crop(o.getbbox())
    w,h=o.size
    if h>1.45*w: o=o.crop((0,0,w,int(1.45*w)))
    H=330;o=o.resize((int(o.width*H/o.height),H),Image.LANCZOS)
    b=io.BytesIO();o.save(b,'WEBP',quality=82);out[k]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    o.save('png_'+k+'.png');print(k,o.size,len(b.getvalue()))
json.dump(out,open('bodies.json','w'))
