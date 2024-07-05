import simpy


class Drone(object):
    def __init__(self, start, end, velocity, id):
        self.start = start
        self.end = end
        self.velocity = velocity
        self.pos = self.start
        self.id = id

    def finished(self):
        return self.pos == self.end

    def get_velocity(self):
        return self.velocity

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_position(self):
        return self.pos

    def get_id(self):
        return self.id