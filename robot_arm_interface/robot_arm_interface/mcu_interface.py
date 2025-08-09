import sys
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QSlider, QLabel, 
                             QHBoxLayout, QGroupBox, QPushButton)
from sensor_msgs.msg import JointState
from PyQt5.QtCore import Qt, QTimer
import math 

class MainWindow(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle("Robot Arm Controller")
        self.setGeometry(100, 100, 600, 400)
        
        # Joint names and ranges
        # All sliders now have a range of 0 to 180
        self.joint_names = ["base_joint", "joint2", "joint3", "joint4", "end_effector_joint"]
        self.joint_ranges = [(0, 180), (0, 180), (0, 180), (0, 180), (0, 180)]
        self.current_values_deg = [90.0] * 5 # Start all sliders at 90 degrees
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create sliders for each joint
        self.sliders = []
        self.value_labels = []
        
        for i, (name, (min_val, max_val)) in enumerate(zip(self.joint_names, self.joint_ranges)):
            group = QGroupBox(name)
            layout = QVBoxLayout()
            
            # Value display
            value_label = QLabel(f"90°")
            self.value_labels.append(value_label)
            layout.addWidget(value_label)
            
            # Slider
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(90) # Default to 90 degrees
            # Connect the slider's valueChanged signal to the publish method
            slider.valueChanged.connect(lambda value, idx=i: self.slider_changed(value, idx))
            self.sliders.append(slider)
            layout.addWidget(slider)
            
            group.setLayout(layout)
            main_layout.addWidget(group)
        
        # Button panel (Only the Reset button remains)
        button_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Reset All")
        self.reset_button.clicked.connect(self.reset_sliders)
        button_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)
        
        # Publisher for joint states
        self.joint_pub = self.node.create_publisher(
            JointState, '/joint_states', 10)
            
        # Initial publication when the app starts
        self.publish_joint_angles()
    
    def slider_changed(self, value, joint_index):
        self.current_values_deg[joint_index] = float(value)
        self.value_labels[joint_index].setText(f"{value}°")
        # Publish the joint angles immediately when a slider changes
        self.publish_joint_angles()

    def reset_sliders(self):
        for i, slider in enumerate(self.sliders):
            slider.setValue(90)
            self.current_values_deg[i] = 90.0
            self.value_labels[i].setText("90°")
        self.node.get_logger().info("Reset all sliders to 90")
        # Publish the new joint angles after reset
        self.publish_joint_angles()

    def publish_joint_angles(self):
        msg = JointState()
        msg.header.stamp = self.node.get_clock().now().to_msg()
        msg.name = self.joint_names
        
        joint_positions_rad = []
        for angle_deg in self.current_values_deg:
            angle_offset_deg = angle_deg - 90
            joint_positions_rad.append(math.radians(angle_offset_deg))
        
        msg.position = joint_positions_rad
        
        self.joint_pub.publish(msg)
        self.node.get_logger().info(f"Published joint states (radians): {joint_positions_rad}")

class UINode(Node):
    def __init__(self):
        super().__init__('robot_arm_ui_node')
        self.main_window = MainWindow(self)

def main(args=None):
    rclpy.init(args=args)
    
    app = QApplication(sys.argv)
    
    try:
        ui_node = UINode()
        
        def ros_spin_once():
            rclpy.spin_once(ui_node, timeout_sec=0.1)
        
        spin_timer = QTimer()
        spin_timer.timeout.connect(ros_spin_once)
        spin_timer.start(100)
        
        ui_node.main_window.show()
        
        app.exec_()
        
    finally:
        ui_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()