#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('testcamproc')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("/grayscale_node",Image)
    self.image_sub = rospy.Subscriber("/original_node",Image,self.callback)

  def callback(self,data):
    self.image_pub.publish(data)

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
