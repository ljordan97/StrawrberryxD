The Strawrberry xD robot is a serial manipulator consisting of 4 revolute joints. The end effector
has a camera to sense strawberries using computer vision.

Sensing and actuation is done by a BeagleBone Black, with telemetry to offload any graphics 
processing to a remote device. 

General workflow:
Get camera data
Run CV algorithm to generate circles around each strawberry (target)
Selecting the leftmost target, the manipulator will orient itself to 
	make the target circle's centroid as close to the center of the frame as possible
Actuation will then occur to move straight towards the target
Reaquire camera data
Reprocess data through CV
Make position corrections as forward motion continues
When target circle reaches a threshold radius in the frame, begin rotation of the end effector 
	to harvest the strawberry (rotating right) 
Reset position and re-evaluate targets

 
Development is intended to be as modular as possible, with successful builds of smaller functions
being combined later


