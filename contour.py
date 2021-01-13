import random
import cv2

def contour(feats):

    temp = []
    temp_temp = []
    sorted(feats, key=lambda k: [k[1], k[0]])

    for x in range(1, len(feats)):
        if feats[x][1] == feats[x-1][1]:
            temp_temp.append(feats[x-1])
        else:
            temp_temp.append(feats[x-1])
            temp.append(temp_temp[0])
            temp.append(temp_temp[len(temp_temp)- 1])
            temp_temp = []
            temp_temp.append

    return temp

def bad_contour(contours):
    temp = []

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015*peri, True)

        if not len(approx) == 2:
            temp.append(c)

    return temp


    
    
