from sub_modules import alarm
from fish import *

import cv2
import numpy as np
import threading
import time

#Create a camera object, and set the width to 420 and the height 240 (420x240 pixels)
cap = cv2.VideoCapture(0)
cap.set(3,420)
cap.set(4,240)

#Intialize a background subtraction object
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

#Intialize a screen object
fish_screen = fish_screen()

#Set it so the program automatically exits at 3:00pm
end_time = 15 * 60 * 60


class compile:
    def __init__(self):
        self.alarm = None

    def session(self):

        while True:
            
            #Read an image from the camera, and apply background reduction
            ret, frame = cap.read()
            fgmask = fgbg.apply(frame)
            
            #(OPTIONAL) show the reduced image
            cv2.imshow("cam",fgmask)
            
            #If there is no alarm, i.e: no up-to-date point for fish to avoid
            if self.alarm is None:

                #Initialize a thread object with the target function "update_AVOID_POINTS", and give the reduced image as input
                t1 = threading.Thread(target=fish_screen.update_AVOID_POINTS, args=(fgmask,))

                #Run the thread
                t1.start()

                #Fill the self.alarm variable with an alarm object representing the begining of the alarm, and the time it will take to elapse (2 seconds)
                self.alarm = alarm(int(time.time()), 2)

            #If there is a thread currently out.....
            elif self.alarm is not None:
                
                #Check alarm time has elapsed.....
                if self.alarm.check(): 
                    self.alarm = None 
                
                #Check if the thread is still computing.....
                if t1.isAlive() is False:  
                    t1.join()

            #(OPTIONAL) waitKey method is used for the displaying of the reduced image
            cv2.waitKey(1)

            #Calls the update method from fish.py to draw the fish
            fish_screen.update()

            #Check if the progam schedule has been satisified and should the loop be broken
            if int(time.time()) is end_time: 
                break

#Initalize a compiler object
run = compile()

#Run the session
run.session()

#Release the camera one the session has been exited
cap.release()
