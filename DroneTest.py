import unittest
from DroneFile import Drone

# written to be tested without real airspace,
# commented out airspace references in drone file for testing
class DroneTest(unittest.TestCase):

    def test_param_number_checks(self):
        self.assertRaises(TypeError,Drone)
        with self.assertRaises(TypeError):
            Drone(1)
        with self.assertRaises(TypeError):
            Drone(1, [1, 2, 3])
        with self.assertRaises(TypeError):
            Drone(1, [1, 2, 3], [1, 2, 4])
        with self.assertRaises(TypeError):
            Drone(1, [1, 2, 3], [1, 2, 4], "a","a")


