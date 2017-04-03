# Papyr: A Paper Trackpad

## Inspiration
We were looking at the Apple Magic TrackPads last week since they seemed pretty cool. But then we saw the price tag, $130! That's crazy! So we set out to create a college student budget friendly "magic" trackpad.

## What it does
Papyr is a trackpad for your computer that is just a single sheet of paper, no wires, strings, or pressure detecting devices attached. Paypr allows you to browse the computer just like any other trackpad and supports clicking and scrolling.

## How we built it
We use a webcam and a whole lot of computer vision to make the magic happen. The webcam first calibrates itself by detecting the four corners of the paper and maps every point on the sheet to a location on the actual screen. Our program then tracks the finger on the sheet by analyzing the video stream in real time, frame by frame, blurring, thresholding, performing canny edge detection, then detecting the contours in the final result. The furthest point in the hand’s contour corresponds to the user's fingertip and is translated into both movement and actions on the computer screen. Clicking is detailed in the next section, with scrolling is activated by double clicking.

## Challenges we ran into
Light sensitivity proved to be very challenging since depending on the environment, the webcam would sometimes have trouble tracking our fingers. However, finding a way to detect clicking was by far the most difficult part of the project. The problem is the webcam has no sense of depth perception: it sees each frame as a 2D image and as a result there is no way to detect if your hand is on or off the paper. We turned to the Internet hoping for some previous work that would guide us in the right direction, but everything we found required either glass panels, infrared sensors, or other non college student budget friendly hardware. We were on our own. We made many attempts including: having the user press down very hard on the paper so that their skin would turn white and detect this change of color, track the shadow the user's finger makes on the paper and detect when the shadow disappears, which occurs when the user places his finger on the paper. None of these methods proved fruitful, so we sat down and for the better part of 5 hours thought about how to solve this issue. Finally, what worked for us was to track the “hand pixel” changes across several frames to detect a valid sequence that can qualify as a “click”. Given the 2D image perception with our web cam, it was no easy task and there was a lot of experimentation that went into this.

## Accomplishments that we're proud of
We are extremely proud of getting clicking to work. It was no easy feat. We also developed our own algorithms for fingertip tracking and click detection and wrote code from scratch. We set out to create a cheap trackpad and we were able to. In the end we transformed a piece of paper, something that is portable and available nearly anywhere, into a makeshift-high tech device with only the help of a standard webcam. Also one of the team members was able to win a ranked game of Hearthstone using a piece of paper so that was cool (not the match shown in the video).

## What we learned
From normalizing the environment's lighting and getting rid of surrounding noise to coming up with the algorithm to provide depth perception to a 2D camera, this project taught us a great deal about computer vision. We also learned about efficiency and scalability since numerous calculations need to be made each second in analyze each frame and everything going on in them.

## What's next for Papyr - A Paper TrackPad
We would like to improve the accuracy and stability of Papyr. This would allow Papyr to function as a very cheap replacement for Wacom digital tablets. Papyr already supports various "pointers" such as fingers or pens.
