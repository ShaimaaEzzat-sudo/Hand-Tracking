import os
import time
from gtts import gTTS
import cv2

import HandTrackindModule as htm

##############################
wCam, hCam = 640, 480
##############################
def magic(numList): # [1,2,3]
    s = map(str, numList) # ['1','2','3']
    s = ''.join(s) # '123'
    s = int(s) # 123
    return s

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
folderPath = "Fingerphotos"
mylist = os.listdir(folderPath) #my image list
#print(mylist)
overlayList = []
for impath in mylist: # loop throw mylist
    image = cv2.imread(f'{folderPath}//{impath}')
    image = cv2.resize(image,(200,200))
    #print(f'{folderPath}//{impath}')
    overlayList.append(image)
#print(len(overlayList))
print(overlayList[0].shape)
#,w,ch = overlayList[0].shape

pTime = 0
totalFingersList = []
detector = htm.HandDetector(detectionCon=0.7)

tipIds = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    if success:
        #img[0:h, 0:w] = overlayList[0]
        img = detector.findHands(img)
        lmlist = detector.findPosition(img, draw=False)

        #img[0:h,0:w] = overlayList[0]
        if len(lmlist) != 0:
            fingers = []

            #thumb
            if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            #4fingers
            for id in range(1, len(tipIds)):
                if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            #print(fingers)
            totalFingers = fingers.count(1)
            totalFingersList.append(totalFingers)
            print(totalFingersList)
            #voiceList = ['']

            #print(totalFingers)
            h, w, ch = overlayList[totalFingers-1].shape
            img[0:h, 0:w] = overlayList[totalFingers-1]#index of array -1 is last element
            ###########

            # tts = gTTS(str(totalFingers), lang='en')
            # voiceList.append(tts)
            # print(voiceList)
            # tts.save('fingerCountVoice.mp3')
            ############
            cv2.rectangle(img, (20,225),(170,425),(0,255,0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (45,375),cv2.FONT_HERSHEY_PLAIN,
                        10,(255, 0, 0),25)

        # voiceList = []
        # voiceList.append(totalFingers)
        # voiceRecord = []
        #for item in totalFingersList:
        print(totalFingersList)
        # voice = magic(totalFingersList)
        # tts = gTTS(voice, lang='en')
        # #totalFingersList.append(tts)
        # tts.save('fingerCountVoice.mp3')

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {(int(fps))}', (480, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()