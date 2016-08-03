#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from pytesseract import image_to_string

class video_player:

  def __init__(self):
    self.image_pub = rospy.Publisher("/usb_cam/test",Image)
    self.cap = cv2.VideoCapture('vid.mp4')
    self.cap.set(5,35)
    self.bridge = CvBridge()

  def play(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        print('restart...')
        self.cap.set(2,0)
        continue

      outimg = frame
      message = 'hi'
      cv2.putText(outimg, message, (200,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
      #ret,outimg = cv2.threshold(cv_image,127,255,cv2.THRESH_BINARY)
      # try:
      #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(outimg, "bgr8"))
      # except CvBridgeError as e:
      #   print(e)

def main(args):
  rospy.init_node('video_player', anonymous=True)
  ic = video_player()
  ic.play()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
