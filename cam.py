import numpy as np

class pedestrian_detector:
    def __init__(self, img):

        self.whites = []
        self.pixel_spacing = 10
		self.thresh = 200
        self.matrix = img

        self.pathway = {"x": 0,
                        "y": 30,
                        "x1": len(self.matrix),
                        "y1":250}

        for r in range(0,len(self.matrix)), self.pixel_spacing:
            for c in range(0,len(self.matrix[r]),self.pixel_spacing):

                pixel = matrix[r][c] 

                if pixel is (255,255,255):
                    if r - self.pixel_spacing >= 0 and c - self.pixel_spacing >= 0:
                        if self.matrix[r -self.pixel_spacing][c -self.pixel_spacing] is (255,255,255):
                            if c >= self.pathway["x"] and c <= self.pathway["x1"] and r >= self.pathway["y1"] and r <= self.pathway["y"]:

                                self.whites.append([c,r])

    def snap(self):
        for pair in self.whites:
            left_count = 0
            right_count = 0

            if pair[0] >= len(self.matrix)//2:
                right_count += 1
            
            else:
                left_count += 1

			if left_count <= self.thresh and right_count <= self.thresh:
				return None

            if left_count > right_count:
                return 0
            
            else:
                return 1
