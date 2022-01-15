import cv2
import numpy as np
import time
import Hand_Tracking_module as htm
import math

# below methods is from pycow library
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################
wCam, hCam = 720, 1080
###############

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

myDetector = htm.handDetector()

# here
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
volRange = volume.GetVolumeRange()
print(volRange)

minVol = volRange[0]
maxVol = volRange[1]
vol= 0
volBar = 400
volPer = 0



while True:
    success, img = cap.read()
    img = myDetector.findHands(img)
    lmList =myDetector.findPosition(img ,draw=False )
    # print(lmList)
    if len (lmList) != 0:
        # print(lmList[4] , lmList[8])

        x1, y1 = lmList[4][1] ,lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx ,cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img , (x1, y1) ,15 , (0,255,0) ,cv2.FILLED)
        cv2.circle(img , (x2, y2) ,15 , (0,255,0) ,cv2.FILLED)
        cv2.line(img,(x1,y1), (x2, y2),(0,120,255),3)
        cv2.circle(img, (cx , cy) , 12 , (0,255,0), cv2.FILLED)


        lenth = math.hypot(x2-x1 , y2-y1)
        print(lenth)
        # Hand-Range 40-250
        # Volume Range  -96-0

        # convert volume range into hand range as following
        vol = np.interp(lenth,[20,150],[minVol,maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        # convert volume Bar range into hand range as following
        volBar = np.interp(lenth,[40,250],[400,150])
        # convert volume Hand range into Percentage as following
        volPer = np.interp(lenth, [40, 250], [0, 100])




        if lenth<40:
            cv2.circle(img , (cx , cy) , 15 ,(0,0,255), cv2.FILLED)

    # Volume Bar Decoration
    cv2.rectangle(img, (50,150), (85,400), (255,255,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (240, 120, 240), cv2.FILLED)
    cv2.putText(img,  (f'{int(volPer)} %'), (30, 450), cv2.FONT_HERSHEY_COMPLEX, 1.5,
                (255, 0, 0), 3)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 60), cv2.FONT_HERSHEY_COMPLEX, 2,
                (255, 0, 0), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1)
