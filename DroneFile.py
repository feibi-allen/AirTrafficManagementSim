import math
# from AirspaceFile import Airspace


class Drone:
    def __init__(self, speed, start, end, airspace, id_str):
        from AirspaceFile import Airspace

        if not isinstance(speed, (int, float)):
            raise TypeError("Speed must be numeric")
        self._check_coord(start)
        self._check_coord(end)
        if start == end:
            raise ValueError("Start and end points cannot be the same")
        if speed == 0:
            raise ValueError("Speed cannot be 0")

        # assign attributes
        self.pos = start.copy()
        self.start = start
        self.end = end
        self.target_height = start[2]
        self.max_speed = speed  # maximum speed
        self.max_h_velocity = self._calculate_horizontal_velocity()
        self.current_velocity = [0, 0, 0]
        self.id = str(id_str)
        self.airspace = airspace
        airspace.add_drone(self)

    @staticmethod
    def _check_coord(param):
        if not (type(param) is list):
            raise TypeError("Start and end must be in form [x,y,z]")
        if len(param) != 3:
            raise TypeError("Start and end must be in form [x,y,z]")
        for i in param:
            if not isinstance(i, (int, float)):
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
            return [0, 0, 0]

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

    def get_id(self):
        return self.id

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
        self.current_velocity[:] = self.max_h_velocity[:]

    def go_vertical(self):
        if self.pos[2] > self.target_height:
            self.current_velocity = [0, 0, -abs(self.max_speed)]
        else:
            self.current_velocity = [0, 0, self.max_speed]

    def stop(self):
        print(f"{self.id},stopping")
        self.current_velocity = [0, 0, 0]

    def move(self, time):
        if self.current_velocity[2] != 0:
            self._move_vertical(time)
        else:
            self._move_horizontal(time)

    def _move_horizontal(self, time):
        print(f"{self.id}, moving horizontal at {self.get_velocity()}")
        x_change = self.current_velocity[0] * time
        y_change = self.current_velocity[1] * time

        if self.end_between(self.pos[0], x_change, self.end[0]) and \
                self.end_between(self.pos[1], y_change, self.end[1]):
            self.pos[0] = self.end[0]
            self.pos[1] = self.end[1]

        # error if x or y end is reached but the drone will move off it
        # this would mean there was an error in velocity calcs
        elif self.end_between(self.pos[0], x_change, self.end[0]) and \
                self.current_velocity[0] != 0:
            raise ArithmeticError("Drone path incorrectly followed, x end "
                                  "reached but not y")

        elif self.end_between(self.pos[1], y_change, self.end[1]) and \
                self.current_velocity[1] != 0:
            raise ArithmeticError("Drone path incorrectly followed, y end "
                                  "reached but not x")

        else:
            self.pos[0] += self.current_velocity[0] * time
            self.pos[1] += self.current_velocity[1] * time

    def _move_vertical(self, time):
        print(f"{self.id},moving vertical at {self.get_velocity()}")
        z_change = self.current_velocity[2] * time
        if self.end_between(self.pos[2], z_change, self.target_height):
            self.pos[2] = self.target_height
        else:
            self.pos[2] += self.current_velocity[2]

    @staticmethod
    def end_between(position, change, end):
        # change should be positive or negative already be signed
        if position < end < position + change:
            return True
        if position > end > position + change:
            return True
        return False

    def end_reached(self):
        if self.pos == self.end:
            return True