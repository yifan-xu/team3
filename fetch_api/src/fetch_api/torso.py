#!/usr/bin/env python

import actionlib
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from trajectory_msgs.msg import JointTrajectory
import rospy

ACTION_NAME = "torso_controller/follow_joint_trajectory"
JOINT_NAME = "torso_lift_joint"
TIME_FROM_START = 5  # How many seconds it should take to set the torso height.


class Torso(object):
    """Torso controls the robot's torso height.
    """
    MIN_HEIGHT = 0.0
    MAX_HEIGHT = 0.4

    def __init__(self):
        self.client = actionlib.SimpleActionClient(ACTION_NAME, FollowJointTrajectoryAction)
        rospy.logerr("initialized client")
        self.client.wait_for_server()
        rospy.logerr("got server response")

    def set_height(self, height):
        """Sets the torso height.

        This will always take ~5 seconds to execute.

        Args:
            height: The height, in meters, to set the torso to. Values range
                from Torso.MIN_HEIGHT (0.0) to Torso.MAX_HEIGHT(0.4).
        """

        rospy.logerr("setting height")
        if height < Torso.MIN_HEIGHT or height > Torso.MAX_HEIGHT:
            rospy.logerr('Height not set (out of bounds)')
            return
        point = JointTrajectoryPoint()
        point.positions.append(height)
        point.time_from_start = rospy.Duration(TIME_FROM_START)

        trajectory = JointTrajectory()
        trajectory.joint_names.append(JOINT_NAME)
        trajectory.points.append(point)

        goal = FollowJointTrajectoryGoal()
        goal.trajectory = trajectory
        #goal.path_tolerance =
        #goal.goal_tolerance =
        #goal.goal_time_tolerance =

        self.client.send_goal(goal)
        rospy.logerr("sent set height")
        self.client.wait_for_result()
        rospy.logerr("height set") 
