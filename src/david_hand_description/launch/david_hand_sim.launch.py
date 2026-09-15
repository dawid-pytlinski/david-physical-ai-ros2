from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # ----------------------------------------------------------
    # Paths
    # ----------------------------------------------------------

    hand_description_share = FindPackageShare(
        "david_hand_description"
    )

    xacro_file = PathJoinSubstitution([
        hand_description_share,
        "urdf",
        "right_hand.urdf.xacro",
    ])

    gazebo_launch_file = PathJoinSubstitution([
        FindPackageShare("ros_gz_sim"),
        "launch",
        "gz_sim.launch.py",
    ])

    # ----------------------------------------------------------
    # Robot description
    # ----------------------------------------------------------

    robot_description = ParameterValue(
        Command([
            "xacro ",
            xacro_file,
        ]),
        value_type=str,
    )

    # ----------------------------------------------------------
    # Robot State Publisher
    # ----------------------------------------------------------

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }
        ],
    )

    # ----------------------------------------------------------
    # Gazebo
    # ----------------------------------------------------------

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            gazebo_launch_file
        ),
        launch_arguments={
            "gz_args": "-r -v 4 empty.sdf",
        }.items(),
    )

    # ----------------------------------------------------------
    # Spawn right hand
    # ----------------------------------------------------------

    spawn_hand = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_david_right_hand",
        output="screen",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "david_right_hand",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "0.5",
        ],
    )

    # ----------------------------------------------------------
    # ros2_control
    # ----------------------------------------------------------

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "60",
        ],
        output="screen",
    )

    right_hand_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "right_hand_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "60",
        ],
        output="screen",
    )

    # ----------------------------------------------------------
    # DAVID Hand Controller
    # ----------------------------------------------------------

    david_hand_controller = Node(
        package="david_hand_control",
        executable="hand_controller",
        name="david_hand_controller",
        output="screen",
    )

    # ----------------------------------------------------------
    # DAVID UDP -> ROS 2 Bridge
    # ----------------------------------------------------------

    david_ros_bridge = Node(
        package="david_hand_control",
        executable="david_ros_bridge",
        name="david_ros_bridge",
        output="screen",
    )

    # ----------------------------------------------------------
    # Launch description
    # ----------------------------------------------------------

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_hand,
        joint_state_broadcaster_spawner,
        right_hand_controller_spawner,
        david_hand_controller,
        david_ros_bridge,
    ])