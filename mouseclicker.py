import pyautogui
import time
import random

from screenshoter import DistanceDetector

pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = 1

x_button = 550
y_button = 1200

pyautogui.click(x=x_button, y=y_button)

distance_detector = DistanceDetector()

while True:
    time.sleep(random.uniform(0.5, 2))
    distance_detector.screen_shoot()
    distance_detector.foot_detection()
    distance_detector.find_center()
    distance = distance_detector.get_distance()
    print('start clicking')
    pyautogui.dragTo(x=x_button, y=y_button, duration=distance*0.0018)
    print('released')