# -Instructions:
#to compile simply run the main.py file.

# -Required modules:
#-Numpy
#-OpenCV
#-Pygame
#-time
#-random
#-math
#-threading
  
# -Required Equipment:
#-Camera
#-Screen (projector, or otherwise)
  
# -Quality of life adjustments:
#-If the envirment detected through your camera is highyl vaiable, increase pedestrian_detector.density_thresh
#-If you find that the fish run towards you, within sub_modules --> max(). Switch the return statments 1 -> 0 and 0 -> 1

# -Code Explaination:

#   Within the main.py file, all the seperate files are compiled. fish.py controls the movement and drawing of the fishs, img_transform.py contains an class (pedestrian detector) that takes in a black and white image, and computes the ratio of black and white on the left and right sides of the camera view (self.left_sum & self.right_sum), sub_modules.py contains all the little functions that should not be floating around in the specific files (functions include: distance, lerp, etc).

#   Main.py explaination 
--> Firstly within the session method, the camera takes a photo every iteration, and applies a background reduction not only updating the fgbg object to increase background accuracy, but also to have a picture in memory for when a thread needs to be started.

--> Secondly there is a system of alarms using the time module. The system exists so that a new thread can be created every certain period, the system checks if there is an existing alarm, if not it creates one and initializes a thread to transform the black and white image into a 0,1, or None stating the side of the camera where a person is present if any at all. If the alarm timer has expired after N seconds then a new alarm is started an in term a new thread.

--> Lastly fish_screen.update() is called to draw the fish at the approprate locations, compute a new location for their food if need be, and run away from the person if they are seen through the camera.
