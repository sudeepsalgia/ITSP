import cv2
import numpy as np
import time
from math import sqrt


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
    return [cv2.inRange(img, lowerb, upperb), averageB, averageG, averageR, [sdB, sdG, sdR]]


def my_thresh(img, res, error):
    factor = 1
    lowerb = np.array([res[0]-error[0]*factor, res[1]-error[1]*factor, res[2]-error[2]*factor])
    upperb = np.array([res[0]+error[0]*factor, res[1]+error[1]*factor, res[2]+error[2]*factor])
    return cv2.inRange(img, lowerb, upperb)