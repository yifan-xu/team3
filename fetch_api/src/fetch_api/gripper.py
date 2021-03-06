#! /usr/bin/env python

import rospy
import actionlib
from control_msgs.msg import GripperCommandAction
from control_msgs.msg import GripperCommand
from control_msgs.msg import GripperCommandGoal

CLOSED_POS = 0.0  # The position for a fully-closed gripper (meters).
OPENED_POS = 0.10  # The position for a fully-open gripper (meters).
ACTION_NAME = 'gripper_controller/gripper_action'


class Gripper(object):
    """Gripper controls the robot's gripper.
    """
    MIN_EFFORT = 35  # Min grasp force, in Newtons
    MAX_EFFORT = 100  # Max grasp force, in Newtons

    def __init__(self):
        self.client = actionlib.SimpleActionClient(ACTION_NAME, GripperCommandAction)
        rospy.logerr("initialized client")
	self.client.wait_for_server()
        rospy.logerr("got server response")

    def open(self):
        """Opens the gripper.
        """

        rospy.logerr("opening")
	goal = GripperCommandGoal()
	goal.command.position = OPENED_POS
        self.client.send_goal(goal)
        rospy.logerr("sent open")
	self.client.wait_for_result()
        rospy.logerr("opened")

    def close(self, max_effort=MAX_EFFORT):
        """Closes the gripper.

        Args:
            max_effort: The maximum effort, in Newtons, to use. Note that this
                should not be less than 35N, or else the gripper may not close.
        """

        rospy.logerr("closing")
        goal = GripperCommandGoal()
        goal.command.position = CLOSED_POS
        goal.command.max_effort = max_effort
	self.client.send_goal(goal)
        rospy.logerr("sent close")
        self.client.wait_for_result()
        rospy.logerr("closed")
