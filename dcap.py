#!/usr/bin/env python3

import cv2
import time
import sys
import numpy as np

#supplementary files
from display import Display
from extractor import FeatureExtractor
from check_accuracy import *
from contour import *

W = 1920*2//5
H = 1080*2//5

disp = Display(W, H*2)

fe = FeatureExtractor()

diff = []

def process_frame(img_original, img_test, accuracy_range):
    
    #contour via opencv built-in contour function

    '''imggray_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    imggray_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)
    
    ret_original, thresh_original = cv2.threshold(imggray_original, 127, 255, 0)
    ret_test, thresh_test = cv2.threshold(imggray_test, 127, 255, 0)

    contours_original, hierarchy_original = cv2.findContours(thresh_original, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours_test, hierarchy_test = cv2.findContours(thresh_test, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    contours_original = bad_contour(contours_original)


    cv2.drawContours(img_original, contours_original, -1, (0, 255, 0), 2)
    cv2.drawContours(img_test, contours_test, -1, (0, 255, 0), 2)'''
    
    #contour through goodFeaturesToTrack

    original_coords = []
    test_coords = []

    img_original = cv2.resize(img_original, (W, H))
    img_test = cv2.resize(img_test, (W, H))

    feats_original, kps_original, des_original, matches_original = fe.extract(img_original)
    feats_test, kps_test, des_test, matches_test = fe.extract(img_test)

    for p in kps_original:
        u, v = map(lambda x: int(round(x)), p.pt)
        original_coords.append([u, v])

    for p2 in kps_test:
        a, b = map(lambda y: int(round(y)), p2.pt)
        test_coords.append([a, b])

    #contour test points

    #original_coords = contour_random(original_coords)
    #test_coords = contour_random(test_coords)

    #draw test points

    for point in original_coords:
        cv2.circle(img_original, (point[0], point[1]), color = (0,255,0), radius = 3)
    
    for point2 in test_coords:
        cv2.circle(img_test, (point2[0], point2[1]), color = (0,255,0), radius = 3)

    #check for accuracy

    diff.extend(check_accuracy(feats_test, feats_original, accuracy_range))

    #display image

    disp.paint(img_test, img_original)

#capture video

cap_original = cv2.VideoCapture("original.mp4")
cap_test = cv2.VideoCapture("test.mp4")

#get duration of videos

fps_original = cap_original.get(cv2.CAP_PROP_FPS)
frame_count_original = int(cap_original.get(cv2.CAP_PROP_FRAME_COUNT))
duration_original = frame_count_original/fps_original

fps_test = cap_test.get(cv2.CAP_PROP_FPS)
frame_count_test = int(cap_test.get(cv2.CAP_PROP_FRAME_COUNT))
duration_test = frame_count_test/fps_test

#variables

frame = 0

original = "original.mp4"
test = "test.mp4"

accuracy_range = 40

#main function

if __name__ == "__main__":
    
    if len(sys.argv) == 4:
        original = sys.argv[3]
        test = sys.argv[2]
        accuracy_range == sys.argv[1]
 
    while cap_original.isOpened() and cap_test.isOpened():
        ret_original, frame_original = cap_original.read()
        ret_test, frame_test = cap_test.read()

        frame += 1

        if ret_original == True and ret_test == True:
            process_frame(frame_original, frame_test, accuracy_range)
        else:
            print(round(100 - np.mean(diff), 2))
            break

 
