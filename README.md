Set of ROS2 packages to Control and visualize a [5-DOF robotic arm](https://github.com/NafieAlhilaly/5-dof-arm-design) using ROS 2, RViz and MoveIt, as well as interface with microcontrollers.

## Setup
> This project is tested and run on ROS2 **Kilted**

make sure you have ROS2 **Kilted** and source the workspace before running the commands below.

Use Makefile to build the project:
```bash
make clean build
```

source the workspace:
```bash
source install/setup.bash
```
----

## Packages Overview
### Robot Arm UI
The Robot Arm UI. This interface allows you to interact with the arm in a user-friendly way.

![Robot Arm UI](./screenshot/img1.png)

### Robot Arm Description
Contains necessary Robot Arm difnition files, such as URDF and SRDF, to describe the robot's physical structure and capabilities.

### Robot Arm Interface
This package provides the necessary interfaces to control the robotic arm, including communication with microcontrollers and other hardware components.

### Robot Arm MoveIt
This package integrates MoveIt with the robotic arm, allowing for advanced motion planning and control. It includes launch files for various MoveIt functionalities such as move group, RViz visualization, and setup assistant.

## Loanching the Robot Arm
To launch the robot arm in rViz with MoveIt, use the following command:
```bash
ros2 launch robot_arm_moveit demo.launch.py
```
in another terminal, you can launch the robot arm UI to control the arm:
```bash
ros2 run robot_arm_ui robot_arm_ui_node
```

## Testing
![Robot Arm UI](./screenshot/img2.png)