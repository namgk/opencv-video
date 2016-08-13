#!/usr/bin/env python

from StringIO import StringIO

from PIL import Image

import cv2
import numpy as np
import math

def list_camera_ids():
  return ['0', '1']

class Camera(object):

  def __init__(self, camera_id, size, fps):
    self.width = size[0]
    self.height = size[1]
    self.count = 0
    self.last_state = 0
    self.cap = cv2.VideoCapture('vid.mp4')
    self.fgbg = cv2.BackgroundSubtractorMOG()
    self.fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
    #fourcc = int(self.cap.get(cv2.cv.CV_CAP_PROP_FOURCC))
    self.out = cv2.VideoWriter('output.avi',self.fourcc, self.cap.get(cv2.cv.CV_CAP_PROP_FPS), (int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))



  def get_frame(self):
    ret, img = self.cap.read()
    image1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    image2 = self.fgbg.apply(image1)

    x, y, w, h = rf_overlay(img)
    ref = image2[y:y+h, x:x+w]
    white = cv2.countNonZero(ref)

    if white > 0 and self.last_state == 0:
      self.count += 1
      self.last_state = 1

    if white == 0 and self.last_state == 1:
      self.last_state = 0

    cv2.putText(img, str(self.count), (x-5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    
    ret, image2 = cv2.imencode('.jpg', img)

    if self.count < 3:
      self.out.write(image2)
    else:
      self.out.release()

    image2 = Image.fromarray(image2)
    #image = Image.new('RGB', (self.width, self.height), 'black')
    # buf = StringIO()
    # image.save(buf, 'JPEG')
    return image2.tobytes()

def rf_overlay(image):
  height, width = image.shape[:2]
  x1 = int(width*0.3)
  y1 = int(height*0.8)
  rf_width = int(width*0.15)
  rf_height = int(height*0.1)

  cv2.rectangle(image,
    (x1,y1),
    (x1+rf_width, y1+rf_height ),
    (0,255,0),2)
  return (x1, y1, rf_width, rf_height)


