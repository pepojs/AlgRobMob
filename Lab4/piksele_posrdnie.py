from bresenham import bresenham
import numpy as np

def points(x0,y0,x1,y1):
	p = bresenham(x0,y0,x1,y1)
	return np.array(list(p))

print(points(-1,-4,1,3))
