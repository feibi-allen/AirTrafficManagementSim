import simpy


class Airspace(object):
    def __init__(self, env):
        self.env = env
        self.activeSpace = env.process(self.run())
        self.aircraft = []

    def add_drone(self, drone):
        self.aircraft.append(drone)

    def remove_drone(self, drone):
        self.aircraft.remove(drone)

    def run(self):
        while True:
            # check next move for all drones
            # compair for collisions
            # resolve collisions
            #
            pass


class Drone(object):
    def __init__(self, env, speed, start, end):
        self.env = env
        self.flightProcess = env.process(self.fly_path())
        self.speed = speed
        self.start = start
        self.end = end
        self.pos = start
        self.nextMove = None

    def set_next_move(self):
        while not (self.pos == self.end):
            if self.pos[0] != self.end[0]:
                # set next move towards x-pos
                pass
            else:
                # set next move towards y-pos
                pass

    def check_collision(self):
        return self.nextMove()

    def move(self):
        self.pos[0], self.pos[1] = self.nextMove[0], self.nextMove[1]

    def fly_path(self):
        pass

    def finished(self):
        return self.pos == self.end
