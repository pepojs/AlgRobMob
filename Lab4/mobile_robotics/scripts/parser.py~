from __future__ import division
import json
import numpy as np
import math


class Parser(object):
    MIN_ANGLE = -np.pi/2 # skaner range
    MAX_ANGLE = np.pi/2

    def __init__(self, scan,x,y,theta):
        #with open(filename, 'r') as file:
        self.data = scan
        self.global_coordinates = []
        self.x = x
        self.y = y
        self.theta = theta
        self.scaner_shift_x = 0.18 # w meterach
        self.scaner_shift_y = 0
        self.__change_into_global()

    def __change_scaner_global(self,x,y,theta):
        robot_x = math.cos(self.theta)*x - math.sin(self.theta)*y + self.x
        robot_y = math.sin(self.theta)*x + math.cos(self.theta)*y + self.y
        scaner_x = math.cos(self.theta + theta)*self.scaner_shift_x - math.sin(self.theta + theta)*self.scaner_shift_y + robot_x
        scaner_y = math.sin(self.theta + theta)*self.scaner_shift_x + math.cos(self.theta + theta)*self.scaner_shift_y + robot_y
        return robot_x, robot_y, scaner_x, scaner_y

    def __change_into_global(self):
        index = 0
        # self.global_coordinates.append({})
        self.global_coordinates.append({})
        x, y, theta = self.x, self.y, self.theta
        theta= theta*np.pi/180.0
        print("x,y,theta",x,y,theta)
        robot_x, robot_y, scaner_x, scaner_y = self.__change_scaner_global(x,y,theta)
        self.global_coordinates[index]['pose'] = [robot_x, robot_y, theta+self.theta]
        #self.global_coordinates[index]['time'] = measure['time']
        self.global_coordinates[index]['coordinates'] = []
        for i in range(len(self.data)):
            d = self.data[i]
            if np.isfinite(d):
                alpha = i / len(self.data) * (self.MAX_ANGLE - self.MIN_ANGLE) + self.MIN_ANGLE
                x_0 = scaner_x + np.cos(theta + alpha + self.theta) * d
                y_0 = scaner_y + np.sin(theta + alpha+ self.theta) * d
                self.global_coordinates[index]['coordinates'].append([x_0, y_0])
            # if index == 1:
            #     break
        index += 1



