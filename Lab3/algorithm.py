import map
import pdb
from piksele_posrdnie import points
import numpy as np

class Algorithm():

    def __init__(self, grid_map, hits, robot_positon, worldwidth, cellsize):

        self.grid_map = grid_map
        self.hits = hits
        self.robot_position = robot_positon
        self.worldwidth = worldwidth
        self.cellsize = cellsize
        # self.approach = newapproach.Approach()

    def getCellX(self,x):
        for cellX in range(1,int(self.worldwidth/self.cellsize)):
            if x < cellX*self.cellsize:
                return cellX-1

    def getCellY(self,y):
        for cellY in range(1,int(self.worldwidth/self.cellsize)):
            if y < cellY*self.cellsize:
                return cellY-1

    def getCell(self,x,y):
        return [self.getCellX(x), self.getCellY(y)]

    def run(self):
        for i in range(len(self.hits[0])):
            # pdb.set_trace()
            hit = (self.getCellX(self.hits[0][i]), self.getCellY(self.hits[1][i]))
            # hit = (self.hits[0][i],self.hits[1][i])
            misses_from_points = points(self.getCellX(self.robot_position[0]),self.getCellY(self.robot_position[1]), self.getCellX(self.hits[0][i]), self.getCellY(self.hits[1][i]))
            # misses_from_points = points(self.robot_position[0],self.robot_position[1], self.hits[0][i], self.hits[1][i])
            misses_from_points = np.delete(misses_from_points,-1,0)
            # pdb.set_trace()
            # misses_from_points = np.flip(misses_from_points,axis=0)
            self.grid_map.set_hit_point([hit])
            self.grid_map.set_miss_point(misses_from_points)
