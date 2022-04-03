from ctypes.wintypes import WCHAR
import cv2


import cv2
import numpy as np
import time
import HandTrakingModule as htm

wcam , hcam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
detector = htm.hand_detector()
Ptime = 0
while True:
    succes, img = cap.read()
    img = detector.find_hands(img)
    Ptime = htm.print_fps(cv2, Ptime, img)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
