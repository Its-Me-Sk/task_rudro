import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleNav(Node):
    def __init__(self):
        super().__init__('turtle_nav')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.target_x = 8.0
        self.target_y = 2.0
        self.pose = None
        self.total_distance = 0.0

    def pose_callback(self, msg):
        self.pose = msg
        distance = math.sqrt((self.target_x - self.pose.x)**2 + (self.target_y - self.pose.y)**2)
        heading = math.atan2(self.target_y - self.pose.y, self.target_x - self.pose.x)
        angle_diff = heading - self.pose.theta
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        twist = Twist()
        if abs(angle_diff) > 0.1:
            twist.angular.z = 2.0 * angle_diff
        elif distance > 0.1:
            twist.linear.x = 2.0 * distance
        else:
            self.get_logger().info(f"Reached target ({self.target_x},{self.target_y}). Traveled: {self.total_distance:.2f} units")
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleNav()
    rclpy.spin(node)
    rclpy.shutdown()

