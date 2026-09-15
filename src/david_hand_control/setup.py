from setuptools import find_packages
from setuptools import setup


package_name = "david_hand_control"


setup(
    name=package_name,
    version="0.1.0",

    packages=find_packages(
        exclude=["test"]
    ),

    data_files=[
        (
            "share/ament_index/resource_index/packages",
            [
                "resource/" + package_name
            ],
        ),
        (
            "share/" + package_name,
            [
                "package.xml"
            ],
        ),
    ],

    install_requires=[
        "setuptools"
    ],

    zip_safe=True,

    maintainer="dawid",
    maintainer_email="pytlinski.david@gmail.com",

    description=(
        "ROS 2 controller for the DAVID "
        "DFRobot Bionic Hand digital twin."
    ),

    license="Apache-2.0",

    tests_require=[
        "pytest"
    ],

    entry_points={
        "console_scripts": [
            "hand_controller = "
            "david_hand_control.hand_controller_node:main",

            "david_ros_bridge = "
            "david_hand_control.david_ros_bridge:main",
        ],
    },
)