import sys,json,numpy as np,cv2
from PIL import Image
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks']
L=np.array(Image.open(f'masks/{sid}_label.png'))
isr=lambda t:t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))=='r'
objs=[k for k,t in enumerate(T) if not t.get('final') and not isr(t)]
M={k:(L==k+1) for k in objs};K=np.ones((5,5),np.uint8)
D={k:cv2.dilate(M[k].astype(np.uint8),K)>0 for k in objs}
bot={k:(np.percentile(np.nonzero(M[k])[0],98) if M[k].any() else 0) for k in objs}
for i,k in enumerate(objs):
    for j in objs[i+1:]:
        b=(D[k]&M[j]).sum()
        if b<60:continue
        # boundary pixels: where is j relative to k: front if j's bottom lower
        if bot[j]>bot[k]+5:
            print(f"{sid}: {k} '{T[k]['name']}' arkada, sonra gelen {j} '{T[j]['name']}' önünde; sınır {b}")
