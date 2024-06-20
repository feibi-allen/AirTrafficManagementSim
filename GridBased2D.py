import simpy

class Airspace(object):
    def __init__(self, env):
        self.env = env
        self.aircraft = []

    def addDrone(self,drone):
        self.aircraft.append(drone)

    def removeDrone(self,drone):
        self.aircraft.remove(drone)

    def run(self):
        while True:
            # check next move for all drones
            # compair for collisions
            # resolve collisions
            #
            pass


class Drone(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.pos = start
        self.nextMove = []

    def setNextMove(self):
        while not(self.pos == self.end):
            if self.pos[0]!=self.end[0]:
                # set next move towards x-pos
                pass
            else:
                # set next move towards y-pos
                pass

    def checkCollision(self):
        return self.nextMove()

    def move(self):
        self.pos[0],self.pos[1] = self.nextMove[0],self.nextMove[1]