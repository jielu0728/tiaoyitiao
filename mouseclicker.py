import pyautogui
import time
import random

from screenshoter import DistanceDetector

pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = 1

x_button = 290+66
y_button = 470+450

pyautogui.click(x=x_button, y=y_button)

distance_detector = DistanceDetector()

while True:
    x_button = random.uniform(300,400)
    y_button = random.uniform(700,950)
    time.sleep(random.uniform(0.5, 2))
    distance_detector.screen_shoot()
    distance_detector.foot_detection()
    distance_detector.find_center()
    distance = distance_detector.get_distance()
    distance_detector.save_im()
    print('start clicking')
    pyautogui.moveTo(x=x_button, y=y_button)
    pyautogui.dragTo(x=x_button, y=y_button, duration=distance * 0.0024)
    print('released')
