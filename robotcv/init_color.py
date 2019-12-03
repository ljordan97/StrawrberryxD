#from colorlabeler import RedMasker
import argparse
import imutils
import cv2
lower = [3, 3, 220]
upper = [125, 132, 255]
import numpy as np
def redmask(image, low, up):

	#****NOTE**** Color in opencv is BGR not RGB
	#lower color  bounds
	#init_color.lower = [0, 0, 55]
	#lower = [0, 0, 55]
	#upper color bounds
	#init_color.upper = [100, 76, 255]
	#upper = [100, 76, 255]
	# create NumPy arrays from the boundaries
	#lower = np.array(init_color.lower, dtype = "uint8")
	#upper = np.array(init_color.upper, dtype = "uint8")
	lower = np.array(low, dtype = "uint8")
	upper = np.array(up, dtype = "uint8")
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)
	#show the output. Comment this line if running continously
	cv2.imshow("OUTPUT", output)

	return output

# command line argument parser
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to the input image")
#args = vars(ap.parse_args())
cap = cv2.VideoCapture(0)
while(True):
	#image = cv2.imread(args["image"])
	if not(cap.isOpened()):
		print("Camera not open")
	ret, image = cap.read();

	#store a copy of the original image
	og_image = image.copy()
	#init redmasker
	#rm = RedMasker()
	#call red mask function
	red_masked = redmask(image, lower, upper)
	# grab the image and resize to be smaller so that
	# the shapes can be approximated better
	resized = imutils.resize(red_masked, width=300)
	ratio = image.shape[0] / float(resized.shape[0])
	# blur the resized image slightly, then convert it to both
	# grayscale and the L*a*b* color spaces
	blurred = cv2.GaussianBlur(resized, (5, 5), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
	thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]

	#show the intermediate steps. Comment these out if not debugging
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Gray", gray)
	#cv2.imshow("Original", og_image)



	# find contours in the red-masked image
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# for each of the controus in the image
	for c in cnts:
		if cv2.contourArea(c) > 15.0:
			# compute the center of the contour
			M = cv2.moments(c)
			#print(cv2.contourArea(c))
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)

			# multiply the contour (x, y)-coordinates by the resize ratio,
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			#find the min encosing circle for the contour
			(x,y),radius = cv2.minEnclosingCircle(c)
			#center of the mincircle
			center = (int(x),int(y))
			#radius of min circle
			radius = int(radius)
			#text that we want to put for debugging
			cir_text = str(radius)
			#height, width, channels = thresh.shape
			#print(height, width, channels)
			print("Radius" + cir_text)
			print("Center: {}, {}".format(int(x),int(y)))
			img = cv2.circle(image,center,radius,(0,255,0),2)

			cv2.putText(image, cir_text, (int(x), int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

			# show the output image
			#cv2.namedWindow("CV", cv2.WND_PROP_FULLSCREEN)
			cv2.imshow("Image", image)
			#cv2.waitKey(0)

	key = cv2.waitKey(0)

	if key == ord('r'):
		lower = [lower[0], lower[1], lower[2] +1]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('g'):
		lower = [lower[0], lower[1]+1, lower[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('b'):
		lower = [lower[0] + 1, lower[1], lower[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('1'):
		upper = [upper[0] , upper[1], upper[2] +1]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('2'):
		upper = [upper[0], upper[1]+1, upper[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('3'):
		upper = [upper[0] + 1, upper[1], upper[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('4'):
		lower = [lower[0], lower[1], lower[2]-1]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('5'):
		lower = [lower[0], lower[1]-1, lower[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('6'):
		lower = [lower[0]-1, lower[1], lower[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('7'):
		upper = [upper[0] , upper[1], upper[2]-1]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('8'):
		upper = [upper[0], upper[1]-1, upper[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('9'):
		upper = [upper[0]-1, upper[1], upper[2]]
		print("lower ", lower)
		print("upper ", upper)
	elif key == ord('q'):
		print("lower ", lower)
		print("upper ", upper)
		break
	#cv2.waitKey(0)
	else:
		continue
cap.release()
cv2.destroyAllWindows()
