#!/usr/bin/env python3

import cv2
import time
from display import Display
from extractor import FeatureExtractor
import numpy as np
import sys
from check_accuracy import *

W = 1920*2//5
H = 1080*2//5

disp = Display(W, H*2)

fe = FeatureExtractor()

diff = []

def process_frame(img_original, img_test, accuracy_range):

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

 
