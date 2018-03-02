#!/usr/bin/env python

import rospy
from camera import Camera
from cv_bridge import CvBridge, CvBridgeError
import cv2

from sensor_msgs.msg import Image
from std_msgs.msg import Bool


class CameraBase(Camera):
	def __init__(self):
		rospy.init_node('camera_node', anonymous=True)
		Camera.__init__(self)
		self.image_publisher = rospy.Publisher('/image', Image , queue_size=10)
		self.state_subscriber = rospy.Subscriber('/life_cycle_state',Bool, self.on_life_cycle_state_changed)
		self.bridge = CvBridge()
		self.start_camera_buffering()
	def on_life_cycle_state_changed(self, life_cycle_state):
		print "publish the next image from buffer"

if __name__ == '__main__':
	camera = CameraBase()
	rospy.spin()
