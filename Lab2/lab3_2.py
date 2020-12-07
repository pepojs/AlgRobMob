import pdb
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import json

global first_line
global second_line
global pose_shift
first_line = []
second_line = []
pose_shift = []
global scaner_shift
scaner_shift = 0.17

# line1 = [A, B, C] -> Ax + By + C = 0
def line_intersection(line1, line2):
    [A1, B1, C1] = line1
    [A2, B2, C2] = line2
    
    if A1 == 0:
        if A2 == 0:
            return None

        else:
            y = -(A1*C2-C1*A2)/(B2*A1-A2*B1)
            x = (-B2*y-C2)/A2

    else:
        y = -(A2*C1-C2*A1)/(B1*A2-A1*B2)
        x = (-B1*y-C1)/A1
        
    return x,y

def line_intersection_angle(line1, line2):
    [A1, B1, C1] = line1
    [A2, B2, C2] = line2
    
    return math.atan2(A1*B2 - A2*B1, A1*A2 + B1*B2) #math.acos((A1*A2 + B1*B2)/(math.sqrt(A1*A1+B1*B1)*math.sqrt(A2*A2+B2*B2)))

def rotate_point(point, angle):
    x, y = point
    rotate_x = math.cos(angle)*x - math.sin(angle)*y
    rotate_y = math.sin(angle)*x + math.cos(angle)*y

    return rotate_x, rotate_y

def robot_location(line1, line2, second_angle):
	global first_line
	global second_line
	global pose_shift


	if(len(first_line) == 0):
		first_line = line1
		second_line = line2

		x,y = line_intersection(line1, line2)
		if len(pose_shift) == 0:
			pose_shift = [-x, -y]
		return [-x, -y, 0]

	else:
		print('Kat miedzy first_line i line1: {}'.format((-line_intersection_angle(first_line, line1))))
		print('Kat miedzy first_line i line2: {}'.format((-line_intersection_angle(first_line, line2))))

		x,y = line_intersection(line1, line2)
		print('robot_loc: {}, {}'.format(x,y))
		if second_angle:
			theta = line_intersection_angle(first_line, line1)
			theta = (theta + math.pi)
		else:
			theta = line_intersection_angle(first_line, line1)

		print('robot_loc: {}'.format(-theta))
		x, y = rotate_point([x,y], -theta)

		return [-x, -y, -theta]

def ransac(P, epsilon, t, N, angle):
	# Transformacja do współrzędnych kartezjańskich
	Pkart = []
	samplesLeft = 512
	listOfLines = []
	linesABC = []
	Sall = []
	Mall = []
	ListOfCounters = []
	for i in range(len(P)):
		if P[i] != np.inf and P[i] != -np.inf and P[i] != np.nan and not math.isnan(P[i]) and P[i]<=2.5 :
			x, y = wsp_kart(P[i], -math.pi/2.0+i*math.pi/512.0)
#			x, y = wsp_kart(P[i], -math.pi/4.0+i*math.pi/512.0)
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
			ListOfCounters.append(counter)
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

	return Sall, Sstar, listOfLines, linesABC, Mall, Pdisp, ListOfCounters


def read_json(path,i):
	json_data = open(path)
	data = json.load(json_data)
	return data[i]["scan"], data[i]["pose"]


def dist(A, B, C, xp, yp):
	d_l = abs(A*xp+B*yp+C)
	d_m = math.sqrt(A*A+B*B)
	return d_l/d_m


def wsp_kart(R, theta):
	global scaner_shift
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

def prostopadle(idx,M):
	A1 = M[idx][0]
	dist = np.Inf
	for i in range(len(M)):
		if i!=idx:
			A2 = M[i][0]
			d = abs(A1*A2+1)
			if (d<dist):
				dist = d
				r = i
	return r
				
# x = np.array([0,1,2,3,4,5])
# y = np.array([2.1, 2.9, 4.15, 4.98, 5.5, 6])
# z = np.polyfit(x, y, 1)
# print(z)
# for i in range(len(x)):
#	print(dist(z[0],-1,z[1],x[i],y[i]))
# p = np.poly1d(z)
# plotting
# xp = np.linspace(-1, 6, 100)
# plt.plot(x, y, '.', xp, p(xp))
# plt.show()


# pdb.set_trace()

for i in range(5):
	P, poseR = read_json('line_localization_1.json',i)
	poseR[2] = poseR[2]*math.pi/180.0

	x = np.arange(0,512)
	theta = (np.pi/512 )*(x-256)  # angle in rad

	fig1 = plt.figure()
	ax1 = fig1.add_axes([0.1,0.1,0.8,0.8],polar=True)
	line, = ax1.plot(theta,P,lw=2.5)
	#ax1.set_ylim(0,2)  # distance range

	# print(P)
	# S,Sstar,Mstar,M,Pkart = ransac(P,0.01,30,100,5)
	# pdb.set_trace()
	Sall, Sstar, listOfLines, linesABC, Mall, Pkart, ListOfCounters = ransac(P, 0.01, 40, 50, 20)

	# print("sstar", Sstar)
	# print("sall", Sall)
	# print("listofLines", listOfLines)
	# print("Mall", Mall)
	print("length", len(listOfLines))

	Xp,Yp = xy(Pkart)
	# XP, YP = xy(Sstar)
	# XP, YP = xy(listOfLines)
	# X,Y = xy(S)
	plt.figure(2)
	plt.plot(Xp,Yp,'c*')
	for i, line in enumerate(listOfLines):
		XP, YP = xy(Sall[i])
		px = np.linspace(min(XP),max(XP),100)
		p = np.poly1d(line)
		plt.plot(px,p(px),'g')

# p = np.poly1d(listOfLines[0])
# m = np.poly1d(M)
# plt.plot(XP,YP,'b*')
# plt.plot(X,Y,'r*')
# plt.plot(px,p(px),'g')
# plt.plot(px,m(px),'k')
# plt.plot(Sstar[:][0],Sstar[:][1],'bo')
	plt.savefig("line_loc_1d.png")
	print(linesABC)
	maxCounter = ListOfCounters.index(max(ListOfCounters))

	i = prostopadle(maxCounter, linesABC)
	print('wybrana prosta prostopadla: ', i)
	'''if len(first_line) > 0:
		first_to_first = abs(linesABC[0][0] - first_line[0])
		first_to_second = abs(linesABC[i][0] - first_line[0])
		second_to_first = abs(linesABC[0][0] - second_line[0])
		second_to_second = abs(linesABC[i][0] - second_line[0])
		print(first_to_first)
		print(first_to_second)
		print(second_to_first)
		print(second_to_second)
		print('first_to_first - second_to_first: {}'.format(first_to_first - second_to_first))
		print('first_to_second - second_to_second: {}'.format(first_to_second - second_to_second))

		if first_to_first <= second_to_first and first_to_second > second_to_second:
			pose = robot_location(linesABC[0], linesABC[i])

		elif first_to_first > second_to_first and first_to_second <= second_to_second:
			pose = robot_location(linesABC[i], linesABC[0])

		else:
			pose = robot_location(linesABC[0], linesABC[i])

	else:'''
	#pose1 =
	#pose2 = robot_location
	if linesABC[maxCounter][0] > 0 and linesABC[i][0] < 0:
		pose = robot_location(linesABC[maxCounter], linesABC[i], False)

	else:
		pose = robot_location(linesABC[i], linesABC[maxCounter], True)


	print(pose)
	poseR_x, poseR_y, poseR_theta = poseR #rotate_point([poseR[0]+scaner_shift, poseR[1]], -math.pi/2.0)
	poseR_x += pose_shift[0]
	poseR_y = poseR_y + pose_shift[1]
	print([poseR_x, poseR_y, poseR[2]])
	print([poseR[0], poseR[1], poseR[2]])
	plt.show()
