from pygame.locals import *
import math
import pygame
import random

entity_ar = []
WIDTH = 500
HEIGHT = 500

def distance(self,x, y, x1, y1):
	return math.sqrt((x - x1)**2 + (y - y1)**2)

def lerp(self, p, p1, factor):
		return ((p1 - p) * factor)

class point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class entity:
	def __init__(self, id):
		self.ID = id
		self.pos = point(random.randint(0, WIDTH), random.randint(0, HEIGHT))
		self.dest = point(random.randint(0, WIDTH),random.randint(0, HEIGHT))
		self.satisfaction_dist = 50
		self.speed = .1

	def move(self, val, plane):
		if plane is "x":
			self.pos.x += val
		if plane is "y":
			self.pos.y += val

	def avoid(self, x, y):
		val = lerp(self.pos.x, x, self.speed)
		val1 = lerp(self.pos.y, y, self.speed)

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
		fish = entity(num)
		entity_ar.append(fish)

class fish_screen:

	def __init__(self):

		gen_entity(1)
		flags = DOUBLEBUF
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
		self.screen.set_alpha(None)

		self.AVOID_POINT = point(None, None)

	def update_avoid_point(self, x, y):
		self.AVOID_POINT = point(x,y)
		
	def update(self):
		
		for event in pygame.event.get():  
			if event.type == pygame.QUIT: 
				pygame.quit()

		for fish in self.entity_ar:

			if fish.at_dest() is not True:

				if (self.AVOID_POINT.x is not None) and (self.AVOID_POINT.y is not None):
					new_dest = fish.avoid(self.AVOID_POINT.x, self.AVOID_POINT.y)
					fish.move(new_dest.x , "x")
					fish.move(new_dest.y, "y")

				else:
					fish.move(int(lerp(fish.pos.x, fish.dest.x, fish.speed)), 'x')
					fish.move(int(lerp(fish.pos.y, fish.dest.y, fish.speed)), 'y')

			else:
				fish.gen_new_dest()

			self.screen.fill((155,155,155))
			
			if (self.AVOID_POINT.x is not None) and (self.AVOID_POINT.y is not None):
				pygame.draw.rect(self.screen, (0,255,0),((self.AVOID_POINT.x, self.AVOID_POINT.y),(10,10)))

			pygame.draw.rect(self.screen, (255,255,255),((fish.pos.x, fish.pos.y),(10,10)))
			pygame.draw.rect(self.screen, (255,0,0),((fish.dest.x, fish.dest.y),(10,10)))

			pygame.display.update()
