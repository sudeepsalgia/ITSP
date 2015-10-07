import cv2
import cPickle


def find_closest_match(grp, cnt):
    minimum = 1000
    for letter in grp:
        cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
        temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
        if temp < minimum:
            minimum = temp
            l = letter
    #print l,
    return l


def contour_compare_using_group(cnt, number_of_fingers, images):

    grp0 = ["0", "E", "S", "M", "N", "O", "P"]
    grp1 = ["0", "1", "A", "B", "C", "D", "E", "I", "G", "M", "N", "O", "P", "S"]
    grp2 = ["2", "6", "9", "A", "B", "C", "D", "G", "H", "K", "L", "M", "P", "Q", "R", "S", "T", "U", "V", "X", "Y"]
    grp3 = ["3", "6", "7", "8", "9", "B", "C", "F", "G", "H", "K", "M", "P", "Q", "U", "W", "X"]
    grp4 = ["4", "5", "P", "W"]
    grp5 = ["5"]
    l = ""
    if number_of_fingers == 0:
        l = find_closest_match(grp0, cnt)

    elif number_of_fingers == 1:
        l = find_closest_match(grp1, cnt)

    elif number_of_fingers == 2:
        l = find_closest_match(grp2, cnt)

    elif number_of_fingers == 3:
        l = find_closest_match(grp3, cnt)

    elif number_of_fingers == 4:
        l = find_closest_match(grp4, cnt)

    elif number_of_fingers == 5:
        l = find_closest_match(grp5, cnt)

    cv2.imshow("result", images[l])
