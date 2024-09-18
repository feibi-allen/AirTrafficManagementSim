# Air Traffic Management

This project is designed to simulate an airspace of drones.
The airspace is represented by coordinates [x,y,z] with no limit on values.

## Assumptions:
- Drones travel with constant velocity
- Drones are able to stop for an indefinite amount of time
- Drones are modeled as particles

## Protocols
To manage the airspace a number of protocols are used:
- Drones cannot move vertically unless taking off and landing
- Drones which ate taking off and landing cannot move horizontally
- Drones moving horizontally must fly at designated height according to heading 
(similar to Visual Flight Rules used in aviation)

## Instructions
To run the program:

- Create and environment using the SimPy library
- Create an instance of an airspace (takes the environment as a parameter)
- Create instances of drones, Drone(speed,start_coord,end_coord,airspace,ID)
This adds them to the airspace
- Run the environment for chosen amount of time

An example can be found in RunAirspace File