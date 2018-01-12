import pyscreenshot
import numpy as np
import cv2

x1 = 66
x2 = 760 + x1
y1 = 50
y2 = 1200 + y1
im = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
im = np.array(im)

im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

edge_detected_image = cv2.Canny(im_gray, 30, 200)
_, contours, _= cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



cv2.drawContours(im_gray, contours,  -1, (0,0,0), 2)


cv2.imshow('compressed', im_gray )
cv2.waitKey(0)
cv2.destroyAllWindows()
