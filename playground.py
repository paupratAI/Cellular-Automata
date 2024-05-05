import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, Colormap, LinearSegmentedColormap


a = np.array([0,0,0])
b = np.array([1,1,1])

c = (b+1) * (a+1)

print(c)