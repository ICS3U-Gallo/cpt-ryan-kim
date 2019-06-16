import numpy as np
import time
import math

class alarm:
	def __init__(self,start, time):
		"""Create an end time for the alarm.check() method to compare to"""

		self.start = start
		self.end = start + time

	def check(self):
		"""Check the current time against the end time of the alarm object"""
		if int(time.time()) >= self.end: return True
		
		else: return False

class point:
	def __init__(self,x,y):
		"""Used for easy storage of an x,y point pair"""

		self.x = x
		self.y = y

def equadistant_point(x, y, x1, y1, factor):
	""" Return an equadistant point times a factor in the opposite direction."""

	delta_x = x - x1
	delta_y = y - y1

	return x + delta_x * factor, y - delta_y  * factor

def distance(x, y, x1, y1):
	"""Simple distnce, requiring 2 point pairs"""

	return math.sqrt((x - x1)**2 + (y - y1)**2)

def lerp(p, p1, factor):
	"""distance of a singe point pair, x, x1 or y, y1 multiplied by a factor""" 

	return ((p1 - p) * factor)

def max(num, num1):
	"""find the largest of a pair on numbers"""

    if num > num1:
        return 0
    
    else:
        return 1
