#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan

warner = None

def callback(msg):
    global warner
    warner = msg

def turner():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('turner', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    move = Twist()
    move.linear.x = 0.5
    move.angular.z = 0.0
    rospy.Subscriber("/scan", LaserScan, callback)
    try:
        while not rospy.is_shutdown():
            if warner is not None:
                
                if (warner.ranges[355] < 1.5)or(warner.ranges[5] < 1.5)or(warner.ranges[0] < 1.5):
                    move.angular.z = 1.0
                else:
                    move.angular.z = 0.0
                rospy.loginfo(move)
                pub.publish(move)
            rate.sleep()
        rospy.spin()
    except KeyboardInterrupt:
        move.linear.x = 0.0
        move.angular.z = 0.0
        rospy.loginfo(move)
        pub.publish(move)
        pub.publish(move)
        pub.publish(move)
        
if __name__ == '__main__':
    try:
        turner()
    except rospy.ROSInterruptException:
        pass
