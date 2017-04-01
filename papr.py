import cv2
import numpy as np
import quad

cap = cv2.VideoCapture(0)
screenCnt = np.array([])
k_thresh = 140 # adjust for lighting

# track when paper has stabilized
counter = 0
counter_thresh = 6
gap_counter = 0
gap_thresh = 3
bg_thresh = None
ppr_quad = None

while(True):
    ret,img = cap.read()
    img = cv2.flip(img,1)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, k_thresh, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(thresh, 50, 200)
    (contours, _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our paper
        if len(approx) == 4 and peri > 1500 and area > 50000:
            counter += 1
            gap_counter = 0
            if counter >= counter_thresh:
                counter = 0
                screenCnt = approx
                bg_thresh = np.zeros(thresh.shape, dtype=np.uint8)
                ppr_quad = quad.Quad(map(lambda x: x[0], screenCnt))
                cv2.fillConvexPoly(bg_thresh, ppr_quad.get_points(), 255)
            break

    gap_counter += 1
    if gap_counter >= gap_thresh:
        counter = 0

    # Draw red circles highlighting the corners
    for point in screenCnt:
        cv2.circle(img, (point[0][0], point[0][1]), 5, (0, 0, 255), 3)
    # Draw green lines outlining the box
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)


    if bg_thresh != None:
        # cv2.imshow('Frame', bg_thresh)
        img = cv2.bitwise_and(img, img, mask=bg_thresh)
        cv2.imshow('Frame',img)
    else:
        cv2.imshow('Frame',img)

    if cv2.waitKey(1) &0xFF == ord('q'):
        break
