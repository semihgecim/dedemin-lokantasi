import sys
from PIL import Image,ImageDraw
ks=sys.argv[2:];n=len(ks);cols=10;rows=(n+cols-1)//cols
c=Image.new('RGB',(cols*120,rows*180),(120,170,200));d=ImageDraw.Draw(c)
for i,k in enumerate(ks):
  im=Image.open('png_'+k+'.png');im=im.resize((120,int(im.height/2)))
  x,y=(i%cols)*120,(i//cols)*180;c.paste(im,(x,y+165-im.height),im);d.text((x+3,y+167),k,fill='white')
c.save(sys.argv[1])
