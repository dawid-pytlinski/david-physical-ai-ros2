import rclpy

from rclpy.duration import Duration
from rclpy.node import Node

from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


# ============================================================
# DIGITAL TWIN - RIGHT DFRobot BIONIC HAND
# ============================================================

JOINT_NAMES = [
    "right_thumb_actuator_joint",
    "right_index_actuator_joint",
    "right_middle_actuator_joint",
    "right_ring_actuator_joint",
    "right_little_actuator_joint",
]


# ============================================================
# SIMULATION JOINT POSITIONS
# ============================================================

THUMB_OPEN = 0.0
THUMB_CLOSED = 1.0

FINGER_OPEN = 0.0
FINGER_CLOSED = 1.2


# ============================================================
# GESTURES
# ============================================================

GESTURES = {

    "HAND_OPEN": [
        THUMB_OPEN,
        FINGER_OPEN,
        FINGER_OPEN,
        FINGER_OPEN,
        FINGER_OPEN,
    ],

    "HAND_CLOSE": [
        THUMB_CLOSED,
        FINGER_CLOSED,
        FINGER_CLOSED,
        FINGER_CLOSED,
        FINGER_CLOSED,
    ],

    "HAND_PEACE": [
        THUMB_CLOSED,
        FINGER_OPEN,
        FINGER_OPEN,
        FINGER_CLOSED,
        FINGER_CLOSED,
    ],
}


class DavidHandController(Node):

    def __init__(self):

        super().__init__(
            "david_hand_controller"
        )

        # Input:
        # /hand/intent
        self.intent_subscription = self.create_subscription(
            String,
            "/hand/intent",
            self.intent_callback,
            10,
        )

        # Output:
        # trajectory for future ros2_control / Gazebo
        self.trajectory_publisher = self.create_publisher(
            JointTrajectory,
            "/right_hand_controller/joint_trajectory",
            10,
        )

        self.get_logger().info(
            "DAVID Hand Controller ONLINE"
        )

        self.get_logger().info(
            "Listening: /hand/intent"
        )

        self.get_logger().info(
            "Publishing: "
            "/right_hand_controller/joint_trajectory"
        )

        self.get_logger().info(
            "Controlled joints:"
        )

        for joint in JOINT_NAMES:
            self.get_logger().info(
                f"  - {joint}"
            )

    def intent_callback(
        self,
        message: String
    ):

        intent = message.data.strip()

        self.get_logger().info(
            f"Intent received: {intent}"
        )

        if intent == "EMERGENCY_STOP":

            self.get_logger().warning(
                "EMERGENCY STOP received."
            )

            return

        if intent not in GESTURES:

            self.get_logger().warning(
                f"Unsupported intent: {intent}"
            )

            return

        positions = GESTURES[
            intent
        ]

        self.publish_trajectory(
            intent,
            positions
        )

    def publish_trajectory(
        self,
        gesture_name: str,
        positions: list[float]
    ):

        trajectory = JointTrajectory()

        trajectory.joint_names = JOINT_NAMES

        point = JointTrajectoryPoint()

        point.positions = positions

        point.time_from_start = Duration(
            seconds=1.0
        ).to_msg()

        trajectory.points.append(
            point
        )

        self.trajectory_publisher.publish(
            trajectory
        )

        self.get_logger().info(
            f"Gesture published: {gesture_name}"
        )

        self.get_logger().info(
            "Target positions:"
        )

        for joint, position in zip(
            JOINT_NAMES,
            positions
        ):

            self.get_logger().info(
                f"  {joint}: {position:.2f} rad"
            )


def main(args=None):

    rclpy.init(
        args=args
    )

    node = DavidHandController()

    try:

        rclpy.spin(
            node
        )

    except KeyboardInterrupt:

        node.get_logger().info(
            "Stopping DAVID Hand Controller."
        )

    finally:

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()