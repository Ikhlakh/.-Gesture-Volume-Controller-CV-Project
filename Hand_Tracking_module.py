import cv2
import mediapipe as mp
import time

# initialization part
class handDetector():
    def __init__(self,mode=False, max_num_hands=2, modelComplex =1,detectioncon=0.5,trackCon=0.5):
        self.mode = mode
        self.max_num_hands = max_num_hands
        self.modelComplex = modelComplex
        self.detectionCon = detectioncon
        self.trackCon = trackCon


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.max_num_hands,self.modelComplex,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

# Detection Part
    def findHands(self,img,draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # extract landmark points details  and connection between points
        # from multiple hands using for loop

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img


    def findPosition(self, img ,handNo=0, draw = False):

        lmList =[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]


            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                # h,w,c = height ,weidhth and channel
                cx, cy = int(lm.x * w), int(lm.y * h)
                # cx , cy = central point
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return lmList


def main():

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        succces, img = cap.read()
        img = detector.findHands(img)
        lmList =detector.findPosition(img)
        if len(lmList) !=0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 2, (255, 80, 0), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()

