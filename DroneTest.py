import unittest
from DroneFile import Drone

# written to be tested without real airspace,
# commented out airspace references in drone file for testing
class DroneTest(unittest.TestCase):

    def setup(self):
        self.drone1 = Drone(speed=5, start=[0, 0, 0], end=[10, 0, 2],airspace="a")

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

    def test_param_value_checks(self):
        with self.assertRaises(TypeError):
            Drone("a", [1, 2, 3], [1, 2, 4], "a")

        with self.assertRaises(TypeError) as context:
            Drone(1, [2, 3], [1, 2, 4], "a")
        self.assertEqual(str(context.exception),
                         "Start and end must be in form [x,y,z]")

        with self.assertRaises(TypeError) as context:
            Drone(1, "[2, 3]", [1, 2, 4], "a")
        self.assertEqual(str(context.exception),
                         "Start and end must be in form [x,y,z]")

        with self.assertRaises(TypeError) as context:
            Drone(1, [1,2, 3], "[1, 2, 4]", "a")
        self.assertEqual(str(context.exception),
                         "Start and end must be in form [x,y,z]")

        with self.assertRaises(TypeError) as context:
            Drone(1, ["a", 2, 3], [1, 2, 4], "a")
        self.assertEqual(str(context.exception),
                         "[x,y,z] must be numeric")

        with self.assertRaises(ValueError) as context:
            Drone(1, [1, 2, 3], [1, 2, 3], "a")
        self.assertEqual(str(context.exception),
                         "Start and end points cannot be the same")

    def test_calculate_vel(self):
