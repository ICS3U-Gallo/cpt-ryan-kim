from sub_modules import split
import numpy as np

class pedestrian_detector:
	def __init__(self, img):

		self.ar = img

		self.density_thresh = 138465.0

		self.left_sum = 0
		self.right_sum = 0

		self.sum_thread = np.sum(self.ar, axis=0)

		half_count = len(self.sum_thread) // 2

		for row_sum in range(len(self.sum_thread)):

			if row_sum <= half_count:
				self.left_sum += self.sum_thread[row_sum]
			
			else:
				self.right_sum += self.sum_thread[row_sum]

		print(self.left_sum, self.right_sum)
