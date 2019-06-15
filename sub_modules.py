import numpy as np
import time
import math

class alarm:
	def __init__(self,start, time):
		self.start = start
		self.end = start + time

	def check(self):
		if int(time.time()) >= self.end: return True
		
		else: return False

class point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

#!~!~~!~!~!~!~! note: this is code from the internet (lines 20-26)
def split(array, nrows, ncols): 
    """Split a matrix into sub-matrices."""

    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols))

def equadistant_point(x, y, x1, y1, factor):
	""" Return an equadistant point times a factor in the opposite direction."""

	delta_x = x - x1
	delta_y = y - y1

	return x + delta_x * factor, y - delta_y  * factor

def distance(x, y, x1, y1):
	return math.sqrt((x - x1)**2 + (y - y1)**2)

def lerp(p, p1, factor):
	return ((p1 - p) * factor)

def reverse_lerp(p, p1, factor):
	return -(factor // (p1-p))

def max(num, num1):

    if num > num1:
        return 0
    
    else:
        return 1
