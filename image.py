import numpy as np
import cv2

img = cv2.imread('test.jpg')
img2 = cv2.imread('test2.jpg')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

cv2.imwrite('test_gray.jpg',cv2.subtract(imgray2, imgray))


