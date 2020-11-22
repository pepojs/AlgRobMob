import csv
import math
import datetime
import matplotlib 
import matplotlib.pyplot as plt

d_k=195 # srednica kola
wsp_kalib=0.9384
l=170.5*wsp_kalib  # rozstaw kół

def csv_reader(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
        posL= []
        posR = []
        velL =[]
        velR = []
        t = []
        for row in reader:
            t.append(row['#time'])
            posL.append(float(row['posL']))
            posR.append(float(row['posR']))
            velL.append(float(row['velL']))
            velR.append(float(row['velR']))
    return t,posL,posR,velL,velR 



def calc_Velocity( vel_R, vel_L):
    V=(vel_R+vel_L)/2.0
    return V

def calc_pos(vel_R, vel_L, time, theta):
    deltaX=calc_Velocity(vel_R,vel_L)*time*math.cos(theta)
    deltaY=calc_Velocity(vel_R,vel_L)*time*math.sin(theta)
    deltatheta=(vel_R-vel_L)/(2*l)*time

    return [deltaX,deltaY,deltatheta]

def timeparser(time1, time2):
    date_time_obj1 = datetime.datetime.strptime(time1, '%H:%M:%S.%f') 
    date_time_obj2 = datetime.datetime.strptime(time2, '%H:%M:%S.%f')
    deltaT=date_time_obj2-date_time_obj1
    return deltaT.seconds + float(deltaT.microseconds)/1000000.0



x = [0]
y = [0]
theta = [0]
time = [0]
t,posL,posR,velL,velR = csv_reader('square_left.csv')

for i in range(len(t)):
    if(i == 0):
        deltaT = timeparser('0:0:0.0',t[i])
    else:
        deltaT = timeparser(t[i-1],t[i])
    deltaX,deltaY,deltaTheta = calc_pos(velR[i],velL[i],deltaT,theta[i])
    x.append(x[i]+deltaX)
    y.append(y[i]+deltaY)
    theta.append(theta[i]+deltaTheta)
    time.append(time[i]+deltaT)
wsp_kalib = theta[len(theta)-1]/(2*math.pi)
print('wspolczynnik kalibracji: ', wsp_kalib)
print('x= ',x[len(x)-1],'y= ', y[len(y)-1],'theta= ', theta[len(theta)-1])
plt.figure(1)
plt.plot(x,y)
plt.figure(2)
plt.plot(time,theta)
plt.show()