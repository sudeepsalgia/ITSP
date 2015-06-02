import cv2
import numpy as np
import time
from math import sqrt
import contour_compare
import load_images

cv2.namedWindow("result", 500*500)
images = {}
print "loading images"
load_images.load_display_images(images)
print "images loaded"


def distance(point1, point2):
    return sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)


def thresh_det(x1, y1, x2, y2, img):
    averageB = 0
    averageG = 0
    averageR = 0
    sumB = 0
    sumG = 0
    sumR = 0
    for i in range(x1, x2):
        for j in range(y1, y2):
            sumB += img[i, j, 0]
            sumG += img[i, j, 1]
            sumR += img[i, j, 2]
    averageB = sumB/400
    averageG = sumG/400
    averageR = sumR/400
    varB, varG, varR = 0, 0,  0
    for i in range(x1, x2):
        for j in range(y1, y2):
            varB += (averageB - img[i,j,0])**2
            varG += (averageG - img[i,j,1])**2
            varR += (averageR - img[i,j,2])**2
    sdB = int(sqrt(varB/400))
    sdG = int(sqrt(varG/400))
    sdR = int(sqrt(varR/400))
    factor = 1
    lowerb = np.array([averageB-sdB*factor, averageG-sdG*factor, averageR-sdR*factor])
    upperb = np.array([averageB+sdB*factor, averageG+sdG*factor, averageR+sdR*factor])
    return [cv2.inRange(img,lowerb,upperb), averageB, averageG, averageR, [sdB, sdG, sdR]]


def my_thresh(img, res, error):
    factor = 1
    lowerb = np.array([res[0]-error[0]*factor, res[1]-error[1]*factor, res[2]-error[2]*factor])
    upperb = np.array([res[0]+error[0]*factor, res[1]+error[1]*factor, res[2]+error[2]*factor])
    return cv2.inRange(img, lowerb, upperb)


def distance(point1, point2):
    return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def find_fingers(centre, radius, poly_points):
    error_margin = radius*0.25
    finger_points = []
    for i in range(len(poly_points)):
        if distance(centre, poly_points[i][0]) > radius+error_margin:
            finger_points.append(poly_points[i][0])
    return finger_points

cap = cv2.VideoCapture(1)
start_time = time.time()
frequency_of_finger = [0, 0, 0, 0, 0, 0]

while 1:
    _, im = cap.read()
    img = im
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret2, th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dst = cv2.medianBlur(th2, 7)
    blur = cv2.medianBlur(th2, 15)
    blur_copy = blur.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(blur, kernel)

    contours, hierarchy = cv2.findContours(blur.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    maxarea = 0
    pos = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxarea:
            maxarea = area
            pos = i

    contour = cv2.drawContours(im, contours, pos, (0, 0, 255), 3)
    cnt = contours[pos]
    cv2.drawContours(im, cv2.convexHull(cnt, True, True), -1, (255, 0, 0), 3)

    # x,  y, w, h = cv2.boundingRect(contours[pos])
    # cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)

    hull = cv2.convexHull(cnt, returnPoints=False)
    hull1 = cv2.convexHull(cnt, returnPoints=True)

    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    radius = 0
    for i in range(len(cnt)):
        radius += distance((cx, cy), cnt[i][0])

    radius /= len(cnt)

    pts = np.array(hull1, np.int32)
    pts = pts.reshape((-1,1,2))
    img = cv2.polylines(im, [pts], True, (255, 0, 0))
    poly = cv2.approxPolyDP(pts, 20, True)

    for i in range(len(poly)):
        cv2.circle(im, tuple(poly[i][0]), 10, [255, 0, 255], 1)
        cv2.line(im, (cx, cy), tuple(poly[i][0]), [0,0,0], 2 )

    cv2.drawContours(im, poly, -1, (0, 0, 0), 3)

    validPoints = []
    defects = cv2.convexityDefects(cnt, hull)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        far = tuple(cnt[f][0])
        # cv2.circle(im, far, 20, [255, 255, 0], 1)
        dis = distance(far, (cx,cy))
        if dis < 1.25*radius:
            validPoints.append(far)
            cv2.circle(im, far, 20, [255, 255, 0], 1)

    cxNew = 0
    cyNew = 0
    for point in validPoints:
        cxNew += point[0]
        cyNew += point[1]

    if len(validPoints)>0:
        cxNew /= len(validPoints)
        cyNew /= len(validPoints)

    radiusNew = 0
    for point in validPoints:
        radiusNew += distance((cxNew, cyNew), point)
    if len(validPoints):
        radiusNew /= len(validPoints)

    # cv2.circle(im, (cx, cy), int(radiusNew), [255, 255, 255], 1)
    cv2.circle(im, (cxNew, cyNew), int(radiusNew), [255, 255, 255], 1)

    pointOfFingers = find_fingers((cxNew, cyNew), radiusNew, poly)

    numberOfFingers = len(pointOfFingers)
    if time.time() - start_time > 1.5:
        maximum = max(frequency_of_finger)
        l = [i for i, j in enumerate(frequency_of_finger) if j == maximum]
        frequency_of_finger = [0, 0, 0, 0, 0, 0]
        start_time = time.time()
    else:
        if numberOfFingers - 2 >= 0 and numberOfFingers <= 7:
            frequency_of_finger[numberOfFingers - 2] += 1

    for point in pointOfFingers:
        cv2.circle(im, tuple(point), 10, [0, 255, 0], -1)


    print numberOfFingers,
    contour_compare.find_letter(cnt)
    contour_compare.contour_compare_using_group(cnt, numberOfFingers-2, images)

    x,  y, w, h = cv2.boundingRect(contours[pos])
    cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("dilate", dilated)
    cv2.imshow("im", im)

    k = cv2.waitKey(5)
    if k == 27:
        break
cv2.destroyAllWindows()

