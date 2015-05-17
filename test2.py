import cv2
import numpy as np
from math import sqrt
def fun():
    pass
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
    averageB = sumB/400
    averageG = sumG/400
    averageR = sumR/400
    varB , varG, varR = 0,0,0
    for i in range(x1, x2):
        for j in range(y1, y2):
            varB += (averageB - img[i,j,0])**2
            varG += (averageG - img[i,j,1])**2
            varR += (averageR - img[i,j,2])**2
    sdB = int(sqrt(varB/400))
    sdG = int(sqrt(varG/400))
    sdR = int(sqrt(varR/400))
    factor = 2
    lowerb= np.array([averageB-sdB*factor, averageG-sdG*factor, averageR-sdR*factor])
    upperb= np.array([averageB+sdB*factor, averageG+sdG*factor, averageR+sdR*factor])
    return [cv2.inRange(img,lowerb,upperb), averageB, averageG, averageR, [sdB, sdG, sdR]]

def my_thresh(img, res, error):
    factor = 2
    lowerb= np.array([res[0]-error[0]*factor, res[1]-error[1]*factor, res[2]-error[2]*factor])
    upperb= np.array([res[0]+error[0]*factor, res[1]+error[1]*factor, res[2]+error[2]*factor])
    return cv2.inRange(img, lowerb, upperb)

cap = cv2.VideoCapture(1)
res1, res2, res3, res4, res5, res6 = [], [], [], [], [], []
sd1, sd2, sd3, sd4, sd5, sd6 =[], [], [], [], [], []
hull = []
while (1):
    _, img1=cap.read()

    cv2.rectangle(img1, (241, 230), (263, 208), (0, 255, 0), 0)
    cv2.rectangle(img1, (219, 281), (241, 259), (0, 255, 0), 0)
    cv2.rectangle(img1, (271, 285), (293, 263), (0, 255, 0), 0)
    cv2.rectangle(img1, (263, 185), (285, 163), (0, 255, 0), 0)
    cv2.rectangle(img1, (281, 215), (301, 235), (0, 255, 0), 0)
    cv2.rectangle(img1, (309, 172), (329, 192), (0, 255, 0), 0)



    images = []
    images.append(thresh_det(242, 209, 262, 229, img1)[0])
    images.append(thresh_det(220, 260, 240, 280, img1)[0])
    images.append(thresh_det(272, 264, 292, 284, img1)[0])
    images.append(thresh_det(264, 164, 284, 184, img1)[0])
    images.append(thresh_det(281, 215, 301, 235, img1)[0])
    images.append(thresh_det(309, 172, 329, 192, img1)[0])

    img2 = np.zeros((480,640), np.uint8)
    for i in range(6):
        img2 += images[i]

    res1 = thresh_det(242, 209, 262, 229, img1)[1:4]
    res2 = thresh_det(220, 260, 240, 280, img1)[1:4]
    res3 = thresh_det(272, 264, 292, 284, img1)[1:4]
    res4 = thresh_det(264, 164, 284, 184, img1)[1:4]
    res5 = thresh_det(281, 215, 301, 235, img1)[1:4]
    res6 = thresh_det(309, 172, 329, 192, img1)[1:4]



    sd1 = thresh_det(242, 209, 262, 229, img1)[4]
    sd2 = thresh_det(220, 260, 240, 280, img1)[4]
    sd3 = thresh_det(272, 264, 292, 284, img1)[4]
    sd4 = thresh_det(264, 164, 284, 184, img1)[4]
    sd5 = thresh_det(281, 215, 301, 235, img1)[4]
    sd6 = thresh_det(309, 172, 329, 192, img1)[4]

    blur = cv2.medianBlur(img2, 13)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(blur, kernel)
    cv2.imshow("dst", dilated)
    cv2.imshow("blur",blur)
    cv2.imshow("img", img1)


    k = cv2.waitKey(5)
    if k == 27:
        break
cv2.destroyAllWindows()


while 1:
    _, im = cap.read()
    ims=[]
    ims.append(my_thresh(im, res1, sd1))
    ims.append(my_thresh(im, res2, sd2))
    ims.append(my_thresh(im, res3, sd3))
    ims.append(my_thresh(im, res4, sd4))
    ims.append(my_thresh(im, res5, sd5))
    ims.append(my_thresh(im, res6, sd6))

    img_add = np.zeros((480,640), np.uint8)
    for i in range(4):
        img_add += ims[i]

    blur = cv2.medianBlur(img_add, 7)
    '''kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(blur, kernel'''
    blur_copy= blur.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(blur, kernel)

    contours, hierarchy = cv2.findContours(blur.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contour = cv2.drawContours(im, contours, -1, (0,255,0), 3)


    maxarea = 0
    pos = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxarea:
            maxarea = area
            pos = i
    contour = cv2.drawContours(im, contours, pos, (0, 0, 255), 3)

    cv2.drawContours(im, cv2.convexHull(contours[pos], True, False), -1, (255, 0, 0), 3)
    hull = cv2.convexHull(contours[pos], True, True)
    pts = np.array(hull, np.int32)
    pts = pts.reshape((-1,1,2))
    img = cv2.polylines(im,[pts],True,(255, 0, 0))
    

    cv2.imshow("blur", blur)
    cv2.imshow("dilate", dilated)
    cv2.imshow("im", im)

    k=cv2.waitKey(5)
    if k==27:
        break
cv2.destroyAllWindows()