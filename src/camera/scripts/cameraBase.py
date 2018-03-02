#!/usr/bin/env python

import rospy
from camera import Camera
from cv_bridge import CvBridge, CvBridgeError
import cv2

from sensor_msgs.msg import Image


class CameraBase(Camera):
	def __init__(self):
		rospy.init_node('camera_node', anonymous=True)
		Camera.__init__(self)
		self.image_publisher = rospy.Publisher('/image', Image , queue_size=10)
		self.bridge = CvBridge()
		self.start_camera_buffering()

if __name__ == '__main__':
	camera = cameraBase()
	rospy.spin()
