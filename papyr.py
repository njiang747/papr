import cv2
import numpy as np
import quad
import mouse
import ring_buffer

screen = mouse.screensize()
cap = cv2.VideoCapture(1)
screenCnt = np.array([])
k_thresh = 125 # adjust for lighting

# track when paper has stabilized
counter = 0
counter_thresh = 6
gap_counter = 0
gap_thresh = 3
bg_thresh = None
ppr_quad = None
f_thresh2 = None
k_stable = 0.01
farthest = (0,0)

# ~~Click detection methods and variables~~ #
# Method that takes in 2 points and returns the distance between them
curr_pos = (0,0)
last_pos = (0,0)
num_frames = 3
zero_epsilon = 30
click_epsilon = 70
history = ring_buffer.Ring_Buffer(num_frames)
scrolling = False
scroll_pos = (0,0)

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
                f_thresh2 = np.zeros(thresh.shape, dtype=np.uint8)
                ppr_quad = quad.Quad(map(lambda x: x[0], screenCnt))
                cv2.fillConvexPoly(bg_thresh, ppr_quad.get_points(), 255)
                cv2.polylines(bg_thresh, [ppr_quad.get_points()], True, 0, 5)
            break

    # allow for brief losses in tracking the paper
    gap_counter += 1
    if gap_counter >= gap_thresh:
        counter = 0

    # Draw red circles highlighting the corners
    for point in screenCnt:
        cv2.circle(img, (point[0][0], point[0][1]), 5, (0, 0, 255), 3)
    # Draw green lines outlining the box
    cv2.drawContours(img, [screenCnt], -1, (255, 0, 0), 3)

    if bg_thresh != None:
        thresh2 = cv2.threshold(blurred, k_thresh+10, 255, cv2.THRESH_BINARY)[1]
        f_thresh = cv2.bitwise_xor(thresh2, bg_thresh, mask=bg_thresh)
        dif_val = np.sum(cv2.bitwise_xor(f_thresh, f_thresh2, mask=bg_thresh))/(np.sum(f_thresh)+0.1)
        f_thresh2 = f_thresh
        if scrolling:
            d = scroll_pos[1] - curr_pos[1]
            speed = max(3 * round(abs(d) * 30.0 / screen[1]), 10)
            if d < 0:
                mouse.scrolldown(speed)
            else:
                mouse.scrollup(speed)
        # print dif_val
        if dif_val > k_stable:
            ys, xs = np.where(f_thresh > 0)
            if len(ys) > 0:
                idx = np.argmax(ys)
                farthest = (xs[idx], ys[idx])
                f_x, f_y = ppr_quad.convert(farthest)
                curr_pos = (int(screen[0]*f_x), int(screen[1]*f_y))
                if not scrolling and quad.p2p_dist(curr_pos,last_pos) < click_epsilon:
                    mouse.mousemove(curr_pos[0], curr_pos[1])
                last_pos = curr_pos

                # Check for click
                found_0 = False
                found_0_pos = -1111111
                found_up = False
                for elem in np.roll(history.array, -history.head, axis=0):
                    dist = quad.p2p_dist(elem, curr_pos)
                    if dist < zero_epsilon:
                        if not found_0:
                            found_0 = True
                            found_0_pos = elem
                    if found_0 and dist > click_epsilon:
                        found_up = True
                if found_0 and found_up:
                    cv2.circle(img, farthest, 5, (0, 255, 0), 3)
                    cv2.imwrite('img/img.jpg', img)
                    cv2.imwrite('img/gray.jpg', gray)
                    cv2.imwrite('img/thresh.jpg', thresh)
                    cv2.imwrite('img/edges.jpg', edges)
                    cv2.imwrite('img/bg_thresh.jpg', bg_thresh)
                    cv2.imwrite('img/f_thresh.jpg', f_thresh)
                    print "========== CLICK FOUND =========="
                    history.print_me()
                    print curr_pos
                    if not scrolling:
                        mouse.mousedown(found_0_pos[0],found_0_pos[1])
                        mouse.mouseup(found_0_pos[0],found_0_pos[1])
                    elif scrolling:
                        scrolling = False
                    if not history.fast_click():
                        scrolling = True
                        scroll_pos = curr_pos
                    history.clear()
        # Update history queue
        history.enqueue(curr_pos)
        # draw the fingertip
        cv2.circle(img, farthest, 5, (0, 255, 0), 3)
        cv2.imshow('Frame',img)
    else:
        cv2.imshow('Frame',thresh)

    if cv2.waitKey(1) &0xFF == ord('q'):
        break
