#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('testcamproc')
import sys
import rospy
import cv2
from std_msgs.msg import Int8
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("/usb_cam/image_carcount",Int8)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam/image_foreground",Image,self.callback)
    self.count_changed = False
    self.count = 0  
    self.last_state = 0

  def callback(self,data):
    try:
      image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    x, y, w, h = rf_overlay(image)
    ref = image[y:y+h, x:x+w]
    white = cv2.countNonZero(ref)

    if white > 0 and self.last_state == 0:
      self.count += 1
      self.count_changed = True
      self.last_state = 1

    if white == 0 and self.last_state == 1:
      self.last_state = 0

    if self.count_changed:
      self.image_pub.publish(self.count)
      self.count_changed = False

  def rf_overlay(image):
    height, width = image.shape[:2]
    x1 = int(width*0.3)
    y1 = int(height*0.8)
    rf_width = int(width*0.15)
    rf_height = int(height*0.1)

def main(args):
  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
