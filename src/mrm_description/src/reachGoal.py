#! /usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander("/mrm/robot_description", "/mrm")
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("arm", "/mrm/robot_description", "/mrm")
display_trajectory_publisher = rospy.Publisher('/mrm/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)

pose_target = geometry_msgs.msg.Pose()

pose_target.position.x = -0.412919044556
pose_target.position.y = -0.224890608369
pose_target.position.z = 0.407519807768

pose_target.orientation.x = 0.0632767152512
pose_target.orientation.y = 0.0850872409274
pose_target.orientation.z = 0.236000862232
pose_target.orientation.w = 0.965950211845

group.set_pose_target(pose_target)
rospy.sleep(3)
plan2 = group.plan()
group.execute(plan2, wait=True)
#group.go(wait=True)

moveit_commander.roscpp_shutdown()
