import cv2
import StringIO
import numpy
import json

cap = cv2.VideoCapture('vid.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print(ret)
        break

    memfile = StringIO.StringIO()
    numpy.save(memfile, frame)
    memfile.seek(0)
    serialized = json.dumps(memfile.read().decode('latin-1'))
    print(serialized)

    #cv2.imshow('frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# cap.release()
# cv2.destroyAllWindows()