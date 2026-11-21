import sys,json,numpy as np
from PIL import Image,ImageDraw
d=json.load(open(sys.argv[1]));U=Image.new('L',(1200,900),0);D=ImageDraw.Draw(U)
for t in d['tasks']:
    if 'poly' in t and 'sam' not in t: D.polygon([tuple(v) for v in t['poly']],fill=255)
a=np.array(U)>0;print(sys.argv[1],'uncovered',round(1-a.mean(),3))
U.save('cov_'+d['id']+'.png')
