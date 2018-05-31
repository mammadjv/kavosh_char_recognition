#!/usr/bin/env python

import rospy
#from serialConnector import SerialConnector
from std_msgs.msg import String
from std_msgs.msg import Bool
import time
#import serial
import RPi.GPIO as GPIO

#ser = serial.Serial(port = '/dev/ttyS0',baudrate = 9600, parity = serial.PARITY_NONE, bytesize = serial.EIGHTBITS, timeout = 1)

class GPIOConnector:
	def __init__(self , id1 , id2 , id3):
		self.pinid1 = id1
		self.pinid2 = id2 
		self.pinidRead = id3
		rospy.init_node('serial_connector_node', anonymous=True)
		self.state_subscriber = rospy.Subscriber('/char_type',String, self.on_char_type_received)
		self.reset_gpio_subscriber = rospy.Subscriber('/write_gpio',Bool, self.reset)
		self.life_cycle_publisher = rospy.Publisher('/life_cycle_state',Bool,queue_size = 10)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pinid1 , GPIO.OUT)
		GPIO.setup(self.pinid2 , GPIO.OUT)
		GPIO.setup(self.pinidRead , GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
		self.reset("first reset")

	def writeData(self, pin1value , pin2value):
		GPIO.output(self.pinid1,pin1value)
#		GPIO.output(self.pinid1,GPIO.HIGH)
		time.sleep(0.002)
		GPIO.output(self.pinid2,pin2value)
#		GPIO.output(self.pinid2,GPIO.HIGH)
		time.sleep(0.002)

	def readData(self):
		return GPIO.input(self.pinidRead)

	def reset(self, data):
		print "reset             !!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		GPIO.output(self.pinid1,0)
		time.sleep(0.002)
		GPIO.output(self.pinid2,0)
		time.sleep(0.002)

	def on_char_type_received(self,char_type):
		print "wriiiiiiiiiiiteee", char_type.data
		if(char_type.data == "H"):
		        self.writeData(0,1)
		if(char_type.data == "S"):
		        self.writeData(1,0)
		if(char_type.data == "U"):
		        self.writeData(1,1)
		life_cycle_state = Bool()
		life_cycle_state.data = True
		self.life_cycle_publisher.publish(life_cycle_state)
		

if __name__ == '__main__':
	gpioConnector = GPIOConnector(23,24,18)
	rospy.spin()
