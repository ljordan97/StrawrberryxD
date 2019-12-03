from colorlabeler import RedMasker
import argparse
import imutils
import cv2

# command line argument parser
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to the input image")
cap = cv2.VideoCapture(0)
while(True):
	if not (cap.isOpened):
		print("Camera Not Open")
	ret, image = cap.read();
	#store a copy of the original image
	og_image = image.copy()
	#init redmasker
	rm = RedMasker()
	#call red mask function
	red_masked = rm.redmask(image)
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
			#print(cir_text)
			#print("Center: {}, {}".format(int(x),int(y)))
			img = cv2.circle(image,center,radius,(0,255,0),2)

			cv2.putText(image, cir_text, (int(x), int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

			# show the output image
			#cv2.namedWindow("CV", cv2.WND_PROP_FULLSCREEN)
			cv2.imshow("Image", image)
			#cv2.waitKey(0)
	cv2.waitKey(0)
