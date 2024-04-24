import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, Colormap, LinearSegmentedColormap


data = np.array([[[1,1,0],[0,0,1]],
                 [[1,0,0],[0.5,0.5,1]]], dtype=float)
print(data)
fig, ax = plt.subplots()
img = ax.imshow(data, interpolation=None)
ax.axis('off')

def animate(t):

    img.set_data(data)
    ax.set_title(f'Step {t}')

ani = FuncAnimation(fig, animate, frames=100, repeat=False)
plt.show()