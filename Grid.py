import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from operator import add


class Grid:
    def __init__(self, height: int, width: int, humidity: np.array, vegetation: np.array) -> None:
        self.height = height
        self.width = width
        
        self.color_grid = np.array([[[0,0.4,0] for _ in range(width)] for _ in range(height)], dtype=float)
        self.fire_status = np.zeros((height, width))
        #self.fire_start = np.zeros((height, width))
        #self.fire_burning = np.zeros((height, width))
        #self.fire_burnt = np.zeros((height, width))
        
        self.fire_start_cells = {}
        self.fire_burning_cells = {}
        self.fire_burnt_cells = {}
        
 

        self.vegetation = vegetation
        self.humidity = humidity

        self.HUM_MAX = np.max(humidity)
        self.HUM_MIN = np.min(humidity)

        self.VEG_MAX = np.max(vegetation)
        self.VEG_MIN = np.min(vegetation)

        self.humidity_colors = {}
        self.vegetation_colors = {}

        for hum in range(self.HUM_MIN, self.HUM_MAX+1):
            self.humidity_colors[f"{hum}"] = [0,0, ((self.HUM_MAX - hum) / self.HUM_MAX)*0.4]
        
        for veg in range(self.VEG_MIN, self.VEG_MAX+1):
            self.vegetation_colors[f"{veg}"] = [((self.VEG_MAX-veg)/self.VEG_MAX)*0.15, ((veg) / self.VEG_MAX)*0.3+0.4, 0]
        


        self.updated_cells = {}   # Vector que indica si una casilla ha sido actualizada, para colorear solo estas
        self.t = 0

    def init(self):
        """Inicializamos la cuadrícula, con vegetación, humedad y fuego"""
        self.fire_status[self.height//2, self.width//2] = 1  # Iniciem el foc al centre
        self.fire_start_cells[self.height//2, self.width//2] = 1
        for i in range(self.height): 
            for j in range(self.width): 
                self.updated_cells[i,j] = 1 

    def update_fire(self):
        """Actualizamos el estado del fuego, guardamos en un vector fuego == 1 las casillas cuyo fuego es 1, y aquellas que hayan propagado el fuego, lo pasamos a 2 (quemado)"""
        fire_burning_cells_copy = self.fire_burning_cells.copy()
        for i, j in self.fire_burning_cells:
            # Extender el fuego a casillas próximas
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
                    if self.fire_status[i_radius,j_radius] == 0:
                        self.fire_status[i_radius,j_radius] = 1
                        self.fire_start_cells[i_radius,j_radius] = 1
                        self.updated_cells[i,j] = 1

                # Extinguir el fuego si se queda sin vegetación
                if self.vegetation[i,j]==0:
                    self.fire_status[i,j] = 2  # 2 simboliza fuego extinto y casilla quemada
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
        """Actualizamos la humedad de cada casilla, en caso de tener fuego, ya que al no tener la consideraremos quemada"""
        for i,j in self.fire_start_cells:
            if self.humidity[i,j] > 0:
                self.humidity[i,j] -= 1
                self.updated_cells[i,j] = 1
        
    def update_vegetation(self):
        for i,j in self.fire_burning_cells:
            if self.vegetation[i,j] > 0:
                self.vegetation[i,j] -= 1
                self.updated_cells[i,j] = 1

    def update_colors(self):
        """Actualizamos los colores de las casillas, en función de la humedad, la vegetación y el fuego"""
        for i,j in self.updated_cells:
            h_level = self.humidity[i,j] 
            v_level = self.vegetation[i,j]
            if h_level > 0:
                self.color_grid[i,j] = list(map(add, self.humidity_colors[f'{h_level}'], self.vegetation_colors[f'{v_level}']))
            elif self.fire_status[i,j] == 1:
                self.color_grid[i,j] = [1,0,0]
            elif self.fire_status[i,j] == 2:
                self.color_grid[i,j] = [0,0,0]
        self.updated_cells = {}  # Reseteamos las casillas actualizadas

    def execute(self, n_iter = 50):
            
        def animate(t):    
            self.update_humidity()
            self.update_vegetation()
            self.update_fire()
            self.update_colors()
            self.img.set_data(self.color_grid)
            self.ax.set_title(f'Step {t}')

        self.fig, self.ax = plt.subplots()

        self.init()
        self.img = self.ax.imshow(self.color_grid)
        self.ax.axis('off')

        ani = FuncAnimation(self.fig, animate, frames=n_iter, repeat=False, interval=200)
        plt.show()