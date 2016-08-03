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

from pytesseract import image_to_string

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("/usb_cam/image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 100, 255)
    
    outimg = cv_image
    message = 'hi'
    cv2.putText(outimg, message, (200,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
    #ret,outimg = cv2.threshold(cv_image,127,255,cv2.THRESH_BINARY)

    print(type(outimg))

    try:
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
