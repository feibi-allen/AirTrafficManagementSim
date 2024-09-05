import unittest
import math
import simpy
from DroneFile import Drone
from AirspaceFile import Airspace, MINIMUM_DISTANCE


class AirspaceTest(unittest.TestCase):

    def setUp(self):
        self.env = simpy.Environment()
        self.airspace = Airspace(self.env)

    def tearDown(self):
        # Remove all drones from the airspace
        for drone in self.airspace.drones:
            self.airspace.remove_drone(drone)

    def test_add_drones(self):
        drone1 = Drone(speed=5, start=[0, 0, 0], end=[10, 10, 10],
                       airspace=self.airspace)
        drone2 = Drone(speed=5, start=[10, 10, 10], end=[0, 0, 10],
                       airspace=self.airspace)
        self.assertIn(drone1, self.airspace.drones)
        self.assertIn(drone2, self.airspace.drones)

    def test_drones_start_too_close(self):
        drone1 = Drone(speed=5, start=[9.5, 10, 0], end=[10, 10, 10],
                       airspace=self.airspace)
        drone2 = Drone(speed=5, start=[10, 10, 10], end=[0, 0, 10],
                       airspace=self.airspace)
        self.assertIn(drone1, self.airspace.drones)
        self.assertNotIn(drone2, self.airspace.drones)

    def test_remove_drone(self):
        drone = Drone(speed=5, start=[0, 0, 0], end=[10, 10, 10],
                      airspace=self.airspace)
        self.airspace.remove_drone(drone)
        self.assertNotIn(drone, self.airspace.drones)

    def test_set_drone_target_height(self):
        drone1 = Drone(speed=5, start=[0, 0, 0], end=[10, 10, 5],
                       airspace=self.airspace)
        drone2 = Drone(speed=5, start=[10, 0, 0], end=[0, 1, 8],
                       airspace=self.airspace)
        self.airspace.set_drone_target_height()
        self.assertEqual(drone1.get_target_height(), 2 * MINIMUM_DISTANCE)
        self.assertEqual(drone2.get_target_height(), 8 * MINIMUM_DISTANCE)

    def test_collision_detection(self):
        Drone(speed=5, start=[0, 0, 0], end=[10, 10, 0],
              airspace=self.airspace)
        Drone(speed=5, start=[15, 15, 0], end=[5, 5, 0],
              airspace=self.airspace)
        self.env.run(until=20)
        self.assertIsNone(self.airspace.next_collision)
