from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    turtulesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node"
    )
    ld.add_action(turtulesim_node)

    spawner_node=Node(
        package="turtleGame",
        executable="turtle_spawner"
    )
    ld.add_action(spawner_node)

    hunter_node=Node(
        package="turtleGame",
        executable="turtle_killer"
    )
    ld.add_action(hunter_node)

    # teleop_node = Node(
    #     package="turtlesim",
    #     executable="turtle_teleop_key"
    # )
    # ld.add_action(teleop_node)
    
    
    return ld 