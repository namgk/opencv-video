import numpy as np
import cv2

img = cv2.imread('test_small.jpg')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imwrite('test_gray.jpg',imgray)


