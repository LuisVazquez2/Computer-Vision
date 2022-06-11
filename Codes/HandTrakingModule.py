import cv2
import mediapipe as mp
import time


class hand_detector:
    def __init__(
        self, mode=False, maxHands=2, complexity=1, detectionCon=0.5, trackCon=0.5
    ):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode,
            self.maxHands,
            self.complexity,
            self.detectionCon,
            self.trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for Hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, Hand, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, handNo=0, draw=True):
        #for one hand
        # lmlist = list()
        # if self.results.multi_hand_landmarks:
        #     myhand = self.results.multi_hand_landmarks[handNo]
        #     for id, lm in enumerate(myhand.landmark):
        #         h, w, c = img.shape
        #         cx, cy = int(lm.x*w), int(lm.y*h)
        #         lmlist.append([id,cx,cy])
        #         if draw:
        #             cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)
        # return lmlist for one hand

        # for multiple hands
        auxi = list()
        lmlist = [[],[]]
        if self.results.multi_hand_landmarks:
            for Hand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(Hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    auxi.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)

            if auxi[0][1] > auxi[4][1]:
                #print("Left Hand")
                if len(auxi)>20:
                    lmlist[1]=auxi[0:21]
                    lmlist[0]=auxi[21::]
                else:
                    lmlist[1]=auxi[0:21]
            elif auxi[4][1] > auxi[0][1]:
                #print("Right Hand")
                if len(auxi)>20:
                    lmlist[0]=auxi[0:21]
                    lmlist[1]=auxi[21::]
                else:
                    lmlist[0]=auxi[0:21]
        return lmlist


def print_fps(obj, Ptime, img):
    Ctime = time.time()
    fps = 1 / (Ctime - Ptime)
    Ptime = Ctime
    obj.putText(
        img,
        str(f"FPS : {int(fps)}"),
        (10, 30),
        cv2.FONT_HERSHEY_PLAIN,
        3,
        (255, 0, 255),
        3,
    )
    return Ptime


# def main():
#     #code for hand tracking and use in other ptojects
#     cap = cv2.VideoCapture(0)
#     Ptime = 0
#     detector = hand_detector()
#     while True:
#         succes, img = cap.read()
#         Ptime = print_fps(cv2, Ptime, img)
#         img = detector.find_hands(img)
#         lmlist = detector.find_position(img)
#         if lmlist:
#             print(lmlist[4])
#         cv2.imshow('Image', img)
#         cv2.waitKey(1)


# if __name__ == "__main__":
#     main()
