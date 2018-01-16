import pyscreenshot
import numpy as np
import cv2


class DistanceDetector:
    x1 = 66
    x2 = 540 + x1
    y1 = 400
    y2 = 600 + y1
    def __init__(self):
        self.step = 0
    def screen_shoot(self):

        im = pyscreenshot.grab(bbox=(self.x1, self.y1, self.x2, self.y2))
        self.im = np.array(im)
        self.im_gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)

        # getting background color range
        left_top = self.im[0][0]
        self.b_range_background = (left_top[0] - 10, left_top[0] + 10)
        self.g_range_background = (left_top[1] - 10, left_top[1] + 10)
        self.r_range_background = (left_top[2] - 40, left_top[2] + 10)

    def foot_detection(self):
        circles = cv2.HoughCircles(self.im_gray,cv2.HOUGH_GRADIENT,1.2,100,
                                   param1=50, param2=20, minRadius=15, maxRadius=20)
        head = circles[0][0]
        self.foot = head
        self.foot[1] += 78
        #cv2.circle(im, (foot[0], foot[1]), 2, (0, 0, 255), 3)

    def is_background(self, color):
        return color[0] >= self.b_range_background[0] and color[0] <= self.b_range_background[1] and\
               color[1] >= self.g_range_background[0] and color[1] <= self.g_range_background[1] and\
               color[2] >= self.r_range_background[0] and color[2] <= self.r_range_background[1]


    def check_color_sim(self, color1, color2):
        if abs(int(color1[0]) - int(color2[0])) > 30 or abs(int(color1[1]) - int(color2[1])) > 30 or\
                abs(int(color1[2]) - int(color2[2])) > 30:
            return False
        return True

    def find_first_point(self, im):
        for y in range(im.shape[0]):
            for x in range(im.shape[1]):
                color = im[y][x]
                color_down = im[y+1][x]
                if not self.is_background(color) and self.check_color_sim(color, color_down):
                    return (y, x)

    def find_left_right_point(self, im, first_point, foot):
        y_top, x_top = first_point
        x_range_left = range(x_top, max(int(foot[0]), x_top - 100), -1) if foot[1] < x_top else \
            range(x_top, x_top - 100, -1)
        x_range_right = range(x_top, min(int(foot[0]), x_top + 100)) if foot[1] > x_top else \
            range(x_top, min(x_top + 100, im.shape[1] - 1))
        y_range = range(y_top, y_top + 200)
        sim_colors = []
        for y in y_range:
            if self.is_background(im[y][x_top]):
                break
            for x in x_range_left:
                if self.is_background(im[y][x]):
                    break
                if self.check_color_sim(im[y][x], im[first_point[0]][first_point[1]]):
                    sim_colors.append((y, x))
            for x in x_range_right:
                if self.is_background(im[y][x]):
                    break
                if self.check_color_sim(im[y][x], im[first_point[0]][first_point[1]]):
                    sim_colors.append((y, x))
        if foot[1] < x_top:
            return max(sim_colors, key = lambda x: x[1])
        return min(sim_colors, key=lambda x: x[1])


    def find_center(self):
        first_point = self.find_first_point(self.im)
        another_point = self.find_left_right_point(self.im, first_point, self.foot)
        self.center = (first_point[1], another_point[0])


    def get_distance(self):
        return np.math.hypot(self.foot[0] - self.center[0], self.foot[1] - self.center[1])
    def save_im(self):
        self.step +=1
        cv2.circle(self.im, (self.foot[0], self.foot[1]), 2, (0, 0, 255), 3)
        cv2.circle(self.im, self.center, 2, (0, 0, 255), 3)
        cv2.imwrite('step_'+str(self.step)+'.png', self.im)

'''
cv2.circle(im, (first_point[1], another_point[0]), 2, (0, 0, 255), 3)


cv2.imshow('foot', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''