from drive import RosAriaDriver
import math
robot=RosAriaDriver('/PIONIER6') # w miejsce X wstaw numer robota

t=6.30
s=1.15

def go_right_square(robot):
    robot.SetSpeedLR(s/t,s/t,t)
    robot.SetSpeedLR(0,math.pi/(2*t),t)
    robot.SetSpeedLR(s/t,s/t,t)
    robot.SetSpeedLR(0,math.pi/(2*t),t)
    robot.SetSpeedLR(s/t,s/t,t)
    robot.SetSpeedLR(0,math.pi/(2*t),t)
    robot.SetSpeedLR(s/t,s/t,t)
    

go_right_square(robot)
[(posL,posR),(vL,vR)]=robot.ReadEncoder()
posL, posR

