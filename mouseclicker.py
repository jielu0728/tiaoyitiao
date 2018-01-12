import pyautogui
import time

pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = 1

x_button = 550
y_button = 1200

pyautogui.click(x=x_button, y=y_button)

while True:
    time.sleep(2)
    print('start clicking')
    pyautogui.dragTo(x=x_button, y=y_button, duration=0.5)
    print('released')