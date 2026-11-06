import sys,io,base64,json
from PIL import Image
from rembg import remove,new_session
A='/mnt/user-data/attachments/c0d5230d-7105-5da4-b31a-134b6e127703/'
M=[("efd64c86","p1"),("2fd35a59","gen:Çay sepeti"),("8e853ac4","card:10:l0"),("643af36a","gen:Ocak"),
("4aa00b80","item:Et"),("82552546","item:Un"),("16954f58","k4"),("56999f40","B2"),("1388f10b","gen:Badem sepeti"),("318fa713","gen:Üzüm sepeti"),
("aa0b6992","p4"),("d50c41ba","gen:Arı kovanı"),("5a17970c","A3"),("f3090ee4","gen:Kahve cezvesi"),("c6ddc576","scene:3"),("e75c40ee","gen:Tandır ocağı"),
("0ca20c62","p3"),("207aefc4","gen:Nohut kasası"),("437aa52c","B1"),("d943428c","gen:Zeytin kasası")]
ses=new_session("isnet-general-use")
out={}
for f,k in M:
  im=Image.open(A+f+'-image.jpg').convert('RGB')
  if k.startswith('scene:'):
    im.save(f'res2/{k.replace(":","_")}.jpg',quality=92);continue
  cut=remove(im,session=ses)
  a=cut.split()[3].point(lambda v:255 if v>128 else 0);bb=a.getbbox();cut=cut.crop(bb)
  w,h=cut.size
  if k.startswith('card:'):
    s=min(170/w,170/h);cut=cut.resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS);can=Image.new('RGBA',(180,180),(0,0,0,0));can.paste(cut,((180-cut.width)//2,(180-cut.height)//2),cut)
  else:
    s=min(144/(w*h)**.5,170/w,140/h);cut=cut.resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS);can=Image.new('RGBA',(176,176),(0,0,0,0));can.paste(cut,((176-cut.width)//2,172-cut.height),cut)
  can.save(f'res2/{k.replace(":","_").replace(" ","_")}.png')
  b=io.BytesIO();can.save(b,'WEBP',quality=95);out[k]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
json.dump(out,open('res2/out.json','w'))
print(len(out))
