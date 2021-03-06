from time import sleep
import datetime
from drive import RosAriaDriver

# Enter robot number instead of X 
robot=RosAriaDriver('/PIONIER4')

ar=[]
robot.ResetPose()

t0=datetime.datetime.now()
# Zapisanie 3 zestawow danych 
for x in range(0,3):
        rec={}
        scan=robot.ReadLaser()
        pose=robot.GetPose()
        rec['pose']=pose
        rec['scan']=scan
        t1=datetime.datetime.now()-t0
        rec['time']=t1.seconds+t1.microseconds/1000000.0
        ar.append(rec)
        robot.setSpeedLR(0.5/10,0.5/10,10)
        nb = raw_input('Press enter')

import json
with open('data_stereo4.json','w') as json_data_file:
    json.dump(ar,json_data_file)
