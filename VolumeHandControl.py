import math
import time
from ctypes import cast, POINTER

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackindModule as htm

##############################
wCam, hCam = 640, 480
##############################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0

detector = htm.HandDetector(detectionCon=0.7)

########## pycaw ########################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetVolumeRange()-->range (-95.25, 0.0, 0.75)-->(0,1,2)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxvol = volRange[1]
vol = 0
volBar = 400
volPer = 0
#volume.SetMasterVolumeLevel(0, None)
#########################################

while True:
    success, img = cap.read()
    if success:
        img = detector.findHands(img)
        lmlist = detector.findPosition(img,draw=False)

        if len(lmlist) != 0:
            #print(lmlist[4], lmlist[8])
            x1, y1 = lmlist[4][1], lmlist[4][2]
            x2, y2 = lmlist[8][1], lmlist[8][2]
            cx, cy = (x1+x2)//2 , (y1+y2)//2

            cv2.circle(img, (x1,y1),15,(0,0,255),cv2.FILLED)
            cv2.circle(img, (x2, y2),15,(0, 0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

            length = math.hypot(x2-x1, y2-y1)
            print(length)
            if length < 50:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            #####################################################
            #convert our volume ranges
            # Hand range 50 : 300
            # Volume range -95.25 : 0.0
            vol = np.interp(length,[50,300],[minVol,maxvol])
            volBar = np.interp(length,[50,300],[400,150])
            volPer = np.interp(length,[50,300],[0,100])
            print(int(length), vol)

            volume.SetMasterVolumeLevel(vol, None)
        ## volume Bar ##############################
        # cv2.rectangle(img, (50, 150), (85, 400), (255, 100, 0), 3)
        # cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 100, 0), cv2.FILLED)
        #cv2.putText(img, f' {(int(volPer))}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2,
         #           (255, 100, 0), 2)
        cv2.rectangle(img,(590,150), (555,400),(255,100,0),3)
        cv2.rectangle(img, (590, int(volBar)), (555, 400), (255,100, 0),cv2.FILLED)
        cv2.putText(img, f' {(int(volPer))}%', (540, 450), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 100, 0), 2)
        ##################################################################

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 3)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()