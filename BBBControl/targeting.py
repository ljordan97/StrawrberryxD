import time
import math
import Adafruit_BBIO.GPIO as GPIO
from colorlabeler import RedMasker
import imutils
import cv2


####################################################
#               MOTOR INITIALIZATION               #
####################################################
stepPin1 = "P8_7"
dirPin1 = "P8_8"
stepPin2 = "P8_9"
dirPin2 = "P8_10"
stepPin3 = "P8_11"
dirPin3 = "P8_12"
stepPin4 = "P8_15"
dirPin4 = "P8_16"

GPIO.setup(stepPin1, GPIO.OUT)
GPIO.setup(dirPin1, GPIO.OUT)
GPIO.setup(stepPin2, GPIO.OUT)
GPIO.setup(dirPin2, GPIO.OUT)
GPIO.setup(stepPin3, GPIO.OUT)
GPIO.setup(dirPin3, GPIO.OUT)
GPIO.setup(stepPin4, GPIO.OUT)
GPIO.setup(dirPin4, GPIO.OUT)

steps_per_rev_big = 200
steps_per_rev_small = 200

####################################################
#               MOTOR CONTROL FUNCTIONS            #
####################################################
#R1, if direction is positive, motor moves clockwise
def stepR1(direction):
    degrees = 1.8
    rpm = 5

    #calculate seconds per step
    wait_time = 60.0/(steps_per_rev_big*rpm)

    #set direction
    if direction < 0:
        GPIO.output(dirPin1, GPIO.LOW)
    else:
        GPIO.output(dirPin1, GPIO.HIGH)

    #turn the motor on long enough to step once
    GPIO.output(stepPin1, GPIO.HIGH)
    time.sleep(wait_time)
    GPIO.output(stepPin1, GPIO.LOW)
    print("R1 Moved")


#R2, if direction is positive, motor moves clockwise
def stepR2(direction):
    degrees = 1.8
    rpm = 5

    wait_time = 60.0 / (steps_per_rev_big * rpm)

    # set direction
    if direction < 0:
        GPIO.output(dirPin2, GPIO.LOW)
    else:
        GPIO.output(dirPin2, GPIO.HIGH)

    # turn the motor on long enough to step once
    GPIO.output(stepPin2, GPIO.HIGH)
    time.sleep(wait_time)
    GPIO.output(stepPin2, GPIO.LOW)
    print("R2 Moved")

#R3, if direction is positive, motor moves clockwise
def stepR3(direction):
    degrees = 1.8
    rpm = 5

    wait_time = 60.0 / (steps_per_rev_big * rpm)

    # set direction
    if direction < 0:
        GPIO.output(dirPin3, GPIO.LOW)
    else:
        GPIO.output(dirPin3, GPIO.HIGH)

    # turn the motor on long enough to step once
    GPIO.output(stepPin3, GPIO.HIGH)
    time.sleep(wait_time)
    GPIO.output(stepPin3, GPIO.LOW)
    print("R3 Moved")

#R4, if direction is positive, motor moves clockwise
def stepR4(direction):
    degrees = 1.8
    rpm = 5

    wait_time = 60.0 / (steps_per_rev_big * rpm)

    # set direction
    if direction < 0:
        GPIO.output(dirPin4, GPIO.LOW)
    else:
        GPIO.output(dirPin4, GPIO.HIGH)

    # turn the motor on long enough to step once
    GPIO.output(stepPin4, GPIO.HIGH)
    time.sleep(wait_time)
    GPIO.output(stepPin4, GPIO.LOW)
    print("R4 Moved")

#########################################################
#           COMPUTER VISION FUNCTIONS AND VALUES        #
#########################################################
def detectStrawb():
    cap = cv2.VideoCapture(0)

    if not (cap.isOpened):
        print("Camera Not Open")
    ret, image = cap.read();
    # store a copy of the original image
    og_image = image.copy()
    # init redmasker
    rm = RedMasker()
    # call red mask function
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

    # show the intermediate steps. Comment these out if not debugging
    # cv2.imshow("Thresh", thresh)
    # cv2.imshow("Gray", gray)
    # cv2.imshow("Original", og_image)


    # find contours in the red-masked image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)


    #list to store circle values
    circle_x = 0
    circle_y = 0
    circle_radius = 0

    circle_element = [circle_x, circle_y, circle_radius]
    circles = [circle_element]

    #counter
    i = 0
    # for each of the contours in the image
    for c in cnts:
        if cv2.contourArea(c) > 15.0:
            # compute the center of the contour
            M = cv2.moments(c)
            # print(cv2.contourArea(c))
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            # find the min encosing circle for the contour
            (x, y), radius = cv2.minEnclosingCircle(c)
            # center of the mincircle
            center = [int(x), int(y)]
            # radius of min circle
            radius = int(radius)
            # text that we want to put for debugging
            #cir_text = str(radius)
            # print(cir_text)
            # print("Center: {}, {}".format(int(x),int(y)))
            img = cv2.circle(image, center, radius, (0, 255, 0), 2)
            circles[i] = [center[0], center[1], radius]
            i += 1

    return

#########################################################
#               CONTROL FUNCTIONS AND VALUES            #
#########################################################
#Closed loop feedback: need targets for x, y position of CV circle, and radius threshold before harvesting occurs
#define frame centers, radius threshold
x_center = 314
y_center = 230

#direction readability
CCW = -1
CW = 1

#default target values
x = 0
y = 0
radius = 0

#define initial x_err, target should appear at frame left, which means positive error
x_err = x_center - x
y_err = y_center - y

#due to motor resolution, exact alignment not possible. Allow for some level of error
acceptable_x_err = 10
acceptable_y_err = 10

#STEP 1: Rotate base until target is centered
def alignTargetHorizontally():
    while (x_err > acceptable_x_err):
        #1 step CCW
        stepR1(CCW)
        #get CV reading [x, y, radius]
        #define x_err = x_center - x

#STEP 2: begin approach
def approachTarget():

def snag():




