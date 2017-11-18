import numpy as np
import cv2

#capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture('./Song3.mp4')
FOURCC = cv2.VideoWriter_fourcc(*'XVID')
outfile = cv2.VideoWriter('output.avi', FOURCC, 20.0, (640,480))

while(True):
    ret, frame = capture.read()
    if(ret == None):
        break

    cv2.imshow('webcam', frame)
    outfile.write(frame)
    cv2.waitKey(25)

capture.release()
outfile.release()
cv2.destroyAllWindows()