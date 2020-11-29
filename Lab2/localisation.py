import math

global first_line
first_line = []

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
    
    return math.acos((A1*A2 + B1*B2)/(math.sqrt(A1*A1+B1*B1)*math.sqrt(A2*A2+B2*B2)))

def rotate_point(point, angle):
    x, y = point
    rotate_x = math.cos(angle)*x - math.sin(angle)*y
    rotate_y = math.sin(angle)*x + math.cos(angle)*y

    return rotate_x, rotate_y

def robot_location(line1, line2):
    global first_line
    if(len(first_line) == 0):
        first_line = line1
        
        x,y = line_intersection(line1, line2)
        return [-x, -y, 0]

    else:
        x,y = line_intersection(line1, line2)
        theta = line_intersection_angle(first_line, line1)
        x, y = rotate_point([x,y], theta)
        return [-x, -y, theta]
    
print(line_intersection_angle([0,1,1], [1, 0,1]))
print(robot_location([1,0,1], [0, 1,1]))
print(robot_location([0,1,1], [1, 0,1]))

