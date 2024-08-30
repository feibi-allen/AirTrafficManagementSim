import unittest
import math
from DroneFile import Drone


# written to be tested without real airspace,
# commented out airspace references in drone file for testing
class DroneTest(unittest.TestCase):

    def test_param_number_checks(self):
        self.assertRaises(TypeError, Drone)
        with self.assertRaises(TypeError):
            Drone(1)
        with self.assertRaises(TypeError):
            Drone(1, [1, 2, 3])
        with self.assertRaises(TypeError):
            Drone(1, [1, 2, 3], [1, 2, 4])
        with self.assertRaises(TypeError):
            Drone(1, [1, 2, 3], [1, 2, 4], "a", "a")

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
            Drone(1, [1, 2, 3], "[1, 2, 4]", "a")
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

    def test_check_direction_velocity1(self):
        drone1 = Drone(speed=5, start=[0, 0, 0], end=[18, 24, 0], airspace="a")
        drone1.go_vertical()
        self.assertEqual(drone1.get_velocity(), [0, 0, 5])
        drone1.go_horizontal()
        self.assertEqual(drone1.get_velocity(), [3, 4, 0])

        drone1 = Drone(speed=3, start=[0, 0, 0], end=[10, 0, 2], airspace="a")
        drone1.go_vertical()
        self.assertEqual(drone1.get_velocity(), [0, 0, 3])
        drone1.go_horizontal()
        self.assertEqual(drone1.get_velocity(), [3, 0, 0])

        drone1 = Drone(speed=2, start=[0, 0, 0], end=[2, 2, 2], airspace="a")
        drone1.go_vertical()
        self.assertEqual(drone1.get_velocity(), [0, 0, 2])
        drone1.go_horizontal()
        self.assertEqual(drone1.get_velocity(),
                         [math.sqrt((2 ** 2) / 2), math.sqrt((2 ** 2) / 2), 0])
