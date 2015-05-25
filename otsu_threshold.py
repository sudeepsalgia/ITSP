import cv2
import numpy as np

cap = cv2.VideoCapture(1)
while 1:
    _, img = cap.read()
    img1 = img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret2, th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dst = cv2.medianBlur(th2, 7)

    contours, hierarchy = cv2.findContours(th2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contour = cv2.drawContours(img1, contours, -1, (0,255,0), 3)

    maxarea = 0
    pos = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxarea:
            maxarea = area
            pos = i
    contour = cv2.drawContours(img1, contours, pos, (0, 0, 255), 3)

    cv2.drawContours(img1, cv2.convexHull(contours[pos], True, False), -1, (255, 0, 0), 3)
    hull = cv2.convexHull(contours[pos], True, True)
    pts = np.array(hull, np.int32)
    pts = pts.reshape((-1,1,2))
    img = cv2.polylines(img1,[pts],True,(255, 0, 0))

    poly = cv2.approxPolyDP(pts, 20, True)
    cv2.drawContours(img1, poly, -1, (0, 0, 0), 3)

    cv2.imshow("img", img1)
    cv2.imshow("th", dst)

    k = cv2.waitKey(5)
    if k == 27:
        break
cv2.destroyAllWindows()


