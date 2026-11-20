import sys,io,base64,json,os
from PIL import Image
from rembg import remove,new_session
U='/mnt/user-data/uploads/resim 2/'
M=[("edirne-01-ocak","gen:Ciğer ocağı"),("edirne-02-badem-sepeti","gen:Edirne badem sepeti"),("edirne-03-yayik","gen:Yayık"),
("edirne-04-ciger","name:Ciğer"),("edirne-06-ince-ciger","name:Dilim ciğer"),("edirne-08-tava-ciger","name:Tava ciğer"),("edirne-07-ciger-tabagi","name:Ciğer tabağı"),("edirne-09-ciger-sofrasi","name:Ciğer sofrası"),
("edirne-10-badem","name:Çiğ badem"),("edirne-11-ezme-kase","name:Dövülmüş badem"),("edirne-12-ezme-kalip","name:Edirne ezmesi"),("edirne-13-meyve-ezme","name:Meyve ezmesi"),("edirne-14-ezme-kutusu","name:Ezme kutusu"),
("edirne-15-taze-peynir","name:Taze peynir"),("edirne-16-helva-tencere","name:Helva kazanı"),("edirne-17-peynir-helvasi","name:Peynir helvası"),("edirne-18-fistikli-helva","name:Fıstıklı helva"),("edirne-19-helva-tepsisi","name:Helva tepsisi"),
("edirne-20-leylek","face:leylek")]
ses=new_session("isnet-general-use");out={};pv=[]
for f,k in M:
  im=Image.open(U+f+'.png').convert('RGB')
  cut=remove(im,session=ses)
  a=cut.split()[3].point(lambda v:255 if v>128 else 0);cut=cut.crop(a.getbbox());w,h=cut.size
  if k.startswith('face:'):
    s=min(150/w,150/h);cut=cut.resize((int(w*s),int(h*s)),Image.LANCZOS);can=Image.new('RGBA',(160,160),(0,0,0,0));can.paste(cut,((160-cut.width)//2,(160-cut.height)//2),cut)
  else:
    s=min(144/(w*h)**.5,170/w,140/h);cut=cut.resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS);can=Image.new('RGBA',(176,176),(0,0,0,0));can.paste(cut,((176-cut.width)//2,172-cut.height),cut)
  pv.append(can)
  b=io.BytesIO();can.save(b,'WEBP',quality=95);out[k]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
json.dump(out,open('s2img/edirne/items.json','w'),ensure_ascii=False)
sh=Image.new('RGB',(176*10,176*2),(90,140,90))
for i,c in enumerate(pv): sh.paste(c,((i%10)*176,(i//10)*176),c)
sh.save('s2img/edirne/items.jpg');print(len(out),sum(len(v) for v in out.values())//1024,'KB')
