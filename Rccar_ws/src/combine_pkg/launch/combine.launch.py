import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    # Task 1: VESC driver (motor + steering servo)
    vesc_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('vesc_driver'),
            'launch', 'vesc_driver_node.launch.py')))
    ld.add_action(vesc_driver_launch)

    # Task 2: joystick
    joy_node = Node(package='joy', executable='joy_node', output='screen')
    ld.add_action(joy_node)

    # Add more IncludeLaunchDescription actions or Nodes for other packages

    return ld
