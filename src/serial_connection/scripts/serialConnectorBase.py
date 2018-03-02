#!/usr/bin/env python

import rospy
from serialConnector import SerialConnector
from std_msgs.msg import String
from std_msgs.msg import Bool

class SerialConnectorBase(SerialConnector):
	def __init__(self):
		rospy.init_node('serial_connector_node', anonymous=True)
		SerialConnector.__init__(self)
		self.state_subscriber = rospy.Subscriber('/char_type',String, self.on_char_type_received)
		self.life_cycle_publisher = rospy.Publisher('/life_cycle_state',Bool)
	def on_char_type_received(self, char_type):
		print "receive the char type"
		self.write_data(char_type.data)
		life_cycle_state = Bool()
		life_cycle_state.data = True
		life_cycle_publisher.publish(life_cycle_state)
		

if __name__ == '__main__':
	serialConnector = SerialConnectorBase()
	rospy.spin()
