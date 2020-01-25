#! /usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import xlsxwriter
import math
import os # to inforce python to create the excel sheet at the same place as the script

row = 0 
col = 0

def extract_points(data, x, s_ofst = 0):
	global row
	i = 0
	for item in data:
		x.write(row, col   , data[i].positions[0])
		x.write(row, col+1 , data[i].positions[1])
		x.write(row, col+2 , data[i].positions[2])
		x.write(row, col+3 , data[i].positions[3])
		x.write(row, col+4 , data[i].positions[4])
		x.write(row, col+5 , data[i].positions[5])
		x.write(row, col+6 , data[i].velocities[0])
		x.write(row, col+7 , data[i].velocities[1])
		x.write(row, col+8 , data[i].velocities[2])
		x.write(row, col+9 , data[i].velocities[3])
		x.write(row, col+10, data[i].velocities[4])
		x.write(row, col+11, data[i].velocities[5])
		x.write(row, col+12, data[i].accelerations[0])
		x.write(row, col+13, data[i].accelerations[1])
		x.write(row, col+14, data[i].accelerations[2])
		x.write(row, col+15, data[i].accelerations[3])
		x.write(row, col+16, data[i].accelerations[4])
		x.write(row, col+17, data[i].accelerations[5])
		x.write(row, col+18, data[i].time_from_start.secs+s_ofst)
		x.write(row, col+19, data[i].time_from_start.nsecs)
		row += 1
		i   += 1
#########################################################
# creating excel file
workbook = xlsxwriter.Workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)),"result.xlsx"))
worksheet = workbook.add_worksheet()
#########################################################
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander("/mrm/robot_description", "/mrm")
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("arm", "/mrm/robot_description", "/mrm")

group.set_planner_id("RRT")
group.set_goal_tolerance(0.1)
group.set_num_planning_attempts(10)
group.set_planning_time(10.0)
group.set_max_velocity_scaling_factor(0.1)
group.set_max_acceleration_scaling_factor(1.0)
########################################################
group.set_named_target("Start")
plan1 = group.plan()
group.execute(plan1, wait=True)
########################################################
extract_points(plan1.joint_trajectory.points, worksheet)
ss = plan1.joint_trajectory.points[-1].time_from_start.secs
ns = plan1.joint_trajectory.points[-1].time_from_start.nsecs / 1e9
ss = ss + math.ceil(ns)
########################################################
group_variable_values = group.get_current_joint_values()
for x in range(30):
	group_variable_values[0] += 0.1
	group.set_joint_value_target(group_variable_values)
	plan2 = group.plan()
group.execute(plan2, wait=True)
#########################################################
# extracting points to excel sheet
extract_points(plan2.joint_trajectory.points, worksheet, ss)
ss += plan2.joint_trajectory.points[-1].time_from_start.secs
ns = plan2.joint_trajectory.points[-1].time_from_start.nsecs / 1e9
ss = ss + math.ceil(ns)
#########################################################
group_variable_values = group.get_current_joint_values()
for x in range(30):
	group_variable_values[0] += 0.1
	group.set_joint_value_target(group_variable_values)
	plan2 = group.plan()
group.execute(plan2, wait=True)
#########################################################
# extracting points to excel sheet
extract_points(plan2.joint_trajectory.points, worksheet, ss)
#########################################################
workbook.close()
#########################################################
#lens = len(plan2.joint_trajectory.points)
#print plan2.joint_trajectory.points[x-1].positions[5]
#print plan2
