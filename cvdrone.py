#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TwistStamped

rospy.init_node('drone', anonymous=True)

mid = PoseStamped()

def callback(data):
    global mid
    mid=data
    assign(data)

rospy.Subscriber("cv_bounding_box", PoseStamped, callback)

current_pos = PoseStamped()

def current_pos_callback(position):

    global current_pos
    current_pos = position

rospy.Subscriber('mavros/local_position/pose',PoseStamped,current_pos_callback)

def assign(data):
    print("x: ")
    print(data.pose.position.x-350)
    print("y: ")
    print(data.pose.position.y-250)


    mid.pose.position.x=data.pose.position.x-350
    mid.pose.position.y=data.pose.position.y-250
    setvel_client = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',TwistStamped, queue_size=1)
    velocity_msg = TwistStamped()

    if(mid.pose.position.x>100):
        velocity_msg.twist.linear.y = 4


    if(mid.pose.position.x<-50):
        velocity_msg.twist.linear.y = -4


    if(mid.pose.position.y<90):
        velocity_msg.twist.linear.z = 4


    if(mid.pose.position.y>40):
        velocity_msg.twist.linear.z = -4

    setvel_client.publish(velocity_msg)

rospy.spin()

