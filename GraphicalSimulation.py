import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Simulation:
    def __init__(self, x_lim,y_lim,z_lim):
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(111, projection='3d')
        self.axis.set_xlim(x_lim)
        self.axis.set_ylim(y_lim)
        self.axis.set_zlim(z_lim)
        self.scat = self.axis.scatter([], [], [])

    def update_plot(self, drones):
        positions = [drone.get_position() for drone in drones]
        x_coords, y_coords, z_coords = zip(*positions)
        self.scat._offsets3d = (x_coords, y_coords, z_coords)
        plt.draw()
        plt.pause(0.5)
