import simpy

class Drone(object):
    def __init__(self, env, id, speed, start, end, startTime):
        self.env = env
        self.flightProc = env.process(self.fly_path())
        self.id = id
        self.speed = speed
        self.start = start
        self.end = end
        self.pos = start
        self.nextMove = None
        self.startTime = startTime

    def get_id(self):
        return self.id

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
        self.pos = (self.nextMove[0], self.nextMove[1])

    def fly_path(self):
        # wait for schedule time
        yield self.env.timeout(self.startTime)

        self.set_next_move()
        self.check_collision()
        pass

    def finished(self):
        return self.pos == self.end

    def get_velocity(self):
        return self.speed
    def get_start(self):
        return self.start