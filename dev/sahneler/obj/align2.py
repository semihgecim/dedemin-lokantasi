import cv2,numpy as np,sys
A=cv2.resize(cv2.imread(sys.argv[1]),(1200,900));B=cv2.resize(cv2.imread(sys.argv[2]),(1200,900))
s=cv2.SIFT_create(4000);ga=cv2.cvtColor(A,cv2.COLOR_BGR2GRAY);gb=cv2.cvtColor(B,cv2.COLOR_BGR2GRAY)
ka,da=s.detectAndCompute(ga,None);kb,db=s.detectAndCompute(gb,None)
m=cv2.BFMatcher().knnMatch(db,da,k=2);g=[x for x,y in m if x.distance<0.75*y.distance]
src=np.float32([kb[x.queryIdx].pt for x in g]);dst=np.float32([ka[x.trainIdx].pt for x in g])
M,inl=cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=4)
print(len(g),int(inl.sum()),M.round(3).tolist())
Bw=cv2.warpAffine(B,M,(1200,900),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite(sys.argv[3],Bw,[cv2.IMWRITE_JPEG_QUALITY,93])
