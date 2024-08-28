import math
# from AirspaceFile import Airspace


class Drone:
    def __init__(self, speed, start, end, airspace):
        # FIXME - error checking for speed and pos correct structure
        # check for correct params
        if not isinstance(speed,(int,float)):
            raise TypeError("Speed must be numeric")
        self._check_coord(start)
        self._check_coord(end)
        if start == end:
            raise ValueError("Start and end points cannot be the same")

        # assign attributes
        self.pos = start
        self.start = start
        self.end = end
        self.target_height = start[2]
        self.max_speed = speed  # maximum speed
        self.max_h_velocity = self._calculate_horizontal_velocity()
        self.current_velocity = [0, 0, 0]
        self.airspace = airspace
        #airspace.add_drone(self)

    @staticmethod
    def _check_coord(param):
        if not (type(param) is list):
            raise TypeError("Start and end must be in form [x,y,z]")
        if len(param) != 3:
            raise TypeError("Start and end must be in form [x,y,z]")
        for i in param:
            if not isinstance(i,(int,float)):
                raise TypeError("[x,y,z] must be numeric")

    def _calculate_horizontal_velocity(self):
        """
        Converts max scalar speed to max vector velocity (2D only).
        :return: Velocity as a list [x,y,0]
        """
        delt_x_sq, delt_y_sq = ((self.end[0] - self.start[0]) ** 2,
                                (self.end[1] - self.start[1]) ** 2)
        delt_square_sum = delt_x_sq + delt_y_sq

        if delt_square_sum == 0:
            return [0,0,0]

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

    @staticmethod
    def _end_between(upper, lower, end):
        if upper < end < lower or upper > end > lower:
            return True
        return False

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
            self._move_vertical(time)
        elif self.pos[0] != self.end[0] and self.pos[1] != self.end[1]:
            self._move_horizontal(time)

        # if drone has reached x or y but not both path is incorrectly
        # calculated and should raise error
        else:
            raise ArithmeticError("Drone path incorrectly followed, end at x "
                                  "or y but not both")

        if self.pos == self.end:
            print(f"{self},end reached")
            self.airspace.remove_drone(self)

    def _move_horizontal(self, time):
        x_change = self.current_velocity[0] * time
        y_change = self.current_velocity[0] * time

        if self._end_between(self.pos[0], x_change, self.end[0]) and \
                self._end_between(self.pos[1], y_change, self.end[1]):
            self.pos[0] = self.end[0]
            self.pos[1] = self.end[1]

        # if drone will move past x or y but not both path is incorrectly
        # calculated and should raise error
        elif self._end_between(self.pos[0], x_change, self.end[0]) or \
                self._end_between(self.pos[1], y_change, self.end[1]):
            raise ArithmeticError("Drone path incorrectly followed, end "
                                  "between x or y but not both")

        else:
            self.pos[0] += self.current_velocity[0] * time
            self.pos[1] += self.current_velocity[0] * time

    def _move_vertical(self, time):
        z_change = self.current_velocity[2] * time
        if self._end_between(self.pos[2], z_change, self.end[2]):
            self.pos[2] = self.end[2]
        else:
            self.pos[2] += z_change
