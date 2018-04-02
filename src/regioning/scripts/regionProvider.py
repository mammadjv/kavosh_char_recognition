#!/usr/bin/pythom
import numpy as np
import cv2
from Queue import Queue
from threading import Thread
import sys

class RegionProvider:
        def __init__(self):
		print 'Region provider module created'
	
	def checkFirstFrame(self, thresh):
#                ret,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY_INV)
		thresh = cv2.resize(thresh, (30,30))
#                edged = cv2.Canny(thresh, 100, 50 ,1)
                _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                best_x , best_y , best_w , best_h = 0 , 0 , 0 , 0
                height, width = thresh.shape[:2]
                for cnt in contours :
                        x,y,w,h = cv2.boundingRect(cnt)
                        if(w  > 4 * width /5):
                                continue
                        if(x < width/5 or x > 4*width/5 or x + w < width/5 or x+w > 4*width/5):
                        #       print "1"
                                continue
                        if( y < width/5 or y + h < width/5 or y+h > 4*height/5):
                        #       print "2"
                                continue
                        if (w*h < 5):
                                continue
                        if(w*h > best_w*best_h):
                        	best_x , best_y , best_w , best_h = x , y , w , h
		if (best_w*best_h != 0):
			return True
		return False

	def findContours(self, image):
		image = cv2.resize(image, (150,120))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                ret,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY_INV)

#		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                #gray = cv2.GaussianBlur(gray, (3, 3), 0)
		valid_contour = self.checkFirstFrame(thresh)
		if(valid_contour == True):
			print 'valid!!!!!'
		else : 
			print 'not valid'
			return image,image,image,False,image,image
#		cv2.imshow('thresh2',thresh)
#		cv2.waitKey(1)
#		return image,image,image,False,image,image
#		print "kharrr!!"
	#edged = cv2.Canny(thresh, 100, 50 ,1)i
#		print image.shape
		
		
#		image = cv2.resize(image, (150,120))
#		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#                ret,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY_INV)
#		cv2.imshow('thresh',thresh)
#		cv2.waitKey(1)
		_, contours, hierarchy = cv2.findContours(thresh , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		best_x , best_y , best_w , best_h = 0 , 0 , 0 , 0
		#print image.shape
		draw_image = image.copy()
		height, width = image.shape[:2]
		for cnt in contours :
			x,y,w,h = cv2.boundingRect(cnt)
			if(w  > 2 * width /3):
				continue
			if(x < 10 or x > width -10 or x + w < 10 or x+w > width -10):
			#	print "1"
				continue
			if( y < 10 or y + h < 10 or y+h > height - 20):
			#	print "2"
				continue
			if (w*h < 20):
				continue
			thresh_croped = thresh[y:y+h, x:x+w]
			blacks = len(np.where(thresh_croped == 0))
			whites = len(np.where(thresh_croped == 255))
			if(float(blacks)/float(w*h) > 0.8 or float(whites)/float(w*h) > 0.8):
				continue
			if(w*h > best_w*best_h):
				best_x , best_y , best_w , best_h = x , y , w , h
			#cv2.rectangle(draw_image,(x,y),(x+w,y+h),(255,255,0),2)
		edged = thresh 
		crop_img = image
		contour_found = False
		if(best_w > 20 and best_h > 20):
			best_w ,best_h = best_w + 20, best_h + 20
			if ( best_x + best_w > width-1 ):
				best_w = width-1 - best_x
			if ( best_y + best_h > height-1 ):
				best_h = height-1 - best_y 
			best_x  , best_y  = max(best_x - 10 , 0) , max(best_y -10 , 0)
			crop_img = image[best_y:best_y + best_h, best_x:best_x + best_w]
			contour_found = True
		return image ,draw_image ,crop_img , contour_found , edged, thresh

		


