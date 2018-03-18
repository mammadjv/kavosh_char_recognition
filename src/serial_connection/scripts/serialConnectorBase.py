#!/usr/bin/env python

import rospy
#from serialConnector import SerialConnector
from std_msgs.msg import String
from std_msgs.msg import Bool
import time
import serial

class SerialConnectorBase:
	def __init__(self):
		rospy.init_node('serial_connector_node', anonymous=True)
#		SerialConnector.__init__(self)
		self.state_subscriber = rospy.Subscriber('/char_type',String, self.on_char_type_received)
		self.life_cycle_publisher = rospy.Publisher('/life_cycle_state',Bool,queue_size = 10)
		self.serialConnector = serial.Serial(port=' /dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0 \
		        baudrate = 9600, \
		        parity=serial.PARITY_NONE, \
		        stopbits=serial.STOPBITS_ONE, \
		        bytesize=serial.EIGHTBITS, \
		        timeout=1)

	def on_char_type_received(self, char_type):
		self.serialConnector.write(char_type)
		life_cycle_state = Bool()
		life_cycle_state.data = True
		self.life_cycle_publisher.publish(life_cycle_state)
		

if __name__ == '__main__':
	serialConnector = SerialConnectorBase()
	rospy.spin()
