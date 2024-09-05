import simpy
from AirspaceFile import Airspace
from DroneFile import Drone


env = simpy.Environment()

airspace = Airspace(env)

Drone(speed=5, start=[0, 0, 0], end=[10, 10, 0],
      airspace=airspace, id_str="c")
Drone(speed=5, start=[2, 0, 0], end=[10, 10, 0],
      airspace=airspace, id_str="d")
env.run(until=20)