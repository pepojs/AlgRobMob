import csv
import datetime

def csv_EncoderReader(filepath):
	with open(filepath) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
		posL = []
		posR = []
		velL = []
		velR = []
		t = []
		for row in reader:
			t.append(datetime.datetime.strptime(row['#time'],'%H:%M:%S.%f'))
			posL.append(row['posL'])
			posR.append(row['posR'])
			velL.append(row['velL'])
			velR.append(row['velR'])
	return t,posL,posR,velL,velR
	
def csv_EncoderWriter(filepath,time,posL,posR,velL,velR):
	with open(filepath,'w') as csvfile:
		fieldnames = ['#time', 'posL', 'posR', 'velL', 'velR']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';',quotechar='|')
		writer.writeheader()
		for i in range(len(posL)):
			writer.writerow({'#time': time[i], 'posL': posL[i], 'posR': posR[i], 'velL': velL[i], 'velR': velR[i]})

def csv_PoseReader(filepath):
	with open(filepath) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
		x = []
		y = []
		z = []
		t = []
		for row in reader:
			t.append(datetime.datetime.strptime(row['#time'],'%H:%M:%S.%f'))
			x.append(row['x'])
			y.append(row['y'])
			z.append(row['z'])
	return t,x,y,z
	
def csv_PoseWriter(filepath,time,x,y,z):
	with open(filepath,'w') as csvfile:
		fieldnames = ['#time', 'x', 'y', 'z']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';',quotechar='|')
		writer.writeheader()
		for i in range(len(posL)):
			writer.writerow({'#time': time[i], 'x': x[i], 'y': y[i], 'z': z[i]})

