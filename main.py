from cam import *
from fish import *
import threading
import time

camera = camera()

fish_screen = fish_screen()

step = 0
step_cap = 100

while True:

    t1 = threading.Thread(target=fish_screen.update_avoid_point(camera.snap())) 
    t1.start()
    t1.join()

    fish_screen.update()

    if step is step_cap: 
        camera.end_session
        break
    step += 1
