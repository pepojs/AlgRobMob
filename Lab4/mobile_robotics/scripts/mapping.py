#!/usr/bin/env python

import sys
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import rospy
import tf

from mobile_robotics.msg import matrix, vector, cell, path
from mobile_robotics.srv import set_target

from drive import RosAriaDriver

from map import Map
from wavefront import path_planning, wavefront_map, is_robot
from parser import Parser
import algorithm as algorithm

POSE = (0, 0, 0)
GOAL = (25,22)
THRESHOLD = 0.05
CELLSIZE=0.5
WORLDWIDTH=20

scan = []
scan_received = False
robot_ready = True

def callback_ready(msg):
	global robot_ready
	robot_ready = msg.data
	
def callback_scan(msg):
	global scan_received, scan
	scan = msg.ranges
	rospy.loginfo("Scan received!")
	rospy.loginfo("================================================")
	scan_received = True

def callback_pose(msg):
	## extract position data from data frame
	pos=msg.pose.pose.position
	rot=msg.pose.pose.orientation
	quaternion = (    rot.x,    rot.y,    rot.z,    rot.w)
	euler= tf.transformations.euler_from_quaternion(quaternion)
	# return position and orientation in radians
	global POSE
	POSE = (pos.x,pos.y,euler[2])
	rospy.loginfo("Pose: x=%f y=%f theta=%f" % POSE)
    
def mapping():
	global scan, scan_received, robot_ready
	nr = 4
        rospy.init_node("mapping",anonymous = True)
        pub = rospy.Publisher('map', matrix, queue_size=1)
        pub_pose = rospy.Publisher('planning_time',cell,queue_size=1)
	rospy.Subscriber("/PIONIER4/RosAria/pose", Odometry, callback_pose, queue_size=1)
	rospy.Subscriber("/PIONIER4/scan", LaserScan, callback_scan,queue_size=1)
	rospy.Subscriber("ready", Bool, callback_ready, queue_size=1)
	grid_map = Map()
        while len(scan) == 0:
                print("I'm waiting")
        data = Parser(scan, WORLDWIDTH/2,WORLDWIDTH/2,0).global_coordinates
        print(data)
	x, y = list(map(list, zip(*data[0]['coordinates'])))
	robot_position = (data[0]['pose'][0], data[0]['pose'][1])
	a = algorithm.Algorithm(grid_map, (x, y), robot_position,WORLDWIDTH,CELLSIZE)
        vec = []
        mat = []
	while True:
		rospy.sleep(0.001)
		if scan_received and robot_ready:
			rospy.loginfo("Scan handling!")
			## extract ranges from message
                        data = Parser(scan, POSE[0], POSE[1], POSE[2]).global_coordinates
			x, y = list(map(list, zip(*data[0]['coordinates'])))
			robot_position = (data[0]['pose'][0], data[0]['pose'][1])
			a.robot_position = (data[0]['pose'][0],data[0]['pose'][1])
			a.hits = list(map(list, zip(*data[0]['coordinates'])))
			a.run()
			a.grid_map.update()
                        print(a.grid_map.return_map())
                        size_x = len(a.grid_map.return_map())
                        size_y = len(a.grid_map.return_map()[0])
                        for i in range(size_x):
                                for j in range(size_y):
                                        vec.append(a.grid_map.return_map()[i][j])
                                vec1 = vector()
                                vec1 = vec
                                mat.append(vec1)
                                vec = []
			pub.publish(mat)
                        pub_pose.publish(a.robot_positon)
			scan_received = False
			robot_ready = False

if __name__ == '__main__':
	mapping()
	
