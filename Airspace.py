class Airspace(object):

    def __init__(self):
        self.occupied_space = {}
        self.next_pos = {}

    # im so confused
    def __force_yield(self,drone):
        pass
    def __imminent_collision(self, drone):
        """
        :param: (object) Takes the asking drone
        :return: List of drones close to asking drones next position or who's
        next position is close to asking drones next position
        """
        pass

    def stop_drone(self, drone):
        """
        :param: (object) Takes the asking drone
        :return: True if asking drone must stop to avoid collision
        """