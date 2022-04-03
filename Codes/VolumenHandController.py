import math
import cv2
import numpy as np
import HandTrakingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam , hcam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
detector = htm.hand_detector()
Ptime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumen_range = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)
minvolumen = volumen_range[0]
maxvolumen = volumen_range[1]
vol = 0
volBar = 400
volPer = 0
while True:
    succes, img = cap.read()
    img = detector.find_hands(img)
    Ptime = htm.print_fps(cv2, Ptime, img)
    lmlist = detector.find_position(img,draw=False)
    if lmlist:
        #print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        center_x,center_y = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(0,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(128,255,0),2)
        cv2.circle(img,(center_x,center_y),10,(0,0,255),cv2.FILLED)
        lengt = math.hypot(x2-x1, y2-y1)
        #print(lengt)
        #Hand range 50 - 300
        vol = np.interp(lengt,[50,300],[minvolumen,maxvolumen])
        volBar = np.interp(lengt,[50,300],[400,150])
        volPer = np.interp(lengt,[50,300],[0,100])  
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img, str(f"{int(volPer)} %"), (40, 450),
                cv2.FONT_HERSHEY_PLAIN, 3, (51, 255, 255), 3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
