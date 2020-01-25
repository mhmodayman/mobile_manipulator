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

print group.get_current_pose().pose

group.set_planner_id("RRT")
group.set_goal_tolerance(0.1)
group.set_num_planning_attempts(10)
group.set_planning_time(5.0)
group.set_max_velocity_scaling_factor(1.0)
group.set_max_acceleration_scaling_factor(1.0)

group_variable_values = group.get_current_joint_values()
group_variable_values[0] = 1
group.set_joint_value_target(group_variable_values)

rospy.sleep(0.1)
plan2 = group.plan()
group.execute(plan2, wait=True)

print group.get_current_pose().pose

moveit_commander.roscpp_shutdown()
