import cv2
import pyscreenshot
import numpy as np

img = cv2.imread('./debug_images/step_139.png')
'''
x1 = 66
x2 = 760 + x1
y1 = 450
y2 = 800 + y1
img = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
img = np.array(img)
'''
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(img_gray,cv2.HOUGH_GRADIENT,1.2,100,
                                   param1=50, param2=20, minRadius=20, maxRadius=25)[0]
print(len(circles))

def filter_foot_color(c):
    color = img[int(c[1]), int(c[0])]
    return abs(color[0] - 88) < 20 and abs(color[1] - 81) < 20 and abs(color[2] - 128) < 20

circles = list(filter(filter_foot_color, circles))

head = circles[0]
foot = head
foot[1] += 114


cv2.circle(img, (foot[0], foot[1]), 2, (0, 127, 255), 3)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()