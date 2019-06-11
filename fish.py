from pygame.locals import *
import math
import pygame
import random

entity_ar = []
WIDTH = 500
HEIGHT = 500

def distance(x, y, x1, y1):
	return math.sqrt((x - x1)**2 + (y - y1)**2)

def lerp(p, p1, factor):
	return ((p1 - p) * factor)

def reverse_lerp(p, p1, factor):
	return ((p1-p) // factor )

class point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class alarm:
	def __init__(self,start, time):
		self.start = start
		self.end = start + time

	def check(self):
		if int(time.time()) >= self.end: return True
		
		else: return False

class entity:
	def __init__(self, id):
		self.ID = id
		self.pos = point(random.randint(0, WIDTH), random.randint(0, HEIGHT))
		self.dest = point(random.randint(0, WIDTH),random.randint(0, HEIGHT))
		self.satisfaction_dist = 50
		self.speed = .03

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
		fish = entity(num)
		entity_ar.append(fish)

class fish_screen:

	def __init__(self):

		self.snap_interval = 3

		gen_entity(1)

		flags = DOUBLEBUF
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
		self.screen.set_alpha(None)

		self.alarm = None

	def update_AVOID_POINTS(self, second_time, val):

		alarm = alarm(int(time.time()), 10)
		
		if self.alarm is None:	
			self.alarm = alarm(int(time.time()), 10)

			for entity in entity_ar:
				entity.current_avoid = val
			
		elif second_time >= self.alarm.end:
			self.alarm.start = None
			self.alarm.end = None

			for entity in entity_ar:
				entity.current_avoid = None

	def update(self):

		for event in pygame.event.get():  
			if event.type == pygame.QUIT: 
				pygame.quit()

		self.screen.fill((155,155,155))

		if self.alarm is not None:
			if self.alarm.check() is True:
				for fish in entity_ar: fish.current_avoid = None

		for fish in entity_ar:
			if fish.at_dest() is False:
				if fish.current_avoid is None:
					fish.move(int(lerp(fish.pos.x, fish.dest.x, fish.speed)), 'x')
					fish.move(int(lerp(fish.pos.y, fish.dest.y, fish.speed)), 'y')

				else:
					fish.move(int(reverse_lerp(fish.pos.x, fish.avoid_ar[fish.current_avoid].x, "x")))
					fish.move(int(reverse_lerp(fish.pos.y, fish.avoid_ar[fish.current_avoid].y, "y")))
			else:
				fish.gen_new_dest()

			
		for fish in entity_ar:	
			if fish.current_avoid is not None:
				pygame.draw.rect(self.screen, (0,255,0),((fish.avoid_ar[fish.current_avoid].x, fish.avoid_ar[fish.current_avoid].y),(10,10)))

			pygame.draw.rect(self.screen, (255,255,255),((fish.pos.x, fish.pos.y),(10,10)))
			pygame.draw.rect(self.screen, (255,0,0),((fish.dest.x, fish.dest.y),(10,10)))

			pygame.display.update()
