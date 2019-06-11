from cam import *
from fish import *
import threading
import time

camera = camera()
fish_screen = fish_screen()

end_time = 15 * 60 * 60 # Ends the program at 15:00 (3:00 pm)

snapped = False

def thread_process(alarm_start):

    person = camera.snap() # 0 for left /// 1 for right

    fish_screen.update_AVOID_POINTS(alarm_start, person)

while True:

    time.sleep(0.03)
    seconds = int(time.time() % 10)

    if fish_screen.alarm is not None:
            
        t1 = threading.Thread(target=thread_process, args=(int(time.time()),))

        if t1.isAlive() is False: t1.join()

        if seconds % fish_screen.snap_interval is not 0: snapped = False
            
        elif seconds % fish_screen.snap_interval is 0 and snapped is False:
            
            snapped = True
            t1.start()

    fish_screen.update()

    if int(time.time()) is end_time: 
        camera.end_session()
        break
