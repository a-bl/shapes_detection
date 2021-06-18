# Import necessary libraries
import numpy as np
import cv2


def nothing(*arg):
    pass

# Loading video from disk
video = cv2.VideoCapture('C:/Users/Lenovo/Projects/test_tasks/Internship2021testtask.mp4')
# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (frame_width, frame_height)
cv2.namedWindow('VIDEO', cv2.WINDOW_NORMAL)
cv2.resizeWindow('VIDEO', frame_width, frame_height)
cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Mask', frame_width, frame_height)
# Below VideoWriter object will create
# a frame of above defined. The output
# is stored in 'output.avi' file.
result = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
# Creating TrackBar for catching the color of shapes
# cv2.namedWindow('TrackBar')
# cv2.resizeWindow('TrackBar', 600, 300)
#
# cv2.createTrackbar('hue_min', 'TrackBar', 0, 179, nothing)
# cv2.createTrackbar('hue_max', 'TrackBar', 179, 179, nothing)
# cv2.createTrackbar('sat_min', 'TrackBar', 0, 255, nothing)
# cv2.createTrackbar('sat_max', 'TrackBar', 255, 255, nothing)
# cv2.createTrackbar('val_min', 'TrackBar', 0, 255, nothing)
# cv2.createTrackbar('val_max', 'TrackBar', 255, 255, nothing)

while True:
    ret, img = video.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hue_min = cv2.getTrackbarPos('hue_min', 'TrackBar')
    # hue_max = cv2.getTrackbarPos('hue_max', 'TrackBar')
    # sat_min = cv2.getTrackbarPos('sat_min', 'TrackBar')
    # sat_max = cv2.getTrackbarPos('sat_max', 'TrackBar')
    # val_min = cv2.getTrackbarPos('val_min', 'TrackBar')
    # val_max = cv2.getTrackbarPos('val_max', 'TrackBar')
    #
    # lower = np.array([hue_min, sat_min, val_min])
    # upper = np.array([hue_max, sat_max, val_max])
    # Setting fixed parameters for catching color of shapes
    lower = np.array([30, 30, 60])
    upper = np.array([90, 90, 230])
    mask = cv2.inRange(hsv, lower, upper)

    # Finding contours
    cnts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 300:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)

            # Drawing the contours and the name of the shape on the image
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, 'Points:' + str(len(approx)), (x+w//2+10, y-40), cv2.FONT_HERSHEY_COMPLEX,
                        0.7, (0, 255, 0), 2)
            if len(approx) == 4:
                cv2.putText(img, 'Rectangle', (x+w//2+10, y-10), cv2.FONT_HERSHEY_COMPLEX,
                            0.7, (50, 150, 250), 2)
            elif len(approx) == 3:
                cv2.putText(img, 'Triangle', (x+w//2+10, y-10), cv2.FONT_HERSHEY_COMPLEX,
                            0.7, (250, 150, 50), 2)
            else:
                cv2.putText(img, 'Circle', (x+w//2+10, y-10), cv2.FONT_HERSHEY_COMPLEX,
                            0.7, (250, 50, 150), 2)
    result.write(img)
    cv2.imshow('VIDEO', img)
    # cv2.imshow('hsv', hsv)
    cv2.imshow('Mask', mask)

    k = cv2.waitKey(5)
    if k == ord('q'):
        break
    if k == ord('p'):
        cv2.waitKey(-1)

# Showing output
video.release()
result.release()
cv2.destroyAllWindows()
