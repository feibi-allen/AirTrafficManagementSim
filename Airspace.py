import math


class Airspace(object):

    def __init__(self):
        self.occupied_space = {}
        self.next_pos = {}
        self.drones = []
        self.MINIMUM_DISTANCE = 3

    def predict_collisions(self, drone):
        """
        Calculates when drones will collide based on start pos and velocity
        :param drone: asking drone
        :return:
        """
        # assign variables
        start_x, start_y = drone.get_start()[0], drone.get_start()[1]
        x_vel, y_vel = drone.get_velocity()[0], drone.get_velocity()[0]
        # dont check itself
        for other_drone in self.drones.remove(drone):
            # assign variables
            other_start_x, other_start_y = other_drone.get_start()[0], \
                other_drone.get_start()[1]
            other_x_vel, other_y_vel = other_drone.get_velocity[0], \
                other_drone.get_velocity[1]

            # maths variables
            delta_x = other_start_x - start_x
            delta_x_vel = other_x_vel - x_vel
            delta_y = other_start_y - start_y
            delta_y_vel = other_y_vel - y_vel

            a = (delta_x_vel ^ 2) + (delta_y_vel ^ 2)
            b = 2 * (delta_x * delta_x_vel + delta_y * delta_y_vel)
            c = (delta_x ^ 2) + (delta_y * 2) - (self.MINIMUM_DISTANCE ^ 2)

            # maths equations

            # check b< or = or > 4ac
            # FIXME - check within range of drones paths
            if b < 4 * a * c:
                pass
            if b == 4 * a * c:
                point_of_collision = b + math.sqrt((b ^ 2) - 4 * a * c)
                self.set_callback(drone, other_drone, point_of_collision)
                pass
            if b > 4 * a * c:
                point_of_collision_1 = b + math.sqrt((b ^ 2) - 4 * a * c)
                point_of_collision_2 = b - math.sqrt((b ^ 2) - 4 * a * c)

                pass
            # set appropriate call backs

    def _in_range(self, drone, other_drone, point_of_collision):
        """
        Checks if intersection of drone paths will happen within path ranges
        :param drone:
        :param other_drone:
        :param point_of_collision:
        :return:
        """
        d_start_x, d_start_y = drone.get_start()[0], drone.get_start()[1]
        od_start_x, od_start_y = other_drone.get_start()[0], \
        other_drone.get_start()[1]
        # FIXME - fill rest
        return True

    def _set_callback(self, drone, other_drone, point_of_collision):
        """
        Sets a callback for the two drones involved in the potential collision,
        so they can resolve it later
        :param drone:
        :param other_drone:
        :param point_of_collision:
        :return:
        """
        pass
