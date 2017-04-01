import numpy as np
import cv2
import math

cap = cv2.VideoCapture(1)

while(True):
    ret,img = cap.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]


    cv2.imshow('Frame',img)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break

