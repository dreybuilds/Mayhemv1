from pynput.mouse import Controller
import time

mouse = Controller()

# Move mouse in a square pattern to check if the mouse is moving
mouse.position = (100, 100)
time.sleep(1)
mouse.position = (200, 200)
time.sleep(1)
mouse.position = (100, 200)
time.sleep(1)
mouse.position = (200, 100)
time.sleep(1)

print("Mouse moved successfully.")
