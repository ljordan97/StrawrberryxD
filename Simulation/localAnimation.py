import numpy as np
import time
import json
import socket
from vpython import *

def current_time(start_time):
    current_time = time.time() - start_time
    day = current_time // (24 * 3600)
    current_time = current_time % (24 * 3600)
    hour = current_time // 3600
    current_time %= 3600
    minutes = current_time // 60
    current_time %= 60
    seconds = round(current_time,3)
    return hour, minutes, seconds

def log(*args):
    t = current_time(start_time)
    print("%02d:%02d:%02.3f -" % (t[0],t[1],t[2]),' '.join(map(str, args)))

start_time = time.time()

#some constants
d1 = 1 #distance from point of instersection of R1's shaft axis w/ R2 shaft axis and REF ({0} to {1})
a2 = 6 #distance from {1} to end of R3's shaft {2}
a3 = 6 #distance from {2} shaft base of R4
d4 = 3 #distance from {3} to EE's eyeball {4}
REF = (np.array([0,0,0])).tolist() #define origin
fps = 25 #define FPS of animation

#short hand 90 deg conversion
d90 = np.pi/2

#Let user define final motor angles
def getFinalAngles():
    try:
        thetaOne = input('Input the final angle of Motor 1 in degrees: ')
    except:
        thetaOne = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)
    try:
        thetaTwo = input('Input the final angle of Motor 2 in degrees: ')
    except:
        thetaTwo = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)
    try:
        thetaThree = input('Input the final angle of Motor 3 in degrees: ')
    except:
        thetaThree = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)
    try:
        thetaFour = input('Input the final angle of Motor 4 in degrees: ')
    except:
        thetaFour = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)

    # convert input to float
    thetaOne = float(thetaOne)
    thetaTwo = float(thetaTwo)
    thetaThree = float(thetaThree)
    thetaFour = float(thetaFour)

    #sanitize input to limits of motor
    if (thetaOne > 90):   #max limit
        thetaOne = 90
    if (thetaOne < -90):  #min limit
        thetaOne = -90

    if (thetaTwo > 90):   #max limit
        thetaTwo = 90
    if (thetaTwo < -90):  #min limit
        thetaTwo = -90

    if (thetaThree > 90):   #max limit
        thetaThree = 90
    if (thetaThree < -90):  #min limit
        thetaThree = -90

    if (thetaFour > 90):   #max limit
        thetaFour = 90
    if (thetaFour < -90):  #min limit
        thetaFour = -90

    #convert to rads for ease of calculation with trig functions
    thetaOne = thetaOne * (np.pi/180)
    thetaTwo = thetaTwo * (np.pi / 180)
    thetaThree = thetaThree * (np.pi / 180)
    thetaFour = thetaFour * (np.pi / 180)

    return round(thetaOne, 2), round(thetaTwo, 2), round(thetaThree, 2), round(thetaFour, 2)

#let user define motor speeds
def getAngularVelocities():
    try:
        omegaOne = input('Input the speed of Motor 1 in degrees/sec: ')
    except:
        omegaOne = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)
    try:
        omegaTwo = input('Input the speed of Motor 2 in degrees/sec: ')
    except:
        omegaTwo = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)
    try:
        omegaThree = input('Input the speed of Motor 3 in degrees/sec: ')
    except:
        omegaThree = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)
    try:
        omegaFour = input('Input the speed of Motor 4 in degrees/sec: ')
    except:
        omegaFour = 0 #set a default value to acconut for misuse (yeah, you. feel bad.)

    # convert input to float
    omegaOne = float(omegaOne)
    omegaTwo = float(omegaTwo)
    omegaThree = float(omegaThree)
    omegaFour = float(omegaFour)

    #sanitize input to limits of motor
    if (omegaOne > 90):   #max limit
        omegaOne = 90
    if (omegaOne < -90):  #min limit
        thetaOne = -90

    if (omegaTwo > 90):   #max limit
        omegaTwo = 90
    if (omegaTwo < -90):  #min limit
        omegaTwo = -90

    if (omegaThree > 90):   #max limit
        omegaThree = 90
    if (omegaThree < -90):  #min limit
        omegaThree = -90

    if (omegaFour > 90):   #max limit
        omegaFour = 90
    if (omegaFour < -90):  #min limit
        omegaFour = -90

    #convert to rads for ease of calculation with trig functions
    omegaOne = omegaOne * (np.pi/180)
    omegaTwo = omegaTwo * (np.pi / 180)
    omegaThree = omegaThree * (np.pi / 180)
    omegaFour = omegaFour * (np.pi / 180)

    return round(omegaOne, 2), round(omegaTwo, 2), round(omegaThree, 2), round(omegaFour, 2)

#compute the current position of each frame given the current motor angles
def fwdKin(th1, th2, th3, th4):
    # compute current position for each frame
    ''' TRANSFORMATION MATRIX DEFINITIONS, all 4x4
    variable naming: TABCD
    T - transformation matrix
    A - starting frame
    B - next frame
    C - type of subtransformation (R for rotation, T for translation)
    D - if rotation, the axis of rotation
    '''

    ############################################
    # DEFINE TRANSFORMATION MATRIX COMPONENTS
    ############################################

    # TRANSFORMATION FROM {0} TO {1}
    # Z rotation by theta 1
    T01RZ = np.array([[np.cos(th1), -1 * np.sin(th1), 0, 0],
                      [np.sin(th1), np.cos(th1), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    # Z translation by d1
    T01TZ = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, d1],
                      [0, 0, 0, 1]])

    # X rotation by +90deg
    T01RX = np.array([[1, 0, 0, 0],
                      [0, np.cos(d90), -1 * np.sin(d90), 0],
                      [0, np.sin(d90), np.cos(d90), 0],
                      [0, 0, 0, 1]])

    # All together, (!!) function is binary, multiply in parts, ensure integrity of result
    temp = np.matmul(T01RZ, T01TZ)  # temp variable for two step matrix mult
    T01 = np.matmul(temp, T01RX)
    temp = 0  # reset temp for future use

    #############################################

    # TRANSFORMATION FROM {1} TO {2}
    # Z rotation by theta 2 + 90 degrees (variable is converted to rads)
    T12RZ = np.array([[np.cos(th2 + d90), -1 * np.sin(th2 + d90), 0, 0],
                      [np.sin(th2 + d90), np.cos(th2 + d90), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    # X translation by a2
    T12TX = np.array([[1, 0, 0, a2],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    # All together
    T12 = np.matmul(T12RZ, T12TX)

    #############################################

    # TRANSFORMATION FROM {2} TO {3}
    # Z rotation by theta 3
    T23RZ = np.array([[np.cos(th3), -1 * np.sin(th3), 0, 0],
                      [np.sin(th3), np.cos(th3), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    # X translation by a3
    T23TX = np.array([[1, 0, 0, a3],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    # X rotation by +90deg
    T23RX = np.array([[1, 0, 0, 0],
                      [0, np.cos(d90), -1 * np.sin(d90), 0],
                      [0, np.sin(d90), np.cos(d90), 0],
                      [0, 0, 0, 1]])

    # All together, (!!) function is binary, multiply in parts, ensure integrity of result
    temp = np.matmul(T23RZ, T23TX)  # temp variable for two step matrix mult
    T23 = np.matmul(temp, T23RX)
    temp = 0  # reset temp for future use

    #############################################

    # TRANSFORMATION FROM {3} TO {4}
    # Z rotation by theta 4
    T34RZ = np.array([[np.cos(th4), -1 * np.sin(th4), 0, 0],
                      [np.sin(th4), np.cos(th4), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    # Z translation by d4
    T34TZ = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, d4],
                      [0, 0, 0, 1]])

    # All together
    T34 = np.matmul(T34RZ, T34TZ)

    ############################################
    # COMPUTE COMPLETE TRANSFORMATION MATRIX
    ############################################
    # print('\nShow Transformation from 0 to 1 \n', np.round(T01,2))

    T02 = np.matmul(T01, T12)
    # print('\nShow Transformation from 0 to 2 \n', np.round(T02,2))
    # pack it up

    T03 = np.matmul(T02, T23)
    # print('\nShow Transformation from 0 to 3 \n', np.round(T03,2))

    T04 = np.matmul(T03, T34)
    # print('\nShow Transformation from 0 to 4 \n', np.round(T04,2))

    # extract position data from each transform
    R2 = [T01[0][3], T01[1][3], T01[2][3]]
    R3 = [T02[0][3], T02[1][3], T02[2][3]]
    R4 = [T03[0][3], T03[1][3], T03[2][3]]
    EE = [T04[0][3], T04[1][3], T04[2][3]]

    return T01, T02, T03, T04, R2, R3, R4, EE

#provide position vectors for each frame
def drawRobot(R1, R2, R3, R4, EE):
    #put points at each from location
    gREF = sphere(pos=vector(REF[0], REF[1], REF[2]), radius=0.2, color=color.white)
    gR2 = sphere(pos=vector(R2[0], R2[1], R2[2]), radius=0.2, color=color.white)
    gR3 = sphere(pos=vector(R3[0], R3[1], R3[2]), radius=0.2, color=color.white)
    gR4 = sphere(pos=vector(R4[0], R4[1], R4[2]), radius=0.2, color=color.white)
    gEE = sphere(pos=vector(EE[0], EE[1], EE[2]), radius=0.5, color=color.white)

    #define geometric center for each link, because vPython draws from center of shapes
    d1center = (gR2.pos + gREF.pos) / 2
    a2center = ((gR3.pos + gR2.pos)) / 2
    a3center = ((gR4.pos + gR3.pos)) / 2
    d4center = ((gEE.pos + gR4.pos)) / 2

    #draw links
    D1 = box(pos=d1center, axis=(gR2.pos - gREF.pos), length=d1, height=0.2, width=0.2, color=color.red)
    A2 = box(pos=a2center, axis=(gR3.pos - gR2.pos), length=a2, height=0.2, width=0.2, color=color.blue)
    A3 = box(pos=a3center, axis=(gR4.pos - gR3.pos), length=a3, height=0.2, width=0.2, color=color.green)
    D4 = box(pos=d4center, axis=(gEE.pos - gR4.pos), length=d4, height=0.2, width=0.2, color=color.yellow)

thetas = getFinalAngles()
omegas = getAngularVelocities()
frameInfo = fwdKin(thetas[0], thetas[1], thetas[2], thetas[3])
transforms = frameInfo[0:3]
framePositions = frameInfo[4:8]
drawRobot(REF, framePositions[0], framePositions[1], framePositions[2], framePositions[3])

#verify
print('Final angle 1, 2, 3, 4 [rad]: ', thetas[0], thetas[1], thetas[2], thetas[3])
print('Final speed 1, 2, 3, 4 [rad/s]: ', omegas[0], omegas[1], omegas[2], omegas[3])

#find out how many frames will complete the animation
timeOfMotion = [thetas[0]/omegas[0], thetas[1]/omegas[1], thetas[2]/omegas[2], thetas[3]/omegas[3]]
motorFrames = [timeOfMotion[0]*fps, timeOfMotion[1]*fps, timeOfMotion[2]*fps, timeOfMotion[3]*fps]
finalFrame = max(motorFrames)
print('Final frame: ', finalFrame)

#each loop is one frame
#get radians per frame, update theta by this amount per loop to animate
RpF = [(omegas[0]/fps), (omegas[1]/fps), (omegas[2]/fps), (omegas[3]/fps)]

#define current angle of each motor
motor1angle = 0
motor2angle = 0
motor3angle = 0
motor4angle = 0

#animate
currentFrame = 0 #loop counter
while currentFrame <= finalFrame:
    print(currentFrame)
    print(motor1angle, motor2angle, motor3angle, motor4angle)
    #move motors
    if motor1angle < thetas[0]:
        motor1angle += RpF[0]
    else:
        motor1angle = thetas[0]

    if motor2angle < thetas[1]:
        motor2angle += RpF[1]
    else:
        motor2angle = thetas[1]

    if motor3angle < thetas[2]:
        motor3angle += RpF[2]
    else:
        motor3angle = thetas[2]

    if motor4angle < thetas[3]:
        motor4angle += RpF[3]
    else:
        motor4angle = thetas[3]
    print
    # update forward kinematics
    frameInfo = fwdKin(motor1angle, motor2angle, motor3angle, motor4angle)
    transforms = frameInfo[0:3]
    framePositions = frameInfo[4:8]

    # update visualization
    drawRobot(REF, framePositions[0], framePositions[1], framePositions[2], framePositions[3])

    #go to next frame
    currentFrame += 1