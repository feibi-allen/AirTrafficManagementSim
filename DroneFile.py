import math
from AirspaceFile import Airspace


class Drone:
    def __init__(self, speed, start, end, airspace):
        # FIXME - error checking for speed and pos correct structure
        self.pos = start
        self.start = start
        self.end = end
        self.target_height = start[2]
        self.max_speed = speed  # maximum speed
        self.max_h_velocity = self._calculate_horizontal_velocity()
        self.current_velocity = [0, 0, 0]
        self.airspace = airspace
        #airspace.add_drone(self)

    def _calculate_horizontal_velocity(self):
        """
        Converts max scalar speed to max vector velocity (2D only).
        :return: Velocity as a list [x,y,0]
        """
        delt_x_sq, delt_y_sq = ((self.end[0] - self.start[0]) ** 2,
                                (self.end[1] - self.start[1]) ** 2)
        delt_square_sum = delt_x_sq + delt_y_sq

        if delt_square_sum == 0:
            raise ValueError("Start and end points cannot be the same")

        vel_x = math.sqrt(
            ((self.max_speed ** 2) / delt_square_sum) * delt_x_sq)
        if self.end[0] < self.start[0]:
            vel_x = -abs(vel_x)
        vel_y = math.sqrt(
            ((self.max_speed ** 2) / delt_square_sum) * delt_y_sq)
        if self.end[1] < self.start[1]:
            vel_y = -abs(vel_y)
        velocity = [vel_x, vel_y, 0]

        return velocity

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_position(self):
        return self.pos

    def set_target_height(self, height):
        self.target_height = height

    def get_target_height(self):
        return self.target_height

    def get_speed(self):
        return self.max_speed

    def get_velocity(self):
        return self.current_velocity

    def go_horizontal(self):
        for val in self.current_velocity:
            self.current_velocity[val] = self.max_h_velocity[val]

    def go_vertical(self):
        self.current_velocity = [0, 0, self.max_speed]

    def stop(self):
        self.current_velocity = [0, 0, 0]

    def move(self, time):
        if self.current_velocity[2] != 0:
            z_change = self.current_velocity[2] * time
            if self.end_between(self.pos[2], z_change, self.end[2]):
                self.pos[2] = self.end[2]
            else:
                self.pos[2] += z_change

        elif self.pos[0] != self.end[0] and self.pos[1] != self.end[1]:
            x_change = self.current_velocity[0] * time
            y_change = self.current_velocity[0] * time
            if self.end_between(self.pos[0], x_change, self.end[0]) and \
                    self.end_between(self.pos[1], y_change, self.end[1]):
                self.pos[0] = self.end[0]
                self.pos[1] = self.end[1]
            # if drone will move past x or y but not both path is incorrectly
            # calculated and should raise error
            elif self.end_between(self.pos[0], x_change, self.end[0]) or \
                    self.end_between(self.pos[1], y_change, self.end[1]):
                raise ArithmeticError("Drone path incorrectly followed, end "
                                      "between x or y but not both")
            else:
                self.pos[0] += self.current_velocity[0] * time
                self.pos[1] += self.current_velocity[0] * time
        # if drone has reached x or y but not both path is incorrectly
        # calculated and should raise error
        else:
            raise ArithmeticError("Drone path incorrectly followed, end at x "
                                  "or y but not both")
        if self.pos == self.end:
            print(f"{self},end reached")
            self.airspace.remove_drone(self)

    @staticmethod
    def end_between(upper, lower, end):
        if upper < end < lower or upper > end > lower:
            return True
        return False
