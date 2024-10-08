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
            Drone(1, [1, 2, 3], [1, 2, 4], "a", "a", "b")

    def test_param_value_checks(self):
        with self.assertRaises(TypeError):
            Drone("a", [1, 2, 3], [1, 2, 4], "a", "1")

        with self.assertRaises(TypeError) as context:
            Drone(1, [2, 3], [1, 2, 4], "a", "1")
        self.assertEqual(str(context.exception),
                         "Start and end must be in form [x,y,z]")

        with self.assertRaises(TypeError) as context:
            Drone(1, "[2, 3]", [1, 2, 4], "a", "1")
        self.assertEqual(str(context.exception),
                         "Start and end must be in form [x,y,z]")

        with self.assertRaises(TypeError) as context:
            Drone(1, [1, 2, 3], "[1, 2, 4]", "a", "1")
        self.assertEqual(str(context.exception),
                         "Start and end must be in form [x,y,z]")

        with self.assertRaises(TypeError) as context:
            Drone(1, ["a", 2, 3], [1, 2, 4], "a", "1")
        self.assertEqual(str(context.exception),
                         "[x,y,z] must be numeric")

        with self.assertRaises(ValueError) as context:
            Drone(1, [1, 2, 3], [1, 2, 3], "a", "1")
        self.assertEqual(str(context.exception),
                         "Start and end points cannot be the same")

    def test_check_direction_velocity(self):
        drone = Drone(speed=5, start=[0, 0, 0], end=[18, 24, 0], airspace="a",
                      id_str="1")
        drone.go_vertical()
        self.assertEqual(drone.get_velocity(), [0, 0, 5])
        drone.go_horizontal()
        self.assertEqual(drone.get_velocity(), [3, 4, 0])

        drone = Drone(speed=3, start=[0, 0, 0], end=[10, 0, 2], airspace="a",
                      id_str="1")
        drone.go_vertical()
        self.assertEqual(drone.get_velocity(), [0, 0, 3])
        drone.go_horizontal()
        self.assertEqual(drone.get_velocity(), [3, 0, 0])

        drone = Drone(speed=2, start=[0, 0, 2], end=[2, 2, 0], airspace="a",
                      id_str="1")
        drone.go_vertical()
        self.assertEqual(drone.get_velocity(), [0, 0, -2])
        drone.go_horizontal()
        self.assertEqual(drone.get_velocity(),
                         [math.sqrt((2 ** 2) / 2), math.sqrt((2 ** 2) / 2), 0])

    def test_move_horizontal_y(self):
        drone = Drone(speed=7, start=[1, -4, 2], end=[1, 9, 2], airspace="a",
                      id_str="1")
        drone.go_horizontal()
        drone.move(1)
        self.assertEqual(drone.get_position(), [1, 3, 2])

    def test_move_horizontal_x(self):
        drone = Drone(speed=6, start=[1, -4, 2], end=[-10, -4, 2],
                      airspace="a", id_str="1")
        drone.go_horizontal()
        drone.move(1)
        self.assertEqual(drone.get_position(), [-5, -4, 2])

    def test_reach_end_horizontal(self):
        """Tests if drone moves through end point that it will stop the drone
        in that horizontal plane"""
        drone = Drone(speed=5, start=[1, -4, 1], end=[4, -8, 2], airspace="a",
                      id_str="1")
        drone.go_horizontal()
        drone.move(3)
        self.assertEqual(drone.get_position(), [4, -8, 1])

    def test_move_vertical(self):
        drone = Drone(speed=6, start=[1, -4, 2], end=[-10, -4, 11],
                      airspace="a", id_str="1")
        drone.go_vertical()
        drone.move(1)
        self.assertEqual(drone.get_position(), [1, -4, 8])

    def test_reach_end_vertical(self):
        """Tests if the drone moves through end point that it will stop"""
        drone = Drone(speed=5, start=[1, -4, 9], end=[4, -8, 2], airspace="a",
                      id_str="1")
        drone.go_vertical()
        drone.move(3)
        self.assertEqual(drone.get_position(), [1, -4, 2])

    def test_reach_end(self):
        drone = Drone(speed=5, start=[1, -4, 9], end=[4, -8, 2], airspace="a",
                      id_str="1")
        drone.go_vertical()
        drone.move(3)
        drone.go_horizontal()
        drone.move(3)
        self.assertEqual(drone.get_position(), drone.get_end())

# FIXME - more tests
# zero speed
#small movements
