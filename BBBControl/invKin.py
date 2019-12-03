from sympy import *

init_printing(use_unicode=True)

#constants
p = 3.1415 / 2 #for shorthanding 90 degrees in radians
#frame offsets
#DISTANCE UNITS = INCHES
d1 = 1 #distance from point of instersection of R1's shaft axis w/ R2 shaft axis and REF ({0} to {1})
a2 = 6 #distance from {1} to end of R3's shaft {2}
a3 = 6 #distance from {2} shaft base of R4
d4 = 3 #distance from {3} to EE's eyeball {4}

th1, th2, th3, th4 = symbols('th1 th2 th3 th4')

#define Matrices