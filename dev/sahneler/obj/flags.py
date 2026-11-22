import sys,json,numpy as np
from PIL import Image
for sp in sys.argv[1:]:
    spec=json.load(open(sp));sid=spec['id'];T=spec['tasks']
    try:L=np.array(Image.open(f'masks/{sid}_label.png'))
    except:continue
    for k,t in enumerate(T):
        if t.get('final') or not t.get('sam'):continue
        B=np.zeros((900,1200),bool)
        for p in t['sam']:
            if 'box' in p:x1,y1,x2,y2=p['box'];B[y1:y2,x1:x2]=1
        cov=((L==k+1)&B).sum()/max(1,B.sum())
        per=[]
        for p in t['sam']:
            if 'box' in p:
                x1,y1,x2,y2=p['box'];bb=np.zeros_like(B);bb[y1:y2,x1:x2]=1;per.append(((L==k+1)&bb).sum()/max(1,bb.sum()))
        if cov<0.15 or (per and min(per)<0.08):print(f"{sid} {k} {t['name']} cov={cov:.2f} per={[round(x,2) for x in per]}")
