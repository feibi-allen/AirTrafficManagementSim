import simpy
import math
from DroneFile import Drone

COLLISION_DISTANCE = 1  # distance at which drones are considered crashing
BUFFER_TIME = 1  # time before reaching minimum distance that drones stop
TIME_STEP = 1  # amount of time between drones position being updated


class Airspace(object):

    def __init__(self, env):
        self.drones = []
        self.next_collision = None  # tuple or none (time, drones involved)
        self.env = env
        self.check_collisions_process = env.process(self.run_airspace())
        self.stop_airspace = env.event()

    def add_drone(self, drone):
        # To avoid issues with drones crashing vertically no drones will be
        # able to start in the same column.
        # additional checks can be made to allow more drones to be added:
        # check target height of drones when adding, then check if drones will
        # get too close when traveling to their required heights
        for other_drone in self.drones:
            x_pos, y_pos = drone.get_position()[0], drone.get_position()[1]
            other_x_pos, other_y_pos = other_drone.get_position()[0], \
                other_drone.get_position()[1]

            if math.sqrt(((other_x_pos - x_pos) ** 2) + (
                    (other_y_pos - y_pos) ** 2)) <= COLLISION_DISTANCE:
                print("Drones start too close")
                return
        self.drones.append(drone)

    def remove_drone(self, drone):
        self.drones.remove(drone)
        print(f"{drone.get_id()},removed")

    def run_airspace(self):
        """
        synchronise and runs the airspace until all drones have reached their
        destination
        :return:
        """
        while self.drones:
            for drone in self.drones:
                print(f"{drone.get_id()}:{drone.get_position()}", end=", ")
            print()
            self.set_drone_target_height()
            self.set_drone_velocities()

            self.get_time_of_next_collision()
            if self.next_collision is not None:
                imminent_collision = True
            else:
                imminent_collision = False
            while imminent_collision:
                print("collision imminent")
                if self.next_collision[0] <= TIME_STEP:
                    # faster drone will be one overtaking so must give way
                    self.get_faster_drone().stop()

                self.get_time_of_next_collision()
                if self.next_collision is None or \
                        self.next_collision[0] > TIME_STEP:
                    imminent_collision = False

            yield self.env.timeout(TIME_STEP)

            for drone in self.drones:
                # logic handled in drone to reduce load on airspace
                drone.move(TIME_STEP)
        self.stop_airspace.succeed()

    def set_drone_velocities(self):
        for drone in self.drones:
            if drone.get_position()[2] != drone.get_target_height():
                drone.go_vertical()
            else:
                drone.go_horizontal()

    def set_drone_target_height(self):
        for drone in self.drones:
            x_pos, y_pos = drone.get_position()[0], drone.get_position()[1]
            end_x, end_y = drone.get_end()[0], drone.get_end()[1]
            # fly at protocol height unless end column is reached, then target
            # height is set to end pos so drone will move toward end pos
            if x_pos == end_x and y_pos == end_y:
                drone.set_target_height(drone.get_end()[2])
            else:
                drone.set_target_height(self.get_required_drone_height(drone))

    @staticmethod
    def get_required_drone_height(drone):
        """
        Returns height that the drone should fly at depending on heading,
        0-89, 90-179, 180-269, 270-359. x * minimum distance ensures that even
        if drones fly in a column they will not get within minimum distance of
        each-other
        :param drone:
        :return:
        """
        delta_x = drone.get_end()[0] - drone.get_start()[0]
        delta_y = drone.get_end()[1] - drone.get_start()[1]
        if delta_x >= 0 and delta_y > 0:
            return 2 * COLLISION_DISTANCE
        if delta_x > 0 and delta_y <= 0:
            return 4 * COLLISION_DISTANCE
        if delta_x <= 0 and delta_y < 0:
            return 6 * COLLISION_DISTANCE
        if delta_x < 0 and delta_y >= 0:
            return 8 * COLLISION_DISTANCE
        raise ArithmeticError("Could not calculate required height")

    def get_faster_drone(self):
        drone1, drone2 = self.next_collision[1][0], self.next_collision[1][1]
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
        collision_info = None

        # can be optimised to check pairs only,
        # not all other drones for each drone
        for drone in self.drones:
            pos_x, pos_y = drone.get_position()[0], drone.get_position()[1]
            x_vel, y_vel = drone.get_velocity()[0], drone.get_velocity()[1]

            # helps to reduce number of checks by not iterating for drones
            # that are not moving horizontally
            if x_vel == 0 and y_vel == 0:
                continue

            else:
                # FIXME - maths is wrong
                for other_drone in [d for d in self.drones if d != drone]:
                    # reduce number of calculations by only checking for a
                    # collision if drones are on the same height level
                    # or the other drone is moving vertically
                    if other_drone.get_position()[2] != drone.get_position()[2] and other_drone.get_velocity[2] == 0:
                        continue
                    else:
                        # primary variables
                        other_pos_x = other_drone.get_position()[0]
                        other_pos_y = other_drone.get_position()[1]

                        other_x_vel = other_drone.get_velocity()[0]
                        other_y_vel = other_drone.get_velocity()[1]

                        # secondary variables
                        diff_x = other_pos_x - pos_x
                        diff_x_vel = other_x_vel - x_vel
                        diff_y = other_pos_y - pos_y
                        diff_y_vel = other_y_vel - y_vel

                        # quadratic variables
                        a = (diff_x_vel ** 2) + (diff_y_vel ** 2)
                        b = 2 * (diff_x * diff_x_vel + diff_y * diff_y_vel)
                        c = (diff_x ** 2) + (diff_y ** 2) - (COLLISION_DISTANCE ** 2)

                        # maths equations
                        time_of_collision = self.calculate_collision_time(a, b, c, drone, other_drone)

                        if time_of_collision is not None:
                            if collision_info is None:
                                collision_info = (
                                    time_of_collision, [drone, other_drone])
                            elif time_of_collision < collision_info[0]:
                                collision_info = (
                                    time_of_collision, [drone, other_drone])

            self.next_collision = collision_info

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
            time = (-b + math.sqrt((b ** 2) - 4 * a * c)) / (2 * a)
            if self._in_range(drone, other_drone, time):
                return time

        if (b ** 2) > 4 * a * c:
            time_1 = (-b + math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            time_2 = (-b - math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            time = min(time_2, time_1)
            if self._in_range(drone, other_drone, time):
                return time

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
