import simpy
import math

MINIMUM_DISTANCE = 1 # closest drones can get to each-other
BUFFER_TIME = 1 # time before reaching minimum distance that drones stop
TIME_BETWEEN_CALCULATIONS = 1 # time between each collision calculation

class Airspace(object):

    def __init__(self,env):
        self.stationary_drones = {} # drone:position?
        self.moving_drones = []
        self.collision = None # head of linked list
        self.env = env
        self.check_collsions_process = env.process(self.run_airspace())


    def add_drone(self, drone):
        self.stationary_drones.append(drone)

    def remove_drone(self, drone):
        self.stationary_drones.remove(drone)


    def run_airspace(self):
        """
        synchronise the airspace
        :return:
        """
        #set all drones to go
        while True: # FIXME - change to while some drone not finished
            self.collision = self.get_time_of_first_collisions()
            yield self.env.timeout(TIME_BETWEEN_CALCULATIONS)


    def get_time_of_first_collisions(self, drone):
        # FIXME - split into smaller functions
        """
        Calculates times (from drones current position) to which safety
        circumference around the drones will intersect based on position
        and velocity. Since calculations are only made when both drones are
        moving time is the same for both.
        (quadratic of distance between drones against time)
        :param drone: asking drone
        :return: dict of first upcoming collision (drone colliding with, time)
        """
        collision_times = {}
        # assign variables
        pos_x, pos_y = drone.get_position()[0], drone.get_position()[1]
        #print("d1 pos:", pos_x, pos_y)
        x_vel, y_vel = drone.get_velocity()[0], drone.get_velocity()[1]
        #print("d1 vels:", x_vel, y_vel)
        # don't check itself
        for other_drone in [d for d in self.drones if d != drone]:
            # assign variables
            other_pos_x, other_pos_y = other_drone.get_position()[0], \
                other_drone.get_position()[1]
            #print("d2 pos:", other_pos_x, other_pos_y)
            other_x_vel, other_y_vel = other_drone.get_velocity()[0], \
                other_drone.get_velocity()[1]
            #print("d2 vels:", other_x_vel, other_y_vel)

            # maths variables
            delta_x = other_pos_x - pos_x
            #print("delt x:", delta_x)
            delta_x_vel = other_x_vel - x_vel
            #print("delt x vel:", delta_x_vel)
            delta_y = other_pos_y - pos_y
            #print("delt y:", delta_y)
            delta_y_vel = other_y_vel - y_vel
            #print("delt y vel:", delta_y_vel)

            a = (delta_x_vel ** 2) + (delta_y_vel ** 2)
            b = 2 * (delta_x * delta_x_vel + delta_y * delta_y_vel)
            c = (delta_x ** 2) + (delta_y ** 2) - (self.MINIMUM_DISTANCE ** 2)
            #print("a:", a, "b:", b, "c:", c)

            # maths equations
            time_of_collision = self.calculate_collision_time(a,b,c,drone,other_drone)
            if time_of_collision is not None:
                collision_times[other_drone] = time_of_collision

        #print(collision_times)
        if len(collision_times) > 0:
            time_of_first_collision = min(
                [val for val in collision_times.values()])
            return {key: val for key, val in collision_times.items() if
                    val == time_of_first_collision}
        return None

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
