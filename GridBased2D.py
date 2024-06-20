import simpy

class Airspace(object):
    def __init__(self, env):
        self.env = env
        self.aircraft = []

    def add


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