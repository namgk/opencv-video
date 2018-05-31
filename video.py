import cv2
import StringIO
import numpy
import json
import time

cap = cv2.VideoCapture('vid.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print(ret)
        break

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    memfile = StringIO.StringIO()
    numpy.save(memfile, frame)
    memfile.seek(0)
    serialized = json.dumps(memfile.read().decode('latin-1'))
    print(serialized)
    time.sleep(1)


    #cv2.imshow('frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# cap.release()
# cv2.destroyAllWindows()