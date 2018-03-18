#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from system_messages.msg import ImageMsg
from charRecognition import CharRecognition
from cv_bridge import CvBridge, CvBridgeError
import cv2


class CharRecognitionBase(CharRecognition):
	def __init__(self):
		CharRecognition.__init__(self)
		self.image_subscriber = rospy.Subscriber("/contour", ImageMsg, self.on_image_received)
		self.char_type_publisher = rospy.Publisher("/char_type",String,queue_size=10)

	def on_image_received(self, image):
		rgb_image = CvBridge().imgmsg_to_cv2(image.rgb, "bgr8")
#		cv2.imshow('rgb',rgb_image);
#		cv2.waitKey(1)
		char_type = self.find_character_type(rgb_image)
		char_type_msg = String()
		char_type_msg.data = char_type
		self.char_type_publisher.publish(char_type_msg)
		

if __name__ == '__main__':
	rospy.init_node('char_recognition_node', anonymous=True)
	charRecognition = CharRecognitionBase()
	rospy.spin()
