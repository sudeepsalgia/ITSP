import cv2
import numpy as np
from  math import sqrt


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

while 1:
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 50, 150)

    contours, hierarchy = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contour = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    maxarea = 0
    pos = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxarea:
            maxarea = area
            pos = i

    contour = cv2.drawContours(image, contours, pos, (0, 0, 255), 3)

    cnt = contours[pos]
    cv2.drawContours(image, cv2.convexHull(cnt, True, True), -1, (255, 0, 0), 3)

    x,  y, w, h = cv2.boundingRect(contours[pos])
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

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
    img = cv2.polylines(image, [pts], True, (255, 0, 0))
    poly = cv2.approxPolyDP(pts, 20, True)

    for i in range(len(poly)):
        cv2.circle(image, tuple(poly[i][0]), 10, [255, 0, 255], 1)
        cv2.line(image, (cx, cy), tuple(poly[i][0]), [0,0,0], 2 )

    cv2.drawContours(image, poly, -1, (0, 0, 0), 3)


    defects = cv2.convexityDefects(cnt, hull)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        far = tuple(cnt[f][0])
        cv2.circle(image, far, 20, [255, 255, 0], 1)




    cv2.circle(image, (cx, cy), int(radius), [0, 0, 0], 1)

    pointOfFingers = find_fingers((cx, cy), radius, poly)

    numberOfCircles = len(pointOfFingers)
    print numberOfCircles
    for point in pointOfFingers:
        cv2.circle(image, tuple(point), 10, [0, 255, 0], -1)


    cv2.imshow("Image", image)
    cv2.imshow("Edged", edged)

    k = cv2.waitKey(5)
    if k == 27:
        break
cv2.destroyAllWindows()