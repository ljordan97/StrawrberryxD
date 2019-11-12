from vpython import *

ball = sphere(pos=vector(-5,0,0), radius=0.5, color=color.cyan)
wallR = box(pos=vector(6,0,0), size=vector(0.2,12,12), color=color.green)
wallL = box(pos=vector(-6,0,0), size=vector(0.2,12,12), color=color.green)

ball.velocity = vector(25, 0, 0)
deltat = 0.005
t = 0
vscale = 0.1
varr = arrow(pos=ball.pos, axis=vscale*ball.velocity, color=color.white)

while t < 500:
    rate(100)
    varr.pos = ball.pos
    varr.axis = vscale*ball.velocity
    if(ball.pos.x >= wallR.pos.x):
        ball.velocity = -1*ball.velocity
    if(ball.pos.x <= wallL.pos.x):
        ball.velocity = -1*ball.velocity
    ball.pos = ball.pos + ball.velocity*deltat
    t = t + deltat

