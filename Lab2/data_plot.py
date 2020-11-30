import matplotlib.pyplot as plt
import numpy as np
import json
import math

def wsp_kart(R, theta):
	x = R*math.cos(theta)
	y = R*math.sin(theta)
	return np.array([x, y])
	
def read_json(path):
	json_data = open(path)
	data = json.load(json_data)
	return data[0]["scan"]

def p2c (P):
	Pkart = []
	for i in range(len(P)):
		if P[i] != np.inf and P[i] != -np.inf and P[i] != np.nan and not math.isnan(P[i])  :
			x, y = wsp_kart(P[i], -math.pi/2.0+i*math.pi/512.0)
			Pkart.append([x, y])
	Xp, Yp = xy(Pkart)
	return Xp,Yp

def xy(S):
	XS = []
	YS = []
	for i in range(len(S)):
		XS.append(S[i][0])
		YS.append(S[i][1])
	return XS, YS


P = read_json('data_stereo.json')
Xp, Yp = p2c(P)

x = np.arange(0,512)
theta = (np.pi/512 )*(x-256)  # angle in rad

fig1 = plt.figure()
ax1 = fig1.add_axes([0.1,0.1,0.8,0.8],polar=True)
line, = ax1.plot(theta,P,lw=2.5)
#ax1.set_ylim(0,2)  # distance range

plt.figure(2)
plt.plot(Xp,Yp,'b*')

plt.show()
