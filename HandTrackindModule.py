import time

import cv2
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, MaxHands = 2,model_complexity=1, detectionCon = 0.5, trackCon = 0.5 ):
        self.mode = mode #we creat an object and it had it's variable it's name self.mode
        self.MaxHands = MaxHands # where I need to use that variable it'll be self.mode
        self.model_complexity= model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.MaxHands,
                                        model_complexity=self.model_complexity,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    # drawSpec1 = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                    # drawSpec2 = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0,draw=True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, chs = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return lmlist


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        if success:
            img = detector.findHands(img)
            lmlist = detector.findPosition(img)

            # if len(lmlist) != 0:
            #     print(lmlist[4])

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()







if __name__ == "__main__":
    main()