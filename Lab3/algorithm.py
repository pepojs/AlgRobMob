import map
import pdb
from piksele_posrdnie import points
import numpy as np

class Algorithm():
    CELLSIZE = 0.05
    WORLDWIDTH = 300.0

    def __init__(self, grid_map, hits, robot_positon):

        self.grid_map = grid_map
        self.hits = hits
        self.robot_position = robot_positon
        # self.approach = newapproach.Approach()

    def getCellX(self,x):
        for cellX in range(1,int(self.WORLDWIDTH/self.CELLSIZE)):
            if x < cellX*self.CELLSIZE:
                return cellX-1

    def getCellY(self,y):
        for cellY in range(1,int(self.WORLDWIDTH/self.CELLSIZE)):
            if y < cellY*self.CELLSIZE:
                return cellY-1

    def getCell(self,x,y):
        return [self.getCellX(x), self.getCellY(y)]

    def run(self):
        for i in range(len(self.hits[0])):
            hit = (self.getCellX(self.hits[0][i]), self.getCellY(self.hits[1][i]))
            misses_from_points = points(self.getCellX(self.robot_position[0]),self.getCellY(self.robot_position[1]), self.getCellX(self.hits[0][i]), self.getCellY(self.hits[1][i]))
            misses_from_points = np.delete(misses_from_points,-1,0)
            # pdb.set_trace()
            # misses_from_points = np.flip(misses_from_points,axis=0)
            self.grid_map.set_hit_point([hit])
            self.grid_map.set_miss_point(misses_from_points)
