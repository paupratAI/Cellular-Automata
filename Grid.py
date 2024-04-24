import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap


class Grid:
    def __init__(self, height: int, width: int, humidity: np.array, vegetation: np.array) -> None:
        self.height = height
        self.width = width
        
        self.color_grid = np.array([[[0,0.4,0] for _ in range(width)] for _ in range(height)], dtype=float)
        self.fire_status = np.zeros((height, width))
        self.vegetation = vegetation
        self.humidity = humidity

        self.HUM_MAX = np.max(humidity)

        self.humidity_colors = {}
        for hum in range(self.HUM_MAX+1):
            self.humidity_colors[f"{hum}"] = [(self.HUM_MAX-hum)*0.15, ((self.HUM_MAX - hum) / self.HUM_MAX)*0.3+0.4, 0]
        self.VEG_MAX = np.max(vegetation)

        #self.updated_cells = list()   # Vector que indica si una casilla ha sido actualizada, para colorear solo estas
        self.t = 0

    def init(self):
        """Inicializamos la cuadrícula, con vegetación, humedad y fuego"""
        self.fire_status[self.height//2, self.width//2] = 1  # Iniciem el foc al centre
        self.updated_cells = [(i, j) for i in range(self.height) for j in range(self.width)]
        self.fire_cells = [(self.height//2, self.width//2)]

    def update_fire(self):
        """Actualizamos el estado del fuego, guardamos en un vector fuego == 1 las casillas cuyo fuego es 1, y aquellas que hayan propagado el fuego, lo pasamos a 2 (quemado)"""
        for i, j in self.fire_cells:
            if self.humidity[i, j] == 0:
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
                        self.fire_cells.append((i_radius,j_radius))
                        self.updated_cells.append((i,j))
                # Extinguir el fuego si se queda sin vegetación
                if self.vegetation[i,j]==0:
                    self.fire_status[i,j] = 2  # 2 simboliza fuego extinto y casilla quemada
                    self.fire_cells.remove((i,j))
                    self.updated_cells.append((i,j))


    def update_humidity(self): 
        """Actualizamos la humedad de cada casilla, en caso de tener fuego, ya que al no tener la consideraremos quemada"""
        for i,j in self.fire_cells:
            if self.humidity[i,j] > 0:
                self.humidity[i,j] -= 1
                self.updated_cells.append((i,j))
        
    def update_vegetation(self):
        #for i,j in self.fire_cells
        pass

    def update_colors(self):
        """Actualizamos los colores de las casillas, en función de la humedad, la vegetación y el fuego"""
        for i,j in self.updated_cells:
            humidity_lev = self.humidity[i,j] 
            if humidity_lev > 0:
                self.color_grid[i,j] = self.humidity_colors[f'{humidity_lev}']
            elif self.fire_status[i,j] == 1:
                self.color_grid[i,j] = [1,0,0]

    def execute(self, n_iter = 50):
            
        def animate(t):    
            self.update_humidity()
            #self.update_vegetation()
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
