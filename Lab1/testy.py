import csv
import math
import datetime
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np

d_k=195 # srednica kola
wsp_kalib=0.9384
l=170.5*wsp_kalib  # rozstaw kół
ticks_mm =128 #125 po prostej

def csv_reader(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
        posL= []
        posR = []
        velL =[]
        velR = []
        t = []
        for row in reader:
            if(row['posL'] == 'posL'):
                continue
            t.append(row['#time'])
            posL.append(float(row['posL']))
            posR.append(float(row['posR']))
            velL.append(float(row['velL']))
            velR.append(float(row['velR']))
    return t,posL,posR,velL,velR 

# czytanie danych z getPose
def csv_reader_pose(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
        x= []
        y = []
        theta =[]
        t = []
        for row in reader:
            if(row['x'] == 'x'):
                continue
            t.append(row['#time'])
            x.append(float(row['x']))
            y.append(float(row['y']))
            theta.append(float(row['z']))
    return t,x,y,theta



def calc_Velocity( vel_R, vel_L):
    V=(vel_R+vel_L)/2.0
    return V

#dodany paramter l zeby mozna bylo zrobic porowanie z kalibracja
def calc_pos_V(vel_R, vel_L, time, theta,l):
    deltaX=calc_Velocity(vel_R,vel_L)*time*math.cos(theta)
    deltaY=calc_Velocity(vel_R,vel_L)*time*math.sin(theta)
    deltatheta=(vel_R-vel_L)/(2*l)*time

    return [deltaX,deltaY,deltatheta]

def encoder_increment(posL, posR):
	posL_inc = []
	posR_inc = []
	for i in range(len(posL)-1):
		if posL[i+1] < 0 and  posL[i] > 15000:
			posL_inc.append(2*32767 - posL[i]  + posL[i+1])
			
		elif posL[i+1] < 0 and  posL[i] < 15000 and posL[i] >= 0:
			posL_inc.append(-posL[i] + posL[i+1])
			
		elif posL[i+1] >= 0 and posL[i] < -15000:
			posL_inc.append(-2*32767 - posL[i] + posL[i+1])
			
		elif posL[i+1] >= 0 and posL[i] > -15000 and posL[i] < 0:
			posL_inc.append(-posL[i] + posL[i+1])
			
		else:
			posL_inc.append(posL[i+1] - posL[i])
			
			
		if posR[i+1] < 0 and  posR[i] > 15000:
			posR_inc.append(2*32767 - posR[i]  + posR[i+1])
			
		elif posR[i+1] < 0 and  posR[i] < 15000 and posR[i] >= 0:
			posR_inc.append(-posR[i] + posR[i+1])
			
		elif posR[i+1] >= 0 and posR[i] < -15000:
			posR_inc.append(-2*32767 - posR[i] + posR[i+1])
			
		elif posR[i+1] >= 0 and posR[i] > -15000 and posR[i] < 0:
			posR_inc.append(-posR[i] + posR[i+1])
			
		else:
			posR_inc.append(posR[i+1] - posR[i])

	for i in range(len(posL_inc)):
		posL_inc[i] = (float(posL_inc[i])/ticks_mm)
			
	for i in range(len(posR_inc)):
		posR_inc[i] = (float(posR_inc[i])/ticks_mm)
	
	return [posL_inc, posR_inc]

def calc_Distance(posL, posR):
    dist=(posL+posR)/2.0
    return dist

def calc_pos(posL, posR, theta):
    deltaX=calc_Distance(posL,posR)*math.cos(theta)
    deltaY=calc_Distance(posL,posR)*math.sin(theta)
    deltatheta=(posR-posL)/(2*l)

    return [deltaX,deltaY,deltatheta]


def timeparser(time1, time2):
    date_time_obj1 = datetime.datetime.strptime(time1, '%H:%M:%S.%f') 
    date_time_obj2 = datetime.datetime.strptime(time2, '%H:%M:%S.%f')
    deltaT=date_time_obj2-date_time_obj1
    return deltaT.seconds + float(deltaT.microseconds)/1000000.0

#parser do plikow z robota
def timeparser2(time1, time2):
    date_time_obj1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S.%f') 
    date_time_obj2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S.%f')
    deltaT=date_time_obj2-date_time_obj1
    return deltaT.seconds + float(deltaT.microseconds)/1000000.0



x = [0]
y = [0]
theta = [0]
time = [0]
t,posL,posR,velL,velR = csv_reader('Enkoder_kwadrat.csv')

for i in range(len(t)):
    if(i == 0):
        deltaT = timeparser2('2020-11-23 10:31:26.837977',t[i]) # pierwszy czas 
    else:
        deltaT = timeparser2(t[i-1],t[i])
    deltaX,deltaY,deltaTheta = calc_pos_V(velR[i],velL[i],deltaT,theta[i],l)
    x.append(x[i]+deltaX)
    y.append(y[i]+deltaY)
    theta.append(theta[i]+deltaTheta)
    time.append(time[i]+deltaT)
# wsp_kalib = theta[len(theta)-1]/(2*math.pi)

# x1 = [0]
# y1 = [0]
# theta1 = [0]
# time1 = [0]
# t,posL,posR,velL,velR = csv_reader('square_left.csv')

# for i in range(len(t)):
#     if(i == 0):
#         deltaT = timeparser2('2020-11-23 10:31:26.837977',t[i]) # pierwszy czas 
#     else:
#         deltaT = timeparser2(t[i-1],t[i])
#     deltaX,deltaY,deltaTheta = calc_pos_V(velR[i],velL[i],deltaT,theta[i],l)
#     x.append(x[i]+deltaX)
#     y.append(y[i]+deltaY)
#     theta.append(theta[i]+deltaTheta)
#     time.append(time[i]+deltaT)
# wsp_kalib = theta[len(theta)-1]/(2*math.pi)

x1 = [0]
y1 = [0]
theta1 = [0]
time1 = [0]
t,posL,posR,velL,velR = csv_reader('forward.csv')

for i in range(len(t)):
    if(i == 0):
        deltaT = timeparser('0:0:0.0',t[i])
    else:
        deltaT = timeparser(t[i-1],t[i])
    deltaX,deltaY,deltaTheta = calc_pos_V(velR[i],velL[i],deltaT,theta1[i],l)
    x1.append(x1[i]+deltaX)
    y1.append(y1[i]+deltaY)
    theta1.append(theta1[i]+deltaTheta)
    time1.append(time1[i]+deltaT)
wsp_kalib = theta1[len(theta1)-1]/(2*math.pi)

x_enc = [0]
y_enc = [0]
theta_enc = [0]
time_enc = [0]
posL_inc, posR_inc = encoder_increment(posL, posR)

for i in range(len(posL_inc)):
    deltaT = timeparser(t[i],t[i+1])
		
    deltaX,deltaY,deltaTheta = calc_pos(posL_inc[i],posR_inc[i],theta_enc[i])
    x_enc.append(x_enc[i]+deltaX)
    y_enc.append(y_enc[i]+deltaY)
    theta_enc.append(theta_enc[i]+deltaTheta)
    time_enc.append(time_enc[i]+deltaT)

# print('wspolczynnik kalibracji: ', wsp_kalib)
# print('x= ',x[len(x)-1],'y= ', y[len(y)-1],'theta= ', theta[len(theta)-1])

t_robot, x_robot, y_robot, theta_robot = csv_reader_pose('Robot_kwadrat.csv')
time10 = [0]
for i in range(len(t_robot)):
    if(i == 0): #   10:23:23.127405
        deltaT = timeparser2('2020-11-23 10:31:29.632184',t_robot[i])
    else:
        deltaT = timeparser2(t_robot[i-1],t_robot[i])
    time10.append(time10[i]+deltaT)
    x_robot[i]=x_robot[i]*1000
    y_robot[i]=y_robot[i]*1000


# theta_robot.insert(0,theta_robot[0])

# x_orginal=[0,1150,1150,0,0] # lewy zakręt orginalny
# y_orginal=[0,0,1150,1150,0]
# x_orginal=[0,1150,1150,0,0] # prawy zakręt orginalny
# y_orginal=[0,0,-1150,-1150,0]

x_orginal= [0,400,1150]
y_orginal = [0,0,0]
theta_orginal=[0,0,0]
time_orginal=[0,2,7]
plt.figure(1)
plt.title("Porównanie odometrii na podstawie prędkości oraz pozycji enkoderów")
plt.xlabel("x[mm]")
plt.ylim((-100),(100))
plt.ylabel("y[mm]")
plt.plot(x1,y1)
plt.plot(x_enc,y_enc)
plt.plot(x_orginal,y_orginal)
plt.legend(('prędkości','enkodery','prawdziwa trajektoria'), loc='upper right')
plt.savefig("prawdziwa_forward.png")
plt.figure(2)
plt.title("Porównanie orientacji robota na podstawie prędkości oraz pozycji enkoderów")
plt.xlabel("t[s]")
plt.ylim((-1),(1))
plt.ylabel("theta[radiany]")
plt.plot(time1,theta1)
plt.plot(time_enc,theta_enc)
plt.plot(time_orginal,theta_orginal)
plt.legend(('prędkości','enkodery','prawdziwa orientacja'), loc='upper right')
plt.savefig("theta_forward.png")

plt.plot(time,theta)
plt.plot(time,theta_robot)

# plt.figure(3)
# plt.title("Pozycja robota odczytana przy pomocy pakietu RosAria")
# plt.xlabel("x[mm]")
# # plt.ylim((0),(1))
# plt.ylabel("y[mm]")
# plt.plot(x_robot,y_robot)
# plt.savefig("robot_square.png")
# plt.figure(4)
# # ax=plt.gca()
# # ax
# plt.title("Orientacja robota odczytana przy pomocy pakietu RosAria")
# plt.xlabel("time[s]")

# # plt.ylim((-20),(-10))
# plt.ylabel("theta")
# plt.plot(time10,theta_robot)
# plt.savefig("robot_theta_square.png")

plt.show()
