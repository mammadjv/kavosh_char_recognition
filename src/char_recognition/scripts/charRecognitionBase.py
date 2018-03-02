#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from system_messages.msg import Image
from charRecognition import CharRecognition
from cv_bridge import CvBridge, CvBridgeError
import cv2

class CharRecognitionBase(CharRecognition):
	def __init__(self):
		CharRecognition.__init__(self)
		rospy.init_node('char_recognition_node', anonymous=True)
		image_subscriber = rospy.Subscriber("/image", Image, self.on_image_received)

	def on_image_received(self, image):
		if(image.image_is_prepared == True):
			rgb_image = CvBridge().imgmsg_to_cv2(image.rgb, "bgr8")
			self.find_character_type(rgb_image)
		else:

if __name__ == '__main__':
	charRecognition = CharRecognitionBase()
	rospy.spin()
