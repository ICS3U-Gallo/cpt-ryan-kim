from pygame.locals import *
from cam import pedestrian_detector
from sub_modules import *
import pygame
import random

entity_ar = []
WIDTH = 500
HEIGHT = 500

class entity:
	def __init__(self):
		self.pos = point(random.randint(0, WIDTH), random.randint(0, HEIGHT))
		self.dest = point(random.randint(0, WIDTH),random.randint(0, HEIGHT))
		self.satisfaction_dist = 50
		self.speed = .03
		self.run_speed = 10

		self.avoid_ar = [point(0, HEIGHT//2), point(WIDTH, HEIGHT//2)]
		self.current_avoid = None

	def move(self, val, plane):
		if plane is "x":
			self.pos.x += val
		if plane is "y":
			self.pos.y += val

	def avoid(self, x, y):
		val = reverse_lerp(self.pos.x, x, self.speed)
		val1 = reverse_lerp(self.pos.y, y, self.speed)

		return point(-val, -val1)

	def gen_new_dest(self):
		self.dest.y = random.randint(0,HEIGHT)
		self.dest.x = random.randint(0,WIDTH)

	def at_dest(self):
		if distance(self.pos.x, self.pos.y, self.dest.x, self.dest.y) <= self.satisfaction_dist:
			return True
		else:
			return False

def gen_entity(count):
	for num in range(count):
		fish = entity()
		entity_ar.append(fish)

class fish_screen:
	def __init__(self):
		gen_entity(1)

		flags = DOUBLEBUF
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
		self.screen.set_alpha(None)

	def restrict_pos(self,ar):

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
		
		ped = pedestrian_detector(reduced_img)

		if ped.left_sum >= ped.density_thresh and ped.right_sum >= ped.density_thresh:
			for entity in entity_ar:
				entity.current_avoid = max(ped.left_sum, ped.right_sum)

		else:
			for entity in entity_ar:
				entity.current_avoid = None
			
	def update(self):

		for event in pygame.event.get():  
			if event.type == pygame.QUIT: 
				pygame.quit()

		self.screen.fill((155,155,155))

		for fish in entity_ar:
			if fish.at_dest() is False:
				if fish.current_avoid is None:
					fish.move(int(lerp(fish.pos.x, fish.dest.x, fish.speed)), 'x')
					fish.move(int(lerp(fish.pos.y, fish.dest.y, fish.speed)), 'y')

				else:
					_x , _y = equadistant_point(fish.pos.x, fish.pos.y, fish.avoid_ar[fish.current_avoid].x, fish.avoid_ar[fish.current_avoid].y , .01)

					fish.move(int(lerp(fish.pos.x, _x, fish.run_speed)),  "x")
					fish.move(int(lerp(fish.pos.y, _y, fish.run_speed)), "y")
			else:
				fish.gen_new_dest()
		
		self.restrict_pos(entity_ar)

		for fish in entity_ar:	
			if fish.current_avoid is not None:
				pygame.draw.rect(self.screen, (0,255,0),((fish.avoid_ar[fish.current_avoid].x, fish.avoid_ar[fish.current_avoid].y),(10,10)))
			pygame.draw.rect(self.screen, (255,255,255),((fish.pos.x, fish.pos.y),(10,10)))
			pygame.draw.rect(self.screen, (255,0,0),((fish.dest.x, fish.dest.y),(10,10)))

			pygame.display.update()
