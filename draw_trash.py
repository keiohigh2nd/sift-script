#!/usr/bin/env python
import sys
sys.path.append("/home/appl/opencv-2.4.6.1/lib/python2.6/site-packages")
import numpy as np
import cv2
from common import anorm, getsize
import os


if __name__ == '__main__':
    import sys, getopt,os,time	
    f = open('text.txt')
    lines2 = f.readlines()
    f.close()

    opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
    opts = dict(opts)
    detector, matcher = init_feature(feature_name)

    fn3 = '../../dm1.jpg'
    img = cv2.imread(fn3,0)
    kp3, desc3 = detector.detectAndCompute(img, None)
    print 'img3 - %d features' % (len(kp3))

    green = (0, 255, 0)
    red = (0, 0, 255)	        
	        
    ka = [] 
    kb = []
    for x_a in xrange(len(kp3)):
	    t = lines2[x_a].strip()
	    if int(t) == 0:
		    ka.append(kp3[x_a])
	    elif int(t) == 1:
	        kb.append(kp3[x_a])
	    else:
	        print "okay"

    img = cv2.drawKeypoints(img, ka, flags=4, color=green)
    img = cv2.drawKeypoints(img, kb, flags=4, color=red)

    cv2.imshow('NBNN',img)
    cv2.imwrite('../test.jpg',img)	

    #Showing Window
    cv2.waitKey()
    cv2.destroyAllWindows()
