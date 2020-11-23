from drive import RosAriaDriver
import datetime
import math
from read_write_csv import *

robot=RosAriaDriver('/PIONIER6') # w miejsce X wstaw numer robota

t=4.20
t_obrotu=6.39-t
s=1.15

def go_right_square(robot):
    robot.SetSpeedLR(s/t,s/t,t)
    robot.SetSpeedLR(0,math.pi/(2*t_obrotu),t_obrotu)
    robot.SetSpeedLR(s/t,s/t,t)
    robot.SetSpeedLR(0,math.pi/(2*t_obrotu),t_obrotu)
    robot.SetSpeedLR(s/t,s/t,t)
    robot.SetSpeedLR(0,math.pi/(2*t_obrotu),t_obrotu)
    robot.SetSpeedLR(s/t,s/t,t)
    robot.SetSpeedLR(0,math.pi/(2*t_obrotu),t_obrotu)

go_right_square(robot)
while True:
	measure_time=datetime.datetime.now()
	[(posL,posR),(vL,vR)]=robot.ReadEncoder()
	[(x,y,theta)]=robot.ReadPose()
	csv_EncoderWriter('Enkoder.csv',measure_time,posL,posR,vL,vR)
	csv_PoseWriter('Robot.csv',measure_time,x,y,theta)


time_a=datetime.datetime.now()
time_b=datetime.datetime.now()
time_c=time_b-time_a
time_c.microseconds
time_c.seconds
real_time=time_c


