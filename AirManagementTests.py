import unittest
import Airspace
import Drone


class AirspaceTest(unittest.TestCase):
    def setUp(self):
        self.airspace = Airspace()
        self.drone1 = Drone(1, (0, 0), (1, 1), (10, 10))
        self.drone2 = Drone(2, (5, 5), (-1, -1), (0, 0))
        self.drone3 = Drone(3, (10, 10), (0, -1), (10, 0))
        self.airspace.add_drone(self.drone1)
        self.airspace.add_drone(self.drone2)
        self.airspace.add_drone(self.drone3)

    def test_add_drone(self):
        self.assertEqual(len(self.airspace.drones), 3)
        new_drone = Drone(4, (15, 15), (0, 1), (15, 20))
        self.airspace.add_drone(new_drone)
        self.assertIn(new_drone, self.airspace.drones)

    def test_remove_drone(self):
        self.assertEqual(len(self.airspace.drones), 3)
        self.airspace.remove_drone(self.drone1)
        self.assertNotIn(self.drone1, self.airspace.drones)
        self.assertEqual(len(self.airspace.drones), 2)



if __name__ == '__main__':
    unittest.main()
