import cv2
import cPickle


def find_closest_match(grp, poly, cnt):
    minimum = 1000
    l = '00'
    cmp_poly = find_best_5(grp, cnt)
    cmp_poly = find_best_3(cmp_poly, poly)
    cmp_poly = find_best_2(cmp_poly, cnt)
    for letter in cmp_poly.items():
        poly1 = cPickle.loads(open("ITSP_database_poly/" + str(letter[1])+".txt").read())
        temp = cv2.matchShapes(poly, poly1, 1, 0.0)
        if temp < minimum:
            l = letter[1]
            minimum = temp
    return l


def find_best_5(grp, cnt):
    cmp_poly = {1000: '00', 999: '00', 1001: '00', 1002: '00', 1003: '00'}
    for letter in grp:
        cnt1 = cPickle.loads(open("ITSP_database_contour/" + letter+".txt").read())
        temp1 = cv2.matchShapes(cnt, cnt1, 1, 0.0)
        max_index = max(cmp_poly)
        if temp1 < max_index:
            cmp_poly.pop(max_index)
            cmp_poly.update({temp1: letter})
    return cmp_poly


def find_best_3(dict, poly):
    keys = dict.keys()
    cmp_poly = {1000: '00', 999: '00', 1001: '00'}
    for key in keys:
        poly1 = cPickle.loads(open("ITSP_database_poly/" + dict[key] + ".txt").read())
        temp1 = cv2.matchShapes(poly, poly1, 1, 0.0)
        max_index = max(cmp_poly)
        if temp1 < max_index:
            cmp_poly.pop(max_index)
            cmp_poly.update({temp1: dict[key]})
    return cmp_poly


def find_best_2(dict, cnt):
    keys = dict.keys()
    cmp_poly = {1000: '00', 999: '00'}
    for key in keys:
        cnt1 = cPickle.loads(open("ITSP_database_contour/" + dict[key] + ".txt").read())
        temp1 = cv2.matchShapes(cnt, cnt1, 1, 0.0)
        max_index = max(cmp_poly)
        if temp1 < max_index:
            cmp_poly.pop(max_index)
            cmp_poly.update({temp1: dict[key]})
    return cmp_poly




def contour_compare_using_group(poly, cnt, number_of_fingers):

    grp0 = ["M", "N", "O", "Q", "S"]
    grp1 = ["A", "D", "E", "I", "G", "M", "N", "O", "P", "Q", "S", "T", "U", "V", "X"]
    grp2 = ["A", "B", "E", "D", "G", "H", "I", "K", "L", "M", "N", "P", "R", "T", "U", "V", "X", "Y"]
    grp3 = ["B", "C", "F", "H", "K", "R",   "W"]
    grp4 = ["C", "4"]
    grp5 = ["5"]
    l = "00"
    if number_of_fingers == 0:
        l = find_closest_match(grp0, poly, cnt)

    elif number_of_fingers == 1:
        l = find_closest_match(grp1, poly, cnt)

    elif number_of_fingers == 2:
        l = find_closest_match(grp2, poly, cnt)

    elif number_of_fingers == 3:
        l = find_closest_match(grp3, poly, cnt)

    elif number_of_fingers == 4:
        l = find_closest_match(grp4, poly, cnt)

    elif number_of_fingers == 5:
        l = find_closest_match(grp5, poly, cnt)

    return l


