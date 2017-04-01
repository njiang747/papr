import cv2

import numpy as np
import cv2
import math

while(True):
    ret,frame = cap.read()

    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break

