import numpy as np
import cv2
import math
import image_analysis
from hand_detection import HandDetection
from draw_frame import DrawFrame

cap = cv2.VideoCapture(0)
hd = HandDetection()
df = DrawFrame()

while(True):
    ret,img = cap.read()
    img = cv2.flip(img,1)

    hd.draw_hand_rect(img)
    if cv2.waitKey(1) &0xFF == ord('v'):
        if(not hd.trained_hand):
            hd.train_hand(img)
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #
    # gray = np.float32(gray)
    # dst = cv2.cornerHarris(gray,2,3,0.04)
    #
    # # Threshold for an optimal value, it may vary depending on the image.
    # img[dst>0.01*dst.max()]=[0,0,255]
    if(hd.trained_hand):
        img = df.draw_final(img, hd)
    cv2.imshow('Frame',img)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break

