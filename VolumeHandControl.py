import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import os
import threading

# Camera size
wCam, hCam = 640, 480

# Use Mac webcam
# Using CAP_AVFOUNDATION directly often speeds up initialization and frame grabs on macOS
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)
cap.set(cv2.CAP_PROP_FPS, 60) # Try to force 60 FPS request to camera

pTime = 0
volPer = 0

# Hand detector
detector = htm.handDetector(detectionCon=0.7)

while True:

    success, img = cap.read()
    if not success:
        continue

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        # Thumb tip
        x1, y1 = lmList[4][1], lmList[4][2]

        # Index finger tip
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Distance between fingers
        length = math.hypot(x2 - x1, y2 - y1)

        # Adjusted range for webcam
        volPer = np.interp(length, [30, 200], [0, 100])
        volPer = int(volPer)

        # Use a background thread to call osascript to prevent blocking the camera frame capturing
        def set_mac_volume(v):
            os.system(f"osascript -e 'set volume output volume {v}'")

        if 'last_vol' not in locals() or last_vol != volPer:
            threading.Thread(target=set_mac_volume, args=(volPer,)).start()
            last_vol = volPer

        # Draw circles and line
        cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    # Display volume %
    cv2.putText(img, f'Volume: {volPer} %', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # FPS calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (420, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Volume Control", img)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()