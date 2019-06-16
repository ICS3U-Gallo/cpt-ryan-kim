from pygame.locals import *
from cam import pedestrian_detector
from sub_modules import *
import pygame
import random

#Initialize an array for all the fish objects to be stored into
entity_ar = []

#The pygame screen is 500x500 pixels
WIDTH = 500
HEIGHT = 500

class entity:
	def __init__(self):

		#The fish starts a random location and runs to a random locations
		self.pos = point(random.randint(0, WIDTH), random.randint(0, HEIGHT))
		self.dest = point(random.randint(0, WIDTH),random.randint(0, HEIGHT))

		#The fish must come within the satisfaction_dist before generating a new point to chase
		self.satisfaction_dist = 50

		#Define the speeds that the fishs will run away at, and chase
		self.chase_speed = .03
		self.run_speed = 10

		#The two avoid points are preset for people approaching from the left, or from the right
		self.avoid_ar = [point(0, HEIGHT//2), point(WIDTH, HEIGHT//2)]

		#A bool representing the status of people on the screen (there, or not there?)
		self.current_avoid = None

	def move(self, val, axis):
		"""In put a force to apply to the fish, and the axis upon which to move it"""

		if axis is "x":
			self.pos.x += val
		if asix is "y":
			self.pos.y += val

	def gen_new_dest(self):
		"""This method is only called when the past destination was hit, and a new point my be generated"""

		self.dest.y = random.randint(0,HEIGHT)
		self.dest.x = random.randint(0,WIDTH)

	def at_dest(self):
		"""This method is called to check if the fish is at the chase point"""

		if distance(self.pos.x, self.pos.y, self.dest.x, self.dest.y) <= self.satisfaction_dist:
			return True
		else:
			return False

def gen_entity(count):
	"""This method is used to intialize the fish objects"""

	for num in range(count):
		fish = entity()
		entity_ar.append(fish)

class fish_screen:
	def __init__(self):

		gen_entity(1)

		#Initialize pygame screen instance
		flags = DOUBLEBUF
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
		self.screen.set_alpha(None)

	def restrict_pos(self,ar):
		"""This method restrict the position of the fish to a little bit off the drawable screen"""

		for fish in ar:
			if fish.pos.x <= -300:
				fish.pos.x = -300
			elif fish.pos.x >= WIDTH + 300:
				fish.pos.x = WIDTH + 300
			
			if fish.pos.y <= -300:
				fish.pos.y = -300

			elif fish.pos.y >= HEIGHT + 300:
				fish.pos.y = HEIGHT + 300

	def update_AVOID_POINTS(self, reduced_img):
		"""This method is computed within a sub-thread, to prevent bottle-necking"""

		#Initalize a pedestrian_detection object
		ped = pedestrian_detector(reduced_img)

		#Within the ped object there are left_sum and right_sum, variables representing the sum of active non-background pixels on the left and right side of the camera
		#These sums are compaired to check wether they meet the cut-off for ambient shifts in light, resulting in misleading background reduction
		if ped.left_sum >= ped.density_thresh and ped.right_sum >= ped.density_thresh:

			#Set the current avoid point for the fishes to the greater of the two sums
			for entity in entity_ar:
				entity.current_avoid = max(ped.left_sum, ped.right_sum)

		#If the sums do not pass the miniumum requirement there is no avoid points for the fish
		else:
			for entity in entity_ar:
				entity.current_avoid = None
			
	def update(self):
		"""The general update function for the math, protaining to fish movment, and drawing"""

		#If the window is closed, exit the session
		for event in pygame.event.get():  
			if event.type == pygame.QUIT: 
				pygame.quit()

		self.screen.fill((155,155,155))


		for fish in entity_ar:
			
			#If the fish are still too far from their target....
			if fish.at_dest() is False:

				#If there is no one seen through the camera
				if fish.current_avoid is None:
					fish.move(int(lerp(fish.pos.x, fish.dest.x, fish.chase_speed)), 'x')
					fish.move(int(lerp(fish.pos.y, fish.dest.y, fish.chase_speed)), 'y')

				#If there is....
				else:

					#Generate an equadistant point from the person, and the fish but in the opposite direction
					_x , _y = equadistant_point(fish.pos.x, fish.pos.y, fish.avoid_ar[fish.current_avoid].x, fish.avoid_ar[fish.current_avoid].y , .01)

					#Move the fish in the direction of the person
					fish.move(int(lerp(fish.pos.x, _x, fish.run_speed)),  "x")
					fish.move(int(lerp(fish.pos.y, _y, fish.run_speed)), "y")
			
			#If the fish are at the chosen destintion
			else:
				fish.gen_new_dest()
		
		self.restrict_pos(entity_ar)

		#Draw the fish, the fish chasing point, and if there is a person draw the point the fish are running away from
		for fish in entity_ar:	
			if fish.current_avoid is not None:
				pygame.draw.rect(self.screen, (0,255,0),((fish.avoid_ar[fish.current_avoid].x, fish.avoid_ar[fish.current_avoid].y),(10,10)))
			pygame.draw.rect(self.screen, (255,255,255),((fish.pos.x, fish.pos.y),(10,10)))
			pygame.draw.rect(self.screen, (255,0,0),((fish.dest.x, fish.dest.y),(10,10)))

			pygame.display.update()
