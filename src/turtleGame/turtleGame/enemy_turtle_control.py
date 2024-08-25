#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from turtlesim.srv import Spawn
from functools import partial

names =["t1","t2","t3"]

class turtle_controller(Node):
    def __init__(self,name):
        super().__init__("turtle_controller")
        self.name=name
        self.cmd_vel_pub=self.create_publisher(Twist, f"/{self.name}/cmd_vel", 10)
        self.pose_subscriber=self.create_subscription(Pose,f"/{self.name}/pose",self.pose_callback,10)
        self.get_logger().info("turtle controller has been started")
        self.call_hide_pen_service()
    
    def pose_callback(self,pose:Pose):
        cmd = Twist()
        if pose.x >= 7.5 or pose.y >=7.5 or pose.x <= 2.5 or pose.y <2.5:
            cmd.angular.z=2.0
            cmd.linear.x=2.0
        else:
            cmd.linear.x=4.0
            cmd.angular.z=0.0
        
        self.cmd_vel_pub.publish(cmd)

    def call_hide_pen_service(self):
        client = self.create_client(SetPen,f"/{self.name}/set_pen")

        while not client.wait_for_service(1):
            self.get_logger().warn("waiting for service...")
        
        request = SetPen.Request()
        self.get_logger().info("hiding pen")
        request.off=1

        futrue = client.call_async(request)
        futrue.add_done_callback(partial(self.callback_hide_pen))

    def callback_hide_pen(self,future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("service call failed: %r" %(e,))


def main(args=None):
    rclpy.init(args=args)
    for i in names:
        node = turtle_controller(i)
    rclpy.spin(node)
    rclpy.shutdown()