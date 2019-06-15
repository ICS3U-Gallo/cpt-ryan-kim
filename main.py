import cv2
import numpy as np
from cam import *
from fish import *
import threading
import time

cap = cv2.VideoCapture(0)

cap.set(3,420)
cap.set(4,240)

fgbg = cv2.createBackgroundSubtractorMOG2()

fish_screen = fish_screen()

end_time = 15 * 60 * 60 # Ends the program at 15:00 (3:00 pm)

class alarm:
	def __init__(self,start, time):
		self.start = start
		self.end = start + time

	def check(self):
		if int(time.time()) >= self.end: return True
		
		else: return False

class compile:
    def __init__(self):
        self.alarm = None

    def session(self):

        while True:

            time.sleep(0.03)
            
            ret, frame = cap.read()
            fgmask = fgbg.apply(frame)

            if self.alarm is None:
                t1 = threading.Thread(target=fish_screen.update_AVOID_POINTS, args=(fgmask,))
                t1.start()

                self.alarm = alarm(int(time.time()), 2)

            elif self.alarm is not None:
                if t1.isAlive() is False: t1.join()

                if self.alarm.check(): self.alarm = None   

            fish_screen.update()

            if int(time.time()) is end_time: 

                break

run = compile()

run.session()

cap.release()
