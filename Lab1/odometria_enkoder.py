import csv
import math
import datetime
import matplotlib 
import matplotlib.pyplot as plt

d_k=195 # srednica kola
wsp_kalib=0.944 #0.944
l=170.5*wsp_kalib  # rozstaw kół
ticks_mm = 128 #125 po prostej

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


x = [0]
y = [0]
theta = [0]
time = [0]
t,posL,posR,velL,velR = csv_reader('left_full_turn.csv')
posL_inc, posR_inc = encoder_increment(posL, posR)

for i in range(len(posL_inc)):
    deltaT = timeparser(t[i],t[i+1])
		
    deltaX,deltaY,deltaTheta = calc_pos(posL_inc[i],posR_inc[i],theta[i])
    x.append(x[i]+deltaX)
    y.append(y[i]+deltaY)
    theta.append(theta[i]+deltaTheta)
    time.append(time[i]+deltaT)
wsp_kalib = theta[len(theta)-1]/(2*math.pi)
print('wspolczynnik kalibracji: ', wsp_kalib)
print('x= ',x[len(x)-1],'y= ', y[len(y)-1],'theta= ', theta[len(theta)-1])
print(posL_inc)
print(posR_inc)
plt.figure(1)
plt.plot(x,y)
plt.figure(2)
plt.plot(time,theta)
plt.show()