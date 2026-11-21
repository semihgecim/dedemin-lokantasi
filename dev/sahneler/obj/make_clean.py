# make_clean.py spec.json before.jpg out_clean.jpg  -> C = A with object areas filled by tone-matched B
import sys,json,numpy as np,cv2
from PIL import Image
spec=json.load(open(sys.argv[1]));sid=spec['id'];T=spec['tasks']
A=cv2.resize(cv2.imread(spec['after']),(1200,900)).astype(np.float32)
B=cv2.resize(cv2.imread(sys.argv[2]),(1200,900)).astype(np.float32)
L=np.array(Image.open(f'masks/{sid}_label.png'))
obj=np.zeros(L.shape,bool)
for k,t in enumerate(T):
    if t.get('final'):continue
    kind=t.get('kind',('r' if ('poly' in t and 'sam' not in t) else 'o'))
    if kind=='o': obj|=(L==k+1)
M=cv2.dilate(obj.astype(np.uint8),np.ones((17,17),np.uint8)).astype(np.float32)
keep=1-M
def mblur(X,w,s):
    num=cv2.GaussianBlur(X*w[...,None],(0,0),s);den=cv2.GaussianBlur(w,(0,0),s)[...,None]+1e-4;return num/den
s=45
Ab=mblur(A,keep,s);Bb=mblur(B,keep,s)
G=(Ab+4)/(Bb+4);G=np.clip(G,0.3,3.5)
B2=np.clip(B*G,0,255)
Mf=cv2.GaussianBlur(M,(0,0),3)[...,None]
C=A*(1-Mf)+B2*Mf
cv2.imwrite(sys.argv[3],C.astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,93])
