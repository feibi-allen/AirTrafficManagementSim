import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Simulation:
    def __init__(self, limits):
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(111, projection='3d')
        self.axis.set_xlim(limits[0])
        self.axis.set_ylim(limits[1])
        self.axis.set_zlim(limits[2])
        self.scat = self.axis.scatter([], [], [])

    def update_plot(self, drones):
        positions = [drone.get_position() for drone in drones]
        x_coords, y_coords, z_coords = zip(*positions)
        self.scat._offsets3d = (x_coords, y_coords, z_coords)
        plt.draw()
        plt.pause(0.5)
