import cv2
import numpy as np

def thresh_det(x1,y1,x2,y2,img):
    averageB=0
    averageG=0
    averageR=0
    sumB=0
    sumG=0
    sumR=0
    for i in range(x1, x2):
        for j in range(y1, y2):
            sumB+=img[i, j, 0]
            sumG+=img[i, j, 1]
            sumR+=img[i, j, 2]
    averageB = sumB/400.0
    averageG = sumG/400.0
    averageR = sumR/400.0
    error=40
    lowerb= np.array([averageB-error, averageG-error, averageR-error])
    upperb= np.array([averageB+error, averageG+error, averageR+error])
    return cv2.inRange(img,lowerb,upperb)

cap = cv2.VideoCapture(1)
while (1):
    _, img1=cap.read()
    cv2.rectangle(img1,(242, 229),(262, 209),(0,255,0),3)
    cv2.rectangle(img1,(220, 280),(240,260),(0,255,0),3)
    cv2.rectangle(img1,(272, 284),(292, 264),(0,255,0),3)
    cv2.rectangle(img1,(264, 184),(284, 164),(0,255,0),3)
    images = []
    images.append(thresh_det(242,209,262,229,img1))
    images.append(thresh_det(220,260,240,280,img1))
    images.append(thresh_det(272,264,292,284,img1))
    images.append(thresh_det(264,164,284,184,img1))
    img2 = np.zeros((480,640), np.uint8)

    for i in range(4):
        img2 += images[i]
    dst = cv2.medianBlur(img2, 7)
    cv2.imshow("img2", img2)
    cv2.imshow("blur", dst)

    k=cv2.waitKey(5)
    if k==27:
        break
cv2.destroyAllWindows()
