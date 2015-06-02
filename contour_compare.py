import cv2
import  cPickle



def find_letter(cnt):
    letters = [chr(i) for i in range(65, 90) if i != 74]
    for x in range(10):
        letters.append(str(x))

    minimum = 100
    l = ""
    for letter in letters:
        cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
        temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
        if temp < minimum:
            minimum = temp
            l = letter
    print l,


def contour_compare_using_group(cnt, number_of_fingers, images):

    grp0 = ["0", "E", "S", "M", "N", "O", "P"]
    grp1 = ["0", "1", "A", "B", "C", "D", "E", "I", "G", "M", "N", "O", "P", "S"]
    grp2 = ["2", "6", "9", "A", "B", "C", "D", "G", "H", "K", "L", "M", "P", "Q", "R", "S", "T", "U", "V", "X", "Y"]
    grp3 = ["3", "4", "6", "7", "8", "9", "B", "C", "F", "G", "H", "K", "M", "P", "Q", "U", "W", "X"]
    grp4 = ["4", "5", "P"]
    grp5 = ["5"]
    l = ""
    if number_of_fingers == 0:

        minimum = 1000
        for letter in grp0:
            cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
            temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
            if temp < minimum:
                minimum = temp
                l = letter
        print l


    if number_of_fingers == 1:

        minimum = 100
        for letter in grp1:
            cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
            temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
            if temp < minimum:
                minimum = temp
                l = letter
        print l

    if number_of_fingers == 2:

        minimum = 100

        for letter in grp2:
            cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
            temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
            if temp < minimum:
                minimum = temp
                l = letter
        print l


    if number_of_fingers == 3:

        minimum = 100

        for letter in grp3:
            cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
            temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
            if temp < minimum:
                minimum = temp
                l = letter
        print l


    if number_of_fingers == 4:

        minimum = 100
        for letter in grp4:
            cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
            temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
            if temp < minimum:
                minimum = temp
                l = letter
        print l


    if number_of_fingers == 5:

        minimum = 100
        for letter in grp5:
            cnt1 = cPickle.loads(open("ITSP_database/" + letter+".txt").read())
            temp = cv2.matchShapes(cnt, cnt1, 1, 0.0)
            if temp < minimum:
                minimum = temp
                l = letter
        print l
    cv2.imshow("result", images[l])
