import sys,json,numpy as np
from PIL import Image,ImageDraw
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks']
A=Image.open(spec['after']).convert('RGB').resize((1200,900))
L=np.zeros((900,1200),np.uint8);ms={}
for k,t in enumerate(T):
    if t.get('final'):continue
    ms[k]=np.array(Image.open(f'masks/{sid}_{k}.png'))>128
regions=[k for k in ms if 'poly' in T[k] and 'sam' not in T[k]]
objs=[k for k in ms if k not in regions]
for k in sorted(regions,key=lambda k:-ms[k].sum()): L[ms[k]]=k+1
for k in sorted(objs,key=lambda k:-ms[k].sum()): L[ms[k]]=k+1
# fill unassigned pixels inside object boxes (smallest box wins)
bx=[]
for k in objs:
    for p in T[k].get('sam',[]):
        if 'box' in p: x1,y1,x2,y2=p['box'];bx.append(((x2-x1)*(y2-y1),k,x1,y1,x2,y2))
for _,k,x1,y1,x2,y2 in sorted(bx,reverse=True):
    sub=L[y1:y2,x1:x2];z=(sub==0)
    # only fill holes near the object: within dilated object mask
    import cv2
    near=cv2.dilate((sub==k+1).astype(np.uint8),np.ones((25,25),np.uint8))>0
    sub[z&near]=k+1
Image.fromarray(L).save(f'masks/{sid}_label.png')
# sheet
tiles=[]
for k,t in enumerate(T):
    if t.get('final'):continue
    m=Image.fromarray(((L==k+1)*255).astype(np.uint8))
    tl=Image.composite(A,Image.new('RGB',A.size,(30,30,30)),m).resize((300,225));ImageDraw.Draw(tl).text((4,4),f"{k} {t['name']}".encode('ascii','replace').decode(),fill='yellow');tiles.append(tl)
W=6;c=Image.new('RGB',(W*300,((len(tiles)+W-1)//W)*225))
for i,tl in enumerate(tiles):c.paste(tl,((i%W)*300,(i//W)*225))
c.save(f'lab_{sid}.jpg',quality=80);print('unassigned',round((L==0).mean(),3))
