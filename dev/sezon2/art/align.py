import cv2,numpy as np,sys
D='/home/claude/dedemin-lokantasi/dev/sahneler/s2/'
for c in sys.argv[1:]:
  for j in (1,2):
    A=cv2.imread(f'{D}{c}-{j}-sonra.jpg');B=cv2.imread(f'{D}{c}-{j}-once.jpg')
    ga=cv2.GaussianBlur(cv2.cvtColor(A,cv2.COLOR_BGR2GRAY),(0,0),3);gb=cv2.GaussianBlur(cv2.cvtColor(B,cv2.COLOR_BGR2GRAY),(0,0),3)
    ea=cv2.Canny(ga,30,90).astype(np.float32);eb=cv2.Canny(gb,30,90).astype(np.float32)
    ea=cv2.GaussianBlur(ea,(0,0),4);eb=cv2.GaussianBlur(eb,(0,0),4)
    s=0.25;sa=cv2.resize(ea,None,fx=s,fy=s);sb=cv2.resize(eb,None,fx=s,fy=s)
    W=np.eye(2,3,dtype=np.float32)
    try:
      cc,W=cv2.findTransformECC(sa,sb,W,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,200,1e-5),None,5)
    except Exception as e: print(c,j,'fail',e);continue
    W[:,2]/=s
    sc=np.sqrt(abs(np.linalg.det(W[:,:2])));sh=W[:,2]
    print(c,j,'cc %.3f scale %.3f shift %.1f %.1f'%(cc,sc,sh[0],sh[1]))
    if abs(sc-1)>0.01 or abs(sh).max()>4:
      Bw=cv2.warpAffine(B,W,(A.shape[1],A.shape[0]),flags=cv2.INTER_CUBIC+cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
      cv2.imwrite(f'{D}{c}-{j}-once.jpg',Bw,[cv2.IMWRITE_JPEG_QUALITY,93]);print('  warped')
