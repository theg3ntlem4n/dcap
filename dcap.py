#!/usr/bin/env python3

import cv2
import time
from display import Display
from extractor import FeatureExtractor
import numpy as np
import sys

W = 1920*2//5
H = 1080*2//5

diff = []
high_error = []

disp = Display(W, H*2)

fe = FeatureExtractor()

def percent_error(feats_original, feats_test):
    original_x = feats_original[0]
    original_y = feats_original[1]

    test_x = feats_test[0]
    test_y = feats_test[1]

    temp_x = abs(test_x - original_x)/original_x
    temp_y = abs(test_y - original_y)/original_y

    return (temp_x + temp_y)*100

def process_frame(img_original, img_test, accuracy_range):

    diff_frame = []

    img_original = cv2.resize(img_original, (W, H))
    img_test = cv2.resize(img_test, (W, H))


    feats_original, kps_original, des_original, matches_original = fe.extract(img_original)
    feats_test, kps_test, des_test, matches_test = fe.extract(img_test)

    for p in kps_original:
        u, v = map(lambda x: int(round(x)), p.pt)
        cv2.circle(img_original, (u,v), color = (0,255,0), radius = 3)
    
    for p2 in kps_test:
        a, b = map(lambda y: int(round(y)), p2.pt)
        cv2.circle(img_test, (a, b), color = (0,255,0), radius = 3)

    #check for accuracy

    if len(feats_test) > len(feats_original):
        for x in range(len(feats_original) - 1):
            if abs(feats_original[x][0][0] - feats_test[x][0][0]) < accuracy_range and abs(feats_original[x][0][1] - feats_test[x][0][1]) < accuracy_range: 
                diff.append(percent_error(feats_original[x][0], feats_test[x][0]))
                diff_frame.append(percent_error(feats_original[x][0], feats_test[x][0]))

                
    else:
        for x in range(len(feats_test) - 1):
            if abs(feats_original[x][0][0] - feats_test[x][0][0]) < accuracy_range and abs(feats_original[x][0][1] - feats_test[x][0][1]) < accuracy_range: 
                diff.append(percent_error(feats_original[x][0], feats_test[x][0]))
                diff_frame.append(percent_error(feats_original[x][0], feats_test[x][0]))

    #if np.mean(diff_frame) > 15:
     #   print("shaky")

    #else:
     #   print("accurate")

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

frame = 0

#main function

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        accuracy_range = 50
    else:
        accuracy_range = int(sys.argv[1])

    while cap_original.isOpened() and cap_test.isOpened():
        ret_original, frame_original = cap_original.read()
        ret_test, frame_test = cap_test.read()

        frame += 1

        if ret_original == True and ret_test == True:
            process_frame(frame_original, frame_test, accuracy_range)
        else:
            print(100 - np.mean(diff))
            print(high_error)
            break

 
