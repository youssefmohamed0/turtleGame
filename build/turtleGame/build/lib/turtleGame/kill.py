#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from random import uniform, choice
from turtlesim.msg import Pose
from math import pi

class TurtleKiller(Node):
    def __init__(self):
        super().__init__("turtle_killer")
        self.main_pose_subscriber=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.t1_pose_subscriber=self.create_subscription(Pose,"/t1/pose",self.pose_callback,10)
        self.t2_pose_subscriber=self.create_subscription(Pose,"/t2/pose",self.pose_callback,10)
        self.t3_pose_subscriber=self.create_subscription(Pose,"/t3/pose",self.pose_callback,10)

    def pose_callback(self,msg:Pose):
        self.get_logger().info(str(msg))


def main(args=None):
    rclpy.init(args=args)
    node = TurtleKiller()
    rclpy.spin(node)
    rclpy.shutdown()
