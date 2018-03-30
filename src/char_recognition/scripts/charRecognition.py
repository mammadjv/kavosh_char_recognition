import numpy
import cv2
import caffe
from pattern_perceptor import PatternPerceptor



class CharRecognition:
	def __init__(self):
		print "char_recognition module created!"
		self.pattern_perceptor = PatternPerceptor('/home/ubuntu/Kavosh_Char_Recognition/src/char_recognition/scripts/deploy.prototxt','/home/ubuntu/Kavosh_Char_Recognition/src/char_recognition/scripts/hand_written_99.caffemodel')
	def find_character_type(self, image):
#		return 's'
		output_number = self.pattern_perceptor.recognize(image)
		if(output_number == 0):
			return 'h'
		
		if(output_number == 1):
			return 's'
		else:
			return 'u'

#char = CharRecognition()
