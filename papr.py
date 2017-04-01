import cv2

cap = cv2.VideoCapture(1)
contour = []
k_thresh = 150 # adjust for lighting

while(True):
    ret,img = cap.read()
    img = cv2.flip(img,1)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, k_thresh, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(thresh, 50, 200)
    (contours, _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if 0 < len(contours) < 5:
        contour = max(contours, key=len)

    if len(contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        if len(approx) == 4:
            for point in approx:
                cv2.circle(img, (point[0][0], point[0][1]), 5, (0,0,255), 3)

    cv2.imshow('Frame',img)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break

