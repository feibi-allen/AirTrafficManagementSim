# Example airspace program

import simpy
from AirspaceFile import Airspace
from DroneFile import Drone


env = simpy.Environment()

airspace = Airspace(env)

Drone(speed=0.5, start=[0, 0, 0], end=[10, 10, 0],
      airspace=airspace, id_str="c")
Drone(speed=0.7, start=[2, 0, 0], end=[10, 10, 0],
      airspace=airspace, id_str="d")
Drone(speed=1, start=[2, 5, 0], end=[10, 20, 0],
      airspace=airspace, id_str="e")
env.run(until=50)
