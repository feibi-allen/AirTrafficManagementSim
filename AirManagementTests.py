import unittest
import math
import simpy
import DroneFile, AirspaceFile

class TestDroneCollisionDetection(unittest.TestCase):

    def setUp(self):
        # Set up the simulation environment
        self.env = simpy.Environment()

        # Create drones
        self.drone1 = DroneFile.Drone(speed=5, start=[0, 0, 0], end=[10, 0, 0])
        self.drone2 = DroneFile.Drone(speed=5, start=[10, 1, 0], end=[0, 1, 0])

        # Create airspace
        self.airspace = AirspaceFile.Airspace(self.env)

    def test_initialization(self):
        # Test if drones are initialized correctly
        self.assertEqual(self.drone1.get_start(), [0, 0, 0])
        self.assertEqual(self.drone1.get_end(), [10, 0, 0])
        self.assertEqual(self.drone1.get_speed(), 5)
        self.assertEqual(self.drone2.get_start(), [10, 1, 0])
        self.assertEqual(self.drone2.get_end(), [0, 1, 0])
        self.assertEqual(self.drone2.get_speed(), 5)

    def test_velocity_calculation(self):
        # Test if the horizontal velocity is calculated correctly
        self.assertEqual(self.drone1.max_h_velocity, [5.0, 0.0, 0.0])
        self.assertEqual(self.drone2.max_h_velocity, [-5.0, 0.0, 0.0])

    def test_move(self):
        # Test if drones move according to their velocity
        self.drone1.go_horizontal()
        self.drone1.move(1)
        self.assertEqual(self.drone1.pos, [5.0, 0.0, 0.0])

        self.drone2.go_horizontal()
        self.drone2.move(1)
        self.assertEqual(self.drone2.pos, [5.0, 1.0, 0.0])

    def test_no_collision(self):
        # Test the scenario where no collision is detected
        self.airspace.add_drone(self.drone1)
        self.airspace.add_drone(self.drone2)

        self.airspace.get_time_of_next_collision()
        self.assertIsNone(self.airspace.next_collision)

    def test_collision_detection(self):
        # Adjust the position of the drones to ensure a collision
        self.drone2 = DroneFile.Drone(speed=5, start=[5, 0, 0], end=[-5, 0, 0])
        self.airspace.add_drone(self.drone1)
        self.airspace.add_drone(self.drone2)

        self.airspace.get_time_of_next_collision()
        self.assertIsNotNone(self.airspace.next_collision)

        collision_time, drones_involved = self.airspace.next_collision
        self.assertAlmostEqual(collision_time, 1)
        self.assertIn(self.drone1, drones_involved)
        self.assertIn(self.drone2, drones_involved)

    def test_faster_drone_gives_way(self):
        # Test that the faster drone gives way in the event of an imminent collision
        self.drone2 = DroneFile.Drone(speed=7, start=[10, 0, 0], end=[0, 0, 0])  # Faster drone
        self.airspace.add_drone(self.drone1)
        self.airspace.add_drone(self.drone2)

        self.airspace.get_time_of_next_collision()

        faster_drone = self.airspace.get_faster_drone()
        self.assertEqual(faster_drone, self.drone2)

if __name__ == '__main__':
    unittest.main()
