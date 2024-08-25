#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from random import uniform
from turtlesim.srv import SetPen
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

    def call_hide_pen_servce(self,name):
        client = self.create_client(SetPen,f"/{name}/set_pen")

        while not client.wait_for_service(1):
            self.get_logger().warn("waiting for pen hide service...")
        
        request = SetPen.Request()
        request.off = 1

        futrue = client.call_async(request)
        futrue.result()

def main(args=None):
    rclpy.init(args=args)
    for i in names:
        spawner_node = MyTurtleSpawner(i)
        spawner_node.call_hide_pen_servce(i)
    # rclpy.spin(spawner_node)
    rclpy.shutdown()
