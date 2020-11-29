import numpy as np
import matplotlib.pyplot as plt
import math
import random
import json

def ransac(P,epsilon,t,N,angle):
	#Transformacja do współrzędnych kartezjańskich
	Pkart = []
	for i in range(len(P)):
		x,y = wsp_kart(P[i],-math.pi/2.0+i*math.pi/512.0)
		Pkart.append([x,y])
	
	#wylosowanie kąta i wybór punktów z najbliższej odległości
	middle = random.randint(angle,len(P)-angle)
	S = Pkart[middle-angle:middle+angle]
	XS = []
	YS = []
	for i in range(len(S)):
		XS.append(S[i][0])
		YS.append(S[i][1])
	#Wyznaczenie modelu podstawowego
	M = np.polyfit(XS,YS,1)
	
	Sstar = []
	for i in range(len(P)):
		if i<middle-angle or i>=middle+angle:
			d = dist(M[0],-1,M[1],Pkart[i][0],Pkart[i][1])
			#print(d)
			if(d < epsilon):
				Sstar.append(Pkart[i])
	
	for i in range(len(Sstar)):
		XS.append(Sstar[i][0])
		YS.append(Sstar[i][1])
		
	Mstar = np.polyfit(XS,YS,1)
	
	return S,Sstar,Mstar,M,Pkart
	
def read_json(path):
	json_data = open(path)
	data = json.load(json_data)
	return data[0]["scan"];
	
def dist(A,B,C,xp,yp):
	d_l = abs(A*xp+B*yp+C)
	d_m = math.sqrt(A*A+B*B)
	return d_l/d_m

def wsp_kart(R,theta):
	x = R*math.cos(theta)
	y = R*math.sin(theta)
	return np.array([x,y])
	
def xy (S):
	XS = []
	YS = []
	for i in range(len(S)):
		XS.append(S[i][0])
		YS.append(S[i][1])
	return XS,YS

#x = np.array([0,1,2,3,4,5])
#y = np.array([2.1, 2.9, 4.15, 4.98, 5.5, 6])
#z = np.polyfit(x, y, 1)
#print(z)
#for i in range(len(x)):
#	print(dist(z[0],-1,z[1],x[i],y[i]))
#p = np.poly1d(z)
#plotting
#xp = np.linspace(-1, 6, 100)
#plt.plot(x, y, '.', xp, p(xp))
#plt.show()

P = read_json('line_detection_1.json')
S,Sstar,Mstar,M,Pkart = ransac(P,0.01,30,100,5)
Xp,Yp = xy(Pkart)
XP, YP = xy(Sstar)
X,Y = xy(S)
px = np.linspace(min(XP),max(XP),100)
p = np.poly1d(Mstar)
m = np.poly1d(M)
plt.plot(Xp,Yp,'c*')
plt.plot(XP,YP,'b*')
plt.plot(X,Y,'r*')
plt.plot(px,p(px),'g')
plt.plot(px,m(px),'k')
#plt.plot(Sstar[:][0],Sstar[:][1],'bo')
plt.show()
