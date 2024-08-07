import AirspaceClass0
import DroneClass0
import simpy

env = simpy.Environment()

airspace = AirspaceClass.Airspace()
drone1 = DroneClass.Drone(env,(0,0),(0,5),1,"a", airspace)
drone2 = DroneClass.Drone(env,(0,10),(0,5),1,"b", airspace)

env.run(until=10)
