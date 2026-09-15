import socket

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


UDP_HOST = "0.0.0.0"
UDP_PORT = 5055

ALLOWED_INTENTS = {
    "HAND_OPEN",
    "HAND_CLOSE",
    "HAND_PEACE",
    "EMERGENCY_STOP",
}


class DavidRosBridge(Node):

    def __init__(self):
        super().__init__("david_ros_bridge")

        self.publisher = self.create_publisher(
            String,
            "/hand/intent",
            10
        )

        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        self.sock.bind(
            (UDP_HOST, UDP_PORT)
        )

        self.sock.setblocking(False)

        self.timer = self.create_timer(
            0.02,
            self.receive_udp
        )

        self.get_logger().info(
            f"DAVID ROS Bridge listening on UDP {UDP_PORT}"
        )

        self.get_logger().info(
            "Publishing to /hand/intent"
        )

    def receive_udp(self):

        try:
            data, address = self.sock.recvfrom(1024)

        except BlockingIOError:
            return

        intent = data.decode(
            "utf-8"
        ).strip()

        self.get_logger().info(
            f"UDP from {address}: {intent}"
        )

        if intent not in ALLOWED_INTENTS:

            self.get_logger().warning(
                f"Rejected intent: {intent}"
            )

            return

        message = String()
        message.data = intent

        self.publisher.publish(
            message
        )

        self.get_logger().info(
            f"ROS publish: {intent}"
        )

    def destroy_node(self):

        self.sock.close()

        super().destroy_node()


def main():

    rclpy.init()

    node = DavidRosBridge()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()