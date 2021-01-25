import sys
import math
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
form std_msgs.msg import Bool
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
GOAL = (200,200)
THRESHOLD = 0.2
CELLSIZE=0.05
WORLDWIDTH=20

path = 0
move = False

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
	
def callback_path(msg):
	global path, move
	path = msg
	move = True
	
def section(path):
	cell_number = 0
	x_init = path[0][0]
	y_init = path[0][1]
	if path[1][0] == x_init:
		for cell in path:
			if cell[0]==x_init:
				cell_number += 1
			else:
				break
	elif path[1][1] == y_init:
		for cell in path:
			if cell[1]==y_init:
				cell_number += 1
			else:
				break
	return cell_number
	
def orintation(path): #!!!!!!!!!!!
	x_init, y_init = path[0]
	if path[1][0]==x_init and path[1][1]<y_init: #DOWN
		return -90
	elif path[1][0]==x_init and path[1][1]>y_init: #UP
		return 90
	elif path[1][0]>x_init and path[1][1]==y_init: #RIGHT
		return 0
	elif path[1][0]<x_init and path[1][1]==y_init: #LEFT
		return 180
	return None
	
def rotation(desired_orient):
	global POSE
	if abs(desired_orient - POSE[2])<0.5: #????
		return 0
	else:
		return (desired_orient - POSE[2] + 180)%360 - 180

def sign(a):
	if a > 0:
		return 1;
	return -1;
	
def norm(pos1, pos2):
	return sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

def final(distance,pose,orient):
	final_pose = pose
	if orient==0:
		final_pose[0]+=distance
	elif orient==180:
		final_pose[0]-=distance
	elif orient==90:
		final_pose[1]+=distance
	else:
		final_pose[1]-=distance
	return final_pose
	
def movement():
	global path, move, POSE
	nr = 4
	
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
	pub_map = rospy.Publisher('ready', Bool, queue_size=1)
	msg = Twist()
	msg.linear.x = 0
	msg.linear.y = 0
	msg.linear.z = 0
	msg.angular.x = 0
	msg.angular.y = 0
	msg.angular.z = 0
	
	
	rospy.Subscriber("/PIONIER" + nr + "/RosAria/pose", Odometry, callback_pose, queue_size=1)
	rospy.Subscriber("path", vector, callback_path, queue_size=1)
	
	while True:
		rospy.sleep(0.001)
		if move:
			rospy.loginfo("It's going!")
			distance = section(path)*CELLSIZE
			orient = orintation(path)
			rotate = rotation(orient)
			while abs(rotate) > 0.5:
				msg.angular.z = sign(rotate)*0.2
				pub.publish(msg)
				rotate = rotation(orient)
			msg.agular.z = 0
			pub.publish(msg)
			current_pose = POSE
			final_pose = final(distance, POSE, orient)
			while norm(current_pose,final_pose) > 0.1:
				msg.linear.x = 0.1
				msg.angular.z = 0
				pub.publish(msg)
				current_pose = POSE
				rotate = rotation(orient - math.atan2(POSE[1]-final_pose[1],POSE[0]-final_pose[0]))
				while abs(rotate) > 0.5:
					msg.linear.x = 0
					msg.angular.z = sign(rotate)*0.2
					pub.publish(msg)
					rotate = rotation(orient - math.atan2(POSE[1]-final_pose[1],POSE[0]-final_pose[0]))
			msg.linear.x = 0
			msg.angular.z = 0
			pub.publish(msg)
			map_pub.publish(True)
			move = False

if __name__ == '__main__':
	movement()
	
