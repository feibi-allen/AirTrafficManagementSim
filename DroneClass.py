import simpy

TIME_STEP = 1  # Amount of time passed between each position update
MAX_SPEED = 10  # Speed in ms-1
TIME_BETWEEN_CHECKS = 2  # Amount of time passed between checking for collision


class Drone(object):
    def __init__(self, env, start, end, velocity, id, airspace):
        # FIXME - assert check velocity (try except)
        self.env = env
        self.start = start
        self.end = end
        self.velocity = velocity
        self.pos = self.start
        self.id = id
        self.airspace = airspace
        self.moving_time = 0
        self.fly_process = env.process(self.fly())
        env.process(self.check_collision())
        self.airspace.add_drone(self)  # adds itself to the airspace

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
        """
        Moves drone every time step unless interrupted by collision avoidance
        Stops once drone has reached end point
        Change TIME_STEP for more accurate calculations
        :return:
        """
        print("drone",self.id,self.env.now)
        while not self.end_point_passed():
            time_to_move = TIME_STEP
            print("time stepping:", self.id)
            print(self.env.now)
            while time_to_move:
                try:
                    yield self.env.timeout(time_to_move)
                    time_to_move = 0
                except simpy.Interrupt:
                    self.check_if_go()
            # move the drone
            self.moving_time += TIME_STEP
            self.pos = (self.start[0] + (self.velocity[0] * self.moving_time),
                        self.start[1] + (self.velocity[1] * self.moving_time))
            print("Drone",self.id,"pos:",self.pos)
        # update drone position
        self.pos = (self.end[0], self.end[1])
        self.airspace.remove_drone(self)

    def check_collision(self):
        """
        Checks with airspace to get time of collision and will interrupt flight
        when collision is due to happen, so it can be resolved.
        If no collision within TIME_BETWEEN_CHECKS then another check is performed
        :return:
        """
        while True:
            collision = self.airspace.get_time_of_first_collisions(self)
            print("checking", self.id,"for collision:",collision)

            if not collision:
                yield self.env.timeout(TIME_BETWEEN_CHECKS)
                continue

            time_to_collision = next(iter(collision.values()))
            if time_to_collision > TIME_BETWEEN_CHECKS:
                print("Time between checks timed out")
                yield self.env.timeout(TIME_BETWEEN_CHECKS)
            else:
                yield self.env.timeout(time_to_collision)
                print("Interrupting flight", self.id)
                self.fly_process.interrupt()

    def check_if_go(self):
        print("collision resolve,", self.id)

    def end_point_passed(self):
        # check collinearity of start end and current pos
        # FIXME throw error
        if (self.end[0] - self.start[0]) * (self.pos[1] - self.start[1]) != (
                self.end[1] - self.start[1]) * (self.pos[0] - self.start[0]):
            print("Off Course")
        # check within bounds of start and end points
        # check x coord
        if not (min(self.start[0], self.end[0]) <= self.pos[0] <= max(
                self.start[0], self.end[0])):
            return True
        #check y coord
        if not (min(self.start[1], self.end[1]) <= self.pos[1] <= max(
                self.start[1], self.end[1])):
            return True
        return False

    def permission_to_move(self):
        # collision resolve
        pass
