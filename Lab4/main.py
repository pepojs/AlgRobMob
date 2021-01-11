import sys
import matplotlib.pyplot as plt
import json
import numpy as np

from map import Map
from parser import Parser
import algorithm
from wavefront import *
import cv2

import pdb

CELLSIZE=0.05
WORLDWIDTH=20

GOAL = (200, 240)
ROBOT = (222, 312)

def main():
    if len(sys.argv) < 2:
        print('Nie podano pliku')
        sys.exit(-1)
    data = Parser(sys.argv[1],WORLDWIDTH/2,WORLDWIDTH/2,0).global_coordinates
    grid_map = Map(len_x=int(WORLDWIDTH/CELLSIZE),len_y=int(WORLDWIDTH/CELLSIZE))
    #pdb.set_trace()
    #print(data[0]['coordinates'])
    x, y = list(map(list, zip(*data[0]['coordinates'])))
    robot_position = (data[0]['pose'][0], data[0]['pose'][1])
    a = algorithm.Algorithm(grid_map, (x, y), robot_position,WORLDWIDTH,CELLSIZE)
    for dat in data:
        a.robot_position = (dat['pose'][0],dat['pose'][1])
        a.hits = list(map(list, zip(*dat['coordinates'])))
        # pdb.set_trace()
        a.run()
    a.grid_map.map_plot()
    occup_map = a.grid_map.return_map()
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(occup_map,kernel,iterations = 1)
    plt.figure(3)
    plt.imshow(dilation, interpolation="nearest",cmap='Blues', origin='upper')
    plt.show()
    
    #print(occup_map)

    arr = wavefront_map(occup_map, GOAL, ROBOT, 0.1)
    #print(arr)
    '''
    plt.figure(3)
    plt.imshow(arr, interpolation="nearest",cmap='Blues', origin='upper')
    plt.show()
    '''
    path, moves_list = path_planning(arr, ROBOT)
    print(path)
    plt.figure(2)
    plt.imshow(occup_map, interpolation="nearest",cmap='Blues', origin='upper')
    plt.plot([i[1] for i in path], [i[0] for i in path], 'ro')
    plt.plot(ROBOT[0], ROBOT[1], 'x')
    plt.show()
    
    #input()



if __name__ == '__main__':
    main()
