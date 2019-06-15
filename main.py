from sub_modules import alarm
from fish import *

import cv2
import numpy as np

import threading
import time

cap = cv2.VideoCapture(0)

cap.set(3,420)
cap.set(4,240)

fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

fish_screen = fish_screen()

end_time = 15 * 60 * 60 # Ends the program at 15:00 (3:00 pm)


class compile:
    def __init__(self):
        self.alarm = None

    def session(self):

        while True:
            
            ret, frame = cap.read()
            fgmask = fgbg.apply(frame)
            
            cv2.imshow("cam",fgmask)
            if self.alarm is None:
                t1 = threading.Thread(target=fish_screen.update_AVOID_POINTS, args=(fgmask,))
                t1.start()

                self.alarm = alarm(int(time.time()), 2)

            elif self.alarm is not None:
                if self.alarm.check() and t1.isAlive() is False: 
                    self.alarm = None   
                    t1.join()

            cv2.waitKey(1)
            fish_screen.update()

            if int(time.time()) is end_time: 

                break

run = compile()

run.session()

cap.release()
