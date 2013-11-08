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

def c0(x,y):
	if x > 430 and x < 650:
		if y > 433 and y < 622:
			return 1
	return 0

def c1(x,y):
	if x > 242 and x < 724:
		if y > 136 and y < 340:
			return 1

        if x > 698 and x < 902:
                if y > 266 and y < 735:
			return 1

        if x > 242 and x < 724:
                if y > 635 and y < 850:
			return 1
	return 0

def c2(x,y):
        if x > 650 and x < 926:
                if y > 242 and y < 421:
                        return 1
        return 0

def c3(x,y):
        if x > 301 and x < 910:
                if y > 205 and y < 590:
                        return 1
        return 0

def c4(x,y):
        if x > 430 and x < 650:
                if y > 433 and y < 622:
                        return 1

        if x > 242 and x < 724:
                if y > 136 and y < 340:
                        return 1

        if x > 698 and x < 902:
                if y > 266 and y < 735:
                        return 1

        if x > 242 and x < 724:
                if y > 635 and y < 850:
                        return 1
        return 0


def calc_dis(x0,y0,x1,y1):
	tmp = (x1-x0)*2 + (y1-y0)*2
	return tmp

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
    red_3 = (255, 255, 51)
    red_2 = (255, 153, 255)
	        
    ka = [] 
    kb = []
    kc = []
    kd = []

    f = open('../ranked_point_desc.txt', 'a')
    rank = []
    for x_a in xrange(len(kp3)):
	    t = lines2[x_a].strip()
	    if int(t) == 0:
	        ka.append(kp3[x_a])
	    elif int(t) == 1:
	        kb.append(kp3[x_a])
            elif int(t) == 2:
                kc.append(kp3[x_a])
            elif int(t) == 3:
                kd.append(kp3[x_a])
		rank.append(x_a)
	    else:
	        print "okay"

    #img = cv2.drawKeypoints(img, kd, flags=4, color=red)
    #img = cv2.drawKeypoints(img, kc, flags=4, color=red_3)
    #img = cv2.drawKeypoints(img, kb, flags=4, color=red_2) 
    

    f = open('../classify_result_.txt', 'a')
    if len(ka) > len(kb):
        f.write("Benign")
    else:
        f.write("Malignant")
    f.write('\n')
    f.close()

    
    DM_y = 494.473219557731
    DM_x = 609.762829066857
    AMD_y = 521.185139323592
    AMD_x = 536.710076687492

    tmp_a = 0
    tmp_d = 0

    count_m = 0
    count_n = 0
    count_a = 0
    count_d = 0
    count_center = 0

    for i in kd:
        if c0(i.pt[0],i.pt[1]) == 1:
	    count_center += 1
	else:
	    if c4(i.pt[0],i.pt[1]) == 1:
	        tmp_a = calc_dis(AMD_x, AMD_y, i.pt[0], i.pt[1])
                tmp_d = calc_dis(DM_x, DM_y, i.pt[0], i.pt[1])
	        if tmp_a > tmp_d:
	            count_d += 1
	        else:
		    count_a += 1
	    else:
	        count_n += 1
    
    for i in kc:
        if c0(i.pt[0],i.pt[1]) == 1:
            count_center += 1
        else:
            if c4(i.pt[0],i.pt[1]) == 1:
                tmp_a = calc_dis(AMD_x, AMD_y, i.pt[0], i.pt[1])
                tmp_d = calc_dis(DM_x, DM_y, i.pt[0], i.pt[1])
                if tmp_a > tmp_d:
                    count_d += 1
                else:
                    count_a += 1
            else:
                count_n += 1
    
    for i in kb:
        if c0(i.pt[0],i.pt[1]) == 1:
            count_center += 1
        else:
            if c4(i.pt[0],i.pt[1]) == 1:
                tmp_a = calc_dis(AMD_x, AMD_y, i.pt[0], i.pt[1])
                tmp_d = calc_dis(DM_x, DM_y, i.pt[0], i.pt[1])
                if tmp_a > tmp_d:
                    count_d += 1
                else:
                    count_a += 1
            else:
                count_n += 1


    """
    for i in ka:
        if c4(i.pt[0],i.pt[1]) == 1:
            tmp_a += calc_dis(AMD_x, AMD_y, i.pt[0], i.pt[1])
            tmp_d += calc_dis(DM_x, DM_y, i.pt[0], i.pt[1])
    """

    f2 = open('../pointDM.txt', 'a')
    if len(ka) < len(kp3)*0.4:
	if count_center > 1:
		f2.write("AMD")
                f2.write('\n')
	else:
    		if count_a > count_d:
			f2.write("AMD") 
			f2.write('\n')
    		else:
        		f2.write("DM") 
        		f2.write('\n')
    else:
	f2.write("Normal")
        f2.write('\n')

    f2.close()


    print "Normal  %d, Malignant %d"%(count_n, count_m)
    print "Ka %d"%(len(ka))

    """
    tmp = str(fn3)
    segments = tmp.split("/")
    f1 = open('../ranked_%s_point_desc.txt'%segments[-1], 'a')
    for i in rank:
	for val in desc3[i]:
		f1.write(str(val))
		f1.write('\t')
	f1.write('\n')
    f1.close()
    
    cv2.imwrite('../tmp_pic/res%s'%segments[-1],img)
    """
