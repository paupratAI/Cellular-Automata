import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from Grid import Grid
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from operator import add

def generate_humidity(height, width):
    # Generar valors aleatoris de humitat entre 0 i 4 per a cada cel·la
    data = np.random.randint(0, 5, (height, width))
    return data

def generate_vegetation(height, width):
    # Generar valors aleatoris de vegetació entre 1 i 10 per a cada cel·la
    data = np.random.randint(0, 10, (height, width))
    return data

humidity = pd.read_csv("humidity.csv", header=None).values
vegetation = pd.read_csv("vegetation.csv", header=None).values

HUM_MAX = np.max(humidity)
HUM_MIN = np.min(humidity)

VEG_MAX = np.max(vegetation)
VEG_MIN = np.min(vegetation)

humidity_colors = {}
vegetation_colors = {}
fire_colors = {}




hum_mult = 0.4 / HUM_MAX
hum_basis = [0, 0, 0]

veg_mult_r = 0.15 / VEG_MAX
veg_mult_g = 0.3 / VEG_MAX
veg_basis = [0, 0.4, 0]

fire_mult_r = 0.25 / VEG_MAX
fire_mult_g = 0.3 / VEG_MAX 

fire_basis = [0.75, 0.2, 0]

for hum in range(HUM_MIN, HUM_MAX+1):
    humidity_colors[f"{hum}"] = [ hum_basis[0], hum_basis[1], hum * hum_mult + hum_basis[2]]

for veg in range(VEG_MIN, VEG_MAX+1):
    vegetation_colors[f"{veg}"] = [(VEG_MAX - veg) * veg_mult_r + veg_basis[0], (VEG_MAX - veg) * veg_mult_g + veg_basis[1], veg_basis[2]]
    fire_colors[f"{veg}"] = [veg * fire_mult_r + fire_basis[0], veg * fire_mult_g + fire_basis[1], fire_basis[2]]

i = 0
grid_colors = []
for hum in range(HUM_MIN, HUM_MAX+1):
    grid_colors.append([])
    for veg in range(VEG_MIN, VEG_MAX+1):
        grid_colors[i].append(list(map(add, humidity_colors[f'{hum}'], vegetation_colors[f'{veg}'])))
    i += 1

print(grid_colors)
fig, ax = plt.subplots()


dicts = [humidity_colors, vegetation_colors, fire_colors]

length = 0
for dict_ in dicts:
    if len(dict_.keys()) > length:
        length = len(dict_.keys())


color_grid = [[[1,1,1] for _ in range(length)] for _ in range(len(dicts)+len(humidity_colors))]

for i, dict_ in enumerate(dicts):
    for j, key in enumerate(dict_.keys()):
        color_grid[i][j] = dict_[key]

for i in range(len(dicts), len(grid_colors)+len(dicts)):
    for j in range(len(grid_colors[i-len(dicts)])):
        color_grid[i][j] = grid_colors[i-len(dicts)][j]


img = ax.imshow(color_grid)
ax.axis('off')
plt.show()



"""# Plot colors
fig, ax = plt.subplots(3, 1, figsize=(6, 8))

# Plot humidity colors
ax[0].set_title("Humidity Colors")
ax[0].set_axis_off()
for i, (key, value) in enumerate(humidity_colors.items()):
    ax[0].add_patch(plt.Rectangle((i, 0), 1, 1, color=value))

# Plot vegetation colors
ax[1].set_title("Vegetation Colors")
ax[1].set_axis_off()
for i, (key, value) in enumerate(vegetation_colors.items()):
    ax[1].add_patch(plt.Rectangle((i, 0), 1, 1, color=value))

# Plot fire colors
ax[2].set_title("Fire Colors")
ax[2].set_axis_off()
for i, (key, value) in enumerate(fire_colors.items()):
    ax[2].add_patch(plt.Rectangle((i, 0), 1, 1, color=value))

plt.tight_layout()
plt.show()"""