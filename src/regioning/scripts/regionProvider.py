#!/usr/bin/pythom
import numpy as np
import cv2
from Queue import Queue
from threading import Thread
import sys

class RegionProvider:
        def __init__(self):
		print 'Region provider module created'
	
	def checkFirstFrame(self,threshed_image):
		thresh = cv2.resize(threshed_image, (30,30))
                edged = cv2.Canny(thresh, 100, 50 ,1)
                contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

	def checkFrameColors(self,frame):
		rows,cols = frame.shape[:2]
	        for i in range(rows):
        	    for j in range(cols):
                	r = r + frame[i,j][0]
	                g = g + frame[i,j][1]
        	        b = b + frame[i,j][2]
	        return r/(rows*cols) , g/(rows*cols) , b/(rows*cols)

	def findContours(self,image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (3, 3), 0)
                ret,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
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
		edged = cv2.Canny(thresh, 100, 50 ,1)
		contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		best_x , best_y , best_w , best_h = 0 , 0 , 0 , 0
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
			if(w*h > best_w*best_h):
				best_x , best_y , best_w , best_h = x , y , w , h
			cv2.rectangle(draw_image,(x,y),(x+w,y+h),(255,255,0),2)
 
		crop_img = image
		contour_found = False
		if(best_w > 30 and best_h > 30):
			best_w ,best_h = best_w + 40, best_h + 40
			if ( best_x + best_w > width-1 ):
				best_w = width-1 - best_x
			if ( best_y + best_h > height-1 ):
				best_h = height-1 - best_y 
			best_x  , best_y  = max(best_x - 20 , 0) , max(best_y -20 , 0)
			crop_img = image[best_y:best_y + best_h, best_x:best_x + best_w]
			contour_found = True
		return image ,draw_image ,crop_img , contour_found , edged, thresh

		


