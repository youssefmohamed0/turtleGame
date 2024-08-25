#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from random import uniform, choice
from turtlesim.msg import Pose
from math import pi



names =["t1","t2","t3"]

class MyTurtleSpawner(Node):
    def __init__(self,name):
        super().__init__('spawner')
        self.spawn_client = self.create_client(Spawn, 'spawn')

        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn service not available, waiting...')

        self.spawn_request = Spawn.Request()
         
        self.spawn_request.x = uniform(0.5, 9.5)
        self.spawn_request.y = uniform(0.5, 9.5)
        self.spawn_request.theta = uniform(0, 2 *pi)
        self.declare_parameter('name',name)
        self.spawn_request.name = self.get_parameter('name').value
        future = self.spawn_client.call_async(self.spawn_request)
        future.result()

def main(args=None):
    rclpy.init(args=args)
    for i in names:
        spawner_node = MyTurtleSpawner(i)
    # rclpy.spin(spawner_node)
    rclpy.shutdown()
