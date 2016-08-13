import numpy as np
import cv2

cap = cv2.VideoCapture('vid.mp4')
fgbg = cv2.BackgroundSubtractorMOG()

fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
#fourcc = int(cap.get(cv2.cv.CV_CAP_PROP_FOURCC))
out = cv2.VideoWriter('output.avi',fourcc, cap.get(cv2.cv.CV_CAP_PROP_FPS), (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))



while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
    	print(ret)
    	break

    out.write(frame)

    # Our operations on the frame come here
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = fgbg.apply(frame)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
