from drive import RosAriaDriver
robot=RosAriaDriver('/PIONIER6') # w miejsce X wstaw numer robota

def go_right_square(robot):
    robot.SetSpeedLR(0.05,0.05,10)
    robot.SetSpeedLR(-0.05,0.05,10)
    

[(posL,posR),(vL,vR)]=robot.ReadEncoder()
posL, posR

