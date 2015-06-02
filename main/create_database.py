import cv2
import cPickle


def find_largest_contour(contours):
    maxarea = 0
    pos = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxarea:
            maxarea = area
            pos = i
    return pos

def store_contour(img, s):
    _, thresh = cv2.threshold(img, 100, 255, 0)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    pos = find_largest_contour(contours)
    cnt = contours[pos]

    filename = "ITSP_database/" + s + ".txt"
    f = open(filename, "w")
    f.write(cPickle.dumps(cnt))
    f.close()

letters = [chr(i) for i in range(65, 90) if i != 74]
for x in range(10):
    letters.append(str(x))
for l in letters:
    imageName = "ITSP_templates3/" + l + ".png"
    print imageName
    image = cv2.imread(imageName, 0)
    store_contour(image, l)
