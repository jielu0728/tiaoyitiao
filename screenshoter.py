import pyscreenshot
import numpy as np
import cv2
import os

class DistanceDetector:
    x1 = 66
    x2 = 760 + x1
    y1 = 450
    y2 = 800 + y1

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

    def filter_foot_color(self, c):
        try:
            color = self.im[int(c[1]), int(c[0])]
        except IndexError:
            return False
        return abs(color[0] - 88) < 20 and abs(color[1] - 81) < 20 and abs(color[2] - 128) < 20

    def foot_detection(self):
        circles = cv2.HoughCircles(self.im_gray,cv2.HOUGH_GRADIENT,1.2,100,
                                   param1=50, param2=20, minRadius=20, maxRadius=25)[0]


        circles = list(filter(self.filter_foot_color, circles))
        head = circles[0]
        self.foot = head
        self.foot[1] += 114
        #cv2.circle(im, (foot[0], foot[1]), 2, (0, 0, 255), 3)

    def is_background(self, color):
        return color[0] >= self.b_range_background[0] and color[0] <= self.b_range_background[1] and\
               color[1] >= self.g_range_background[0] and color[1] <= self.g_range_background[1] and\
               color[2] >= self.r_range_background[0] and color[2] <= self.r_range_background[1]


    def check_color_sim(self, color1, color2):
        if abs(int(color1[0]) - int(color2[0])) > 15 or abs(int(color1[1]) - int(color2[1])) > 15 or\
                abs(int(color1[2]) - int(color2[2])) > 15:
            return False
        return True

    def find_first_point(self, im):
        for y in range(im.shape[0]):
            for x in range(im.shape[1]):
                color = im[y][x]
                color_down = im[y+1][x]
                if abs(x - self.foot[0]) > 25 and not self.is_background(color) and\
                        self.check_color_sim(color, color_down):
                    return (y, x)

    def find_left_right_point(self, im, first_point, foot):
        y_top, x_top = first_point
        x_range_left = range(x_top, max(int(foot[0]), x_top - 300), -1) if foot[1] < x_top else \
            range(x_top, x_top - 300, -1)
        x_range_right = range(x_top, min(int(foot[0]), x_top + 300)) if foot[1] > x_top else \
            range(x_top, min(x_top + 300, im.shape[1] - 1))
        y_range = range(y_top, min(y_top + 300, int(foot[1])))
        sim_colors = []
        for y in y_range:
            x_left_max = first_point[1]
            x_right_max = first_point[1]
            if self.is_background(im[y][x_top]):
                break
            for x in x_range_left:
                if self.is_background(im[y][x]):
                    break
                if self.check_color_sim(im[y][x], im[first_point[0]][first_point[1]]) and x < x_left_max:
                    sim_colors.append((y, x))
                    x_left_max = x
            for x in x_range_right:
                if self.is_background(im[y][x]):
                    break
                if self.check_color_sim(im[y][x], im[first_point[0]][first_point[1]]) and x > x_right_max:
                    sim_colors.append((y, x))
                    x_right_max = x
        if foot[0] < x_top:
            return max(sim_colors, key = lambda x: x[1])
        return min(sim_colors, key=lambda x: x[1])


    def find_center(self):
        self.first_point = self.find_first_point(self.im)
        self.another_point = self.find_left_right_point(self.im, self.first_point, self.foot)
        self.center = (self.first_point[1], self.another_point[0])


    def get_distance(self):
        return np.math.hypot(self.foot[0] - self.center[0], self.foot[1] - self.center[1])

    def save_im(self):
        self.step += 1
        cv2.circle(self.im, (self.foot[0], self.foot[1]), 2, (0, 0, 255), 3)
        cv2.circle(self.im, (self.first_point[1], self.first_point[0]), 2, (255, 0, 0), 3)
        cv2.circle(self.im, (self.another_point[1], self.another_point[0]), 2, (0, 255, 0), 3)
        os.makedirs("./debug_images/", exist_ok=True)
        cv2.imwrite('./debug_images/step_'+str(self.step)+'.png', self.im)

