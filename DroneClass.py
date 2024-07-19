import simpy

TIME_STEP = 1  # Amount of time passed between each position update
MAX_SPEED = 10 # Speed in ms-1

class Drone(object):
    def __init__(self, env, start, end, velocity, id):
        # FIXME - assert check velocity (try except)
        self.env = env
        self.start = start
        self.end = end
        self.velocity = velocity
        self.pos = self.start
        self.id = id
        self.moving_time = 0
        #self.fly_process = env.process(self.fly())
        #env.process(self.stopping)

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

    def fly(self):
        while not self.end_point_passed():
            time_to_move = TIME_STEP
            while time_to_move:
                try:
                    yield self.env.timeout(time_to_move)
                    time_to_move = 0
                except simpy.Interrupt:
                    self.check_if_go()
            self.moving_time += TIME_STEP
            self.pos[0], self.pos[1] = self.pos[0] + (
                    self.velocity[0] * self.moving_time), self.pos[1] + (
                                               self.velocity[
                                                   1] * self.moving_time)
        self.pos[0],self.pos[1] = self.end[0],self.end[1]

    def stop(self):
        # check for collisions
        # if no collisions within time boundary check again and repeat
        # timeout for collisions
        # interrupt after timeout
        # repeat
        pass

    def end_point_passed(self):
        # check collinearity of start end and current pos
        if (self.end[0] - self.start[0]) * (self.pos[1] - self.start[1]) != (self.end[1] - self.start[1]) * (self.pos[0] - self.start[0]):
            return False
        # check within bounds of start and end points
        if not(min(self.start[0], self.end[0]) <= self.pos[0] <= max(self.start[0], self.end[0])):
            return False
        if not (min(self.start[1], self.end[1]) <= self.pos[1] <= max(self.start[1], self.end[1])):
            return False
        return True
    def permission_to_move(self):
        # collision resolve
        pass
