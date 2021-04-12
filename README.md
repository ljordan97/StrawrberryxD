**The Strawrberry xD robot** is a serial manipulator consisting of 4 revolute joints. The end effector
has a camera to sense strawberries using computer vision.

Sensing and actuation is processed and controlled by a BeagleBone Black dev board, with telemetry to offload any graphics 
processing to a remote device. 

######State Machine:
 * Get camera data
 * Run the OpenCV strawberry recognition algorithm  (target acquisition)
 * Selecting the leftmost target, the manipulator will orient itself to 
	make the target circle's centroid as close to the center of the camera frame as possible
 * Actuation will then occur to move straight towards the target
 * Reaquire camera data
 * Reprocess data through CV
 * Make position corrections as forward motion continues
 * When target circle reaches a threshold radius in the frame, begin rotation of the end effector 
	to harvest the strawberry (rotating right) 
 * Reset position and re-evaluate targets

 
Development is intended to be as modular as possible, with additional functionalities rolled out over time.
