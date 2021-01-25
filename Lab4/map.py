import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pdb

np.set_printoptions(threshold=np.inf)

class Map():
    RADIUS = np.inf

    def __init__(self, len_x=200, len_y=200, hp=0.9, mp=0.1):
        self.__len_x = len_x
        self.__len_y = len_y
        self.__hit_probability = hp
        self.__miss_probability = mp
        self.area = np.full((self.__len_x, self.__len_y), 0.5, dtype=float)
        # Area with probability from 0 to 1
        self.prob_area = np.full((self.__len_x, self.__len_y), 0.5, dtype=float)
        # self.mPlt = plt.imshow(self.area, interpolation="nearest",cmap='Blues', origin='lower')

    def map_plot(self):
        for x in range(self.__len_x):
            for y in range(self.__len_y):
                self.prob_area[x][y] = self.probability(self.area[x][y])
        #pdb.set_trace()
        plt.imshow(self.prob_area, interpolation="nearest",cmap='Blues', origin='upper')
        plt.show(block=False)
        plt.colorbar()
        plt.pause(1.0)
        #print(self.prob_area)
        
        #plt.show()
    
    def update(self):
        for x in range(self.__len_x):
            for y in range(self.__len_y):
                self.prob_area[x][y] = self.probability(self.area[x][y])
        
    def return_map(self):
        return self.prob_area    

    def probability(self, cell):
        return 1 - (1/(1 + np.exp(cell)))

    def hit(self):
        return np.log(self.__hit_probability/(1-self.__hit_probability))

    def miss(self):
        return np.log(self.__miss_probability/(1-self.__miss_probability))

    def set_miss_point(self, cells):
        for cell in cells:
            x,y = cell
            self.area[x][y] += self.miss()

    def set_hit_point(self, cells):
        for cell in cells:
            x,y = cell
            self.area[x][y] += self.hit()
