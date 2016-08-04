#!/usr/bin/env python

from StringIO import StringIO

from PIL import Image

import cv2
import numpy as np
import math

cap = cv2.VideoCapture('vid.mp4')
fgbg = cv2.BackgroundSubtractorMOG()

def list_camera_ids():
  return ['0', '1']

class Camera(object):

  def __init__(self, camera_id, size, fps):
    self.width = size[0]
    self.height = size[1]
    self.count = 0
    self.last_state = 0

  def get_frame(self):
    ret, img = cap.read()
    image = img
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    image = fgbg.apply(image)

    x, y, w, h = rf_overlay(img)
    ref = image[y:y+h, x:x+w]
    white = cv2.countNonZero(ref)

    if white > 0 and self.last_state == 0:
      self.count += 1
      self.last_state = 1

    if white == 0 and self.last_state == 1:
      self.last_state = 0

    cv2.putText(img, str(self.count), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    ret, img = cv2.imencode('.jpg', img)
    img = Image.fromarray(img)
    #image = Image.new('RGB', (self.width, self.height), 'black')
    # buf = StringIO()
    # image.save(buf, 'JPEG')
    return img.tobytes()

def rf_overlay(image):
  height, width = image.shape[:2]
  x1 = int(width*0.3)
  y1 = int(height*0.8)
  rf_width = int(width*0.15)
  rf_height = int(height*0.1)

  cv2.rectangle(image,
    (x1,y1),
    (x1+rf_width, y1+rf_height ),
    (0,255,0),3)
  return (x1, y1, rf_width, rf_height)


