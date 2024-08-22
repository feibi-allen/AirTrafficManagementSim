import simpy
import math
from DroneFile import Drone

MINIMUM_DISTANCE = 1  # closest drones can get to each-other
BUFFER_TIME = 1  # time before reaching minimum distance that drones stop
TIME_BETWEEN_CALCULATIONS = 1  # time between each collision calculation


class Airspace(object):

    def __init__(self, env):
        self.drones = []
        self.next_collision = None
        self.env = env
        self.check_collisions_process = env.process(self.run_airspace())

    def add_drone(self, drone):
        self.drones.append(drone)

    def remove_drone(self, drone):
        self.drones.remove(drone)

    def run_airspace(self):
        """
        synchronise the airspace
        :return:
        """
        while True:  # FIXME - change to while some drone not finished
            for drone in self.drones:
                # FIXME - check if in correct vertical position first
                # FIXME - check if starting position is too close
                drone.go_horizontal()

            self.get_time_of_next_collision()

            imminent_collision = True
            while imminent_collision:
                if self.next_collision is not None:
                    if self.next_collision <= TIME_BETWEEN_CALCULATIONS:
                        # faster drone will be one overtaking so must give way
                        self.get_faster_drone().stop()

                self.get_time_of_next_collision()
                if self.next_collision is None or self.next_collision > TIME_BETWEEN_CALCULATIONS:
                    imminent_collision = False

            yield self.env.timeout(TIME_BETWEEN_CALCULATIONS)

            for drone in self.drones:
                drone.move()

    def get_faster_drone(self):
        drone1, drone2 = self.next_collision[1][0], self.next_collision[1][2]
        print(f"drone1:{drone1}, drone2:{drone2}")
        if drone1.get_speed() >= drone2.get_speed():
            return drone1
        return drone2

    def get_time_of_next_collision(self):
        """
        Calculates time (from drones current position) to which safety
        circumference around the drones will intersect based on position
        and velocity. (quadratic of distance between drones against time)
        Sets self.next_collision to the smallest time and drones involved.
        (time,[drone,other_drone]) else if no collision: None
        """
        collision_time = None

        # can be optimised to check pairs only,
        # not all other drones for each drone
        for drone in self.drones:
            pos_x, pos_y = drone.get_position()[0], drone.get_position()[1]
            x_vel, y_vel = drone.get_velocity()[0], drone.get_velocity()[1]

            # FIXME
            # If Drone is moving vertically don't check it for collision with
            # other drones, it will reserve the column and other drones will
            # check to see if they will fly into the column and avoid
            if x_vel==0 and y_vel==0:
                continue

            for other_drone in [d for d in self.drones if d != drone]:
                # primary variables
                other_pos_x, other_pos_y = other_drone.get_position()[0], \
                    other_drone.get_position()[1]

                other_x_vel, other_y_vel = other_drone.get_velocity()[0], \
                    other_drone.get_velocity()[1]

                # secondary variables
                delta_x = other_pos_x - pos_x
                delta_x_vel = other_x_vel - x_vel
                delta_y = other_pos_y - pos_y
                delta_y_vel = other_y_vel - y_vel

                # quadratic variables
                a = (delta_x_vel ** 2) + (delta_y_vel ** 2)
                b = 2 * (delta_x * delta_x_vel + delta_y * delta_y_vel)
                c = (delta_x ** 2) + (delta_y ** 2) - (MINIMUM_DISTANCE ** 2)

                # maths equations
                time_of_collision = self.calculate_collision_time(a, b, c,
                                                                  drone,
                                                                  other_drone)

                if time_of_collision is not None:
                    if collision_time is None:
                        collision_time = (
                        time_of_collision, [drone, other_drone])
                    elif time_of_collision < collision_time[0]:
                        collision_time = (
                        time_of_collision, [drone, other_drone])

            self.next_collision = collision_time

    def calculate_collision_time(self, a, b, c, drone, other_drone):
        """
        Does quadratic calculation of distance between drones to find the time
        the drones are within minimum distance of each-other
        :param a: (delta_x_vel ** 2) + (delta_y_vel ** 2)
        :param b: 2 * (delta_x * delta_x_vel + delta_y * delta_y_vel)
        :param c: delta_x ** 2) + (delta_y ** 2) - (self.MINIMUM_DISTANCE ** 2)
        :param drone:
        :param other_drone:
        :return: first time the drones are within minimum distance of
        each-other if there is one
        """
        if a == 0:
            return None
        if (b ** 2) == 4 * a * c:
            time_of_collision = (-b + math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            # print("point of collision", time_of_collision)
            if self._in_range(drone, other_drone, time_of_collision):
                # print("within range")
                return time_of_collision
        if (b ** 2) > 4 * a * c:
            time_of_collision_1 = (-b + math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            time_of_collision_2 = (-b - math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            # print("points of collisions", time_of_collision_1, time_of_collision_2)
            # print("first point of contact:", min(time_of_collision_2, time_of_collision_1))
            if self._in_range(drone, other_drone,
                              min(time_of_collision_2, time_of_collision_1)):
                # print("t min within range")
                return min(time_of_collision_2, time_of_collision_1)
        return None

    def _in_range(self, drone, other_drone, time_of_collision):
        """
        Checks if intersection of drone paths will happen within path ranges
        :param drone:
        :param other_drone:
        :param time_of_collision:
        :return:
        """
        if time_of_collision < 0:
            return False
        if time_of_collision >= self._time_to_arrival(drone):
            return False
        if time_of_collision >= self._time_to_arrival(other_drone):
            return False
        return True

    @staticmethod
    def _time_to_arrival(drone):
        """
        :param drone:
        :return: the time it will take for the drone to reach its end point
        """
        c_pos_x, c_pos_y = drone.get_position()[0], drone.get_position()[1]
        e_pos_x, e_pos_y = drone.get_end()[0], drone.get_end()[1]
        v_x, v_y = drone.get_velocity()[0], drone.get_velocity()[1]
        distance = math.sqrt(
            ((e_pos_x - c_pos_x) ** 2) + ((e_pos_y - c_pos_y) ** 2))
        velocity = math.sqrt((v_y ** 2) + (v_x ** 2))
        return distance / velocity
