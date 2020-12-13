from __future__ import division
import json
import numpy as np


class Parser(object):
    MIN_ANGLE = -np.pi/2 # skaner range
    MAX_ANGLE = np.pi/2

    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.data = json.load(file)
        self.global_coordinates = []
        self.__change_into_global()

    def __change_into_global(self):
        index = 0
        for measure in self.data:
            self.global_coordinates.append({})
            x, y, theta = measure['pose']
            x += 5
            y += 5
            self.global_coordinates[index]['pose'] = [x, y, theta]
            self.global_coordinates[index]['time'] = measure['time']
            self.global_coordinates[index]['coordinates'] = []
            for i in range(len(measure['scan'])):
                d = measure['scan'][i]
                if np.isfinite(d):
                    alpha = i / len(measure['scan']) * (self.MAX_ANGLE - self.MIN_ANGLE) + self.MIN_ANGLE
                    x_0 = x + np.cos(theta + alpha) * d
                    y_0 = y + np.sin(theta + alpha) * d
                    self.global_coordinates[index]['coordinates'].append([x_0, y_0])
            index += 1

