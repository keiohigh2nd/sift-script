#!/usr/bin/env python
import sys
sys.path.append("/home/appl/opencv-2.4.6.1/lib/python2.6/site-packages")
import numpy as np
import cv2
from common import anorm, getsize
import os

def init_feature(name):
    chunks = name.split('-')
    if chunks[0] == 'sift':
        detector = cv2.SIFT()
        norm = cv2.NORM_L2
    elif chunks[0] == 'surf':
        detector = cv2.SURF(800)
        norm = cv2.NORM_L2
    elif chunks[0] == 'orb':
        detector = cv2.ORB(400)
        norm = cv2.NORM_HAMMING
    else:
        return None, None
    if 'flann' in chunks:
        if norm == cv2.NORM_L2:
            flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        else:
            flann_params= dict(algorithm = FLANN_INDEX_LSH,
                               table_number = 6, # 12
                               key_size = 12,     # 20
                               multi_probe_level = 1) #2
        matcher = cv2.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)
    else:
        matcher = cv2.BFMatcher(norm)
    return detector, matcher


def filter_matches(kp1, kp2, matches, ratio = 0.75):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    kp_pairs = zip(mkp1, mkp2)
    return p1, p2, kp_pairs

def explore_match(win, img1, img2, kp_pairs, status = None, H = None):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
        cv2.polylines(vis, [corners], True, (255, 255, 255))

    if status is None:
        status = np.ones(len(kp_pairs), np.bool_)
    p1 = np.int32([kpp[0].pt for kpp in kp_pairs])
    p2 = np.int32([kpp[1].pt for kpp in kp_pairs]) + (w1, 0)

    green = (0, 255, 0)
    red = (0, 0, 255)
    white = (255, 255, 255)

    kp_color = (51, 103, 236)
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            col = green
            cv2.circle(vis, (x1, y1), 2, col, -1)
            cv2.circle(vis, (x2, y2), 2, col, -1)
        else:
            col = red
            r = 2
            thickness = 3
            cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
            cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
            cv2.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
            cv2.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)
    vis0 = vis.copy()
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            cv2.line(vis, (x1, y1), (x2, y2), green)

    cv2.imshow(win, vis)
    def onmouse(event, x, y, flags, param):
        cur_vis = vis
        if flags & cv2.EVENT_FLAG_LBUTTON:
            cur_vis = vis0.copy()
            r = 8
            m = (anorm(p1 - (x, y)) < r) | (anorm(p2 - (x, y)) < r)
            idxs = np.where(m)[0]
            kp1s, kp2s = [], []
            for i in idxs:
                 (x1, y1), (x2, y2) = p1[i], p2[i]
                 col = (red, green)[status[i]]
                 cv2.line(cur_vis, (x1, y1), (x2, y2), col)
                 kp1, kp2 = kp_pairs[i]
                 kp1s.append(kp1)
                 kp2s.append(kp2)
            cur_vis = cv2.drawKeypoints(cur_vis, kp1s, flags=4, color=kp_color)
            cur_vis[:,w1:] = cv2.drawKeypoints(cur_vis[:,w1:], kp2s, flags=4, color=kp_color)

        cv2.imshow(win, cur_vis)
    cv2.setMouseCallback(win, onmouse)
    return vis


if __name__ == '__main__':
    import sys, getopt,os,time	
    f = open('text.txt')
    lines2 = f.readlines()
    f.close()

    opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
    opts = dict(opts)
    feature_name = opts.get('--feature', 'sift')
    starttime = time.clock()
    detector, matcher = init_feature(feature_name)
    
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'Usage: # python %s filename' % argvs[0]
        quit()

    
    fn3 = argvs[1]
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

    img = cv2.drawKeypoints(img, kb, flags=4, color=red)

    print 'Benign class %d, Malignant class %d' % (len(ka),len(kb))
    
    f1 = open('res_class.txt', 'w')
    if(len(ka) > len(kb)):
        f1.write("benign")
    else:
        f1.write("mal")
    f1.write("\t")
    f1.close()
     
    tmp = str(fn3)
    #cv2.imshow('NBNN',img)
    cv2.imwrite('../res%d.jpg'%tmp,img)	

    #Showing Window
    #cv2.waitKey()
    #cv2.destroyAllWindows()
