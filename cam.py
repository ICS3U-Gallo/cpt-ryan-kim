import numpy as np

class pedestrian_detector:
	def __init__(self, img):

		self.ar = img

		#The miniumum pixel activity sum required for a "person" to be in frame on one side of the camera
		self.density_thresh = 138465.0

		#Variables for the sum of the left and right pixel movment
		self.left_sum = 0
		self.right_sum = 0

		#Numpy sum method sums all the columns, and returns a new array or one-dimension
		self.sum_thread = np.sum(self.ar, axis=0)

		#The half way point of the image, used to differenciate between left side and right side of the image
		half_count = len(self.sum_thread) // 2

		#Add to the left or right side based on the half_count
		for row_sum in range(len(self.sum_thread)):

			if row_sum <= half_count:
				self.left_sum += self.sum_thread[row_sum]
			
			else:
				self.right_sum += self.sum_thread[row_sum]
