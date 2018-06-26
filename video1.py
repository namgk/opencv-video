import cv2
import StringIO
import numpy
import json
import sys
import base64

mog = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=36, detectShadows=True);

while True:
    line = sys.stdin.readline()
    
    if len(line) < 2:
        continue

    #line = line.strip().replace("kyng", "\n")
    #nparr = numpy.fromstring(line, numpy.uint8)
    #frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    frameStr = base64.b64decode(line)

    frameNp = numpy.frombuffer(frameStr, dtype=numpy.uint8); 
    frame = cv2.imdecode(frameNp, flags=1)

    fg = mog.apply(frame);
    bg = mog.getBackgroundImage();

    fgthres = cv2.threshold(fg.copy(), 127, 255, cv2.THRESH_BINARY)[1];
    fgEroded = cv2.erode(fgthres.copy(), kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2)), iterations=1);
    fgDilated = cv2.dilate(fgEroded.copy(), kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)), iterations = 2);
    
    im2, contours, hierarchy = cv2.findContours(fgDilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #print len(contours)

    #continue

    carContours = []
    if len(contours) > 0:
        for c in contours:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            xx,yy,w,h = cv2.boundingRect(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            area = cv2.contourArea(c)
            if area > 900:
                carContours.append(c)
                cv2.rectangle(frame,(xx,yy),(xx+w,yy+h),(0,255,0),2)
                
                car = frame[yy:yy+h,xx:xx+w]
                # classify car and write text result back to frame

                retval, frameBuf = cv2.imencode('.png', car)
                frameStrBase64 = base64.b64encode(frameBuf)
                print frameStrBase64
                continue

                memfile2 = StringIO.StringIO()
                numpy.save(memfile2, car)
                memfile2.seek(0)
                serialized = json.dumps(memfile2.read().decode('latin-1'))
                print(serialized)
                
    # memfile2 = StringIO.StringIO()
    # numpy.save(memfile2, fgDilated)
    # memfile2.seek(0)
    # serialized = json.dumps(memfile2.read().decode('latin-1'))
    # print(serialized)

    # cv2.imshow('fg',frame)
    #cv2.imshow('bg',bgmodel)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break



