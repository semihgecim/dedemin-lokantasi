# fetch.sh tag after.jpg : converts staged clean<tag>/once<tag> and aligns
T=$1;A=$2;U="/mnt/user-data/uploads/resim 2"
python3 -c "
from PIL import Image
import sys
for k in ['clean','once']:
    Image.open('$U/'+k+'$T.png').convert('RGB').resize((1200,900)).save(k+'${T}_raw.jpg')"
python3 align1.py $A clean${T}_raw.jpg clean${T}.jpg
python3 align1.py clean${T}.jpg once${T}_raw.jpg once${T}.jpg
python3 -c "
from PIL import Image
a=Image.open('$A');b=Image.open('clean$T.jpg');o=Image.open('once$T.jpg');c=Image.new('RGB',(1200,900));c.paste(b.resize((600,450)),(0,0));c.paste(o.resize((600,450)),(600,0));c.paste(Image.blend(a,b,.5).resize((600,450)),(0,450));c.paste(Image.blend(b,o,.5).resize((600,450)),(600,450));c.save('cmp_$T.jpg')"
