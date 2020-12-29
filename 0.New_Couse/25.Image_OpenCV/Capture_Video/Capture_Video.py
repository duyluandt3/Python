import cv2
import time

# Access and turn on camera
video=cv2.VideoCapture(0)
while True:
    # Create a frame for window camera
    check, frame=video.read()
    time.sleep(3)
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Caturing", gray)
    key=cv2.waitKey(1)

    # press "q" to exit
    if key==ord("q"):
        break
    else:
        pass

video.release()
cv2.destroyAllWindows()