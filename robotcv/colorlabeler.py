import numpy as np
import cv2
#import init_color
class RedMasker:
	def redmask(self, image):

		#****NOTE**** Color in opencv is BGR not RGB
		#lower color  bounds
		#init_color.lower = [0, 0, 55]
		lower = [0, 0, 55]
		#upper color bounds
		#init_color.upper = [100, 76, 255]
		upper = [100, 76, 255]
		# create NumPy arrays from the boundaries
		#lower = np.array(init_color.lower, dtype = "uint8")
		#upper = np.array(init_color.upper, dtype = "uint8")
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)
		#show the output. Comment this line if running continously
		cv2.imshow("OUTPUT", output)

		return output
