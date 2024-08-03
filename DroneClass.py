import math

import simpy

TIME_STEP = 1  # Amount of time passed between each position update (millisecond)
MAX_SPEED = 10  # Speed in ms-1
TIME_BETWEEN_CHECKS = 1  # Amount of time passed between checking for collision


class Drone(object):
    def __init__(self, env, start, end, speed, id, airspace):
        # FIXME - assert check inputs are valid (try except)
        self.id = id
        self.env = env
        self.start = start
        self.end = end
        self.speed = speed
        self.velocity = self.calculate_velocity()
        self.pos = self.start
        self.airspace = airspace
        self.moving_time = 0
        env.process(self.check_collision())
        self.fly_process = env.process(self.fly())
        self.airspace.add_drone(self)  # adds itself to the airspace

    def calculate_velocity(self):
        """
        Converts scalar speed to vector velocity.
        :return: Velocity as a list [x,y]
        """
        delt_x_sq, delt_y_sq = ((self.end[0] - self.start[0]) ** 2,
                                (self.end[1] - self.start[1]) ** 2)
        delt_square_sum = delt_x_sq + delt_y_sq

        if delt_square_sum == 0:
            raise ValueError("Start and end points cannot be the same")

        vel_x = math.sqrt(((self.speed ** 2) / delt_square_sum) * delt_x_sq)
        if self.end[0] < self.start[0]:
            vel_x = -abs(vel_x)
        vel_y = math.sqrt(((self.speed ** 2) / delt_square_sum) * delt_y_sq)
        if self.end[1] < self.start[1]:
            vel_y = -abs(vel_y)
        velocity = [vel_x, vel_y]

        print(f"Drone {self.id} velocity: {velocity}")
        return velocity

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
        yield self.env.timeout(0.5)
        while not self.end_point_passed():
            time_to_move = TIME_STEP
            try:
                yield self.env.timeout(time_to_move)
                self.moving_time += TIME_STEP
                self.pos = (
                self.start[0] + (self.velocity[0] * self.moving_time),
                self.start[1] + (self.velocity[1] * self.moving_time))
                print(f"Time stepping: {self.id} to {self.pos} at time {self.env.now}")
            except simpy.Interrupt:
                self.check_if_go()

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
            print(f"checking {self.id} for collision: {collision} at time {self.env.now}")

            if not collision:
                yield self.env.timeout(TIME_BETWEEN_CHECKS)
                continue

            time_to_collision = next(iter(collision.values()))-0.5
            print(f"Time to collision = {time_to_collision}")
            if time_to_collision > TIME_BETWEEN_CHECKS:
                yield self.env.timeout(TIME_BETWEEN_CHECKS)
            else:
                yield self.env.timeout(time_to_collision)
                print(f"Interrupting flight {self.id} at {self.pos} at time {self.env.now}")
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