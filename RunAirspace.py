import simpy
from AirspaceFile import Airspace
from DroneFile import Drone


env = simpy.Environment()

airspace = Airspace(env)

env.run(until=airspace.stop_event | 50)