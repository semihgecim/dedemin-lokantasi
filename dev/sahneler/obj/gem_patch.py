# gem_patch.py sid k x1,y1,x2,y2 gemini.png  -> replace patch_k content with gemini where objects removed
import sys,json,numpy as np,cv2
from PIL import Image
sid,k=sys.argv[1],sys.argv[2];x1,y1,x2,y2=map(int,sys.argv[3].split(','));gf=sys.argv[4]
SC=json.load(open('scenes.json'))[sid];spec=json.load(open(SC['spec']))
A=np.array(Image.open(spec['after']).convert('RGB').resize((1200,900)))
G=np.array(Image.open(gf).convert('RGB').resize((x2-x1,y2-y1),Image.LANCZOS))
Ac=A[y1:y2,x1:x2]
# align G to Ac (SIFT affine) using background (non-table) features
s=cv2.SIFT_create(3000);ga=cv2.cvtColor(Ac,cv2.COLOR_RGB2GRAY);gg=cv2.cvtColor(G,cv2.COLOR_RGB2GRAY)
ka,da=s.detectAndCompute(ga,None);kg,dg=s.detectAndCompute(gg,None)
m=cv2.BFMatcher().knnMatch(dg,da,k=2);g=[a for a,b in m if a.distance<0.7*b.distance]
src=np.float32([kg[a.queryIdx].pt for a in g]);dst=np.float32([ka[a.trainIdx].pt for a in g])
M,inl=cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=3)
print('matches',len(g),int(inl.sum()),M.round(3).tolist())
G=cv2.warpAffine(G,M,(x2-x1,y2-y1),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
meta=json.load(open(f'masks/{sid}_patch.json'));px,py,pw,ph=meta[k]
P=np.array(Image.open(f'masks/{sid}_patch_{k}.png'))
full=np.zeros((900,1200,4),np.uint8);full[py:py+ph,px:px+pw]=P
GG=A.copy();GG[y1:y2,x1:x2]=G
diff=np.abs(GG.astype(int)-A.astype(int)).sum(2)
removed=(diff>60).astype(np.uint8);removed=cv2.morphologyEx(removed,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8));removed=cv2.dilate(removed,np.ones((7,7),np.uint8))
w=cv2.GaussianBlur((removed*255).astype(np.uint8),(0,0),3)/255.
inbox=np.zeros((900,1200));inbox[y1+4:y2-4,x1+4:x2-4]=1;w=w*inbox
rgb=(full[...,:3]*(1-w[...,None])+GG*w[...,None]).astype(np.uint8)
full[...,:3]=rgb
Image.fromarray(full[py:py+ph,px:px+pw]).save(f'masks/{sid}_patch_{k}.png')
print('replaced frac',float((w[py:py+ph,px:px+pw]*(full[py:py+ph,px:px+pw,3]>0)).sum()/max(1,(full[py:py+ph,px:px+pw,3]>0).sum())))
