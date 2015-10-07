import cv2
import cPickle
import numpy as np


def find_largest_contour(contours):
    maxarea = 0
    pos = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxarea:
            maxarea = area
            pos = i
    return pos


def store_contour_and_poly(img, s):
    _, thresh = cv2.threshold(img, 100, 255, 0)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    pos = find_largest_contour(contours)
    cnt = contours[pos]

    hull1 = cv2.convexHull(cnt, returnPoints=True)
    pts = np.array(hull1, np.int32)
    pts = pts.reshape((-1, 1, 2))
    poly = cv2.approxPolyDP(pts, 20, True)

    filename = "ITSP_database_contour/" + s + ".txt"
    f = open(filename, "w")
    f.write(cPickle.dumps(cnt))
    f.close()

    filename = "ITSP_database_poly/" + s + ".txt"
    f = open(filename, "w")
    f.write(cPickle.dumps(poly))
    f.close()

letters = [chr(i) for i in range(65, 90) if i != 74]
for x in range(10):
    letters.append(str(x))
for l in letters:
    imageName = "ITSP_templates/" + l + ".png"
    print imageName
    image = cv2.imread(imageName, 0)
    store_contour_and_poly(image, l)
