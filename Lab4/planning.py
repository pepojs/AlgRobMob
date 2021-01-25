import sys
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import rospy
import tf
import cv2

from mobile_robotics.msg import matrix, vector, cell, path
from mobile_robotics.srv import set_target

from drive import RosAriaDriver

from map import Map
from wavefront import path_planning, wavefront_map, is_robot
from parser import Parser
import algorithm as algorithm
#       x, y, theta
POSE = (20, 20)
GOAL = (200,200)
THRESHOLD = 0.2
CELLSIZE=0.05
WORLDWIDTH=20
KERNEL = 3

mapa = 0
planning_time = False

def handle_set_target(req):
    #set target
    global GOAL
    GOAL[0] = req.x
    GOAL[1] = req.y
    print "New target = (%d, %d)" % (GOAL[0], GOAL[1])
    return True
    
def callback_map(msg):
    global mapa
    mapa = msg

def callback_planning(msg):
    global planning_time, POSE
    planning_time = True
    POSE = msg

def planning():
    global mapa, planning_time, POSE
    pub = rospy.Publisher('path', vector, queue_size=1)
    rospy.init_node('planning', anonymous=True)
    # Subscribe topics and bind with callback functions
    rospy.Subscriber("map", matrix, callback_map, queue_size=1)
    rospy.Subscriber("planning_time", cell, callback_planning, queue_size=1)
    # Ensure service handling
    rospy.Service('set_target', set_target, handle_set_target)
    
    while True:
        rospy.sleep(0.001)
        if planning_time:
            rospy.loginfo("It's planning time!")
            kernel = np.ones((KERNEL,KERNEL),np.uint8)
            dilation = cv2.dilate(mapa,kernel,iterations = 1)
            wave_front_map = wavefront_map(dilation,GOAL,POSE,THRESHOLD)
            path = path_planning(wave_front_map, POSE)
            path_msg = path()
            for cll in pth:
                path_msg.append(cell(cll[0], cll[1]))
            pub.publish(path_msg)
            planning_time = False

if __name__ == '__main__':
    planning()
