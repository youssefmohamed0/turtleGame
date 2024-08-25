#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from random import uniform
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
from math import pi

class TurtleKiller(Node):
    def __init__(self):
        super().__init__("turtle_killer")
        self.t1_pose=Pose()
        self.t2_pose=Pose()
        self.t3_pose=Pose()
        self.pose=Pose()

        self.main_pose_subscriber=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.t1_pose_subscriber=self.create_subscription(Pose,"/t1/pose",self.t1_pose_callback,10)
        self.t2_pose_subscriber=self.create_subscription(Pose,"/t2/pose",self.t2_pose_callback,10)
        self.t3_pose_subscriber=self.create_subscription(Pose,"/t3/pose",self.t3_pose_callback,10)

    def pose_callback(self,msg:Pose):
        
        self.pose=msg
        # self.get_logger().info(str(self.pose.x))    
    
    def t1_pose_callback(self,msg:Pose):
        self.t1_pose=msg
        if abs(self.pose.x-self.t1_pose.x ) < 0.5 and abs(self.pose.y-self.t1_pose.y ) < 0.5:
            self.get_logger().info(f"user killed t1")
            self.call_tele_service("t1")
        
    def t2_pose_callback(self,msg:Pose):
        self.t2_pose=msg
        if abs(self.pose.x-self.t2_pose.x ) < 0.5 and abs(self.pose.y-self.t2_pose.y ) < 0.5:
            self.get_logger().info(f"user killed t2")
            self.call_tele_service("t2")
    def t3_pose_callback(self,msg:Pose):
        self.t3_pose=msg
        if abs(self.pose.x-self.t3_pose.x ) < 0.5 and abs(self.pose.y-self.t3_pose.y ) < 0.5:
            self.get_logger().info(f"user killed t3")
            self.call_tele_service("t3")
    
    def call_tele_service(self,name):
        client = self.create_client(TeleportAbsolute,f"/{name}/teleport_absolute")

        while not client.wait_for_service(1):
            self.get_logger().warn("waiting for teleport service...")
        
        request = TeleportAbsolute.Request()
        request.x = uniform(0.5, 9.5)
        request.y = uniform(0.5, 9.5)
        request.theta = uniform(0, 2 *pi)
        

        futrue = client.call_async(request)
        futrue.result()


def main(args=None):
    rclpy.init(args=args)
    node = TurtleKiller()
    rclpy.spin(node)
    rclpy.shutdown()
