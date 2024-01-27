import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands = 1)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break