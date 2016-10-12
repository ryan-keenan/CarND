# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:52:40 2016

@author: kadu
"""

import cv2
from math import pi
import numpy as np
import matplotlib.image as mpimg

def canny_callback(x):
    cl = cv2.getTrackbarPos('Canny: lo thresh','image')
    ch = max(cv2.getTrackbarPos('Canny: hi thresh','image'), cl + 1)
    global canny
    canny = cv2.Canny(grey, cl, ch)
    return
    
def hough_callback(x):
    cl = cv2.getTrackbarPos('Canny: lo thresh','image')
    ch = max(cv2.getTrackbarPos('Canny: hi thresh','image'), cl + 1)
    global canny
    canny = cv2.Canny(grey, cl, ch)
    hr = cv2.getTrackbarPos('Hough: rho','image')
    ha = pi / cv2.getTrackbarPos('Hough: theta','image')
    ht = cv2.getTrackbarPos('Hough: thresh','image')
    hl = cv2.getTrackbarPos('Hough: min len','image')
    hg = cv2.getTrackbarPos('Hough: max gap','image')
    lines = cv2.HoughLinesP(canny, hr, ha, ht, np.array([]), minLineLength=hl, maxLineGap=hg)
    global original
    black = np.zeros_like(original)
    if lines is None:
        return
    for line in lines:
        for x1,y1,x2,y2 in line:
            if abs(y1 - y2) < 30: #ignore nearly-horizontal lines
                continue
            cv2.line(black, (x1, y1), (x2, y2), [255, 0, 0], 8)
    global hough 
    hough = black

# load image
original = mpimg.imread('sample.jpg')

grey = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
cv2.namedWindow('image')

# create switch for ON/OFF Canny functionality
cv2.createTrackbar('Canny', 'image',0,1,canny_callback)
# create trackbars for Canny parameters
cv2.createTrackbar('Canny: lo thresh','image',1,255,canny_callback)
cv2.createTrackbar('Canny: hi thresh','image',1,255,canny_callback)

# create switch for ON/OFF Hough functionality
cv2.createTrackbar('Hough', 'image',0,1,hough_callback)
# create trackbars for Canny parameters
cv2.createTrackbar('Hough: rho','image',1,100,hough_callback)
cv2.createTrackbar('Hough: theta','image',1,360,hough_callback)
cv2.createTrackbar('Hough: thresh','image',1,360,hough_callback)
cv2.createTrackbar('Hough: min len','image',1,300,hough_callback)
cv2.createTrackbar('Hough: max gap','image',1,300,hough_callback)


img = grey

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of canny trackbars
    cs = cv2.getTrackbarPos('Canny', 'image')
    
    # get current positions of hough trackbars
    hs = cv2.getTrackbarPos('Hough', 'image')


    if hs == 1:
        img = hough
    elif cs == 1:
        img = canny
    else:
        img = grey

cv2.destroyAllWindows()