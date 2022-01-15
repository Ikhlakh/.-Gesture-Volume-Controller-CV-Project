import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime =0
cTime =0


while True:
    succces, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    # extract landmark points details  and connection between points
    # from multiple hands using for loop

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h ,w , c = img.shape
                # h,w,c = height ,weidhth and channel
                cx, cy = int(lm.x*w), int(lm.y*h)
                # cx , cy = central point
                print(id,cx,cy)
                cv2.circle(img,(cx, cy) ,10 ,(255,0 ,255),cv2.FILLED)

            mpDraw.draw_landmarks(img,handLms ,mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_ITALIC,2,(255,80,0),3)


    cv2.imshow("Image" , img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
