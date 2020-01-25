#! /usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import xlrd
import os
from trajectory_msgs.msg import JointTrajectoryPoint

#########################################################
def add_point(pln, p1, p2, p3, p4, p5, p6, v1, v2, v3, v4, v5, v6, a1, a2, a3, a4, a5, a6, ts, tns):
	lens = len(pln.joint_trajectory.points) # length of old plan
	for i in range(lens-1,-1,-1): # emptizing the old "random" plan
		del(pln.joint_trajectory.points[-1])
	ll = len(p1) # length of my new plan
	for i in range(ll):
		point=JointTrajectoryPoint()
		point.positions.append(p1[i])
		point.positions.append(p2[i])
		point.positions.append(p3[i])
		point.positions.append(p4[i])
		point.positions.append(p5[i])
		point.positions.append(p6[i])
		point.velocities.append(v1[i])
		point.velocities.append(v2[i])
		point.velocities.append(v3[i])
		point.velocities.append(v4[i])
		point.velocities.append(v5[i])
		point.velocities.append(v6[i])
		point.accelerations.append(a1[i])
		point.accelerations.append(a2[i])
		point.accelerations.append(a3[i])
		point.accelerations.append(a4[i])
		point.accelerations.append(a5[i])
		point.accelerations.append(a6[i])
		point.time_from_start.secs = ts[i] #rospy.Time.now() + rospy.Duration(0.05)
		point.time_from_start.nsecs = tns[i]
		pln.joint_trajectory.points.append(point)
	return pln
	
#########################################################
# Opening excel file
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
myfile = os.path.join(THIS_FOLDER, 'result.xlsx')
workbook = xlrd.open_workbook(myfile)
worksheet = workbook.sheet_by_index(0)
#########################################################
pos1 = worksheet.col_values(0)   # positions of joint1
pos2 = worksheet.col_values(1)   # positions of joint2
pos3 = worksheet.col_values(2)   # positions of joint3
pos4 = worksheet.col_values(3)   # positions of joint4
pos5 = worksheet.col_values(4)   # positions of joint5
pos6 = worksheet.col_values(5)   # positions of joint6
#########################################################
vel1 = worksheet.col_values(6)   # velocities of joint1
vel2 = worksheet.col_values(7)   # velocities of joint2
vel3 = worksheet.col_values(8)   # velocities of joint3
vel4 = worksheet.col_values(9)   # velocities of joint4
vel5 = worksheet.col_values(10)  # velocities of joint5
vel6 = worksheet.col_values(11)  # velocities of joint6
#########################################################
acc1 = worksheet.col_values(12)  # accelerations of joint1
acc2 = worksheet.col_values(13)  # accelerations of joint2
acc3 = worksheet.col_values(14)  # accelerations of joint3
acc4 = worksheet.col_values(15)  # accelerations of joint4
acc5 = worksheet.col_values(16)  # accelerations of joint5
acc6 = worksheet.col_values(17)  # accelerations of joint6
#########################################################
secs  = worksheet.col_values(18) # time from start secs
nsecs = worksheet.col_values(19) # time from start nsecs
workbook.release_resources()
del workbook
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
# Initializing the new plan
plan2 = group.plan()
plan2 = add_point(plan2, pos1, pos2, pos3, pos4, pos5, pos6, vel1, vel2, vel3, vel4, vel5, vel6, acc1, acc2, acc3, acc4, acc5, acc6, secs, nsecs)
group.execute(plan2, wait=True)
#########################################################
