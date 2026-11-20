import numpy as np,json,io,base64,pickle,sys
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage as nd
city,n=sys.argv[1],int(sys.argv[2])
exec(open(f'tasks_{city}.py').read())
CL=pickle.load(open(f'clus_{city}.pkl','rb'));S=4
D='/home/claude/dedemin-lokantasi/dev/sahneler/s2/'
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
def png(m):
  a=(m*255).astype(np.uint8);im=Image.fromarray(np.stack([np.full_like(a,255),a],2),'LA').resize((200,150),Image.BILINEAR)
  b=io.BytesIO();im.save(b,'PNG',optimize=True);return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def wb(im,q):
  b=io.BytesIO();im.save(b,'WEBP',quality=q,method=6);return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
R={}
for j in (1,2):
  noun,tl,fin=T[j];assert len(tl)==26 and sorted(k for k,_ in tl)==list(range(26)),j
  cent=np.array(CL[j]);yy,xx=np.mgrid[0:225,0:300];Lab=((xx[...,None]-cent[:,0])**2+(yy[...,None]-cent[:,1])**2).argmin(2)
  masks=[]
  for k,_ in tl:
    m=(Lab==k).astype(float);m=nd.gaussian_filter(m,5);m=np.clip((m-.5)*1.6+.5,0,1);masks.append(m)
  pts=[[round(cent[k][0]*S),round(cent[k][1]*S)] for k,_ in tl]
  R[j]={'noun':noun,'names':[nm for _,nm in tl]+[fin],'m':[png(m) for m in masks],'p':pts}
  B=Image.open(f'{D}{city}-{j}-once.jpg').convert('RGB').resize((300,225));A=Image.open(f'{D}{city}-{j}-sonra.jpg').convert('RGB').resize((300,225))
  sheet=Image.new('RGB',(7*300,4*245),'white');d=ImageDraw.Draw(sheet)
  for i in range(26):
    mk=Image.fromarray((np.clip(sum(masks[:i+1]),0,1)*255).astype(np.uint8));im=Image.composite(A,B,mk)
    sheet.paste(im,((i%7)*300,(i//7)*245+20));d.text(((i%7)*300+2,(i//7)*245+2),f'{i+1} {tl[i][1]}',fill=(0,0,0),font=F)
  sheet.save(f'sh_{city}_{j}.jpg',quality=70)
r1,r2=R[1],R[2]
JOB={'noun':r1['noun'],'cx':600,'t':[[nm,p[0],p[1],120] for nm,p in zip(r1['names'],r1['p']+[[600,450]])]}
JOB2={'noun':r2['noun'],'t':r2['names'],'p':r2['p']}
IMG={}
for j,(a,b) in ((1,('a','b')),(2,('c','d'))):
  IMG[f'{n}{a}']=wb(Image.open(f'{D}{city}-{j}-sonra.jpg').convert('RGB').resize((1000,750),Image.LANCZOS),56)
  IMG[f'{n}{b}']=wb(Image.open(f'{D}{city}-{j}-once.jpg').convert('RGB').resize((1000,750),Image.LANCZOS),50)
json.dump({'n':n,'JOB':JOB,'JOB2':JOB2,'M1':r1['m'],'M2':r2['m'],'IMG':IMG},open(f'art_{n}.json','w'),ensure_ascii=False)
print('ok',sum(len(v) for v in IMG.values())//1024,'KB img')
