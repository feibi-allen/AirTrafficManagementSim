import math

class Drone:
    def __init__(self,speed,start,end):
        # FIXME - error checking for speed and pos correct structure
        self.pos = start
        self.start = start
        self.end = end
        self.target_height = start[2]
        self.max_speed = speed # maximum speed
        self.max_h_velocity = self._calculate_horizontal_velocity()
        self.current_velocity = [0,0,0]

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

        vel_x = math.sqrt(((self.max_speed ** 2) / delt_square_sum) * delt_x_sq)
        if self.end[0] < self.start[0]:
            vel_x = -abs(vel_x)
        vel_y = math.sqrt(((self.max_speed ** 2) / delt_square_sum) * delt_y_sq)
        if self.end[1] < self.start[1]:
            vel_y = -abs(vel_y)
        velocity = [vel_x, vel_y,0]

        return velocity

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_position(self):
        return  self.pos

    def set_target_height(self,height):
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
        self.current_velocity = [0,0,self.max_speed]

    def stop(self):
        self.current_velocity = [0,0,0]

    def move(self,time):
        #FIXME - check if it will move past there it is meant to be
        self.pos[0] += self.current_velocity[0] * time
        self.pos[1] += self.current_velocity[1] * time
        self.pos[2] += self.current_velocity[2] * time

    def has_arrived(self):
        # FIXME - write it
        pass

