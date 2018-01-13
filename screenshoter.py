import pyscreenshot
import numpy as np
import cv2

x1 = 66
x2 = 410 + x1
y1 = 300
y2 = 400 + y1
im = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
im = np.array(im)

im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

#foot detection
circles = cv2.HoughCircles(im_gray,cv2.HOUGH_GRADIENT,1.2,100,
                            param1=50,param2=30,minRadius=20,maxRadius=30)

head = circles[0][0]
foot = head
foot[1] += 130
cv2.circle(im, (foot[0], foot[1]), 2, (0, 0, 255), 3)
#edge_detected_image = cv2.Canny(im_gray, 30, 200)
#_, contours, _= cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(im_gray, contours,  -1, (0,0,0), 2)

#center detection
edges = cv2.Canny(im_gray,50,150,apertureSize = 3)
cv2.imwrite("edge.png",edges)
print(edges.shape)
def squre(img, tmp):
    indexes = []
    l,r = img.shape
    for i in range(l):
        for j in range(r):
            if img[i][j] == 255 and abs(tmp - j) <= 2 and tmp >= j:
                indexes.append((i, j))
                tmp = j
                break

    x = indexes[0][1]
    for i,j in indexes:
        if img[i][j]==img[i+1][j] and img[i][j]==img[i+2][j] and img[i][j]==img[i+3][j]:
            y = i
            break
    print("squre")
    return (y,x)


def oval(img, indexes):
    ys = [j for i,j in indexes]
    x = indexes[0][1]
    for i in range(len(indexes)):
        if ys[i] == ys[i + 1] and ys[i] == ys[i + 2] and ys[i] == ys[i + 3] and ys[i] == ys[i + 4] and ys[i] == ys[
                    i + 5]:
            y = indexes[i][0]
            break

    print("oval")
    return (y+5,x+5)


def find_center(img):
    indexes = []
    l,r = img.shape
    for i in range(l):
        for j in range(r):
            if img[i][j] == 255:
                indexes.append((i, j))
                break
    _, tmp = indexes[0]

    if indexes[0][1] - indexes[1][1] < 4:
        y,x = squre(img, tmp)
    else:
        y,x = oval(img, indexes)
    return y,x


y, x = find_center(edges)

cv2.circle(im, (x, y), 2, (0, 0, 255), 3)
cv2.imshow('foot', im)
cv2.waitKey(0)
cv2.destroyAllWindows()

