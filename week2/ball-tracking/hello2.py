import numpy as np
import cv2

path = "C:/Users/William/Desktop/drone/week1/ball-tracking/ball_tracking_example.mp4"

camera = cv2.VideoCapture(path)

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()