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

    @patch("mock.GPIO.input")
    def test_robot_ibs_action(self, mock_input):
        #Its basically a "mock", mock a robots position, the init. method should overwrite it

        #Boundary test
        for bat_val in range(0, 10):
            mock_input.return_value = bat_val  # Battery full enough
            self.robot.manage_battery()
            self.assertTrue(self.robot.battery_led_on)
            self.assertFalse(self.robot.cleaning_system_on)

        for bat_val in range(11, 100):
            mock_input.return_value = bat_val  # Battery full enough
            self.robot.manage_battery()
            self.assertFalse(self.robot.battery_led_on)
            self.assertTrue(self.robot.cleaning_system_on)

        #Test invalid battery state
        mock_input.return_value = -1
        self.assertRaises(CleaningRobotError, self.robot.manage_battery)

        mock_input.return_value = 101
        self.assertRaises(CleaningRobotError, self.robot.manage_battery)



    def test_robot_movement_eg_execute_command(self):
        #Init bot
        #
        #  01234
        # 0x───┐#4steps
        #-1▲   │
        #-2└─┐ │
        #-3  │ │
        #-4  └─┘#4 steps

        ###
        # MOVE 1
        ###
        self.robot.initialize_robot()
        self.assertEqual("(0,0,N)", self.robot.robot_status())

        self.robot.execute_command("r")
        self.assertEqual("(0,0,E)", self.robot.robot_status())

        #4 steps East
        for i in range(0,4):
            self.robot.execute_command("f")

        self.assertEqual("(4,0,E)", self.robot.robot_status())

        ###
        # MOVE 2
        ###

        #Turn robot
        self.robot.execute_command("r")
        self.assertEqual("(4,0,S)", self.robot.robot_status())

        #4 steps South
        for i in range(0,4):
            self.robot.execute_command("f")

        self.assertEqual("(4,-4,S)", self.robot.robot_status())

        ###
        # MOVE 3
        ###
        #Turn robot
        self.robot.execute_command("r")
        self.assertEqual("(4,-4,W)", self.robot.robot_status())

        for i in range(0, 2):
            self.robot.execute_command("f")

        self.assertEqual("(2,-4,W)", self.robot.robot_status())

        ###
        # MOVE 4
        ###
        self.robot.execute_command("r")
        self.assertEqual("(2,-4,N)", self.robot.robot_status())

        for i in range(0,2):
            self.robot.execute_command("f")

        self.assertEqual("(2,-2,N)", self.robot.robot_status())

        ###
        # MOVE 5
        ###
        self.robot.execute_command("l")
        self.assertEqual("(2,-2,W)", self.robot.robot_status())

        for i in range(0,2):
            self.robot.execute_command("f")

        self.assertEqual("(0,-2,W)", self.robot.robot_status())

        ###
        # MOVE 6
        ###
        self.robot.execute_command("r")
        self.assertEqual("(0,-2,N)", self.robot.robot_status())

        for i in range(0,2):
            self.robot.execute_command("f")

        self.assertEqual("(0,0,N)", self.robot.robot_status())