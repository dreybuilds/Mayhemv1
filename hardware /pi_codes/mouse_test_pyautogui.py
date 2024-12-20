import pyautogui
import time

# Move the mouse in a square pattern to check if the mouse is moving
pyautogui.moveTo(100, 100)
time.sleep(1)
pyautogui.moveTo(200, 200)
time.sleep(1)
pyautogui.moveTo(100, 200)
time.sleep(1)
pyautogui.moveTo(200, 100)
time.sleep(1)

print("Mouse moved successfully.")
