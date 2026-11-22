import sys,json,numpy as np
from PIL import Image,ImageDraw
spec=json.load(open(sys.argv[1]));sid=spec['id'];A=Image.open(spec['after']).convert('RGB').resize((1200,900))
labs=sys.argv[2].split(',');ks=[int(x) for x in sys.argv[3].split(',')];crop=tuple(int(x) for x in sys.argv[4].split(','));out=sys.argv[5]
cw,chh=crop[2]-crop[0],crop[3]-crop[1];sc=min(1,300/cw)
rows=[]
for lf in labs:
    L=np.array(Image.open(lf));row=[]
    for k in ks:
        m=Image.fromarray(((L==k+1)*255).astype('uint8'))
        t=Image.composite(A,Image.new('RGB',A.size,(255,0,255)),m).crop(crop).resize((int(cw*sc),int(chh*sc)));ImageDraw.Draw(t).text((4,4),f"{k} {spec['tasks'][k]['name']}".encode('ascii','replace').decode(),fill='yellow');row.append(t)
    rows.append(row)
W=int(cw*sc);H=int(chh*sc);o=Image.new('RGB',(W*len(ks),H*len(rows)),'white')
for r,row in enumerate(rows):
    for i,t in enumerate(row):o.paste(t,(i*W,r*H))
o.save(out)
