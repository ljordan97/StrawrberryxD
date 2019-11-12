##################################################
#
 #       WHAT UP ITS YA BOI LEVI CODING THIS OFF WAY TOO LITTLE SLEEP
  #          COMIN TO YOU LIVE WITH A LIL SUM I COOKED UP 
 #       YALL GONNA LOVE THIS JOINT(S) FR
#            SO JUST LET THE RICO NASTY BUMP AND SMASH THAT MF RUN BUTTON
#
##################################################
import numpy as np
import time
import json
import socket
#np.set_printoptions(precision=2)

################################SERVER SETUP STUFF######################################
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

ip = "0.0.0.0"      # 0.0.0.0 will make the server accessable on all network interfaces (wifi and ethernet)
port = 2442         # Port to run server on

start_time = time.time()    # Record start time for logging

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Setup UDP Communication
socket.bind((ip, port))

print("Bound to IP:  ",ip,"\n\t Port:",port)
print("\nServer running!")

#ITERATABLE DICTIONARY OF DATA FOR CLIENT TO REQUEST
#currently contains all the frame positions, will update with vectors to define rotated coordinate frames at each
#swag.enlarge()
data = {
      "ref": 1,
      "t01": 2,
      "t02": 3,
      "t03": 4,
      "t04": 5,
      "ee": 6,
      "d1": 7,
      "a2": 8,
      "a3": 9,
      "d4": 10,
      "th1": 11,
      "th2": 12,
      "th3": 13,
      "th4": 14
    }
######################################################################################


#REFERENCE FRAME DEFINED AS THE CENTER OF THE BASE OF R1'S SHAFT
REF = np.array([0,0,0]) #define origin

#CHANGE ME: input angles of each revolute joint
#ANGLE UNITS DEGREES
#TODO: DEFINE JOINT LIMITS
th1deg = 90 #R1
th2deg = 90 #R2
th3deg = 90 #R3
th4deg = 90 #R4

#convert user input angles to rads for numpy ease
th1 = th1deg*(np.pi/180)
th2 = th2deg*(np.pi/180)
th3 = th3deg*(np.pi/180)
th4 = th4deg*(np.pi/180)

#short hand 90 deg conversion
d90 = np.pi/2

#CHANGE ME: LENGTHS OF FRAME OFFSETS
#DISTANCE UNITS = INCHES
d1 = 1 #distance from point of instersection of R1's shaft axis w/ R2 shaft axis and REF ({0} to {1})
a2 = 6 #distance from {1} to end of R3's shaft {2}
a3 = 6 #distance from {2} shaft base of R4
d4 = 3 #distance from {3} to EE's eyeball {4}

data["d1"] = d1
data["a2"] = a2
data["a3"] = a3
data["d4"] = d4

data["th1"] = th1deg
data["th2"] = th2deg
data["th3"] = th3deg
data["th4"] = th4deg

''' TRANSFORMATION MATRIX DEFINITIONS, all 4x4
variable naming: TABCD  
T - transformation matrix
A - starting frame
B - next frame
C - type of subtransformation (R for rotation, T for translation)
D - if rotation, the axis of rotation
'''

############################################
#DEFINE TRANSFORMATION MATRIX COMPONENTS
############################################

#TRANSFORMATION FROM {0} TO {1}
#Z rotation by theta 1
T01RZ = np.array([[np.cos(th1), -1*np.sin(th1), 0, 0],
                  [np.sin(th1),    np.cos(th1), 0, 0],
                  [          0,              0, 1, 0],
                  [          0,              0, 0, 1]])
 
#Z translation by d1
T01TZ = np.array([[1, 0, 0, 0], 
                  [0, 1, 0, 0],
                  [0, 0, 1,d1],
                  [0, 0, 0, 1]])
        
#X rotation by +90deg
T01RX = np.array([[1,           0,              0, 0],
                  [0, np.cos(d90), -1*np.sin(d90), 0],
                  [0, np.sin(d90),    np.cos(d90), 0],
                  [0,           0,              0, 1]])
        
#All together, (!!) function is binary, multiply in parts, ensure integrity of result
temp = np.matmul(T01RZ, T01TZ)   #temp variable for two step matrix mult
T01 = np.matmul(temp, T01RX)
temp = 0                         #reset temp for future use

#############################################

#TRANSFORMATION FROM {1} TO {2}
#Z rotation by theta 2 + 90 degrees (variable is converted to rads)
T12RZ=  np.array([[np.cos(th2 + d90), -1*np.sin(th2 + d90), 0, 0],
                  [np.sin(th2 + d90),    np.cos(th2 + d90), 0, 0],
                  [                0,                    0, 1, 0],
                  [                0,                    0, 0, 1]])
 
#X translation by a2
T12TX = np.array([[1, 0, 0,a2], 
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])
                  
#All together
T12 = np.matmul(T12RZ, T12TX)

#############################################

#TRANSFORMATION FROM {2} TO {3}
#Z rotation by theta 3
T23RZ = np.array([[np.cos(th3), -1*np.sin(th3), 0, 0],
                  [np.sin(th3),    np.cos(th3), 0, 0],
                  [          0,              0, 1, 0],
                  [          0,              0, 0, 1]])
         
#X translation by a3
T23TX = np.array([[1, 0, 0,a3], 
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])
         
#X rotation by +90deg
T23RX = np.array([[1,           0,              0, 0],
                  [0, np.cos(d90), -1*np.sin(d90), 0],
                  [0, np.sin(d90),    np.cos(d90), 0],
                  [0,           0,              0, 1]])
                  
#All together, (!!) function is binary, multiply in parts, ensure integrity of result
temp = np.matmul(T23RZ, T23TX)   #temp variable for two step matrix mult
T23 = np.matmul(temp, T23RX)
temp = 0                         #reset temp for future use

#############################################

#TRANSFORMATION FROM {3} TO {4}
#Z rotation by theta 4
T34RZ = np.array([[np.cos(th4), -1*np.sin(th4), 0, 0],
                  [np.sin(th4),    np.cos(th4), 0, 0],
                  [          0,              0, 1, 0],
                  [          0,              0, 0, 1]])
         
#Z translation by d4
T34TZ = np.array([[1, 0, 0, 0], 
                  [0, 1, 0, 0],
                  [0, 0, 1,d4],
                  [0, 0, 0, 1]])
                  
#All together
T34 = np.matmul(T34RZ, T34TZ)

############################################
#COMPUTE COMPLETE TRANSFORMATION MATRIX
############################################
#print('\nShow Transformation from 0 to 1 \n', np.round(T01,2))

T02 = np.matmul(T01, T12)
#print('\nShow Transformation from 0 to 2 \n', np.round(T02,2))
#pack it up

T03 = np.matmul(T02, T23)
#print('\nShow Transformation from 0 to 3 \n', np.round(T03,2))

T04 = np.matmul(T03,T34)
#print('\nShow Transformation from 0 to 4 \n', np.round(T04,2))

############################################
#UPDATE SERVER DICTIONARY WITH TRANSFORMATION MATRICES
############################################

data["ref"] = REF.tolist()
data["t01"] = np.round(T01,2).tolist()
data["t02"] = np.round(T02,2).tolist()
data["t03"] = np.round(T03,2).tolist()
data["t04"] = np.round(T04,2).tolist()

############################################
#PACK IN THE MAIL, IT'S GONE
############################################
try:

    request, ip = socket.recvfrom(1024)                     # Wait until data is received
    request = json.loads(request.decode('utf-8'))           # Converts data back from bytes to string
    log("Received Request from", ip[0], "for:", request)    # Log to console
    packet = []                                             # Create empty list to construct packet

    for item in request:                # Iterate through requested items and
                                        # assemble packet in order requested
        if item in data:                # Check requested item exists in data dictionary

            packet.append(data[item])   # If items exists append to end of packet

        elif item not in data:                              # If item doesnt exist in data dictionary
            log("Item \"",item,"\"", "does not exist!")     # Log to console
            packet.append(None)                             # append 'None' for better error handling

    packet = json.dumps(packet)                     # Convert message to bytes
    socket.sendto(packet.encode('utf-8'), ip)       # Send back to device that requested
    log("Sent response", packet,"to",ip[0])         # Log to console

except Exception as e:      # If there is an error
    print(e)                # Print error
    exit()                  # Exit code. Replace with "pass" for code to move on after error
