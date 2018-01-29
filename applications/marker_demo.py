#!/usr/bin/env python
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion, Pose, Point, Vector3
from std_msgs.msg import Header, ColorRGBA
from nav_msgs.msg import Odometry
import rospy
import math

def wait_for_time():                                              
    """Wait for simulated time to begin.                          
    """                                                           
    while rospy.Time().now().to_sec() == 0:                       
        pass

class NavPath(object):
    def __init__ (self, publisher):
        self._path = []
        self._publisher = publisher
    # receives an odom message and rebroadcasts the current path to rviz
    def callback(self, msg):
        rospy.loginfo(msg)
        pos = msg.pose.pose.position
        distance = math.sqrt(pos.x * pos.x + pos.y * pos.y + pos.z * pos.z)
        if distance>=0.01:
            self._path.append(pos)
            self.drawPath()
    def drawPath(self):
        marker = Marker(
                    type=Marker.LINE_STRIP,
                    id=0,
                    lifetime = rospy.Duration(0),
                    pose = Pose(Point(0,0,0), Quaternion(0, 0, 0, 1)),
                    scale = Vector3(0.1, 0.1, 0.1),
                    header = Header(frame_id='odom'),
                    color = ColorRGBA(1.0, 1.0, 1.0, 0.8),
                    points = self._path
                    )
        self._publisher.publish(marker)

def main():
    rospy.init_node('nav_path_display')
    wait_for_time()
    marker_publisher = rospy.Publisher('visualization_marker', Marker, queue_size=10) 
    rospy.sleep(0.5)                                                             
    nav_path = NavPath(marker_publisher)
    rospy.Subscriber('odom', Odometry, nav_path.callback)
    rospy.spin()

if __name__ == '__main__':
    main()