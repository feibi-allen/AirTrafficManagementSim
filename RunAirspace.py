import AirspaceClass
import DroneClass
import simpy

env = simpy.Environment()

airspace = AirspaceClass.Airspace()
drone1 = DroneClass.Drone(env,(0,1),(0,5),(0,1),"a", airspace)
drone2 = DroneClass.Drone(env,(0,5),(0,2),(0,1),"b", airspace)

env.run(until=10)
