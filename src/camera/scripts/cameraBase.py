#!/usr/bin/env python

import rospy
from camera import Camera
from cv_bridge import CvBridge, CvBridgeError
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from  system_messages.msg import ImageMsg

class CameraBase(Camera):
	def __init__(self):
#		rospy.init_node('camera_node', anonymous=True)
		Camera.__init__(self)
		self.image_publisher = rospy.Publisher('/image', ImageMsg, queue_size = 10)
		self.bool_publiher = rospy.Publisher('/bool', Bool, queue_size = 10)
		self.state_subscriber = rospy.Subscriber('/life_cycle_state',Bool, self.on_life_cycle_state_changed)
		self.bridge = CvBridge()
		self.start_camera_buffering()
		self.image = cv2.imread('/home/mj/datasets/croped/0.jpg')
#		self.on_life_cycle_state_changed(True)

	def on_life_cycle_state_changed(self, life_cycle_state):
		while not rospy.is_shutdown():
			bool_msg = Bool()
			bool_msg.data = True
			self.bool_publiher.publish(bool_msg)
			image_message = ImageMsg()
			image_message.rgb = self.bridge.cv2_to_imgmsg(self.image, "bgr8")
			image_message.image_is_prepared = True
			self.image_publisher.publish(image_message)
#			print "publish the next image from buffer"

if __name__ == '__main__':
	rospy.init_node('camera_node', anonymous=True)
	camera = CameraBase()
	camera.on_life_cycle_state_changed(True)
	rospy.spin()
