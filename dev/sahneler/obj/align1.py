import cv2,numpy as np,sys
A=cv2.resize(cv2.imread(sys.argv[1]),(1200,900));B=cv2.resize(cv2.imread(sys.argv[2]),(1200,900))
def E(X):
    g=cv2.GaussianBlur(cv2.cvtColor(X,cv2.COLOR_BGR2GRAY),(0,0),3);e=cv2.Canny(g,30,90).astype(np.float32);return cv2.GaussianBlur(e,(0,0),4)
s=0.25;sa=cv2.resize(E(A),None,fx=s,fy=s);sb=cv2.resize(E(B),None,fx=s,fy=s)
W=np.eye(2,3,dtype=np.float32)
cc,W=cv2.findTransformECC(sa,sb,W,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,300,1e-6),None,5)
W[:,2]/=s;print('cc %.3f'%cc,W.round(3).tolist())
Bw=cv2.warpAffine(B,W,(1200,900),flags=cv2.INTER_CUBIC+cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite(sys.argv[3],Bw,[cv2.IMWRITE_JPEG_QUALITY,93])
