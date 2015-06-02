import cv2
import numpy as np
import time
from math import sqrt
import contour_compare
import load_images


# creates window named result to display result
cv2.namedWindow("result", 500*500)

# dictionary to store images of the letters
images = {}

load_images.load_display_images(images)


def distance(point1, point2):
    return sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

# to find position of fingers in image


def find_fingers(centre, radius, poly_points):
    error_margin = radius*0.25
    finger_points = []
    for i in range(len(poly_points)):
        if distance(centre, poly_points[i][0]) > radius+error_margin:
            finger_points.append(poly_points[i][0])
    return finger_points


def find_largest_contour(contours):
    maxarea = 0
    pos = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxarea:
            maxarea = area
            pos = i
    return pos

# creates video capture object
cap = cv2.VideoCapture(1)
# stores start time of the program
start_time = time.time()

while 1:
    # stores the frame
    _, im = cap.read()
    img = im
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret2, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    blur = cv2.medianBlur(th, 15)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(blur, kernel)

    contours, hierarchy = cv2.findContours(blur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    pos = find_largest_contour(contours)

    contour = cv2.drawContours(im, contours, pos, (0, 0, 255), 3)
    cnt = contours[pos]
    cv2.drawContours(im, cv2.convexHull(cnt, True, True), -1, (255, 0, 0), 3)

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
    pts = pts.reshape((-1, 1, 2))
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
        dis = distance(far, (cx,cy))
        if dis < 1.25*radius:
            validPoints.append(far)
            cv2.circle(im, far, 20, [255, 255, 0], 1)

    cxNew = 0
    cyNew = 0
    for point in validPoints:
        cxNew += point[0]
        cyNew += point[1]

    if len(validPoints) > 0:
        cxNew /= len(validPoints)
        cyNew /= len(validPoints)

    radiusNew = 0
    for point in validPoints:
        radiusNew += distance((cxNew, cyNew), point)
    if len(validPoints):
        radiusNew /= len(validPoints)

    cv2.circle(im, (cxNew, cyNew), int(radiusNew), [255, 255, 255], 1)

    pointOfFingers = find_fingers((cxNew, cyNew), radiusNew, poly)

    numberOfFingers = len(pointOfFingers) - 2

    for point in pointOfFingers:
        cv2.circle(im, tuple(point), 10, [0, 255, 0], -1)

    print numberOfFingers,
    contour_compare.find_letter(cnt)
    # if numberOfFingers >= 0 and numberOfFingers <= 5:
    if numberOfFingers in range(6):
        contour_compare.contour_compare_using_group(cnt, numberOfFingers, images)

    x,  y, w, h = cv2.boundingRect(contours[pos])
    cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("dilate", dilated)
    cv2.imshow("im", im)

    k = cv2.waitKey(5)
    if k == 27:
        break
cv2.destroyAllWindows()

