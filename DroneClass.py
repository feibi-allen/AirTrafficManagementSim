import simpy

TIME_STEP = 1 # Amount of time passed between each position update

class Drone(object):
    def __init__(self,env , start, end, velocity, id):
        self.env = env
        self.start = start
        self.end = end
        self.velocity = velocity
        self.pos = self.start
        self.id = id
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
        while True: # FIXME - should be changed to while not finished
            time_to_move = TIME_STEP
            while time_to_move:
                try:
                    yield self.env.timeout(time_to_move)
                except simpy.Interrupt:
                    self.check_if_go()


    def stop(self):
        # check for collisions
        # if no collisions within time boundary check again and repeat
        # timeout for collisions
        # interrupt after timeout
        # repeat
        pass

    def permission_to_move(self):
        # collision resolve
        pass