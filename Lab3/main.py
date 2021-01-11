import sys
import matplotlib.pyplot as plt
import json
import numpy as np

from map import Map
from parser import Parser
import algorithm

import pdb

CELLSIZE=0.02
WORLDWIDTH=20


def main():
    if len(sys.argv) < 2:
        print('Nie podano pliku')
        sys.exit(-1)
    data = Parser(sys.argv[1],WORLDWIDTH/2,WORLDWIDTH/2,0).global_coordinates
    grid_map = Map(len_x=int(WORLDWIDTH/CELLSIZE),len_y=int(WORLDWIDTH/CELLSIZE))
    #pdb.set_trace()
    print(data[0]['coordinates'])
    x, y = list(map(list, zip(*data[0]['coordinates'])))
    robot_position = (data[0]['pose'][0], data[0]['pose'][1])
    a = algorithm.Algorithm(grid_map, (x, y), robot_position,WORLDWIDTH,CELLSIZE)
    for dat in data:
        a.robot_position = (dat['pose'][0],dat['pose'][1])
        a.hits = list(map(list, zip(*dat['coordinates'])))
        # pdb.set_trace()
        a.run()
    a.grid_map.map_plot()
    input()



if __name__ == '__main__':
    main()
