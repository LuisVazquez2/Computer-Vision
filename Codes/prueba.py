import cv2
import mediapipe as mp
import time

def print_fps(obj,Ptime):
    Ctime = time.time()
    fps = 1/(Ctime - Ptime)
    Ptime = Ctime
    obj.putText(img,str(f"FPS : {int(fps)}"),(10,30),cv2.FONT_HERSHEY_PLAIN,3,(255, 0, 255),3)
    return Ptime
    
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
Ptime = 0.0
while True:
    succes , img = cap.read()
    imgrgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgrgb)
    
    #print(results.multi_hand_landmarks) 
    
    if results.multi_hand_landmarks:
        for Hand in results.multi_hand_landmarks:
            for id,lm in enumerate(Hand.landmark):
                    h,w,c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    if id == 4:
                        cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
                        print("Kevin es gei");
            mpDraw.draw_landmarks(img,Hand,mpHands.HAND_CONNECTIONS)
    Ptime = print_fps(cv2,Ptime)
    cv2.imshow('Image',img)
    cv2.waitKey(1)