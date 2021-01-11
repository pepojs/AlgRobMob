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

#parser do plikow z robota
def timeparser2(time1, time2):
    date_time_obj1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S.%f') 
    date_time_obj2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S.%f')
    deltaT=date_time_obj2-date_time_obj1
    return deltaT.seconds + float(deltaT.microseconds)/1000000.0

def obrot(x0,y0,theta0):
    x_prim = math.cos(theta0)*x0-math.sin(theta0)*y0
    y_prim = math.sin(theta0)*x0+math.cos(theta0)*y0
    return x_prim,y_prim
    
x = [0]
y = [0]
theta = [0]
time = [0]
t,posL,posR,velL,velR = csv_reader('Enkoder_kwadrat.csv')

for i in range(len(t)):
    if(i == 0):
        deltaT = timeparser2(t[i],t[i]) # pierwszy czas 
    else:
        deltaT = timeparser2(t[i-1],t[i])
    deltaX,deltaY,deltaTheta = calc_pos_V(velR[i],velL[i],deltaT,theta[i],l)
    x.append(x[i]+deltaX)
    y.append(y[i]+deltaY)
    theta.append(theta[i]+deltaTheta)
    time.append(time[i]+deltaT)

t_robot, x_robot, y_robot, theta_robot = csv_reader_pose('Robot_kwadrat.csv')
print(x_robot[0], x[0])
print(y_robot[0], y[0])
print(theta_robot[0],theta[0])
print(theta_robot)
time10 = [0]
theta0 = theta_robot[0]*math.pi/180.0
theta0 = 0.93*theta0
x0 = x_robot[0]*1000
y0 = y_robot[0]*1000
#theta_robot.insert(0,theta_robot[0])
for i in range(len(t_robot)):
    if(i == 0): #   10:23:23.127405
        deltaT = timeparser2(t_robot[i],t_robot[i])
    else:
        deltaT = timeparser2(t_robot[i-1],t_robot[i])
    time10.append(time10[i]+deltaT)
    x_robot[i]=x_robot[i]*1000
    x_robot[i]=x_robot[i]-x0
    y_robot[i]=y_robot[i]*1000
    y_robot[i]=y_robot[i]-y0
    x_robot[i],y_robot[i] = obrot(x_robot[i],y_robot[i],-theta0)
    theta_robot[i] = theta_robot[i]*math.pi/180.0
    theta_robot[i] = theta_robot[i]-theta0
    #if theta_robot[i] < -0.01:
    #	theta_robot[i] = theta_robot[i] + math.pi*2

print(x_robot[0], x[0])
print(y_robot[0], y[0])
print(theta_robot[0],theta[0])

e_x = []
for i in range(len(x_robot)):
    e_x.append(abs(x_robot[i]-x[i]))

e_y = []
for i in range(len(y_robot)):
    e_y.append(abs(y_robot[i]-y[i]))

e_theta = []
for i in range(len(theta_robot)):
    e_theta.append(abs(theta_robot[i]-theta[i]))#0.93*theta0)
	
plt.figure(1)
plt.title("Porównanie odometrii na podstawie odometrii oraz odczytów z robota")
plt.xlabel("x[mm]")
# plt.ylim((-100),(100))
plt.ylabel("y[mm]")
plt.plot(x,y)
plt.plot(x_robot,y_robot)
plt.legend(('odometria','pomiary'))
#plt.savefig("porownanie_prosta2.png")
plt.figure(2)
plt.title("Orientacja robota")
plt.xlabel("t [s]")
# plt.ylim((-100),(100))
plt.ylabel("theta [rad]")
plt.plot(time[:100],theta[:100])
plt.plot(time10[1:101],theta_robot[:100])
plt.legend(('odometria','pomiary'))
#plt.savefig("porownanie_prosta2.png")

plt.figure(3)
plt.title("Błąd odometrii w kierunku x")
plt.xlabel("time [s]")
# plt.ylim((-100),(100))
plt.ylabel("e_x [mm]")
plt.plot(time10[1:101],e_x[:100])
#plt.savefig("porownanie_prosta2.png")

plt.figure(4)
plt.title("Błąd odometrii w kierunku y")
plt.xlabel("time [s]")
# plt.ylim((-100),(100))
plt.ylabel("e_y [mm]")
plt.plot(time10[1:101],e_y[:100])
#plt.savefig("porownanie_prosta2.png")

plt.figure(5)
plt.title("Błąd odometrii - orientacja")
plt.xlabel("time [s]")
# plt.ylim((-100),(100))
plt.ylabel("e_theta [rad]")
plt.plot(time10[1:101],e_theta[:100])
#plt.savefig("porownanie_prosta2.png")
plt.show()
