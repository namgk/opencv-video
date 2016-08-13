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
    self.image_pub = rospy.Publisher("/usb_cam/image_foreground",Image)
    self.cap = cv2.VideoCapture('vid.mp4')
    self.cap.set(5,35)
    self.bridge = CvBridge()

  def play(self):
    while True:
      ret, image = self.cap.read()
      if not ret:
        print('restart...')
        self.cap.set(2,0)
        continue

      image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      image = cv2.BackgroundSubtractorMOG().apply(image)
        
      outimg = image

      try:
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(outimg, "mono8"))
      except CvBridgeError as e:
        print(e)

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
