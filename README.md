# str-projector-display

# -Fish:
#  -Draws fish on screen via blit, and jpeg files
#  -While in a neutral state (ie: there is not a peron seen) the fish(s) swim around randomly.
#  -If there is a person seen through cam.py , the randomly generated avoid point is swapped out for a choice of two points (0,HEIGHT/2|WIDTH, HEIGHT/2)
#  -The fish seem to be swimming by using a cycle of images, chosen based on the previous fish_image

# -Cam:
#  -Using openCV the program interacts with the webcam
#  -Using the webcam, every time cam.py is called an image is produces. This image is processed using a method seen in *link*, the         #  -resulting output, is an x,y,w,h object that represents the largest person detected on the screen.

# -Main:
#  -Compiles fish.py, and cam.py.
#  -Using multi-threading main.py draws the fish constantly be within a seperate thread checks for people at a set incrememnt using            time.sleep(var).
