
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))

import numpy as np
import cv2
 


# im = cv2.imread('shutterstock_401797897.jpg')
im = cv2.imread('shutterstock_401797897.jpg', cv2.IMREAD_GRAYSCALE)
# imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(im, 88, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
im = cv2.drawContours(im, contours, -1, (0,0,255), 3)
 
cv2.imshow('im',im)
cv2.waitKey(0)
cv2.destroyAllWindows()



