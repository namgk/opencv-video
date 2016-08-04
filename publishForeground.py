#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('testcamproc')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

fgbg = cv2.BackgroundSubtractorMOG()

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("/usb_cam/image_foreground",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam/image_grayscale",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
      image = fgbg.apply(cv_image)
      image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # except CvBridgeError as e:
    #   print(e)
    
      outimg = image

    # try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(outimg, "bgr8"))
    except CvBridgeError as e:
      print(e)

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
