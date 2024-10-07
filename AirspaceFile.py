import simpy
import math
from DroneFile import Drone
import GraphicalSimulation as gs

COLLISION_DISTANCE = 1  # distance at which drones are considered crashing
BUFFER_TIME = 1  # time before reaching minimum distance that drones stop
TIME_STEP = 1  # amount of time between drones position being updated


class Airspace(object):

    def __init__(self, env):
        self.drones = []
        self.next_collision = None  # tuple or none (time, drones involved)
        self.env = env
        self.check_collisions_process = env.process(self.run_airspace)
        self.stop_airspace = env.event()
        self.text_flag_collision_occurred = False
        self.simulation = gs.Simulation([(0,10),(0,15),(0,20)])

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

    @property
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

            self.check_for_collision()

            if self.next_collision is not None:
                imminent_collision = True
            else:
                imminent_collision = False
            while imminent_collision:
                print(f"collision imminent: {self.next_collision[1][0].get_id(), self.next_collision[1][1].get_id()}")
                self.text_flag_collision_occurred = True
                if self.next_collision[0] <= TIME_STEP:
                    self.get_drone_to_stop().stop()

                self.check_for_collision()
                if self.next_collision is None or \
                        self.next_collision[0] > TIME_STEP:
                    imminent_collision = False

            yield self.env.timeout(TIME_STEP)

            for drone in self.drones:
                drone.move(TIME_STEP)

            # matplot
            self.simulation.update_plot(self.drones)


            for drone in self.drones:
                if drone.end_reached():
                    print(f"{drone.get_id()}, end reached")
                    self.remove_drone(drone)

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

    def get_drone_to_stop(self):
        """
        If one of the drones is stopped horizontally the other must stop
        Otherwise returns the faster drone which is required to stop as it
        is overtaking
        :return: drone to stop
        """
        drone1, drone2 = self.next_collision[1][0], self.next_collision[1][1]
        if drone1.get_velocity()[0] == 0 and drone1.get_velocity()[1] == 0:
            return drone2
        if drone2.get_velocity()[0] == 0 and drone2.get_velocity()[1] == 0:
            return drone1
        if drone1.get_speed() >= drone2.get_speed():
            return drone1
        return drone2

    def check_for_collision(self):
        """
        Sets self.next_collision to the smallest time and drones involved.
        (time,[drone,other_drone]) else if no collision: None
        """
        print("checking for collision")
        self.next_collision = None

        # can be optimised to check pairs only,
        for drone in self.drones:

            # helps to reduce number of checks by not iterating for drones
            # that are not moving horizontally and prevents errors in time to collision method
            if drone.get_velocity()[0] == 0 and drone.get_velocity()[1] == 0:
                continue

            else:
                for other_drone in [d for d in self.drones if d != drone]:
                    # reduce number of calculations by only checking for a
                    # collision if drones are on the same height level
                    # or the other drone is moving vertically
                    if other_drone.get_position()[2] != drone.get_position()[2] and other_drone.get_velocity()[2] == 0:
                        continue
                    else:
                        time_of_collision = self._calculate_time_of_intersection(drone, other_drone)

                        if time_of_collision is not None:
                            if self.next_collision is None:
                                self.next_collision = (
                                    time_of_collision, [drone, other_drone])
                            elif time_of_collision < self.next_collision[0]:
                                self.next_collision = (
                                    time_of_collision, [drone, other_drone])

    def _calculate_time_of_intersection(self, drone, other_drone):
        """
        Calculates time (from drones current position) to which safety
        circumference around the drones will intersect based on position
        and velocity. (quadratic of distance between drones against time)
        :param drone:
        :param other_drone:
        :return:
        """
        # primary variables
        pos_x, pos_y = drone.get_position()[0], drone.get_position()[1]
        x_vel, y_vel = drone.get_velocity()[0], drone.get_velocity()[1]
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
        c = (diff_x ** 2) + (diff_y ** 2) - (
                COLLISION_DISTANCE ** 2)

        time_of_collision = None

        if a != 0 and (b ** 2) >= 4 * a * c:
            time_1 = (-b + math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            time_2 = (-b - math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            time = min(time_2, time_1)
            if self._in_range(drone, time) and self._in_range(other_drone, time):
                time_of_collision = time

        if drone.end_between(drone.get_position()[0], drone.get_velocity()[0] * TIME_STEP,
                             drone.get_end()[0]) and drone.end_between(drone.get_position()[0],
                                                                 drone.get_velocity()[0] * TIME_STEP, drone.get_end()[0]):
            time_of_collision = self._calculate_end_collision(drone.get_end(), self._time_to_arrival(drone),
                                                              other_drone)
        if other_drone.end_between(other_drone.get_position()[0], other_drone.get_velocity()[0] * TIME_STEP,
                                   other_drone.get_end()[0]) and other_drone.end_between(other_drone.get_position()[0],
                                                                                   other_drone.get_velocity()[
                                                                                       0] * TIME_STEP,
                                                                                   other_drone.get_end()[0]):
            time_of_collision = self._calculate_end_collision(other_drone.get_end(), self._time_to_arrival(other_drone),
                                                              drone)

        return time_of_collision

    def _calculate_end_collision(self, position, time_of_other_drone_end, drone):
        """
        Calculates time at which a drone will intersect with the other drones end (if applicable)
        :param position:
        :param time_of_other_drone_end:
        :param drone:
        :return:
        """
        x_vel = drone.get_velocity()[0]
        y_vel = drone.get_velocity()[1]
        x_pos = drone.get_position()[0]
        y_pos = drone.get_position()[1]

        a = (x_vel ** 2) + (y_vel ** 2)
        b = ((x_pos - position[0]) * x_vel) + ((y_pos - position[1]) * y_vel)
        c = ((x_pos - position[0]) ** 2) + ((y_pos - position[1]) ** 2) - (COLLISION_DISTANCE ** 2)

        if a != 0 and (b ** 2) >= 4 * a * c:
            time_1 = (-b + math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            time_2 = (-b - math.sqrt((b ** 2) - 4 * a * c)) / (
                    2 * a)
            min_time = min(time_2, time_1)
            if self._in_range(drone, min_time) and min_time >= time_of_other_drone_end:
                return min_time
        return None

    def _in_range(self, drone, time_of_collision):
        """
        Checks if intersection of drone paths will happen within path ranges
        :param drone:
        :param time_of_collision:
        :return:
        """
        if time_of_collision < 0:
            return False
        try:
            if time_of_collision >= self._time_to_arrival(drone):
                return False
        except ZeroDivisionError:
            return True
        return True

    @staticmethod
    def _time_to_arrival(drone):
        """
        :param drone:
        :return: the time it will take for the drone to reach its end point
        """

        cur_pos_x, cur_pos_y = drone.get_position()[0], drone.get_position()[1]
        end_pos_x, end_pos_y = drone.get_end()[0], drone.get_end()[1]
        vel_x, vel_y = drone.get_velocity()[0], drone.get_velocity()[1]
        distance = math.sqrt(
            ((end_pos_x - cur_pos_x) ** 2) + ((end_pos_y - cur_pos_y) ** 2))
        velocity = math.sqrt((vel_y ** 2) + (vel_x ** 2))
        return distance / velocity
