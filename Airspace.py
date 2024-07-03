class Airspace(object):

    def __init__(self):
        self.occupied_space = {}
        self.next_pos = {}
        self.drones = []
        self.MINIMUM_DISTANCE = 3

    def predict_collisions(self):
        """
        Calculates when drones will collide based on start pos and velocity
        :return: nothing
        """
        for drone in self.drones:
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
                #check b< or = or > 4ac
                # check within range of drones paths
                # set appropriate call backs
