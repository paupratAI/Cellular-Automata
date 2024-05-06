import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from operator import add


class Grid:
    def __init__(self, height: int, width: int, humidity: np.array, vegetation: np.array, rivers: np.array) -> None:
        """Inicialitza la graella amb els paràmetres de dimensió, humitat, vegetació i rius."""
        self.height = height
        self.width = width
        
        # Color predeterminat de la graella
        self.color_grid = np.array([[[0,0.4,0] for _ in range(width)] for _ in range(height)], dtype=float)
        self.fire_status = np.zeros((height, width))

        
        self.fire_start_cells = {}
        self.fire_burning_cells = {}
        self.fire_burnt_cells = {}
 
        self.vegetation = vegetation
        self.humidity = humidity
        self.rivers = rivers

        # Màxims i mínims per a la normalització de colors
        self.HUM_MAX = np.max(humidity)
        self.HUM_MIN = np.min(humidity)

        self.VEG_MAX = np.max(vegetation)
        self.VEG_MIN = np.min(vegetation)

        self.humidity_colors = {}
        self.vegetation_colors = {}
        self.fire_colors = {}

        # Càlcul dels colors basat en la humitat i vegetació
        hum_mult = 0.4 / self.HUM_MAX
        hum_basis = [0, 0, 0]

        veg_mult_r = 0.15 / self.VEG_MAX
        veg_mult_g = 0.3 / self.VEG_MAX
        veg_basis = [0, 0.4, 0]

        fire_mult_r = 0.25 / self.VEG_MAX
        fire_mult_g = 0.3 / self.VEG_MAX 

        fire_basis = [0.75, 0.2, 0]

        for hum in range(self.HUM_MIN, self.HUM_MAX+1):
            self.humidity_colors[f"{hum}"] = [ hum_basis[0], hum_basis[1], hum * hum_mult + hum_basis[2]]

        for veg in range(self.VEG_MIN, self.VEG_MAX+1):
            self.vegetation_colors[f"{veg}"] = [(self.VEG_MAX - veg) * veg_mult_r + veg_basis[0], (self.VEG_MAX - veg) * veg_mult_g + veg_basis[1], veg_basis[2]]
            self.fire_colors[f"{veg}"] = [veg * fire_mult_r + fire_basis[0], veg * fire_mult_g + fire_basis[1], fire_basis[2]]


        self.updated_cells = {}   # Vector que indica si una casilla ha sido actualizada, para colorear solo estas
        self.t = 0

    def init(self, fire_init):
        """Inicialitza la simulació amb foc a la cel·la del centre."""
        for cell in fire_init:
            self.fire_status[cell] = 1  # Iniciem el foc al centre
            self.fire_start_cells[cell] = 1
        for i in range(self.height): 
            for j in range(self.width): 
                self.updated_cells[i,j] = 1 

    def update_fire(self):
        """Actualitza l'estat del foc, propagant el foc i extingint-lo si no hi ha vegetació."""
        fire_burning_cells_copy = self.fire_burning_cells.copy()
        for i, j in self.fire_burning_cells:
            # Propaga el foc a les cel·les veïnes
                surrounds = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]
                if i*j==0:
                    if i==0:
                        surrounds.remove((i-1,j))
                    if j==0:
                        surrounds.remove((i,j-1))
                if i==self.height-1:
                    surrounds.remove((i+1,j))
                if j==self.width-1:
                    surrounds.remove((i,j+1))
                    
                for i_radius,j_radius in surrounds:
                    if self.fire_status[i_radius,j_radius] == 0 and self.rivers[i_radius,j_radius]==0:
                        self.fire_status[i_radius,j_radius] = 1
                        self.fire_start_cells[i_radius,j_radius] = 1
                        self.updated_cells[i,j] = 1

                # Extingir el foc si es queda sense vegetació
                if self.vegetation[i,j]==0:
                    self.fire_status[i,j] = 2  # 2 simbolitza foc extingit i cel·la cremada
                    del fire_burning_cells_copy[i,j]
                    self.updated_cells[i,j] = 1

        self.fire_burning_cells = fire_burning_cells_copy
        fire_start_cells_copy = self.fire_start_cells.copy()
        for i,j in self.fire_start_cells:
            if self.humidity[i,j] == 0:
                self.fire_burning_cells[i,j] = 1
                del fire_start_cells_copy[i,j]
                self.updated_cells[i,j] = 1
        self.fire_start_cells = fire_start_cells_copy

    def update_humidity(self): 
        """Disminueix la humitat en les cel·les amb foc"""
        for i,j in self.fire_start_cells:
            if self.humidity[i,j] > 0:
                self.humidity[i,j] -= 1
                self.updated_cells[i,j] = 1
        
    def update_vegetation(self):
        """Disminueix la vegetació en les cel·les que s'estan cremant"""
        for i,j in self.fire_burning_cells:
            if self.vegetation[i,j] > 0:
                self.vegetation[i,j] -= 1
                self.updated_cells[i,j] = 1

    def update_colors(self):
        """Actualitza els colors de la graella basat en l'estat actual de humitat, vegetació i foc."""
        for i,j in self.updated_cells:
            h_level = self.humidity[i,j] 
            v_level = self.vegetation[i,j]
            if self.rivers[i,j] == 1:
                self.color_grid[i,j] = [0.1,0.2,0.9]
            elif h_level > 0:
                self.color_grid[i,j] = list(map(add, self.humidity_colors[f'{h_level}'], self.vegetation_colors[f'{v_level}']))
            elif self.fire_status[i,j] == 1:
                self.color_grid[i,j] = self.fire_colors[f'{v_level}']
            elif self.fire_status[i,j] == 2:
                self.color_grid[i,j] = [0,0,0]
        self.updated_cells = {}  # Reseteamos las casillas actualizadas

    def execute(self, n_iter = 50, fire_init=[(0,0)]):
        """Executa la simulació visual del foc en la graella."""
        def animate(t):    
            self.update_humidity()
            self.update_vegetation()
            self.update_fire()
            self.update_colors()
            self.img.set_data(self.color_grid)
            self.ax.set_title(f'Step {t}')

        self.fig, self.ax = plt.subplots()

        self.init(fire_init=fire_init)
        self.img = self.ax.imshow(self.color_grid)
        self.ax.axis('off')

        self.ani = FuncAnimation(self.fig, animate, frames=n_iter, repeat=False, interval=100)

        return self.ani