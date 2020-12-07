import pdb
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import json

def ransac(P, epsilon, t, N, angle):
	# Transformacja do współrzędnych kartezjańskich
	Pkart = []
	samplesLeft = 512
	listOfLines = []
	linesABC = []
	Sall = []
	Mall = []
	for i in range(len(P)):
		if P[i] != np.inf and P[i] != -np.inf and P[i] != np.nan and not math.isnan(P[i]) and P[i]<=2.5 :
#			x, y = wsp_kart(P[i], -math.pi/2.0+i*math.pi/512.0)
			x, y = wsp_kart(P[i], -math.pi/4.0+i*math.pi/512.0)
			Pkart.append([x, y])
	Pdisp = []
	for i in range(len(Pkart)):
		Pdisp.append(Pkart[i])
	# wylosowanie kąta i wybór punktów z najbliższej odległości
	while N > 0 and samplesLeft > 2 * angle + 1 and angle<len(Pkart)-angle:
		N = N - 1
		middle = random.randint(angle, len(Pkart)-angle)
		S = Pkart[middle-angle:middle+angle]
		#Sall.append(S)
		XS = []
		YS = []
		for i in range(len(S)):
			XS.append(S[i][0])
			YS.append(S[i][1])
		# Wyznaczenie modelu podstawowego
		# pdb.set_trace()
		# print('pierwszy polyfit', XS, YS)
		M = np.polyfit(XS, YS, 1)
		Mall.append(M)
		Sstar = []
		counter = 0
		for i in range(len(Pkart)):
#			if i < middle-angle or i >= middle+angle:
			d = dist(M[0], -1, M[1], Pkart[i][0], Pkart[i][1])
			# print(d)
			if(d < epsilon):
				counter = counter + 1
				Sstar.append(Pkart[i])
		print(counter)
		# pdb.set_trace()
		if counter > t:

			for i in range(len(Sstar)):
				XS.append(Sstar[i][0])
				YS.append(Sstar[i][1])
				# samplesLeft -= 1
			samplesLeft -= counter
			# print('drugi polyfit', XS, YS)
			Mstar = np.polyfit(XS, YS, 1)
			listOfLines.append(Mstar)
			linesABC.append([Mstar[0],-1,Mstar[1]])
			Sall.append(Sstar)
			#print(Sall)
			#print(Pkart)
			for i in range(len(Sstar)):
				Pkart.remove(Sstar[i])

	return Sall, Sstar, listOfLines, linesABC, Mall, Pdisp


def read_json(path,i):
	json_data = open(path)
	data = json.load(json_data)
	return data[i]["scan"], data[i]["pose"]


def dist(A, B, C, xp, yp):
	d_l = abs(A*xp+B*yp+C)
	d_m = math.sqrt(A*A+B*B)
	return d_l/d_m


def wsp_kart(R, theta):
	x = R*math.cos(theta)
	y = R*math.sin(theta)
	return np.array([x, y])


def xy(S):
	XS = []
	YS = []
	for i in range(len(S)):
		XS.append(S[i][0])
		YS.append(S[i][1])
	return XS, YS
				
i=0
P, poseR = read_json('line_detection_2.json',i)
poseR[2] = poseR[2]*math.pi/180.0

x = np.arange(0,512)
theta = (np.pi/512 )*(x-256)  # angle in rad

fig1 = plt.figure()
ax1 = fig1.add_axes([0.1,0.1,0.8,0.8],polar=True)
line, = ax1.plot(theta,P,lw=2.5)

Sall, Sstar, listOfLines, linesABC, Mall, Pkart = ransac(P, 0.01, 15, 50, 10)

Xp,Yp = xy(Pkart)

plt.figure(2)
plt.plot(Xp,Yp,'c*')
for i, line in enumerate(listOfLines):
	XP, YP = xy(Sall[i])
	px = np.linspace(min(XP),max(XP),100)
	p = np.poly1d(line)
	plt.plot(px,p(px),'g')

#plt.savefig("line_loc_1d.png")
plt.show()
