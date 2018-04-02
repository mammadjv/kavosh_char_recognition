#!/usr/bin/env python

from regionProvider import RegionProvider
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from system_messages.msg import ImageMsg
from cv_bridge import CvBridge, CvBridgeError
import cv2
import time


class RegionProviderBase(RegionProvider):
	def __init__(self):
		RegionProvider.__init__(self)
		self.image_subscriber = rospy.Subscriber("/image", ImageMsg, self.on_image_received)
		self.gpio_publisher = rospy.Publisher("/write_gpio",Bool,queue_size=10)
		self.life_cycle_publisher = rospy.Publisher("/life_cycle_state",Bool,queue_size=10)
		self.contour_publisher = rospy.Publisher("/contour",ImageMsg,queue_size=10)
		self.bridge = CvBridge()

	def on_image_received(self, image):
		start = time.time()
		if(image.image_is_prepared == False):
			boolMsg = Bool()
			boolMsg.data = False
			self.gpio_publisher.publish(boolMsg)
			self.life_cycle_publisher.publish(boolMsg)
			return
		rgb = self.bridge.imgmsg_to_cv2(image.rgb, "bgr8")
		image ,draw_image ,crop_img , contour_found , edged, thresh = self.findContours(rgb)
#		cv2.imshow('regioning rgb',rgb)
#		cv2.waitKey(1)
#		contour_found = False
		if(contour_found == False):
			boolMsg = Bool()
                        boolMsg.data = False
			self.gpio_publisher.publish(boolMsg)
                        self.life_cycle_publisher.publish(boolMsg)
                        return
		image_message = ImageMsg()
		image_message.rgb = self.bridge.cv2_to_imgmsg(crop_img, "bgr8")
                image_message.image_is_prepared = True
#		cv2.imshow('croped', crop_img)
#		cv2.waitKey(1)
		print "time   ==  " + str(time.time() - start)
		self.contour_publisher.publish(image_message)


if __name__ == '__main__':
        rospy.init_node('regioning_node', anonymous=True)
        regionProvider = RegionProviderBase()
        rospy.spin()
