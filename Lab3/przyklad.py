import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

f = np.array([[7,8,9], [4,5,6], [1,2,3]])

plt.imshow(f, interpolation="nearest",cmap='Blues')
plt.colorbar()
plt.show()
