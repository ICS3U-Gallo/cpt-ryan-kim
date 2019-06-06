from imutils.object_detection import non_max_suppression
from imutils import paths
from cv2 import *
import numpy as np
import imutils
from datetime import *

class camera:
	
	def __init__(self):
		self.cam = VideoCapture(0)
		ret = self.cam.set(3,420)
		ret = self.cam.set(4,240)

		self.start_time = datetime.now()

		self.hog = cv2.HOGDescriptor()
		self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	def max_body_seen(self, pick):
		max = 0

		for i in range(len(pick)):
			if pick[i][2] * pick[i][3] > pick[max][2] * pick[max][3]:
				max = i
		
		return max

	def snap(self):
		r, image = self.cam.read()

		if r:

			image = imutils.resize(image, width=image.shape[1])
			rects, weights = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

			rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
			pick = non_max_suppression(rects,probs=None, overlapThresh=0.65)
			
			index_of_max = self.max_body_seen(pick) 
			
			if pick is []:
				return None
			else:
				print(pick)
				return pick[index_of_max][0] + pick[index_of_max][2], pick[index_of_max][1] + pick[index_of_max][3]
			
		else:
			return -1

	def end_session(self):
		print(f"Started at --> {self.start_time} \n Ended at --> {datetime.now()}")
		cam.release()
