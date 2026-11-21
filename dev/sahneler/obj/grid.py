import sys
from PIL import Image,ImageDraw
im=Image.open(sys.argv[1]).convert('RGB').resize((1200,900));d=ImageDraw.Draw(im)
for x in range(0,1200,50):d.line([(x,0),(x,900)],fill=(255,0,255) if x%100==0 else (110,0,110))
for y in range(0,900,50):d.line([(0,y),(1200,y)],fill=(255,0,255) if y%100==0 else (110,0,110))
for x in range(0,1200,100):d.text((x+2,2),str(x),fill='yellow')
for y in range(0,900,100):d.text((2,y+2),str(y),fill='yellow')
im.save(sys.argv[2],quality=85)
