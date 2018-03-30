#!/usr/bin/env python

import rospy
from camera import Camera
from cv_bridge import CvBridge, CvBridgeError
import cv2
from sensor_msgs.msg import *
from std_msgs.msg import Bool
from  system_messages.msg import ImageMsg
import time
import numpy as np
import time


class CameraBase(Camera):
	def __init__(self):
		Camera.__init__(self)
		self.image_publisher = rospy.Publisher('/image', ImageMsg, queue_size = 10)
		self.image_subscriber = rospy.Subscriber('raspicam_node/image/compressed', CompressedImage,self.on_image_received)
		self.bool_publiher = rospy.Publisher('/bool', Bool, queue_size = 10)
		self.state_subscriber = rospy.Subscriber('/life_cycle_state',Bool, self.on_life_cycle_state_changed)
		self.bridge = CvBridge()
		self.compressed_images = list()


	def on_image_received(self, compressed_image):
		if(len(self.compressed_images) == 10):
			self.compressed_images.pop(0)
		self.compressed_images.append(compressed_image)

	def on_life_cycle_state_changed(self, life_cycle_state):
		image_message = ImageMsg()
		image = None
		if(len(self.compressed_images) > 0):
			first = time.time()
			compressed_image = self.compressed_images.pop()
			np_arr = np.fromstring(compressed_image.data, np.uint8)
			image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
			print time.time() - first
#			cv2.imshow('image', image)
#			cv2.waitKey(1)
		if(image != None):
			image_message.rgb = self.bridge.cv2_to_imgmsg(image, "bgr8")
			image_message.image_is_prepared = True
		else:
			image_message.image_is_prepared = False
		self.image_publisher.publish(image_message)
		
if __name__ == '__main__':
	rospy.init_node('camera_node', anonymous=True)
	camera = CameraBase()
	rospy.spin()
