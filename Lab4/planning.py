import sys
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import rospy
import tf

from mobile_robotics.msg import matrix, vector, cell, path
from mobile_robotics.srv import set_target

from drive import RosAriaDriver

from map import Map
from wavefront import path_planning, wavefront_map, is_robot
from parser import Parser
import algorithm as algorithm
#       x, y, theta
POSE = (0, 0, 0)
GOAL = (200,200)
THRESHOLD = 0.2
CELLSIZE=0.05
WORLDWIDTH=20

scan_received = False

def handle_set_target(req):
    #set target
    global GOAL
    GOAL[0] = req.x
    GOAL[1] = req.y
    print "New target = (%d, %d)" % (GOAL[0], GOAL[1])
    return True


def callback_scan(msg):
    global scan_received
    scan = msg.ranges
    global scan
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


def callback_map(msg):
    grid_map = Map()
    size_x, size_y = grid_map.area.shape
    for i in xrange(size_x):
        for j in xrange(size_y):
            grid_map.area[i][j] = msg.rows[i].columns[j]
            rospy.loginfo("(i = %d, j = %d), %f" %(i, j, msg.rows[i].columns[j]))
    wave_front_map = wavefront_map(grid_map.area, GOAL, a.robot_position,THRESHOLD)
    path = path_planning(wave_front_map, POSE)
    path_msg = path()
    for cll in pth:
        path_msg.append(cell(cll[0], cll[1]))
    global pub
    pub.publish(path_msg)
            

def planning():
    global pub
    pub = rospy.Publisher('path', vector, queue_size=1)
    rospy.init_node('planning', anonymous=True)
    # Subscribe topics and bind with callback functions
    rospy.Subscriber("map", matrix, callback_map, queue_size=1)
    rospy.Subscriber("/PIONIER" + nr + "/RosAria/pose", Odometry, callback_pose, queue_size=1)
    rospy.Subscriber("/PIONIER"+nr+"/scan", LaserScan, callback_scan,queue_size=1)
    # Ensure service handling
    rospy.Service('set_target', set_target, handle_set_target)
    global scan_received
    while not scan_received:
        pass
    rospy.loginfo("Initilizing completed!")
    grid_map = Map()
    global scan
    data = Parser(scan, POSE).global_coordinates
    x, y = list(map(list, zip(*data['coordinates'])))
    robot_position = (data['pose'][0], data['pose'][1])
    a = algorithm.Algorithm(grid_map, (x, y), robot_position,WORLDWIDTH,CELLSIZE)        
    while True:
        if scan_received:
            rospy.loginfo("Scan handling!")
            ## extract ranges from message
            data = Parser(scan, WORLDWIDTH/2,WORLDWIDTH/2,0).global_coordinates
            x, y = list(map(list, zip(*data['coordinates'])))
            robot_position = (data['pose'][0], data['pose'][1])
            a.robot_position = (data['pose'][0],data['pose'][1])
            a.hits = list(map(list, zip(*data['coordinates'])))
            a.run()
            a.grid_map.map_plot()
            wave_front_map = wavefront_map(grid_map.area, GOAL, a.robot_position,THRESHOLD)
            path = path_planning(wave_front_map, POSE)
            path_msg = path()
            for cll in pth:
                path_msg.append(cell(cll[0], cll[1]))
            pub.publish(path_msg)
            scan_received = False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: sys.argv[0] \n')
        sys.exit(1)
    nr = sys.argv[1]
    planning()
