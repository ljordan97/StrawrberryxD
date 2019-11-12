# This file receives data from a server program and can be used to receive telemetry. 
# The client runs on a local pc.

import math
import json
import time
import socket
import numpy as np
from vpython import *

class network:              # Holds IP and port as global variables

    ip = "localhost"     # SCUTTLE IP
    port = 2442             # SCUTTLE server port

try:

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Setup UDP Communication
    socket.settimeout(0.2)                                      # If response from server takes longer than
                                                                # time in seconds, move on.
except socket.error:

    print("Oops, something went wrong connecting the server!")  # If cannot connect, stop program.
    exit()

def get(items):

    try:

        message = json.dumps(items).encode('utf-8')         # Take requested data and convert to bytes
        socket.sendto(message, (network.ip,network.port))   # Send data to server
        data, ip = socket.recvfrom(4000)                    # Wait for response, create 4000 byte buffer to store response.
        data = json.loads(data)                             # Take response and convert from bytes to string
        data = dict(zip(items, data))                       # Combine request list with respose list to create dictionary
        return data                                         # Return data

    except Exception as e:

        print(e)
        return 1

print("SCUTTLE IP:", network.ip)

items = ['ref','t01','t02','t03','t04','d1','a2','a3','d4','th1','th2','th3','th4']   # Construct request of data you want from server

#while 1:    # Infinite loop
while 1:
    data = get(items)   # Call function to request data from server

    if data != 1:       # If data is not equal to 1 (error code from get() function)
        print(data)     # print whole dictionary
    else:
        pass            # Else, ignore unsuccessful request fro data.

    ############################################
    #CREATE A POSITION VECTOR FOR EACH FRAME
    ############################################

    #define each transformation matrix from data dictionary
    REF = data["ref"]
    T01 = data["t01"]
    T02 = data["t02"]
    T03 = data["t03"]
    T04 = data["t04"]
    d1 = data["d1"]
    a2 = data["a2"]
    a3 = data["a3"]
    d4 = data["d4"]
    th1 = data["th1"]
    th2 = data["th2"]
    th3 = data["th3"]
    th4 = data["th4"]


    #define frame offsets from real motor locations at some point

    #extract position data from each transform
    R2  = [T01[0][3], T01[1][3], T01[2][3]]
    R3  = [T02[0][3], T02[1][3], T02[2][3]]
    R4  = [T03[0][3], T03[1][3], T03[2][3]]
    EE  = [T04[0][3], T04[1][3], T04[2][3]]

    th1 = data["th1"]
    th2 = data["th2"]
    th3 = data["th3"]
    th4 = data["th4"]

    #verify data
    print('\nShow R1 {REF} position, angle\n',REF, '    rotation: ',th1, ' degrees')
    print('\nShow R2 position, angle\n', np.round(R2,2), '    rotation: ',th2, ' degrees')
    print('\nShow R3 position, angle\n', np.round(R3,2), '    rotation: ',th3, ' degrees')
    print('\nShow R4 position, angle\n', np.round(R4,2), '    rotation: ',th4, ' degrees')
    print('\nShow EE position\n', np.round(EE,2))

    ############################################
    #CREATE A ROTATED COORDINATE UNIT VECTORS FOR EACH FRAME
    ############################################

    ############################################
    #VISUALIZE EACH FRAME
    ############################################

    gREF = sphere(pos = vector(REF[0], REF[1], REF[2]), radius = 0.2, color=color.white)
    gR2 = sphere(pos = vector(R2[0], R2[1], R2[2]), radius = 0.2, color=color.white)
    gR3 = sphere(pos = vector(R3[0], R3[1], R3[2]), radius = 0.2, color=color.white)
    gR4 = sphere(pos = vector(R4[0], R4[1], R4[2]), radius = 0.2, color=color.white)
    gEE = sphere(pos = vector(EE[0], EE[1], EE[2]), radius = 0.5, color=color.white)

    d1center = (gR2.pos + gREF.pos)/2
    a2center = ((gR3.pos + gR2.pos))/2
    a3center = ((gR4.pos + gR3.pos))/2
    d4center = ((gEE.pos + gR4.pos))/2

    D1 = box(pos=d1center, axis=(gR2.pos-gREF.pos), length=d1,height=0.2, width=0.2, color=color.red)
    A2 = box(pos=a2center, axis=(gR3.pos-gR2.pos), length=a2,height=0.2, width=0.2, color=color.blue)
    A3 = box(pos=a3center, axis=(gR4.pos-gR3.pos), length=a3,height=0.2, width=0.2, color=color.green)
    D4 = box(pos=d4center, axis=(gEE.pos-gR4.pos), length=d4,height=0.2, width=0.2, color=color.yellow)


    #D1 = arrow(pos=gREF.pos, axis=gR2.pos, color=color.white, headwidth=0, headlength=0)
    #L2 = arrow(pos=gR2.pos, axis=gR3.pos, color=color.magenta, headwidth=0, headlength=0)
    #L3 = arrow(pos=gR3.pos, axis=gR4.pos, color=color.white, headwidth=0, headlength=0)
    #L4 = arrow(pos=gR4.pos, axis=gEE.pos, color=color.magenta, headwidth=0, headlength=0)

