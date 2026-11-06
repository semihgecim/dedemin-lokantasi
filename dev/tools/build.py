import json,re,sys
sys.path.insert(0,'md');from ext import EXTD
d=json.load(open('md/data.json'))
ITEM=lambda x:f"Mobile game item icon: {x}. Semi-realistic digital painting like a premium cozy cooking game, soft studio light from the upper left, gentle soft shadow under the object, glossy highlights, rich warm natural colors, fine painted texture. NO outlines, NO black line art, NOT cartoon, NOT flat vector. One single subject, centered, slight top-down three-quarter view, filling about 80% of the frame, isolated on a pure white background, square 1:1. No text, no letters, no watermark, no border."
PORT=lambda x:f"Round character avatar for a mobile game, in exactly the same style as the attached stil-referans-karakter.png: {x}. Head and shoulders, friendly warm smile, looking straight at the viewer. Warm illustrated portrait with soft thin brown lines, gentle soft shading, rosy cheeks, natural skin tones. Inside a circle with a plain light cream background, square 1:1. No text, no watermark."
SCENE=lambda x:f"{x} Layout: the shop facade is centered and fills the middle 60% of the width and the lower 75% of the height; arched wooden door on the left half of the facade, big arched window on the right half, one long EMPTY wooden sign board above both. Wide landscape 4:3 game background, semi-realistic digital painting, soft warm evening light, NO outlines, NOT cartoon line art, no people, no text, no letters on the sign, no watermark."
STY="cozy hand-painted mobile game art, soft warm lighting, clean dark outlines, vibrant but gentle colors, no text, no watermark"
src=open('/home/claude/gemini-prompts-3-10.md').read()
secs=re.split(r'(?m)^## ',src)[1:]
scene={};ports={}
for sct in secs:
  n=int(sct.split('.')[0]);sc=re.search(r'```\n(.*?)\n```',sct,re.S).group(1).replace(STY,'').strip().rstrip('.').rstrip(',')+'.'
  sc=re.sub(r'\s*Arched wooden door.*?above the door and window,','',sc)
  sc=re.sub(r'\. ([a-z])',lambda m:'. '+m.group(1).upper(),sc);scene[n]=sc
  ports[n]=[(m.group(1),m.group(2).replace('Round portrait avatar of ','').replace(', head and shoulders, smiling, plain soft background, '+STY,'').strip()) for m in re.finditer(r'- \*\*(.+?)\*\*: `(.+?)`',sct)]
HAVE={'Süt','Yufka','Kazandibi','Keşkül','Tatlı tepsisi','Simit','Peynir'}
seen=set(HAVE)
G=[("Fıstık sepeti","Antep","a wicker basket full of Antep pistachios in their shells"),("Mangal","Antep, Hatay","a small traditional Turkish copper charcoal grill (mangal) with glowing coals"),
("Zeytin kasası","İzmir","a wooden crate full of green and black olives"),("Şerbet güğümü","İzmir, Konya","a copper Turkish sherbet jug with a lid and handle"),
("Balık kasası","Trabzon, İstanbul","a wooden crate full of fresh silver anchovies on ice"),("Çay sepeti","Trabzon, İstanbul","a wicker basket full of fresh green tea leaves"),
("Nohut kasası","Hatay","a wooden crate full of dry chickpeas"),("Tandır ocağı","Konya","a traditional round clay tandoor oven with fire inside"),
("Kil fırını","Kapadokya","a small domed clay bread oven with fire inside"),("Üzüm sepeti","Kapadokya","a wicker basket full of purple grapes"),
("Arı kovanı","Van","a traditional straw beehive with two small bees"),("Ocak","Mardin","a traditional stone hearth with fire and a copper pot on top"),
("Badem sepeti","Mardin","a wicker basket full of almonds"),("Kahve cezvesi","Mardin","a hammered copper Turkish coffee pot (cezve) with a few coffee beans")]
AN=[("Un","a small terracotta bowl heaped with white flour"),("Kat kat yufka","a neat stack of thin layered phyllo sheets"),("Şöbiyet","two triangular şöbiyet pastries filled with pistachio and cream, on a plate"),("Baklava","four diamond pieces of pistachio baklava on a small plate"),("Baklava tepsisi","a big round copper tray of pistachio baklava cut in diamonds"),
("Kabuklu fıstık","a small pile of Antep pistachios in their shells"),("Fıstık içi","a small bowl of shelled bright green pistachios"),("Dövülmüş fıstık","a small bowl of crushed green pistachio"),("Fıstık ezmesi","a glass jar of green pistachio paste with a cloth lid"),("Katmer","a Gaziantep katmer pastry with pistachio and clotted cream, cut in squares on a plate"),
("Et","a piece of raw red meat on a small wooden board"),("Kıyma","a bowl of fresh minced meat"),("Lahmacun","a Turkish lahmacun with parsley and a lemon wedge"),("Ali Nazik","Ali Nazik kebab, meat cubes on smoky eggplant yogurt puree, on a plate"),("Beyran","a copper bowl of Gaziantep beyran soup with rice and shredded meat")]
CATS={3:("Kordon kedisi","a cute ginger tabby street cat from the İzmir seaside promenade, with a little blue collar"),4:("Uzungöl kedisi","a fluffy grey and white cat from the Black Sea highlands"),5:("Avlu kedisi","a sleek cream colored courtyard cat from Antakya with green eyes"),6:("Fırın kedisi","a plump brown tabby bakery cat with a little flour on its nose"),7:("Kayalık kedisi","a sandy beige cat from the Cappadocia rocks with amber eyes"),8:("Van kedisi","a pure white Van cat with one blue eye and one amber eye"),9:("Konak kedisi","a black and white tuxedo cat from an old Mardin stone mansion"),10:("Galata kedisi","a tabby Istanbul street cat with a confident look")}
L1=[];L2=[]
def add(L,name,p):L.append((name,p))
# file 1
sec1=[];
sec1.append(("1. Üreteçler (tahtada malzeme çıkaran eşyalar)",[(f"{n} ({w})",ITEM(x)) for n,w,x in G]))
a=[]
for n,x in AN:
  seen.add(n);a.append((n,ITEM(x)))
sec1.append(("2. Antep malzemeleri",a))
sec1.append(("3. Hatıra kartı",[("İstanbul · Hünkâr beğendi",ITEM("Hünkâr beğendi, lamb stew on smoky eggplant puree, on a plate"))]))
def city_sec(C):
  n=C['n'];out=[("Dükkân",SCENE(scene[n]))]
  for c,ch in C['chains'].items():
    for nm,x in ch['items']:
      if nm in seen:continue
      seen.add(nm);out.append((nm,ITEM(x)))
  for nm,x in ports[n]:out.append((f"Karakter: {nm}",PORT(x)))
  if n in CATS:out.append((f"Karakter: {CATS[n][0]}",PORT(CATS[n][1])))
  return (f"{n}. bölüm · {C['place']}",out)
cities=d['city']
for C in cities[:5]:sec1.append(city_sec(C))
sec2=[city_sec(C) for C in cities[5:]]
ext=[]
order=['k','p','m']+[c for C in cities for c in C['chains']]
for c in order:
  for l in range(6,9):
    k=c+str(l)
    if k in EXTD:
      nm=EXTD[k].split(',')[0];ext.append((nm,ITEM(EXTD[k])))
sec2.append(("Uzun zincirler · 6-8. seviye yemekler (en sona kalabilir)",ext))
HDR="""# Dedemin Lokantası · eksik resimler ({p}/2)

**Gemini'ye ver:** bu dosya + `stil-referans.png` + talimat metni. Her satır tek bir resim, sırayla.

**Bu dosyada {n} resim var.**
"""
def write(fn,secs,part):
  n=sum(len(x[1]) for x in secs);t=[HDR.format(p=part,n=n)];i=0
  for title,items in secs:
    t.append(f"\n## {title}\n")
    for name,p in items:
      i+=1;t.append(f"{i}. **{name}**\n`{p}`\n")
  open(fn,'w').write("\n".join(t));return n
print(write('/home/claude/eksik-resimler-1.md',sec1,1),write('/home/claude/eksik-resimler-2.md',sec2,2))
