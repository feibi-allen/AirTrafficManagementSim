import unittest
from unittest.mock import patch
import simpy
from DroneFile import Drone
from AirspaceFile import Airspace, COLLISION_DISTANCE


class AirspaceTest(unittest.TestCase):

    def setUp(self):
        self.env = simpy.Environment()
        self.airspace = Airspace(self.env)

    def test_add_drones(self):
        drone1 = Drone(speed=5, start=[0, 0, 0], end=[10, 10, 10],
                       airspace=self.airspace, id_str="1")
        drone2 = Drone(speed=5, start=[10, 10, 10], end=[0, 0, 10],
                       airspace=self.airspace, id_str="2")
        self.assertIn(drone1, self.airspace.drones)
        self.assertIn(drone2, self.airspace.drones)

    def test_drones_start_too_close(self):
        drone3 = Drone(speed=5, start=[9.5, 10, 0], end=[10, 10, 10],
                       airspace=self.airspace, id_str="3")
        drone4 = Drone(speed=5, start=[10, 10, 10], end=[0, 0, 10],
                       airspace=self.airspace, id_str="4")
        self.assertIn(drone3, self.airspace.drones)
        self.assertNotIn(drone4, self.airspace.drones)

    def test_remove_drone(self):
        drone5 = Drone(speed=5, start=[0, 0, 0], end=[10, 10, 10],
                       airspace=self.airspace, id_str="5")
        self.assertIn(drone5, self.airspace.drones)
        self.airspace.remove_drone(drone5)
        self.assertEqual(self.airspace.drones, [])

    def test_set_drone_target_height(self):
        drone6 = Drone(speed=5, start=[0, 0, 0], end=[10, 10, 5],
                       airspace=self.airspace, id_str="6")
        drone7 = Drone(speed=5, start=[10, 0, 0], end=[0, 1, 8],
                       airspace=self.airspace, id_str="7")
        self.airspace.set_drone_target_height()
        self.assertEqual(drone6.get_target_height(), 2 * COLLISION_DISTANCE)
        self.assertEqual(drone7.get_target_height(), 8 * COLLISION_DISTANCE)

    def test_no_collision(self):
        Drone(speed=5, start=[0, 0, 0], end=[10, 10, 0],
              airspace=self.airspace, id_str="a")
        Drone(speed=5, start=[15, 15, 0], end=[5, 5, 0],
              airspace=self.airspace, id_str="b")
        self.env.run(until=20)
        self.assertEqual(self.airspace.text_flag_collision_occurred, False)

    def test_detect_collision(self):
        Drone(speed=5, start=[0, 0, 0], end=[10, 10, 0],
              airspace=self.airspace, id_str="c")
        Drone(speed=3, start=[2, 0, 0], end=[10, 10, 0],
              airspace=self.airspace, id_str="d")
        self.env.run(until=20)
        self.assertEqual(self.airspace.text_flag_collision_occurred, True)

    def test_collision_resolve(self):
        # fill