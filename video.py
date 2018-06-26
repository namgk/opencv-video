import cv2
import StringIO
import numpy
import json
import time
import base64

cap = cv2.VideoCapture('vid.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print(ret)
        break

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #frameStr = cv2.imencode('.png', frame)[1].tostring().replace("\n","kyng")
    #frameStr = frameStr + '\n'
    retval, frameBuf = cv2.imencode('.png', frame)
    frameStrBase64 = base64.b64encode(frameBuf)
    print frameStrBase64
    #time.sleep(1)
    # break

    # memfile = StringIO.StringIO()
    # numpy.save(memfile, frame)
    # memfile.seek(0)
    # serialized = json.dumps(memfile.read().decode('latin-1'))
    # print(serialized)
    # time.sleep(1)


    #cv2.imshow('frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# cap.release()
# cv2.destroyAllWindows()
