import unittest
from unittest.mock import patch
from CleaningRobot import CleaningRobot
from CleaningRobotError import CleaningRobotError


class CleaningRobotTest(unittest.TestCase):
    """
    Your tests go here
    """
    def setUp(self):
        self.robot = CleaningRobot(0,0)

    def test_init_robot_and_get_status(self):
        #Its basically a "mock", mock a robots position, the init. method should overwrite it
        self.robot.pos_x = 2
        self.robot.pos_y = 3
        self.robot.facing = "S"
        self.assertEqual("(2,3,S)", self.robot.robot_status())

        self.robot.initialize_robot()
        self.assertEqual("(0,0,N)", self.robot.robot_status())
