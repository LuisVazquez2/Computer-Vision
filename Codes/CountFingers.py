import cv2
import HandTrakingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
Ptime = 0
detector = htm.hand_detector(detectionCon=0.75)
finger_ids = [4,8,12,16,20]
while True:
    succes , img = cap.read()
    Ptime = htm.print_fps(cv2,Ptime,img)
    img = detector.find_hands(img)
    lmlist = detector.find_position(img,draw=False)
    if lmlist:
        fingers_right , fingers_left = list(), list()
        #print(lmlist)
        # 0 -> right hand
        # 1 -> left hand
        t_lmlist = list()
        if len(lmlist[0])>0:
            t_lmlist = lmlist[0]
            #Check if the hand is open
            for id in finger_ids:
                if id == 4: #Special case for thumb
                    if t_lmlist[id][1] > t_lmlist[id-1][1]:
                        fingers_right.append(1)
                    else:
                        fingers_right.append(0)
                else:
                    if t_lmlist[id][2] < t_lmlist[id-2][2]:
                        fingers_right.append(1)
                    else:
                        fingers_right.append(0)
        if lmlist[1]:
            t_lmlist = lmlist[1]
            for id in finger_ids:
                if id == 4: #Special case for thumb
                    if t_lmlist[id][1] < t_lmlist[id-1][1]:
                        fingers_right.append(1)
                    else:
                        fingers_right.append(0)
                else:
                    if t_lmlist[id][2] < t_lmlist[id-2][2]:
                        fingers_right.append(1)
                    else:
                        fingers_right.append(0)
        # print(fingers)
        totalfingers = (fingers_right.count(1) + fingers_left.count(1))
        cv2.rectangle(img,(20,150),(150,300),(0,0,255),cv2.FILLED)
        cv2.putText(img,str(totalfingers),(80,220),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)