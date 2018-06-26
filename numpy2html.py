import cv2
import StringIO
import numpy
import json
import sys
import os
import csv
import base64

labels = list()

with open('./imgstr', 'rb') as imgStrFile:

    # nparr = numpy.fromstring(imgStrFile.read().replace("kyng", "\n"), numpy.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    imgStr = base64.encodestring(imgStrFile.read().replace("kyng", "\n"))
    print imgStr

    # cv2.imwrite('test2.png', img, [int(cv2.IMWRITE_PNG_COMPRESSION), 4])
