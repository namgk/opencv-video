#!/usr/bin/env python
from PIL import Image
import pytesseract

import rospy
from std_msgs.msg import String

pub = rospy.Publisher('topic_name', String, queue_size=10)
rospy.init_node('test_pub')
r = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
   pub.publish("hello world")
   r.sleep()
